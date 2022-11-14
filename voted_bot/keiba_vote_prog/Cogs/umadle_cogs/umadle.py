import random
from discord.ext import commands
import discord
import os
import pathlib
import copy

from main_sub_func import json_func as jf



class Umadle_Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def umadle(self, ctx: commands.context):


        # コマンドを打ったユーザーの取得
        user_name = ctx.message.author.name
        user_id  = ctx.message.author.id    # user_idの取得
        flag_dir_path = r'user_record\vote_flag' + '\\' + str(user_id) + '_' + 'umadle_flag.flag'



        if not os.path.exists(flag_dir_path):
            # 投票中flagの設定
            pathlib.Path(flag_dir_path).touch()

            await ctx.channel.send(f"<@{user_id}>さん、Umadleのプレイを開始しました。DMにて遊んでください")
            print(f'{user_name}さんがumadleを開始しました')



            # 難易度選択
            level_embed = discord.Embed(title="『Umadleへようこそ！』", description="難易度を選んでね", color=0xeee657)
            level_embed.add_field(name="難易度 : Easy", value="『1』と入力し送信(『』は外して半角数字のみ送信)", inline=False)
            level_embed.add_field(name="難易度 : Hard", value="『2』と入力し送信(『』は外して半角数字のみ送信)", inline=False)
            level_embed.add_field(name="難易度 : Extra", value="『3』と入力し送信(『』は外して半角数字のみ送信)", inline=False)
            level_embed.add_field(name="難易度 : Lunatic", value="『4』と入力し送信(『』は外して半角数字のみ送信)", inline=False)
            level_embed.add_field(name="【注意】", value="Hardモードはかなり難しいと思うので競馬玄人向けです。", inline=False)
            level_embed.add_field(name="【注意】", value="ExtraとLunaticモードは『ノーヒント』で正解できたら本当にガチのマジですごいと思います。", inline=False)
            
            await ctx.author.send(embed=level_embed)

            # レベルのチェック
            def level_check(message: discord.Message):
                #return m.content == '$投票終了' and type(m.channel) == discord.DMChannel
                print('レベルチェック開始')
                return message.author.id == user_id and len(message.content.lower())!=0 and message.content.lower() in ['1', '2', '3', '4']
            level_ans = await self.bot.wait_for('message', check=level_check, timeout=3600)
            level_ans = level_ans.content.lower()

            # level設定
            if level_ans == '1':    # Easyの場合
                level_name = 'easy'

            elif level_ans == '2':  # Hardの場合
                level_name = 'hard'

            elif level_ans == '3':  # Extraの場合
                level_name = 'extra'

            elif level_ans == '4':  # lunaticの場合
                level_name = 'lunatic'
            

            await ctx.author.send(f'レベル【{level_name}】が選択されました')
            level_dir_path = r"Cogs\umadle_cogs\questions" + "\\" + level_name
            # 問題ファイルの読み込み
            files = os.listdir(level_dir_path)
            files_file_list = [f for f in files if os.path.isfile(os.path.join(level_dir_path, f))]  # ファイルの読み込み
            question_json_name = random.choice(files_file_list)
            question_json_path = level_dir_path + '\\' + question_json_name

            # jsonファイルの読み込み
            question_dict = jf.READ_JSON(json_f_path=question_json_path)

            # 各種パラメータの設定
            question_sentence = question_dict['question_data']['question_sentence']     # 問題文
            ans_limit = question_dict['question_data']['ans_limit']                     # 答えの入力可能回数
            ans_data = question_dict['question_data']['ans_data']

            # リストの要素の最大の長さ
            max_len = max([len(x) for x in ans_data])
            ans_max = len(ans_data) # 答えの数
            
            # 答えのセット
            ans = random.choice(ans_data)
            print('<<=========================================== ゲーム開始 =====================================================>>')
            print(f'管理用 : 回答者『{user_name}』、答え : 『{ans}』、レベル : 『{level_name}』\n問題番号 : 『{question_json_name}』、問題文 : 「{question_sentence}」')
            print('===============================================================================================================')

            # 空の解答枠の生成
            emp_ans = '⬜'
            good_ans = '🟩'
            half_ans = '🟨'

            # ルール表示
            embed = discord.Embed(title="Umadle", description="競馬版Wordle", color=0xeee657)

            embed.add_field(name="ルール1", value="競走馬の名前を当てていくゲーム\nwordleに準拠", inline=False)
            embed.add_field(name="ルール2", value="問題文に該当する名前のみ入力可能", inline=False)
            embed.add_field(name="ルール3", value="DMにて正解だと思う競争馬の名前を入力し送信してください", inline=False)
            if level_name == 'Extra':   # Extraモードの場合のみ
                embed.add_field(name="ルール(Extraのみ)", value="外国の種牡馬も正解になりうる場合があります。このumadleでは英語表記の馬の場合、次のような形で空白は正解に含めていません。\n(EX)「No Nay Never」→「NoNayNever」\n入力の際も空白無しで連続で入力してください", inline=False)
                embed.add_field(name="ルール(Extraのみ)", value="英語表記馬に関しては大文字小文字の区別があります。\n(EX)「NoNayNever」が正解の場合、「Nonaynever」の入力は反応しません。", inline=False)
                embed.add_field(name="ヒント(Extraのみ)", value="データは、netkeibaの「種牡馬リーディング(2021年)」に掲載の上位100件を抽出して居ます。よって正解の表記もそこに掲載のある通りのスペルになります。", inline=False)
            if level_name == 'Lunatic': # Lunaticモードの場合のみ
                embed.add_field(name="ルール(Lunaticのみ)", value="ここでいう三冠馬とは、地方競馬なども含めた、国内で開催（もしくは開催されていた）レースで三冠を達成した競争馬を指します。\nまた現在ではレースとして現存しないアラブ種も含んでおります。", inline=False)
                embed.add_field(name="ヒント(Lunaticのみ)", value="データは、wikipediaの「三冠（競馬）」の記事の日本国内部分を参照し、そこに掲載されている競走馬を問題としています。\nよって正解の表記もそこに掲載のある通りのスペルになります。", inline=False)
            
            embed.add_field(name="記号の説明", value=f"答えの中にその『文字が含まれている』場合：{half_ans}\n更に『場所も合っている』場合 : {good_ans}", inline=False)
            # 開発者
            embed.set_footer(text="made by Domzou (原作:wordle(https://www.nytimes.com/games/wordle/index.html))")

            await ctx.author.send(embed=embed)


            #問題文の提示など
            # 問題表示
            question_embed = discord.Embed(title=f"ゲームモード : {level_name}", description="ゲーム設定", color=0xeee657)

            question_embed.add_field(name="問題", value=f"【{question_sentence}】", inline=False)
            question_embed.add_field(name="解答の入力可能回数", value=f"{ans_limit}回", inline=False)
            question_embed.add_field(name="答えの候補数", value=f"{ans_max}頭", inline=False)

            await ctx.author.send(embed=question_embed)




            # 回答表示フォームembed
            ans_embed = discord.Embed(title="現在の回答状況", description="リザルト", color=0xeee657)

            ans_checker = True
            rm_checker = False
            input_checker = True
            now_ans = emp_ans*len(ans)
            ans_counter = 0
            ans_counter_rule = ans_limit


            def check(message: discord.Message):
                #return m.content == '$投票終了' and type(m.channel) == discord.DMChannel
                print('チェック開始')
                return message.author.id == user_id and len(message.content)!=0

            # 現在の解答
            ans_msg_list = []
            false_word_list = []        # 不正解のワード
            tmp_ans_list = copy.deepcopy(ans_data)           # 正解の可能性のある馬名   
            true_flag = True
            ans_embed.add_field(name="正解文字数", value=f"{len(ans)}文字", inline=False)    # 正解の文字数
            
            
            while ans_checker and ans_counter<ans_counter_rule:

                # 最新の答えの入力フォーム
                new_ans = ''
                # 残りの選択肢の数
                ans_possible_num = len(tmp_ans_list)
                
                # メッセージの削除
                if len(ans_msg_list) != 0 and rm_checker == True:
                    await ans_msg_list[0].delete()
                    ans_msg_list.pop(0)
                    rm_checker = False

                # 初回以降
                if ans_counter != 0 and input_checker == True:
                    ans_embed.add_field(name=f"{ans_counter}回目の回答結果：{user_ans}", value=f"{now_ans}", inline=False)
                    ans_embed.add_field(name=f"残り選択肢数", value=f"{ans_possible_num}／{ans_max}", inline=False)
                    ans_msg = await ctx.author.send(embed=ans_embed)
                    ans_msg_list.append(ans_msg)
                elif ans_counter == 0 and input_checker == True:
                    ans_embed.add_field(name=f"スタート！", value=f"{now_ans}", inline=False)
                    ans_embed.add_field(name=f"残り選択肢数", value=f"{ans_possible_num}／{ans_max}", inline=False)
                    ans_msg = await ctx.author.send(embed=ans_embed)
                    ans_msg_list.append(ans_msg)


                ### print(f'残り回答数：{5-ans_counter}')
                # userの入力
                ### print(now_ans)
                
                ##print('解答の入力', end=' : ')

                
                ### user_ans = input()
                user_ans = await self.bot.wait_for('message', check=check, timeout=3600)
                user_ans = user_ans.content
                # await ctx.author.send(user_ans)

                print('=====================================')
                print(f'入力されたウマ : 【{user_ans}】\n{ans_counter+1}回目')
                print('=====================================')
                if user_ans in ans_data:   # リストに含まれている文字かどうか
                    rm_checker = True
                    input_checker = True
                    if user_ans != ans:         # 答えかどうか
                        ans_counter += 1
                        # 該当文字をチェックする
                        for index, word in enumerate(user_ans):

                            # まず文字を含んでいるか
                            if word in ans:
                                
                                # その文字を含んでいるならば、どの位置に属しているかをチェック
                                if index != ans.index(word):    # 不正解だけど含まれている箱(half_ans)
                                    new_ans += half_ans
                                else:                           # 正解の箱（good_ans）
                                    new_ans += good_ans
                            
                            else:    # その文字を含んでいない場合
                                new_ans += emp_ans
                                false_word_list.append(str(word))    # 不正解の文字
                    else:
                        new_ans = good_ans*len(user_ans)
                        true_flag = True
                        now_ans = new_ans
                        break
                else:
                    await ctx.author.send('その名前のウマ娘は存在しないよ！入力し直してね！')
                    print('存在しない答えが入力されました')
                    new_ans = emp_ans*len(ans)
                    input_checker = False
                    
                now_ans = new_ans   # 現在の一致と部分一致の絵文字の更新
                
                if input_checker == True:
                    # 残り正解数の確認
                    tmp_copy_list = []
                    for tmp_ans_data in tmp_ans_list:
                        for false_word in false_word_list:        
                            # 不正解文字が含まれているウマは除外 = 不正解文字が含まれていないウマは正解の可能性がある
                            in_checker = False
                            if false_word in tmp_ans_data:
                                in_checker = True   # Trueなら除外
                                break
                        if in_checker == False:     # 除外しない
                            tmp_copy_list.append(tmp_ans_data)
                    tmp_ans_list = copy.deepcopy(tmp_copy_list)
                    print(tmp_ans_list)




            


            if ans_counter == ans_counter_rule:
                true_flag = False   # 設定回数以上の場合、ゲーム終了
            
            if true_flag == True:   # 正解の場合
                ans_counter += 1
                #await ctx.author.send(new_ans)
                await ctx.author.send(f'正解は、『{ans}』でした！\n{ans_counter}回目の回答で正解です！')
                ans_embed.add_field(name=f"{ans_counter}回目の回答結果：{user_ans}", value=f"{now_ans}", inline=False)
                ans_embed.add_field(name=f"回答", value=f"正解は...『{ans}』でした！正解おめでとうございます！", inline=False)
                ans_msg = await ctx.author.send(embed=ans_embed)
                ans_msg_list.append(ans_msg)
            elif true_flag == False:   # 不正解の場合
                ans_embed.add_field(name=f"{ans_counter}回目の回答結果：{user_ans}", value=f"{now_ans}", inline=False)
                ans_embed.add_field(name=f"回答", value=f"正解は...『{ans}』でした", inline=False)
                ans_msg = await ctx.author.send(embed=ans_embed)
            else:
                pass

            # flagファイルの削除
            print('flagファイルを削除します')
            os.remove(flag_dir_path)
            print(f'{user_name}さんは正常に終了しました')
    
        else:   # プレイ中の場合
            print(flag_dir_path)
            print(os.path.exists(flag_dir_path))
            await ctx.channel.send(f"<@{user_id}>さんは、現在umadleをプレイ中です。現在のゲームを終えてから次のゲームを行ってください")


def setup(bot):
    bot.add_cog(Umadle_Cog(bot))