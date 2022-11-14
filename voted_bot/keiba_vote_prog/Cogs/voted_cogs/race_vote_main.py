from asyncore import poll
from discord.ext import commands
import discord
import datetime
import os
import pathlib

from main_sub_func import gate_color_set as clr_set
from main_sub_func import json_func as jf
from main_sub_func import race_info_getting as race_get

class Race_Vote_Cmd_Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # 日付の取得
        dt_now = datetime.datetime.now()
        self.today_data = str(dt_now.year) + str(dt_now.month).zfill(2) + str(dt_now.day).zfill(2)
        
    
    @commands.command()
    async def vote_start(self, ctx, *voted_race_id):

        # コマンドを打ったユーザーの取得
        user_name = ctx.message.author.name
        user_id  = ctx.message.author.id    # user_idの取得
        flag_dir_path = r'user_record\vote_flag' + '\\' + str(user_id) + '_' + 'vote_flag.flag'
        
        
        if not os.path.exists(flag_dir_path):
            # 投票するレースidの確認
            user_voted_race_id = voted_race_id[0]
            # 日付の取得
            today_str = self.today_data
        
            # レース名の取得
            _, race_data_list, _, _, _, _ = race_get.race_jsons(race_id=user_voted_race_id)
            race_name = race_data_list[0]

            """
            ################################
            userの基礎情報フォルダの作成
            ################################
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
            
            # ++++++++++++++++++++++++++++++++++++++++++++
            # user専用のファイルの作成があるかの確認
            # ++++++++++++++++++++++++++++++++++++++++++++

            print('===== <== ユーザーの個別ファイルの確認 ==> =====')
            user_dir_path = r'user_record\user_records' + '\\' + str(user_id)  # ユーザーの個別フォルダパス
            print('検索ディレクトリ : {}'.format(user_dir_path))

            if os.path.exists(user_dir_path):
                
                print('ユーザーディレクトリがありました.本日の日付のファイルの確認を実行')
                today_file_path = user_dir_path + '\\' + today_str
                # 日付ファイルの確認
                if os.path.exists(today_file_path):
                    print('既にファイルが存在しています')
                else:
                    os.mkdir(today_file_path)
                    print('作成先 : {}'.format(today_file_path))

                temp_file_path = today_file_path + '\\' + r'temp'
                if os.path.exists(temp_file_path):
                    print('既にファイルが存在しています')
                else:
                    print('レース投票用のtempファイルの作成を行います')
                    os.mkdir(temp_file_path)
                    print('レースtemp作成先 : {}'.format(temp_file_path))
                
            else:
                print('ユーザーディレクトリがありません.個別ユーザーディレクトリの作成を行います')
                user_file_path = user_dir_path
                os.mkdir(user_file_path)
                print('作成先 : {}'.format(user_file_path))

                print('本日の日付のファイルを作成します')
                today_file_path = user_dir_path + '\\' + today_str
                os.mkdir(today_file_path)
                print('作成先 : {}'.format(today_file_path))

                print('レース投票用のtempファイルの作成を行います')
                temp_file_path = today_file_path + '\\' + r'temp'
                os.mkdir(temp_file_path)
                print('レースtemp作成先 : {}'.format(temp_file_path))
            # ++++++++++++++++++++++++++++++++++++++++++++
                
            
            print('========== <== レースtempディレクトリ内に投票結果の一時保存jsonの作成 ==> ==========')
            saved_user_temp_dict = {}
            user_temp_json_path = temp_file_path + r'\res_temp.json' 
            jf.SAVE_JSON(json_f_save_path=user_temp_json_path, saved_dict=saved_user_temp_dict)
            print('作成jsonパス : {}'.format(user_temp_json_path))



            print('========== <== 作成完了 ==> ==========')
            print('\n\n')




            # 該当レースが投票されているかの確認
            user_dict_saved_path = user_dir_path  + '\\' + today_str + '\\' + str(user_id) + '_' + str(user_voted_race_id) + '.json'
            if not os.path.exists(user_dict_saved_path):

                # 投票中flagの設定
                pathlib.Path(flag_dir_path).touch()
                

                # 辞書の作成
                dict_user_list = [user_name]
                dict_value_list = [make_template_dict(race_id=user_voted_race_id)]
                user_dict = dict(zip(dict_user_list, dict_value_list))
                
                print('========== <== 投票開始userの基本情報 ==> =========='.format(user_name))
                print('user name : {}'.format(user_name))
                print('user id : {}'.format(user_id))

                print('========== <== {}の投票結果用dictが作成されました ==> =========='.format(user_name))
                print('レースID : {}'.format(user_voted_race_id))
                print('投票ユーザー : {}'.format(user_name))
                print(user_dict)

                # メッセージ削除用リストの取得
                msg_list = user_dict[user_name]['del_msg']

            
                _, _, umatest_list, _, _, _ = race_get.race_jsons(race_id=user_voted_race_id)

                # 投票項目のリアクションの設定
                reaction_buttons = [ '🧿', '⭕', '🔼', '🔽', '⭐', '❌' ] 
                # 枠色の設定
                waku_color = clr_set.gate_color(uma_list=umatest_list)



                # 投票開始時にメンションで簡易的な注意事項を投げる
                #await ctx.channel.send(f"<@{user_id}>さん、投票開始ありがとうございます。DMにて投票を行ってください。\nなお投票欄生成完了まで投票を行わないでください。")
                await ctx.channel.send(f"<@{user_id}>さん、【{race_name}】への投票開始ありがとうございます。DMにて投票を行ってください。\nなお投票欄生成完了まで投票を行わないでください。\n最後にメッセージが表示されてから投票を開始してください")

                # 投票方法のEmbedの送信
                voted_method_embed = discord.Embed(title="予想の投票方法(画像は投票例)", color=0x00ff00, description="必ず、投票方法をよく読んだ上で予想を投稿してください")

                voted_method_embed.add_field(name='【手順１】',value='印をつけたい馬のリアクションを押してください',inline=False)
                voted_method_embed.add_field(name='【手順２】',value='印をつけ終わったら「投票終了」と入力して送信してください',inline=False)
                voted_method_embed.add_field(name='【tips】',value='全ての印を投票する必要はありません。\n◎1つだけの投票でも可能です。\nまた投票は1時間以内に行ってください。',inline=False)

                voted_method_embed.add_field(name=reaction_buttons[0],value='印：◎',inline=True)
                voted_method_embed.add_field(name=reaction_buttons[1],value='印：○',inline=True)
                voted_method_embed.add_field(name=reaction_buttons[2],value='印：△',inline=True)
                voted_method_embed.add_field(name=reaction_buttons[3],value='印：▲',inline=True)
                voted_method_embed.add_field(name=reaction_buttons[4],value='印：☆',inline=True)
                voted_method_embed.add_field(name=reaction_buttons[5],value='印：×',inline=True)

                vote_ok_file = discord.File(r"example_img\ok3.png", filename=r"keiba_info_ok_1.png")
                voted_method_embed.set_image(url=r"attachment://keiba_info_ok_1.png")
                info_msg = await ctx.author.send(file=vote_ok_file, embed=voted_method_embed)
                msg_list.append(info_msg)

                # 注意事項1
                voted_infos_embed_1 = discord.Embed(title="注意事項1(画像はNG例)", color=0xff0000, description='1つの馬に複数のチェックをつけるのはご遠慮ください\n（もし間違えてつけてしまったら間違えたリアクションを外してください）')
                ng1_file = discord.File(r"example_img\ng1.png", filename=r"keiba_info_1.png")
                voted_infos_embed_1.set_image(url=r"attachment://keiba_info_1.png")
                ng1_msg = await ctx.author.send(file=ng1_file, embed=voted_infos_embed_1)
                msg_list.append(ng1_msg)

                # 注意事項2
                voted_infos_embed_2 = discord.Embed(title="注意事項2(画像はNG例)", color=0xff0000, description='投票終了を1回以上送信しないでください')
                ng2_file = discord.File(r"example_img\ng2.png", filename=r"keiba_info_2.png")
                voted_infos_embed_2.set_image(url=r"attachment://keiba_info_2.png")
                ng2_msg = await ctx.author.send(file=ng2_file, embed=voted_infos_embed_2)
                msg_list.append(ng2_msg)

                
                # 注意事項3
                voted_infos_embed_3 = discord.Embed(title="注意事項3", color=0xff0000, description='投票は、投票欄がすべて生成されてから行って下さい。\n生成途中にクリックすると投票ができなくなりますのでご注意ください。')
                ng3_msg = await ctx.author.send(embed=voted_infos_embed_3)
                msg_list.append(ng3_msg)
                
                
                # 馬情報の取り出し
                for uma_info, gate_color_code in zip(umatest_list, waku_color):
                    uma_info_list = uma_info.split(',')

                    # 出力する馬の情報の設定
                    uma_value = str(uma_info_list[0]) + '枠' + str(uma_info_list[1]) + '番' + ':' + str(uma_info_list[2])

                    # userのdmに送信
                    uma_info_embed = discord.Embed(title=uma_value, color=gate_color_code)
                    msg = await ctx.author.send(embed=uma_info_embed)
                    msg_list.append(msg)
                    # １つの馬名に対して個別にリアクションの設定
                    for i in range(len(reaction_buttons)):
                        await msg.add_reaction(reaction_buttons[i])   


                # buttonの生成
                #voted_button = await ctx.author.send('投票が完了したら、以下の投票ボタンを押してください。（一回以上押さないでください）', view=pollButton(button_name='投票', msg_del_list=msg_list))
                
                """
                ボタン廃止してwait_forによる記載に変更
                """
                await ctx.author.send(f'投票を終える際は、本DMにて「投票終了」と入力し送信してください。')


                def check(message: discord.Message):
                    #return m.content == '$投票終了' and type(m.channel) == discord.DMChannel
                    print('チェック開始')
                    return message.author.id == user_id and message.content.lower() == '投票終了'

                
                # 投票終了入力待ち部分
                while True:
                    print('True チェック開始')
                    m = await self.bot.wait_for('message', check=check, timeout=3600)
                    if m.content.lower() == '投票終了':
                        print('========== <== {}が投票を終了しました ==> =========='.format(user_name))
                        break
                    

                print(m.content.lower())
                
                if m.content.lower() == '投票終了':

                    await ctx.author.send(f'<@{user_id}>さん投票ありがとうございました.しばらくお待ちください')
                    
                    # 投票メッセージの削除。
                    if len(msg_list) != 0:
                        for msg_del in msg_list:
                            await msg_del.delete()

                
                    print('========== <== 投票終了 ==> ==========')
                else:
                    await ctx.author.send(f'投票の有効時間が失効しました。<@{user_id}>さん投票失敗です。')

                
                """
                try:
                    msg = await bot.wait_for('vote_start', check=check, timeout=3600)
                except asyncio.TimeoutError:
                    await ctx.author.send(f'<@{user_id}>さん、時間切れです')
                else:
                    # メンション付きでメッセージを送信する。
                    if len(msg_list) != 0:
                        for msg_del in msg_list:
                            await msg_del.delete()
                
                    await ctx.author.send(f'<@{user_id}>さん投票ありがとうございました')
                """

                # 投票結果の取得及びpoll_res dictにアップデート
                race_user_poll_dict = jf.READ_JSON(json_f_path=user_temp_json_path)
                user_dict[user_name][user_voted_race_id]['res'] = race_user_poll_dict  # 結果の挿入
                user_dict[user_name][user_voted_race_id]['poll_checker'] = True # 投票済みの印
                user_dict[user_name].pop('del_msg')
                
                user_dict[user_name]['user_id'] = str(user_id)

                print("=====================================")
                print(race_user_poll_dict)
                print('\n')
                print(user_dict)
                print('\n')
                print("=====================================")
                
                print('========== <== {}の投票結果用dictの保存 ==> =========='.format(user_name))
                print('投票結果保存json保存先 : {}'.format(user_dict_saved_path))
                jf.SAVE_JSON(json_f_save_path=user_dict_saved_path, saved_dict=user_dict)
                

                await ctx.author.send(f'続いて、コメントの投票を行う場合、このままDMにて「$comment_help」のコマンドを入力してください。')
                await ctx.author.send('今回の投票レース【{}】'.format(race_name))
                await ctx.author.send('今回の投票レース【{}】'.format(user_voted_race_id))
                
                # 投票者のレコードの記録
                print('投票者を記録します')
                vote_user_record_path = r'vote_user_record' + '\\' + today_str + '\\' + str(user_voted_race_id) + '_' + r'vote_user_record.json'
                vote_user_record_json = jf.READ_JSON(json_f_path=vote_user_record_path)
                vote_user_record_json[user_name] = str(user_id)
                jf.SAVE_JSON(json_f_save_path=vote_user_record_path, saved_dict=vote_user_record_json)
                print('投票者記録完了')
                
                # flagファイルの削除
                print('flagファイルを削除します')
                os.remove(flag_dir_path)
            else:   # 既にレースIDがあった場合
                await ctx.channel.send(f"投票は1度のみです。<@{user_id}>さんは既に投票済みのため、投票できません。")
        else:
            print(flag_dir_path)
            print(os.path.exists(flag_dir_path))
            await ctx.channel.send(f"<@{user_id}>さんは、現在投票中です。現在の投票を終えてから次の投票を行ってください")



def make_template_dict(race_id):

    # 予想結果をユーザーごとに管理するdict
    predict_res_dict_key = [ str(race_id), 'del_msg', 'user_id' ]
    msg_removed_list = []
    #predict_res_dict_value = [ make_reaction_dict(), "temp_comment", msg_removed_list ]    ### ~2022/01/07
    predict_res_dict_value = [ res_make_dict(), msg_removed_list, '' ]

    # 予想用テンプレート辞書
    predict_template_dict = dict(zip(predict_res_dict_key, predict_res_dict_value))
    return predict_template_dict


def res_make_dict():

    # レースごとの投票結果の具体的な記録辞書
    res_dict_key = ['res', 'comment_check', 'poll_checker']
    res_dict_value = [dict(), False, False]
    res_dict = dict(zip(res_dict_key, res_dict_value))
    return res_dict 



"""
2022/01/2x~
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
        },
        "race_id" : {
            "res" : {
            uma A : reaction x,
            uma B : reaction y,
            uma C : reaction z,
            }
            "comment_check" : False
            "del_msg" : [ removed msg list ]
        },
        "user_id" : userのID
    },
    "user_name" : {
        "race_id" : {
            "res" : {
            uma A : reaction x,
            uma B : reaction y,
            uma C : reaction z,
            }
            "comment_check" : False
            "del_msg" : [ removed msg list ]
        },
        "race_id" : {
            "res" : {
            uma A : reaction x,
            uma B : reaction y,
            uma C : reaction z,
            }
            "comment_check" : False
            "del_msg" : [ removed msg list ]
        },
        "user_id" : userのID
    }
}



"""


def setup(bot):
    bot.add_cog(Race_Vote_Cmd_Cog(bot))