from discord.ext import commands
import discord
import requests
import cv2
import os
import datetime
from PIL import Image, ImageDraw, ImageFont
from main_sub_func import json_func as jf

class Comment_Vote_Cmd_Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # 日付の取得
        dt_now = datetime.datetime.now()
        self.today_data = str(dt_now.year) + str(dt_now.month).zfill(2) + str(dt_now.day).zfill(2)
        

    @commands.command()
    async def comment_voted(self, ctx, *user_comments):
    
        # 文字入れの設定
        comment_main_path = r"paper\comment_form\comment_form_main.png"
        name_font_size = 25
        font_path = r'C:\Windows\Fonts\HGRME.TTC'
        text_color = (0,0,0,255)
        name_font = ImageFont.truetype(font_path, name_font_size)
        comment_im = Image.open(comment_main_path)
        comment_main_img = ImageDraw.Draw(comment_im)

        # コマンドを打ったユーザーの取得
        user_name = ctx.message.author.name
        user_id  = ctx.message.author.id
        # コメント投票先のレースIDの取得
        race_id = user_comments[0]
        # 日付の取得
        today_str = self.today_data

        # 投票済jsonの取得
        json_f_name = str(user_id) + '_' + str(race_id) + '.json'
        voted_json_path = r'user_record\user_records' + '\\' + str(user_id) + '\\' + str(today_str) + '\\' + json_f_name


        # 出力するコメント
        new_comment = {}
        if (type(ctx.channel) == discord.DMChannel):    # dmにて投票が行われたか判別
            
            # 既に投票済みかどうか調べる
            if os.path.exists(voted_json_path):

                voted_json = jf.READ_JSON(json_f_path=voted_json_path)
                            
                # コメントが既に投稿されているかの確認
                comment_vote_check = voted_json[user_name][race_id]['comment_check']
                if comment_vote_check is False:

                    # コマンドを打ったユーザーのiconの保存
                    user_id  = ctx.message.author.id
                    user_ = ctx.message.author
                    avatar_128x128_png_url = user_.display_avatar.with_size(64).url
                    saved_p = r'user_record\user_records' + '\\' + str(user_id) + '\\' + str(user_id) + r'_icon.png' 

                    # 保存処理
                    with requests.get(avatar_128x128_png_url) as r:
                        img_data = r.content
                    with open(saved_p, 'wb') as handler:
                        handler.write(img_data)

                    # コメントの表示
                    print(user_comments[1])
                    if len(user_comments[1]) > 120:
                        await ctx.author.send('文字数がオーバーしています。\n再度投稿を行ってください（現在の文字数【{}文字】）'.format(len(user_comments)))
                    else:
                        kaigyo = 30 # 改行する文字数
                        new_comment = ''
                        gyosu = int(len(user_comments[1])/kaigyo)
                        print(gyosu)
                        for counter_ in range(0,gyosu+1):
                            new_comment = new_comment+(user_comments[1])[counter_*kaigyo : (counter_+1)*kaigyo] + '\n'

                        print(new_comment)
                        str_place = (15, 70)
                        comment_main_img.text(str_place, new_comment, font=name_font, fill=text_color)
                        
                        
                        # アイコンの挿入
                        icon_path = saved_p
                        icon_im = Image.open(icon_path)
                        icon_img = ImageDraw.Draw(icon_im)


                        # 画像の大きさ取得
                        print('===== <= リサイズ判定 => =====')
                        good_icon_size = 64
                        icon_w, icon_h = icon_im.size
                        icon_w_zoom = 1.0
                        icon_h_zoom = 1.0
                        icon_size_checker_w = False
                        icon_size_checker_h = False
                        # 横幅のチェック
                        if icon_w != good_icon_size:
                            icon_w_zoom = good_icon_size/icon_w
                            icon_size_checker_w = True
                            print('リサイズが必要になります。（元w : {}、リサイズ倍率 : {}）'.format(icon_w, icon_w_zoom))
                        else:
                            print('wのリサイズ無し')
                        # 高さのチェック
                        if icon_h != good_icon_size:
                            icon_h_zoom = good_icon_size/icon_h
                            icon_size_checker_h = True
                            print('リサイズが必要になります。（元h : {}、リサイズ倍率 : {}）'.format(icon_h, icon_h_zoom))
                        else:
                            print('hのリサイズ無し')
                        # チェッカー判別でリサイズ
                        if (icon_size_checker_w == True) or (icon_size_checker_h == True):
                            print('リサイズの実行')
                            icon_resize = (round(icon_im.width * icon_w_zoom), round(icon_im.height * icon_h_zoom))
                            icon_im = icon_im.resize(icon_resize)
                            print('リサイズ後の画像 : width:{}、height:{}'.format(icon_im.width, icon_im.height))
                        else:
                            print('リサイズは行われませんでした')

                        print('===== <= リサイズ終了 => =====')

                        # 指定した倍率でアイコンをリサイズする。
                        fx, fy = 0.8, 0.8
                        size = (round(icon_im.width * fx), round(icon_im.height * fy))

                        dst = icon_im.resize(size)

                        comment_im.paste(dst, (10, 10))

                        name_font_size = 22
                        name_font = ImageFont.truetype(font_path, name_font_size)
                        name_place = (60, 30)
                        user_str = user_name+'の予想'
                        comment_main_img.text(name_place, user_str, font=name_font, fill=text_color)

                        #comment_saved_p = r"D:\keiba_bot\voted_bot\paper\comment_form\user_comment" + '\\'+ str(user_id) + r'_comment.png'
                        # 個別の結果保存先は、「user_id + todayb + userid_race_id.json　で管理」
                        comment_saved_p = r'user_record\user_records' + '\\' + str(user_id) +  '\\' + self.today_data + '\\' + str(user_id) + '_' + str(race_id) + r'_comment.png'
                        comment_im.save(comment_saved_p)
                        print('saved main uma info')

                        await ctx.author.send(f"<@{user_id}>さんコメントありがとうございます。")
                        voted_json[user_name][race_id]['comment_check'] = True
                        jf.SAVE_JSON(json_f_save_path=voted_json_path, saved_dict=voted_json)
                        print('========== <== Trueに更新済みpoll resの保存 ==> ==========')

                        # コメント画像の生成
                        await ctx.channel.send(file=discord.File(comment_saved_p))

                else:   # 既に一回コメントが投稿されている場合
                    await ctx.author.send(f"<@{user_id}>さんは既に一度コメントを投票しています。再度投稿はできません。")
            else:   # 投票していない場合
                await ctx.author.send(f"投票が行われていません。<@{user_id}>さんは先に投票を行ってください。")
        else:
            await ctx.channel.send(f"<@{user_id}>さん、DMにてコメントの投票を行ってください")





def setup(bot):
    bot.add_cog(Comment_Vote_Cmd_Cog(bot))