from discord.ext import commands
from discord.ext import tasks
import os
import pathlib
import discord
import time
import random
import asyncio


from main_sub_func import json_func as jf


class Uma_Quiz_Cmd_Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def umaquiz(self, ctx: commands.context):


        loop_counter = 0   # タイマーの起動回数

        # コマンドを打ったユーザーの取得
        user_name = ctx.message.author.name
        user_id  = ctx.message.author.id    # user_idの取得
        flag_dir_path = r'user_record\vote_flag' + '\\' + str(user_id) + '_' + 'umaquiz_flag.flag'



        if not os.path.exists(flag_dir_path):
            # 投票中flagの設定
            pathlib.Path(flag_dir_path).touch()

            await ctx.channel.send(f"<@{user_id}>さん、umaquizのプレイを開始しました。DMにて遊んでください")
            print(f'{user_name}さんがumaquizを開始しました')


            # ルール説明
            quiz_embed = discord.Embed(title="『uma quizへようこそ！』", description="ルール説明！", color=0xeee657)
            quiz_embed.add_field(name="ルール : 1", value="解答は『1回』だけしか入力できないよ！", inline=False)
            quiz_embed.add_field(name="ルール : 2", value="20秒ごとに答えとなる馬のヒントが表示されるよ！", inline=False)
            quiz_embed.add_field(name="ルール : 3", value="ヒントは全部で5回出題されるよ！", inline=False)

            await ctx.author.send(embed=quiz_embed)

            # スタートセットアップ
            start_embed = discord.Embed(title="クイズをスタートする", description=" ", color=0xeee657)
            start_embed.add_field(name="クイズをスタートする", value="『start』と入力してね（『』は外してください）", inline=False)
            start_embed.add_field(name="クイズをやめる", value="『exit』と入力してね（『』は外してください）", inline=False)

            await ctx.author.send(embed=start_embed)

            # startの有無
            def start_check(message: discord.Message):
                #return m.content == '$投票終了' and type(m.channel) == discord.DMChannel
                print('スタートチェック開始')
                return message.author.id == user_id and len(message.content.lower())!=0 and message.content.lower() in ['start', 'exit']
            start_ans = await self.bot.wait_for('message', check=start_check, timeout=3600)
            start_ans = start_ans.content.lower()

            
            
            
            if start_ans == 'start':    # ゲーム開始

                await ctx.author.send(f'5秒後からヒントが表示されます\n制限時間は120秒です。答えは1度だけしか入力できないので注意してください')

                quiz_dir_path = r"Cogs\uma_quiz_cogs\questions"
                # 問題ファイルの読み込み
                files = os.listdir(quiz_dir_path)
                files_file_list = [f for f in files if os.path.isfile(os.path.join(quiz_dir_path, f))]  # ファイルの読み込み
                question_json_name = random.choice(files_file_list)
                question_json_path = quiz_dir_path + '\\' + question_json_name
                # jsonファイルの読み込み
                question_dict = jf.READ_JSON(json_f_path=question_json_path)
                # 各種パラメータの設定
                ans_list = list(question_dict.keys())
                ans = ans_list[0]   # 答え
                horse_id = question_dict[ans_list[1]]  # 馬のid番号
                horse_url = r'https://db.netkeiba.com/horse/' + str(horse_id) + '/'
                data_keys_list = list(question_dict[ans].keys())    # 問題のキーリスト


                # ランダムにヒントを選ぶ
                choice_questions_num = 5    # 選ぶヒントの数
                question_list = random.sample(data_keys_list, choice_questions_num) # 問題リスト

                time.sleep(5)
                # ヒントの出題の開始
                start = time.time() # 処理開始時刻
                #self.end_vote.start(ctx, question_list, question_dict, ans) # 5回だけ問題を表示


                # 問題出力部分
                ans_checker = True
                quiz_index_count = 0


                print('<<================================= ゲーム開始 ===========================================>>')
                print(f'管理用 : 回答者『{user_name}』、答え : 『{ans}』')
                print('===========================================================================================')

                while ans_checker:

                    question_key = question_list[loop_counter]
                    main_quiz_dict = question_dict[ans][question_key]
                    quiz_jp = main_quiz_dict["jp_name"]
                    quiz_info = main_quiz_dict["data"]

                    hint_embed = discord.Embed(title=f"ヒント : {loop_counter+1}", description=" ", color=0xff0000)
                    hint_embed.add_field(name=f"【{quiz_jp}】", value=f"{quiz_jp}は{quiz_info}です。", inline=False)
                    await ctx.author.send(embed=hint_embed)

                    print(f'<< =============== {user_name}さんに表示しているヒント:{loop_counter+1} =============== >>')
                    print(f'{main_quiz_dict["jp_name"]}は{main_quiz_dict["data"]}です。')
                    print('================================================================')


                    def check(message: discord.Message):
                        #return m.content == '$投票終了' and type(m.channel) == discord.DMChannel
                        print('回答待ち')
                        return message.author.id == user_id and len(message.content)!=0
                    
                    try:
                        user_ans = await self.bot.wait_for('message', check=check, timeout=20)   # 5秒後ごとに解答を締め切り問題数の確認を行う
                        user_ans = user_ans.content
                        print('回答入力')
                        break
                    except asyncio.TimeoutError:
                        # 120秒で回答締切
                        times = 20*(loop_counter+1)
                        print(f'{times}秒経過')
                        if loop_counter < 4:
                            loop_counter += 1   
                        else:
                            print('時間切れ')
                            ans_checker = False
                            break
                
                # whileを抜けた時点でloopの停止
                result_time = time.time() - start

                # 答えのチェック
                if ans_checker == True: # 何か入力された場合
                    print(f'<< ===== {user_name}の回答 : 【{user_ans}】 ===== >>')
                    if user_ans == ans: # 正解の場合
                        await ctx.author.send(f'正解は、『{ans}』でした！おめでとうございます！')
                        
                        ans_embed = discord.Embed(title="リザルト", description="クイズの結果", color=0xeee657)
                        ans_embed.add_field(name=f"正解の馬", value=f"{ans}", inline=False)
                        ans_embed.add_field(name=f"解答までの時間", value=f"{int(result_time)}秒", inline=False)
                        ans_msg = await ctx.author.send(embed=ans_embed)
                    
                    else:   # 不正解の場合
                        await ctx.author.send(f'不正解です...')
                        
                        ans_embed = discord.Embed(title="リザルト", description="クイズの結果", color=0xeee657)
                        ans_embed.add_field(name=f"正解の馬", value=f"{ans}", inline=False)
                        ans_msg = await ctx.author.send(embed=ans_embed)
                else:   # 時間切れの場合
                    await ctx.author.send(f'時間切れです...')
                        
                    ans_embed = discord.Embed(title="リザルト", description="クイズの結果", color=0xeee657)
                    ans_embed.add_field(name=f"正解の馬", value=f"{ans}", inline=False)
                    ans_msg = await ctx.author.send(embed=ans_embed)
                    
                # 馬の情報を送信
                await ctx.author.send(f'<@{user_id}>\n今回正解の【{ans}】の情報はこちら\n{horse_url}')

            else:   # ゲームを開始しない場合
                await ctx.author.send('また次回遊んでね！')
            
            

            # flagファイルの削除
            print('flagファイルを削除します')
            os.remove(flag_dir_path)
            print(f'{user_name}さんは正常に終了しました')
    

        else:   # プレイ中の場合
            print(flag_dir_path)
            print(os.path.exists(flag_dir_path))
            await ctx.channel.send(f"<@{user_id}>さんは、現在umaquizをプレイ中です。現在のゲームを終えてから次のゲームを行ってください")

    """
    @tasks.loop(seconds=21, count=5)     # ラグを考慮して21秒の設定 # 5回のループで終わり
    async def end_vote(self, ctx, question_list, question_dict, ans):

        question_key = question_list[self.loop_counter]
        main_quiz_dict = question_dict[ans][question_key]
        quiz_jp = main_quiz_dict["jp_name"]
        quiz_info = main_quiz_dict["data"]

        hint_embed = discord.Embed(title=f"ヒント : {self.loop_counter+1}", description=" ", color=0xff0000)
        hint_embed.add_field(name=f"【{quiz_jp}】", value=f"{quiz_jp}は{quiz_info}です。", inline=False)
        await ctx.author.send(embed=hint_embed)

        print('<< ==================== 表示しているヒント ==================== >>')
        print(f'{main_quiz_dict["jp_name"]}は{main_quiz_dict["data"]}です。')
        print('================================================================')

        self.loop_counter += 1  # loopカウンター
    """

    """
    async def quiz_select(self, ctx, question_list, question_dict, ans):

        question_key = question_list[self.loop_counter]
        main_quiz_dict = question_dict[ans][question_key]
        quiz_jp = main_quiz_dict["jp_name"]
        quiz_info = main_quiz_dict["data"]

        hint_embed = discord.Embed(title=f"ヒント : {self.loop_counter+1}", description=" ", color=0xff0000)
        hint_embed.add_field(name=f"【{quiz_jp}】", value=f"{quiz_jp}は{quiz_info}です。", inline=False)
        await ctx.author.send(embed=hint_embed)

        print('<< ==================== 表示しているヒント ==================== >>')
        print(f'{main_quiz_dict["jp_name"]}は{main_quiz_dict["data"]}です。')
        print('================================================================')

        self.loop_counter += 1  # loopカウンター
    """

def setup(bot):
    bot.add_cog(Uma_Quiz_Cmd_Cog(bot))