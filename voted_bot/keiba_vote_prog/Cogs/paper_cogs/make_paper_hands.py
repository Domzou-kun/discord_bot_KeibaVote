from discord.ext import commands
from discord.ext import tasks
import discord
import requests
import json
import datetime
import cv2
import os
from PIL import Image, ImageDraw, ImageFont

from main_sub_func import json_func as jf
from main_sub_func import race_info_getting as race_get
from main_sub_func import gate_color_set as clr_set

from Cogs.paper_cogs.marge_vote_res import marge_vote_res
from Cogs.paper_cogs.poll_score import poll_score


class Hand_Make_Paper_Cmd_Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # 日付の取得
        dt_now = datetime.datetime.now()
        self.today_data = str(dt_now.year) + str(dt_now.month).zfill(2) + str(dt_now.day).zfill(2)
        self.hold_today_data = str(dt_now.year) + '年' + str(dt_now.month).zfill(2) + '月' + str(dt_now.day).zfill(2) + '日' + '開催競争レース'
        
    @commands.command()
    #async def end_vote(self, ctx, *input_race_id):self, ctx, *input_race_id):
    async def hand_end_vote(self, ctx, race_id):

        
        # 使用するレースデータの読み込み
        race_dict, race_info_list, horse_info_list, horse_etc_info_list, parent_list, _ = race_get.race_jsons(race_id=race_id)

        print(f'レース名 : {race_info_list[0]}の新聞生成を開始')
        

        """
        ########################
                新聞作成処理
        ########################
        """
        # botの取得
        bot = self.bot
        
        # 新聞を作るレースIDの取得
        race_id = race_id
        # race名の登録
        target_race_name = race_info_list[0]

        # 投票結果を統合する処理
        poll_res = marge_vote_res(race_id=race_id, today_data=self.today_data)
        if type(poll_res) is dict:  # 投票が存在した場合はdict型でreturnされる

            # savedファイル内にディレクトリの有無を調べる
            saved_file_names_list = ['paper', 'uma_info', 'uma_main', 'uma_prediction', 'uma_score', 'uma_race']
            saved_search_dir_path = r'paper\saved' + '\\' + self.today_data
            
            print('========== <== セーブ用日付ディレクトリの有無 ==> ==========')
            if os.path.exists(saved_search_dir_path):
                print('===== <== ディレクトリ内に保存先ディレクトリの有無 ==> =====')
                saved_files = os.listdir(saved_search_dir_path)
                for saved_file in saved_files:
                    if saved_file not in saved_file_names_list:
                        print('【{}】ディレクトリが存在しないため作成します'.format(saved_file))
                        make_dir_path = saved_search_dir_path + '\\' + str(saved_file)
                        os.mkdir(make_dir_path)
                    else:
                        print(print('【{}】ディレクトリ存在確認'.format(saved_file)))
            else:
                print('===== <== ディレクトリ内に保存先ディレクトリが存在しないため作成の実行 ==> =====')
                os.mkdir(saved_search_dir_path)
                for mkdir_name in saved_file_names_list:
                    make_dir_path = saved_search_dir_path + '\\' + str(mkdir_name)
                    os.mkdir(make_dir_path)
                    print('{}ディレクトリの作成'.format(mkdir_name))
                    print('作成先 : {}'.format(make_dir_path))


            # カラーコードリスト
            color_list = [
                0xffffff,   # 白
                0x000000,   # 黒
                0xff0000,   # 赤
                0x0000ff,   # 青
                0xffff00,   # 黄
                0x008000,   # 緑
                0xffa500,   # 橙
                0xff1493    # 桃
            ]


            # 馬名の分割
            testuma_name_list = []
            for uma_infos in horse_info_list:
                infos_list = uma_infos.split(',')
                testuma_name_list.append(infos_list[2])


            # 画像のパス
            if race_info_list[0] != '凱旋門賞':
                uma_main_path = r"paper\uma_main_color" + "\\uma_main_"
            else:
                print('========== 凱旋門賞特別馬柱 ==========')
                uma_main_path = r"paper\uma_main_color" + "\\uma_main_gaisenmon_"
            print(uma_main_path)
            uma_pred_path = r"paper\uma_predict.png"
            uma_race_path = r"paper\race_main.png"
            # save用のパス
            #saved_path = r'D:\keiba_bot\voted_bot\paper\saved\uma_main' + '\\'
            saved_path = r'paper\saved' + '\\' + self.today_data + r'\uma_main' + '\\'
            # フォントpath
            font_path = r'C:\Windows\Fonts\HGRME.TTC'
            text_color = (0,0,0,255)

            # 枠番号、馬番号
            num_font_size = 30
            num_font = ImageFont.truetype(font_path, num_font_size)
            # 騎手などの情報
            info_font_size = 33
            info_font = ImageFont.truetype(font_path, info_font_size)
            # 馬名
            name_font_size = 30
            name_font = ImageFont.truetype(font_path, name_font_size)


            # 画像結合用リスト
            cat_jpeg = []
            # 最終的な結合用リスト
            all_concated_im = []


            # 枠色の設定
            waku_color = clr_set.gate_color(uma_list=horse_info_list)


            """
            #################################################
            レース情報
            #################################################
            """
            if race_info_list[0] != '凱旋門賞':
                races_info_name_p = r"paper\race_name\race_main.png"
            else:
                print('========== 凱旋門賞特別馬柱 ==========')
                races_info_name_p = r"paper\race_name\race_main_gaisenmon.png"
            races_info_name_im = Image.open(races_info_name_p)
            races_info_name_img = ImageDraw.Draw(races_info_name_im)


            # レース名
            races_info_font_size = 28
            races_info_font_a = ImageFont.truetype(font_path, races_info_font_size)

            y = 130
            for race_name_c in race_info_list[0]:
                
                if race_name_c != 'ー':
                    # 文字の位置
                    str_place = (63, y)
                    races_info_name_img.text(str_place, race_name_c, font=races_info_font_a, fill=text_color)    # 馬番号
                    # 文字の位置の編集
                    y = y+races_info_font_size
                else:
                    # 文字の位置
                    str_place = (71, y+1)
                    races_info_name_img.text(str_place, 'l', font=races_info_font_a, fill=text_color)    # 馬番号
                    # 文字の位置の編集
                    y = y+races_info_font_size

            # race番号
            races_num_font_size = 55
            races_num_font_b = ImageFont.truetype(font_path, races_num_font_size)
            races_info_name_img.text((50,65), str(race_info_list[1]), font=races_num_font_b, fill=text_color)

            # 場所
            races_venue_font_size = 40
            races_venue_font_c = ImageFont.truetype(font_path, races_venue_font_size)
            races_info_name_img.text((35,16), str(race_info_list[2]), font=races_venue_font_c, fill=text_color)

            # 距離
            races_dist_font_size = 20
            races_dist_font_d = ImageFont.truetype(font_path, races_dist_font_size)
            y = 250
            for race_dist_c in race_info_list[3]:
                str_place = (13, y+1)
                races_info_name_img.text(str_place, race_dist_c, font=races_dist_font_d, fill=text_color)    # 馬番号
                # 文字の位置の編集
                y = y+races_dist_font_size

            # 時間
            races_time_font_size = 15
            races_time_font_e = ImageFont.truetype(font_path, races_time_font_size)
            in_text = race_info_list[4]
            races_info_name_img.text((48, 358), in_text, font=races_time_font_e, fill=text_color)

            # 馬情報の結合用リストへ挿入
            #race_save_name = r"D:\keiba_bot\voted_bot\paper\saved\uma_race\uma_race_info.png"
            race_save_name = r'paper\saved' + '\\' + self.today_data + r'\uma_race' + r'\uma_race_info.png'

            races_info_name_im.save(race_save_name)
            print('saved race uma info')
            cat_jpeg.append(races_info_name_im)




            """
            #################################################
            メインの馬の名前など
            #################################################
            """
            # メインの文字入れ
            for uma_name, waku_iro, parent_names in zip(horse_info_list, waku_color, parent_list):
                uma_name_list = uma_name.split(',')

                # 画像の読み込み
                if waku_iro == color_list[0]:   # 白枠
                    uma_p = uma_main_path + 'white.jpg'
                    uma_im = Image.open(uma_p)
                    uma_main_img = ImageDraw.Draw(uma_im)
                elif waku_iro == color_list[1]:   # 黒枠
                    uma_p = uma_main_path + 'black.jpg'
                    uma_im = Image.open(uma_p)
                    uma_main_img = ImageDraw.Draw(uma_im)
                elif waku_iro == color_list[2]:   # 赤枠
                    uma_p = uma_main_path + 'red.jpg'
                    uma_im = Image.open(uma_p)
                    uma_main_img = ImageDraw.Draw(uma_im)
                elif waku_iro == color_list[3]:   # 青枠
                    uma_p = uma_main_path + 'blue.jpg'
                    uma_im = Image.open(uma_p)
                    uma_main_img = ImageDraw.Draw(uma_im)
                elif waku_iro == color_list[4]:   # 黄枠
                    uma_p = uma_main_path + 'yellow.jpg'
                    uma_im = Image.open(uma_p)
                    uma_main_img = ImageDraw.Draw(uma_im)
                elif waku_iro == color_list[5]:   # 緑枠
                    uma_p = uma_main_path + 'green.jpg'
                    uma_im = Image.open(uma_p)
                    uma_main_img = ImageDraw.Draw(uma_im)
                elif waku_iro == color_list[6]:   # 橙枠
                    uma_p = uma_main_path + 'orange.jpg'
                    uma_im = Image.open(uma_p)
                    uma_main_img = ImageDraw.Draw(uma_im)
                elif waku_iro == color_list[7]:   # 桃枠
                    uma_p = uma_main_path + 'pink.jpg'
                    uma_im = Image.open(uma_p)
                    uma_main_img = ImageDraw.Draw(uma_im)



                # 文字入れ
                """
                #################################################
                枠番号、馬番号
                #################################################
                """
                if int(uma_name_list[0]) < 10:
                    uma_main_img.text((72, 8), str(uma_name_list[0]), font=num_font, fill=text_color)    # 枠番号
                elif int(uma_name_list[0]) >= 10:
                    uma_main_img.text((65, 8), str(uma_name_list[0]), font=num_font, fill=text_color)    # 枠番号
                
                if int(uma_name_list[1]) < 10:
                    uma_main_img.text((72, 40), str(uma_name_list[1]), font=num_font, fill=text_color)    # 馬番号
                elif int(uma_name_list[1]) >= 10:
                    uma_main_img.text((65, 40), str(uma_name_list[1]), font=num_font, fill=text_color)    # 馬番号

                """
                #################################################
                馬名
                #################################################
                """
                y = 85
                for uma_name_c in uma_name_list[2]:
                    
                    if uma_name_c != 'ー':
                        # 文字の位置
                        str_place = (65, y)
                        uma_main_img.text(str_place, uma_name_c, font=name_font, fill=text_color)    # 馬番号
                        # 文字の位置の編集
                        y = y+name_font_size
                    else:
                        # 文字の位置
                        str_place = (73, y+1)
                        uma_main_img.text(str_place, 'l', font=name_font, fill=text_color)    # 馬番号
                        # 文字の位置の編集
                        y = y+name_font_size
                """
                #################################################
                血統
                #################################################
                """
                parent_name_font_size = 17
                parent_name_font = ImageFont.truetype(font_path, parent_name_font_size)
                
                yy = 78
                uma_boba_a = '父・' + parent_names[0]
                for uma_name_aa in uma_boba_a:
                    if uma_name_aa != 'ー':
                        # 文字の位置
                        str_place = (120, yy)
                        uma_main_img.text(str_place, uma_name_aa, font=parent_name_font, fill=text_color)    # 馬番号
                        # 文字の位置の編集
                        yy = yy+parent_name_font_size
                    else:
                        # 文字の位置
                        str_place = (125, yy+1)
                        uma_main_img.text(str_place, 'l', font=parent_name_font, fill=text_color)    # 馬番号
                        # 文字の位置の編集
                        yy = yy+parent_name_font_size

                yy = 78
                uma_boba_b = '母・' + parent_names[1]
                for uma_name_bb in uma_boba_b:
                    if uma_name_bb != 'ー':
                        # 文字の位置
                        str_place = (25, yy)
                        uma_main_img.text(str_place, uma_name_bb, font=parent_name_font, fill=text_color)    # 馬番号
                        # 文字の位置の編集
                        yy = yy+parent_name_font_size
                    else:
                        # 文字の位置
                        str_place = (29, yy+1)
                        uma_main_img.text(str_place, 'l', font=parent_name_font, fill=text_color)    # 馬番号
                        # 文字の位置の編集
                        yy = yy+parent_name_font_size


                parent_name_font_size = 15
                parent_name_font = ImageFont.truetype(font_path, parent_name_font_size)
                yyy = 160
                uma_boba_d = '母父・' + parent_names[2]
                for uma_name_dd in uma_boba_d:
                    if uma_name_dd != 'ー':
                        # 文字の位置
                        str_place = (10, yyy)
                        uma_main_img.text(str_place, uma_name_dd, font=parent_name_font, fill=text_color)    # 馬番号
                        # 文字の位置の編集
                        yyy = yyy+parent_name_font_size
                    else:
                        # 文字の位置
                        str_place = (14, yyy+1)
                        uma_main_img.text(str_place, 'l', font=parent_name_font, fill=text_color)    # 馬番号
                        # 文字の位置の編集
                        yyy = yyy+parent_name_font_size




                #uma_im.show()
                save_name = saved_path + 'uma_main_' + str(uma_name_list[1]) + '.jpg'
                uma_im.save(save_name)
                print('saved main uma info')

                # 画像結合
                #im_temp = cv2.imread(save_name)
                #cat_jpeg.append(im_temp)
                cat_jpeg.append(uma_im)
                

                
            # 画像の結合処理
            cat_saved_path = saved_path + 'uma_main_cat.jpeg'
            """
            r_cat_jpeg = list(reversed(cat_jpeg))
            im_cat = cv2.hconcat(r_cat_jpeg)    # 画像の横方向結合  # 馬の名前の表が完成
            cv2.imwrite(cat_saved_path, im_cat)
            print('saved cat file!')
            """
            concated_uma_info_img = concat_height(unconcated_list=cat_jpeg)
            concated_uma_info_img.save(cat_saved_path)
            print('uma info saved file!')

            # 全体結合用のリストに保存
            all_concated_im.append(concated_uma_info_img)



            """
            #############################################################
            情報
            ・性齢(牡3など)
            ・斤量(float型で,56.0など)
            ・騎手(4文字表記)
            ・厩舎(3文字表記)
            #############################################################
            """
            #結合用リスト
            uma_infos_list = []
            # 馬の情報の画像ファイルの読み込み
            uma_info_mokuhi_p = r"paper\race_info\testinfo_mokuji.png"
            uma_info_temp_p = r"paper\race_info\uma_info_template.png"
            # 画像の保存先
            info_saved_path = r'paper\saved' + '\\' + self.today_data + r'\uma_info' + '\\'

            # 目次の読み込み
            info_mokuji_name_im = Image.open(uma_info_mokuhi_p)
            uma_infos_list.append(info_mokuji_name_im)



            for f_info_name, str_uma_name in zip(horse_etc_info_list, testuma_name_list):
                axis_y_counter = 6
                # 馬情報の画像の埋め込み
                infos_im = Image.open(uma_info_temp_p)
                infos_img = ImageDraw.Draw(infos_im)

                # 性齢
                infos_img.text((52, axis_y_counter), str(f_info_name[0]), font=info_font, fill=text_color)
                axis_y_counter = axis_y_counter+40
                
                # 斤量
                infos_img.text((44, axis_y_counter), str(f_info_name[1]), font=info_font, fill=text_color)
                axis_y_counter = axis_y_counter+40
                
                # 騎手  # 文字数によって位置の調整
                if len(str(f_info_name[2])) == 4:
                    infos_img.text((15, axis_y_counter), str(f_info_name[2]), font=info_font, fill=text_color)
                    axis_y_counter = axis_y_counter+40
                elif len(str(f_info_name[2])) > 4:
                    over_jockey = str(f_info_name[2])
                    collect_jockey =over_jockey[:4]
                    infos_img.text((15, axis_y_counter), str(collect_jockey), font=info_font, fill=text_color)
                    axis_y_counter = axis_y_counter+40
                elif  len(str(f_info_name[2])) == 3:
                    infos_img.text((34, axis_y_counter), str(f_info_name[2]), font=info_font, fill=text_color)
                    axis_y_counter = axis_y_counter+40
                elif  len(str(f_info_name[2])) == 2:
                    infos_img.text((50, axis_y_counter), str(f_info_name[2]), font=info_font, fill=text_color)
                    axis_y_counter = axis_y_counter+40
                elif  len(str(f_info_name[2])) == 1:
                    infos_img.text((60, axis_y_counter), str(f_info_name[2]), font=info_font, fill=text_color)
                    axis_y_counter = axis_y_counter+40
                
                
                #厩舎   # 文字数で処理  # 5文字以上なら4文字削除
                if len(str(f_info_name[3])) >= 5:
                    kyusya_over = f_info_name[3]
                    collect_kyusya = kyusya_over[:4]
                    infos_img.text((15, axis_y_counter), str(collect_kyusya), font=info_font, fill=text_color)
                    axis_y_counter = axis_y_counter+40
                else:
                    infos_img.text((15, axis_y_counter), str(f_info_name[3]), font=info_font, fill=text_color)
                    axis_y_counter = axis_y_counter+40

                # リストに保存
                uma_infos_list.append(infos_im)

                # 画像の保存
                info_saved_p = info_saved_path + str(str_uma_name) + '_info.png'
                infos_im.save(info_saved_p)

            # 情報とか目次の結合
            infos_concated_img = concat_height(unconcated_list=uma_infos_list)
            # 情報の保存先
            infos_saved_path = r'paper\saved' + '\\' + self.today_data + r'\uma_info' + '\\'
            infos_saved_p = infos_saved_path + r'all_uma_infos.jpg'
            #user_name_im.save(user_saved_p)
            infos_concated_img.save(infos_saved_p)
            print('predict saved file!')

            # 全体結合用のリストに保存
            all_concated_im.append(infos_concated_img)

            print('info saved file !')




            """
            #############################################################
            予想
            #############################################################
            """

            """
            poll_res : {
                "user_name" : {
                    "race_id" : {
                        "res" : {
                        uma A : reaction x,
                        uma B : reaction y,
                        uma C : reaction z,
                        }
                        "comment_check" : False
                        "del_msg" : [ removed msg list ]
                    }
                    "user_id" : userのID
                }
            }
            """
            # 画像ファイルpath 
            predict_im_path = r'paper\uma_predict' + '\\uma_predict_'
            

            # 投票ボタン
            reaction_buttons = [ '🧿', '⭕', '🔼', '🔽', '⭐', '❌' ] 
            hex_ord_list = [ hex(ord(_rect)) for _rect in reaction_buttons ]
            # ファイル名
            prediction_names_list = [ 'double_maru', 'maru', 'sankaku', 'black_sankaku', 'hoshi', 'batsu', 'zero']

            # user名の抽出
            voted_user_name = list(poll_res.keys()) # 予想表からの出力
            figure_user_name = [ str(user_name[:4]) for user_name in voted_user_name]   # 先頭4文字のみ抽出

            # 予想者の名前
            user_font_size = 34
            user_font = ImageFont.truetype(font_path, user_font_size)

            for voted_user, f_user_name in zip(voted_user_name, figure_user_name):
                # userごとの予想結果のリスト
                each_user_img_list = []

                # 予想dictの取得
                predict_dict = poll_res[voted_user][race_id]['res']
                # 予想された馬名の取得
                predict_uma_name_list = list(predict_dict.keys())


                # user名の画像生成
                user_name_p = r"paper\uma_predict\uma_predict_user_name.png"
                user_name_im = Image.open(user_name_p)
                user_name_img = ImageDraw.Draw(user_name_im)
                user_name_img.text((10, 3), str(f_user_name), font=user_font, fill=text_color)
                
                each_user_img_list.append(user_name_im)

                
                # 画像の抽出
                for predict_uma_name in testuma_name_list:

                    if predict_uma_name not in predict_uma_name_list:   # 予想された馬に含まない場合は予想なし
                        predict_p = predict_im_path + str(prediction_names_list[6]) + '.jpg'
                        pre_im = Image.open(predict_p)
                        
                    else:   # もし含まれている場合

                        # もし馬名が予想された馬リストに存在している場合
                        if predict_dict[predict_uma_name] == hex_ord_list[0]:   # 二重丸
                            predict_p = predict_im_path + str(prediction_names_list[0]) + '.jpg'
                            pre_im = Image.open(predict_p)
                            
                        elif predict_dict[predict_uma_name] == hex_ord_list[1]:   # 丸
                            predict_p = predict_im_path + str(prediction_names_list[1]) + '.jpg'
                            pre_im = Image.open(predict_p)
                            
                        elif predict_dict[predict_uma_name] == hex_ord_list[2]:   # 三角
                            predict_p = predict_im_path + str(prediction_names_list[2]) + '.jpg'
                            pre_im = Image.open(predict_p)
                            
                        elif predict_dict[predict_uma_name] == hex_ord_list[3]:   # 黒三角
                            predict_p = predict_im_path + str(prediction_names_list[3]) + '.jpg'
                            pre_im = Image.open(predict_p)
                            
                        elif predict_dict[predict_uma_name] == hex_ord_list[4]:   # 星
                            predict_p = predict_im_path + str(prediction_names_list[4]) + '.jpg'
                            pre_im = Image.open(predict_p)
                            
                        elif predict_dict[predict_uma_name] == hex_ord_list[5]:   # バツ
                            predict_p = predict_im_path + str(prediction_names_list[5]) + '.jpg'
                            pre_im = Image.open(predict_p)
                            

                    each_user_img_list.append(pre_im)

                # userの予想表の結合
                concated_img = concat_height(unconcated_list=each_user_img_list)
                # userの予想表の保存
                #user_pred_saved_path = r"D:\keiba_bot\voted_bot\paper\saved\uma_prediction" + '\\'
                user_pred_saved_path = r'paper\saved' + '\\' + self.today_data + r'\uma_prediction' + '\\'
                if '/' in str(voted_user):  # 特殊文字の置き換え
                    voted_user = str(voted_user).replace('/', '_')
                if "\\" in str(voted_user):  # 特殊文字の置き換え
                    voted_user = str(voted_user).replace('\\', '_')
                user_saved_p = user_pred_saved_path + str(voted_user) + '_predict.jpg'
                #user_name_im.save(user_saved_p)
                concated_img.save(user_saved_p)
                print('predict saved file!')
                
                # 全体結合用のリストに保存
                all_concated_im.append(concated_img)


            """
            ++++++++++++++++++++++
            指数の計算と導入
            ++++++++++++++++++++++
            """

            # 馬名だけ取得
            print(horse_info_list)
            horse_name_list = []
            for horse_info_commas in horse_info_list:
                horse_info_comma = horse_info_commas.split(',')
                horse_name_list.append(horse_info_comma[2])

            score_dict = poll_score(vote_res=poll_res, regist_horse=horse_name_list, race_id=race_id)
            
            print(score_dict)

            # 結合用リスト
            each_score_list = []
            
            text_color = (0,0,0,255)
            score_font_path = r'C:\Windows\Fonts\HGRME.TTC'
            score_template_path = r"paper\race_score\uma_score.png"
            score_label_path = r"paper\race_score\uma_score_label_a.png"

            score_label_im = Image.open(score_label_path)
            each_score_list.append(score_label_im)

            score_font_size = 36
            score_font = ImageFont.truetype(score_font_path, score_font_size)
            
            for score_tuple in score_dict.items():

                score_im = Image.open(score_template_path)
                score_img = ImageDraw.Draw(score_im)
                print(score_tuple)
        
                if score_tuple[1] == 100.0:
                    
                    # 背景色の設定
                    #max_color = (255, 255, 255)
                    score_color = (255, 255-int(score_tuple[1]), 255-int(score_tuple[1]))
                    dst = Image.new('RGB', (score_im.width-4, score_im.height-4), score_color)
                    score_im.paste(dst, (2,2))

                    str_place = (58, 2)
                    in_score_str = "{:.1f}".format(score_tuple[1])
                    score_img.text(str_place, in_score_str, font=score_font, fill=text_color)

                else:
                    
                    # 背景色の設定
                    score_color = (255, 255-int(score_tuple[1]), 255-int(score_tuple[1]))
                    dst = Image.new('RGB', (score_im.width-4, score_im.height), score_color)
                    score_im.paste(dst, (2,0))
                    if score_tuple[1] < 0:
                        str_place = (37, 2)
                    else:
                        str_place = (47, 2)
                    in_score_str = "{:.1f}".format(score_tuple[1])
                    score_img.text(str_place, in_score_str, font=score_font, fill=text_color)

                each_score_list.append(score_im)


            score_concated_img = concat_height(unconcated_list=each_score_list)

            user_score_saved_path = r'paper\saved' + '\\' + self.today_data + r'\uma_score' + '\\'
            score_saved_p = user_score_saved_path + str(race_id) + '_score.jpg'
            score_concated_img.save(score_saved_p)
            all_concated_im.append(score_concated_img)
            print('score saved file!')


            # 最終的なすべての画像結合と保存
            # ロゴの画像読み込み
            #logo_p = r"D:\keiba_bot\voted_bot\paper_logos\logo_2.jpg"
            #logo_im = Image.open(logo_p)

            """
            #########################################
            開催情報の表示
            #########################################
            """

            # ロゴに情報の付与
            # フォントpath
            hold_info_font_path = r'C:\Windows\Fonts\HGRGY.TTC'
            hold_info_sub_font_path = r'C:\Windows\Fonts\HGRME.TTC'
            text_color = (0,0,0,255)

            # holdなどの情報
            hold_info_font_size = 30
            hold_info_font = ImageFont.truetype(hold_info_sub_font_path, hold_info_font_size)
            hold_place_info_font_size = 65
            hold_place_info_font = ImageFont.truetype(hold_info_font_path, hold_place_info_font_size)
            hold_day_info_font_size = 20
            hold_day_info_font = ImageFont.truetype(hold_info_sub_font_path, hold_day_info_font_size)
                
            hold_info_name_p = r"test_logo\logo_2.jpg"
            hold_info_name_im = Image.open(hold_info_name_p)
            hold_info_name_img = ImageDraw.Draw(hold_info_name_im)

            # 描画する開催情報関連
            race_hold_name = race_info_list[0]  # レース名
            race_hold_info = race_info_list[5]  # レース情報
            race_hold_time = race_info_list[4]  # レース時間
            race_hold_distance = race_info_list[3]  # レース距離

            # レース詳細情報の描画
            # 文字の入力
            str_place = (20, 33)
            hold_info_name_img.text(str_place, race_hold_name, font=hold_place_info_font, fill=text_color)    # レース名

            str_place = (20, 10)
            hold_info_name_img.text(str_place, self.hold_today_data, font=hold_day_info_font, fill=text_color)    # レース開催日

            str_place = (15, 130)
            race_start_info = race_hold_time + ' ' + race_hold_distance
            hold_info_name_img.text(str_place, race_start_info, font=hold_info_font, fill=text_color)    # レースの時間と距離



            # レース情報の長さ  # 地方か中央かで情報数が異なる
            race_hold_len = len(race_hold_info)
            print(race_hold_len)

            if race_hold_len == 9:

                str_place = (15, 165)
                race_hold_info_1 = ''
                for hold_i in range(0, 3):  # 3つ
                    race_hold_info_1 = race_hold_info_1 + race_hold_info[hold_i] + ' '
                hold_info_name_img.text(str_place, race_hold_info_1, font=hold_info_font, fill=text_color)    # レースhold 1

                str_place = (15, 200)
                race_hold_info_2 = ''
                for hold_i in range(3, 5):  # 2つ
                    race_hold_info_2 = race_hold_info_2 + race_hold_info[hold_i] + ' '
                hold_info_name_img.text(str_place, race_hold_info_2, font=hold_info_font, fill=text_color)    # レースhold 2

                str_place = (15, 235)
                race_hold_info_3 = ''
                for hold_i in range(5, 7):  # 2つ
                    race_hold_info_3 = race_hold_info_3 + race_hold_info[hold_i] + ' '
                hold_info_name_img.text(str_place, race_hold_info_3, font=hold_info_font, fill=text_color)    # レースhold 3

                str_place = (15, 270)
                race_hold_info_4 = ''
                for hold_i in range(7, 8):  # 1つ
                    race_hold_info_4 = race_hold_info_4 + race_hold_info[hold_i] + ' '
                hold_info_name_img.text(str_place, race_hold_info_4, font=hold_info_font, fill=text_color)    # レースhold 4

                str_place = (15, 305)
                race_hold_info_5 = ''
                for hold_i in range(8, 9):  # 1つ
                    race_hold_info_5 = race_hold_info_5 + race_hold_info[hold_i] + ' '
                hold_info_name_img.text(str_place, race_hold_info_5, font=hold_info_font, fill=text_color)    # レースhold 5


            elif race_hold_len == 6:
                str_place = (15, 165)
                race_hold_info_1 = ''
                for hold_i in range(0, 2):  # 2つ
                    race_hold_info_1 = race_hold_info_1 + race_hold_info[hold_i] + ' '
                hold_info_name_img.text(str_place, race_hold_info_1, font=hold_info_font, fill=text_color)    # レースhold 1

                str_place = (15, 200)
                race_hold_info_2 = ''
                for hold_i in range(2, 3):  # 1つ
                    race_hold_info_2 = race_hold_info_2 + race_hold_info[hold_i] + ' '
                hold_info_name_img.text(str_place, race_hold_info_2, font=hold_info_font, fill=text_color)    # レースhold 2

                str_place = (15, 235)
                race_hold_info_3 = ''
                for hold_i in range(3, 4):  # 1つ
                    race_hold_info_3 = race_hold_info_3 + race_hold_info[hold_i] + ' '
                hold_info_name_img.text(str_place, race_hold_info_3, font=hold_info_font, fill=text_color)    # レースhold 3

                str_place = (15, 270)
                race_hold_info_4 = ''
                for hold_i in range(4, 5):  # 1つ
                    race_hold_info_4 = race_hold_info_4 + race_hold_info[hold_i] + ' '
                hold_info_name_img.text(str_place, race_hold_info_4, font=hold_info_font, fill=text_color)    # レースhold 4


                re_hold_info_font_size = 20
                re_hold_info_font = ImageFont.truetype(hold_info_sub_font_path, re_hold_info_font_size)
                str_place = (15, 305)
                race_hold_info_5 = ''
                for hold_i in range(5, 6):  # 1つ
                    race_hold_info_5 = race_hold_info_5 + race_hold_info[hold_i] + ' '
                hold_info_name_img.text(str_place, race_hold_info_5, font=re_hold_info_font, fill=text_color)    # レースhold 5

            else:
                print('特殊なレースです。処理を中止します。')
                pass

            

            # 仕上げ

            finish_saved_path = r'paper\saved' + '\\' + self.today_data + r'\paper' + r'\keiba_paper.jpg'
            finish_keiba_paper_img = concat_width(unconcated_list=all_concated_im)
            finish_keiba_paper_img_logo = get_concat_v_blank(im1=finish_keiba_paper_img, im2=hold_info_name_im)


            # コメントが画像の生成
            comment_img = make_comments(width_size=finish_keiba_paper_img_logo.width, race_id=race_id, poll_res=poll_res, today_data=self.today_data)
            
            if comment_img != False:    # コメントが存在しない場合、Falseで返ってくるため
                # 最終的な画像の結合
                finish_keiba_papers = get_concat_comment(im1=comment_img, im2=finish_keiba_paper_img_logo)
                finish_keiba_papers.save(finish_saved_path)
            elif comment_img == False:  # コメントが存在しない場合
                print('コメント投稿がありませんでした')
                finish_keiba_papers = no_comment_concat(im1=finish_keiba_paper_img_logo)
                finish_keiba_papers.save(finish_saved_path)
            

            print('==========================')
            print('競馬新聞の完成です')
            print('==========================')


            # チャンネルに画像の送信
            send_paper_file_path = finish_saved_path
            await ctx.channel.send(file=discord.File(send_paper_file_path))

            # 投票結果の書き出し
            race_id_str = str(race_id)
            res_json_file_p = r'voted_res' + '\\' + race_id_str + r'_result.json'
            poll_res_path = r'user_record\main_poll_json' + '\\' + self.today_data + '\\' + str(race_id) + r'_poll_res.json'

            race_saved_id = race_id

            poll_res['race_id'] = race_id # レースidの追加
            poll_res['race_name'] = race_dict[race_saved_id]['race_name']  # レース名の追加
            poll_res['race_place'] = race_dict[race_saved_id]['race_place']    # 開催場所の追加
            poll_res['race_distance'] = race_dict[race_saved_id]['race_distance']  # レースの距離の追加

            with open(res_json_file_p, mode='wt', encoding='utf-8') as res_file:
                json.dump(poll_res, res_file, ensure_ascii=False, indent=4)

            # main_poll_jsonにも結果の保存
            main_poll_json = jf.READ_JSON(json_f_path=poll_res_path)
            main_poll_json.update(poll_res)
            jf.SAVE_JSON(json_f_save_path=poll_res_path, saved_dict=main_poll_json)

            print('投票結果の保存完了')
            await ctx.channel.send(f'@here {target_race_name}の投票結果です')

        # 投票が存在しない場合（type is str）
        else:
            no_poll_msg = f'【{target_race_name}' + poll_res
            print(no_poll_msg)
            await ctx.channel.send(f'@here {no_poll_msg}')

        



# コメント欄の生成と結合
def make_comments(width_size, race_id, poll_res, today_data):
    
    # userの確認
    user_list = list(poll_res.keys())
    # 倍率
    fx = 0
    fy = 0

    # コメントを投稿しているuserのIDリスト
    comment_user_list = []
    # コメントの有無の確認
    for user_name in user_list:
        if poll_res[user_name][race_id]['comment_check'] == True:
            comment_user_list.append(poll_res[user_name]['user_id'])


    # 画像の読み込み
    comment_saved_p = r'user_record\user_records'
    comment_user_number = int(len(comment_user_list))   # ユーザー数のリスト
    
    # 3列ごとに並べる
    three_counter = 0
    yoko_img_list = []
    concated_img = []

    # コメント画像が3つ以上ある場合結合
    if comment_user_number >= 3:
        
        for user_id in comment_user_list:
            user_comment_img_p = comment_saved_p + '\\' + str(user_id) + '\\' + today_data + '\\' + str(user_id) + '_' + str(race_id) + r'_comment.png'
            comment_im = Image.open(user_comment_img_p)
            
            # 画像の結合
            yoko_img_list.append(comment_im)
            three_counter = three_counter+1
            
            if three_counter == 3:  # 画像が3つ溜まった時
                three_img = concat_height(yoko_img_list)    # 画像の結合
        
                # 元の馬柱の画像の長さ/3つのコメントの画像の長さ=倍率
                bairitsu = width_size/three_img.width
                print(bairitsu)
                fx, fy = bairitsu, bairitsu
                size = (round(three_img.width * fx), round(three_img.height * fy))
                re_three_img = three_img.resize(size)
                
                concated_img.append(re_three_img)

                # 初期化
                three_counter = 0
                yoko_img_list = []
            
        # あまりの画像を結合して最後にくっつける
        if len(yoko_img_list) == 1:
            # 縦に連結
            comment_concated_img = concat_width(concated_img)

            one_img = yoko_img_list[0]
            size = (round(one_img.width * fx), round(one_img.height * fy))
            re_one_img = one_img.resize(size)

            return get_concat_comment(im1=re_one_img, im2=comment_concated_img)
        elif len(yoko_img_list) == 2:
            # 縦に連結
            comment_concated_img = concat_width(concated_img)
            temp_two_img = concat_height(yoko_img_list)

            size = (round(temp_two_img.width * fx), round(temp_two_img.height * fy))
            re_two_img = temp_two_img.resize(size)

            return get_concat_comment(im1=re_two_img, im2=comment_concated_img)
        elif len(yoko_img_list) == 0:
            return concat_width(concated_img)
    
    # 画像が2つの場合
    elif comment_user_number == 2:
        for user_id in comment_user_list:
            user_comment_img_p = comment_saved_p + '\\' + str(user_id) + '\\' + today_data + '\\' + str(user_id) + '_' + str(race_id) + r'_comment.png'
            comment_im = Image.open(user_comment_img_p)
            # 画像の結合
            yoko_img_list.append(comment_im)
        return concat_height(yoko_img_list)

    # 画像が1つの場合
    elif comment_user_number == 1:
        for user_id in comment_user_list:
            user_comment_img_p = comment_saved_p + '\\' + str(user_id) + '\\' + today_data + '\\' + str(user_id) + '_' + str(race_id) + r'_comment.png'
            comment_im = Image.open(user_comment_img_p)
        return comment_im

    elif comment_user_number == 0:
        return False
    else:
        pass

# 縦の高さが同じもの
def concat_height(unconcated_list):

    # 画像の読み込み
    r_user_pred_list = list(reversed(unconcated_list))
    width_im = 0
    for user_pred_im in r_user_pred_list:
        width_im = width_im+user_pred_im.width

    # 貼り付け先画像の生成
    dst_img = Image.new('RGB', (width_im, unconcated_list[0].height))

    # 画像の結合
    paste_x = 0
    for paste_im in r_user_pred_list:
        dst_img.paste(paste_im, (paste_x ,0))
        paste_x = paste_x+paste_im.width

    return dst_img


# 横の幅が同じもの
def concat_width(unconcated_list):

    # 画像の読み込み
    height_im = 0
    for user_pred_im in unconcated_list:
        height_im = height_im+user_pred_im.height

    # 貼り付け先画像の生成
    dst_img = Image.new('RGB', (unconcated_list[0].width ,height_im))

    # 画像の結合
    paste_y = 0
    for paste_im in unconcated_list:
        dst_img.paste(paste_im, (0 ,paste_y))
        paste_y = paste_y+paste_im.height

    return dst_img


# ロゴの結合
def get_concat_v_blank(im1, im2):
    color=(255, 255, 255)
    dst = Image.new('RGB', (max(im1.width, im2.width), im1.height + im2.height), color)
    dst.paste(im2, ((im1.width-im2.width), 0))  # ロゴの画像貼り付け
    dst.paste(im1, (0, im2.height)) # 1枚目の画像貼り付け
    return dst


# コメントの結合
def get_concat_comment(im1, im2):   # im2が馬柱
    color=(255, 255, 255)
    dst = Image.new('RGB', (max(im1.width, im2.width), im1.height + im2.height), color)
    dst.paste(im1, ((im2.width-im1.width), im2.height))
    dst.paste(im2, (0, 0))  # 1枚目の画像貼り付け
    return dst


def no_comment_concat(im1):
    color=(255, 255, 255)
    dst = Image.new('RGB', (im1.width, im1.height), color)
    dst.paste(im1, (0, 0))  # 1枚目の画像貼り付け
    return dst





def setup(bot):
    bot.add_cog(Hand_Make_Paper_Cmd_Cog(bot))



