import asyncio
import sys
import argparse
from discord import channel, reaction, user
from discord.ext import commands
import discord
from discord.ext import tasks
import platform
import pathlib
import re
import unicodedata
import json
import requests
import time
import traceback
import datetime
import os
import cv2
from PIL import Image, ImageDraw, ImageFont


from main_sub_func import json_func as jf
from main_sub_func import race_info_getting as race_get


# cogの設定
DiscordBot_Cogs_list = [
    # helpに関するcogs
    ('Cogs.help_cogs.admin_help', '管理者ヘルプcog'),
    ('Cogs.help_cogs.bot_help', 'botヘルプcog'),
    ('Cogs.help_cogs.comment_help', 'コメント投票ヘルプcog'),
    ('Cogs.help_cogs.omake_help', 'おまけモードヘルプcog'),

    # レースの登録に関するcogs
    ('Cogs.race_resist_cogs.race_check', '登録レース表示cog'),

    # 投票に関するcogs
    ('Cogs.voted_cogs.reaction_cogs.reaction_on', '投票addリアクションcog'),
    ('Cogs.voted_cogs.reaction_cogs.reaction_off', '投票removeリアクションcog'),
    ('Cogs.voted_cogs.race_comment_main', 'レースコメント投票cog'),
    ('Cogs.voted_cogs.race_vote_main', 'レース投票メインcog'),

    # 予想表出力に関するcogs
    ('Cogs.paper_cogs.make_paper', '予想結果出力cog'),
    ('Cogs.paper_cogs.make_paper_hands', '手動予想結果出力cog'),

    # bot終了に関するcogs
    ('Cogs.shutdown_cogs.bot_shutdown', 'botシャットダウンcog'),

    # おまけゲーム（ウマ娘版wordle）に関するcogs
    ('Cogs.umadle_cogs.umadle', '競馬版wordle cog'),

    # おまけゲーム（ウマ娘版クイズ）に関するcogs
    ('Cogs.uma_quiz_cogs.uma_quiz', '競馬クイズcog')
]

# botの設定
class CounterBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or('$'),     # コマンドプレフィックス
            help_command=None,                                  # 標準ヘルプコマンド
            activity=discord.Game('ウマ息子'),                   # botのstatusメッセージ
            status=discord.Status.online
            )

        for cogs in DiscordBot_Cogs:
            try:
                self.load_extension(cogs[0])
            except Exception:
                traceback.print_exc()

    async def on_ready(self):

        # login情報
        login_msg = f'LOGIN {self.user} (ID: {self.user.id})'
        dt_now = datetime.datetime.now()
        run_time = str(dt_now.year) + "年" + str(dt_now.month).zfill(2) + "月" + str(dt_now.day).zfill(2) + "日"
        
        print('Login Information')
        print('--'*len(login_msg))
        print(login_msg)
        print('起動日 : {}'.format(run_time))
        print('--'*len(login_msg)+'\n')



# 全ての記録辞書の作成
def Dict_Setup(mode=None):

    # 空辞書の作成
    poll_res = {}   # 投票結果の保存dict（ネスト構造）の空リストの作成
    poll_res_path = r'user_record\main_poll_json'
    vote_user_record_path = r'vote_user_record'
    
    # 日付の確認
    dt_now = datetime.datetime.now()
    today_data = str(dt_now.year) + str(dt_now.month).zfill(2) + str(dt_now.day).zfill(2)
    today_poll_dir_path = poll_res_path + '\\' + today_data
    today_vote_user_record_path = vote_user_record_path + '\\' + today_data
    
    # レースディレクトリが存在しているかの確認
    race_dir_path = r'..\keiba_race_getting_prog\getting_uma_info\saved_race_jsons' + '\\' + str(today_data)
    if mode != 'test':
        if not os.path.exists(race_dir_path):
            print('================================ <=== 注意 ===> ================================')
            print('レース情報が取得されていません。レース情報を取得後、botを起動してください。')
            print('存在しないディレクトリ : {}'.format(race_dir_path))
            print('5秒後にプログラムを閉じます')
            time.sleep(5)
            sys.exit()

    # 登録されているレースIDのリスト取得
    race_dict, _ = race_get.race_json_data(mode=mode)
    race_ids_list = list(race_dict.keys())
    print('登録されているレースIDリスト')
    print(race_ids_list)

    print('==================== <== 今日のファイルの存在の確認 ==> ====================')
    if os.path.exists(today_poll_dir_path):
        print('本日 : {}のファイルが存在しました.本ディレクトリにファイルを生成します'.format(today_data))
        for race_id in race_ids_list:
            today_poll_path = today_poll_dir_path + '\\' + str(race_id) + '_' + r'poll_res.json'
            jf.SAVE_JSON(json_f_save_path=today_poll_path, saved_dict=poll_res)
    else:
        print('本日 : {}のファイルが存在しませんでした.日付ファイルを作成します'.format(today_data))
        os.mkdir(today_poll_dir_path)
        print('ファイルの生成を行います')
        for race_id in race_ids_list:
            today_poll_path = today_poll_dir_path + '\\' + str(race_id) + '_' + r'poll_res.json'
            jf.SAVE_JSON(json_f_save_path=today_poll_path, saved_dict=poll_res)



    print('==================== <== 今日のuser_recordファイルの存在の確認 ==> ====================')
    if os.path.exists(today_vote_user_record_path):
        print('本日 : {}のファイルが既に存在しました.'.format(today_data))
        #for race_id in race_ids_list:
        #    today_vote_user_path = today_vote_user_record_path + '\\' + str(race_id) + '_' + r'vote_user_record.json'
        #    jf.SAVE_JSON(json_f_save_path=today_vote_user_path, saved_dict=poll_res)
    else:
        print('本日 : {}のファイルが存在しませんでした.日付ファイルを作成します'.format(today_data))
        os.mkdir(today_vote_user_record_path)
        print('ファイルの生成を行います')
        for race_id in race_ids_list:
            today_vote_user_path = today_vote_user_record_path + '\\' + str(race_id) + '_' + r'vote_user_record.json'
            jf.SAVE_JSON(json_f_save_path=today_vote_user_path, saved_dict=poll_res)

    print('==================== <== poll_res dictの作成 ==> ====================')
    print('作成先 : {}'.format(today_poll_dir_path))

    print('')
    print('フォルダの生成が完了しました。')




if __name__ == '__main__':

    # クライアントの作成 ==================================================================
    if platform.system() == 'Windows':  # window環境の場合postを行う
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    discord_intents = discord.Intents.all()


    # TOKENの取得 ========================================================================
    discord_tokens_path = r'ac_key.json'
    discord_token_key = jf.READ_JSON(json_f_path=discord_tokens_path)
    bot_TOKEN = discord_token_key['token']


    # permission server id dictの取得 =========================================================
    #discord_permission_server_id = jf.READ_JSON(json_f_path=discord_tokens_path)
    #bot_permission_ids_dict = discord_permission_server_id['permission_server']


    # pythonのバージョンの確認=============================================================
    python_ver_msg = str(sys.version)
    python_ver_title = '\nPython Version Information'
    max_python_len = max([len(python_ver_msg), len(python_ver_title)])
    print(python_ver_title)
    print('-'*max_python_len)
    print(python_ver_msg)
    print('-'*max_python_len+'\n')


    # modeの確認 =========================================================================
    mode_cog_list = [
        0,  # 管理者 help
        1,  # bot help
        2,  # コメント help
        11  # shutdown
    ]
    mode_check_sum = 0
    # argparseの作成
    bot_msg = "このプログラムは競馬の予想投票及び集計を行い、自動で競馬新聞形式として出力するDiscord botです。\n\
                This program is a discord bot which polls and tabulates horse horse racing predictions and automatically \
                outputs them in a horse racing newspaper format."
    mode_parser = argparse.ArgumentParser(description=bot_msg)
    mode_parser.add_argument('--vote_mode', help='投票モード', choices=['True', 'False'])
    mode_parser.add_argument('--game_mode', help='ミニゲームモード', choices=['True', 'False'])
    mode_parser.add_argument('--test_mode', help='テストモード', choices=['True', 'False'])
    mode_parser.add_argument('--debug_mode', help='デバッグモード', choices=['True', 'False'])
    mode_parser.add_argument('--admin_mode', help='管理者モード', choices=['ADMIN_TRUE'])
    
    mode_args = mode_parser.parse_args()
    
    vote_mode = mode_args.vote_mode    # 投票モード
    if vote_mode == 'True':
        mode_cog_list.extend([
            4,  # レース登録
            5,  # 投票リアクション(add)
            6,  # 投票リアクション(remove)
            7,  # レースコメント 
            8,  # レース投票
            9,  # 予想結果出力
            10  # 手動予想出力
        ])
        mode_check_sum += 1
        flag_path = r'user_record\mode_flag' + '\\' + 'vote_mode_flag_.flag'
        pathlib.Path(flag_path).touch()
    game_mode = mode_args.game_mode    # ゲームモード
    if game_mode == 'True':
        mode_cog_list.extend([
            3,  # おまけモードhelp
            12, # 競馬版wordle(ウマ娘含む)
            13  # ウマ娘x実在馬クイズ
        ])
        mode_check_sum += 1
        flag_path = r'user_record\mode_flag' + '\\' + 'game_mode_flag_.flag'
        pathlib.Path(flag_path).touch()
    test_mode = mode_args.test_mode    # テストモード
    if test_mode == 'True':
        mode_cog_list.extend([
            4,  # レース登録
            5,  # 投票リアクション(add)
            6,  # 投票リアクション(remove)
            7,  # レースコメント 
            8,  # レース投票
            9,  # 予想結果出力
            10  # 手動予想出力
        ])
        mode_check_sum += 1
        flag_path = r'user_record\mode_flag' + '\\' + 'test_mode_flag_.flag'
        pathlib.Path(flag_path).touch()
    debug_mode = mode_args.debug_mode  # デバッグモード
    if debug_mode == 'True':
        mode_check_sum += 1
        flag_path = r'user_record\mode_flag' + '\\' + 'debug_mode_flag_.flag'
        pathlib.Path(flag_path).touch()
    
    admin_mode = mode_args.admin_mode  # 管理者モード
    if admin_mode == 'ADMIN_TRUE':
        mode_check_sum += 1
    
    # モードの出力
    mode_name_list = ['vote mode', 'game mode', 'test mode', 'debug mode']
    mode_status_list = [vote_mode, game_mode, test_mode, debug_mode]

    mode_name_list_len = [ len(mode_1) for mode_1 in mode_name_list ]
    mode_status_list_len = [ len(str(mode_2)) for mode_2 in mode_status_list ]
    
    mode_name_title = 'Mode Name'
    mode_name_list_len.insert(0, len(mode_name_title))
    mode_status_title = 'Mode Status'
    mode_status_list_len.insert(0, len(mode_status_title))

    max_mode_name_len = max(mode_name_list_len)
    max_mode_status_len = max(mode_status_list_len)

    p_mode_name_msg = mode_name_title + ' '*(max_mode_name_len-len(mode_name_title))
    p_mode_status_msg = mode_status_title + ' '*(max_mode_status_len-len(mode_status_title))
    p_mode_title_msg = p_mode_name_msg + '  ' + p_mode_status_msg
    
    print(p_mode_title_msg)
    print('-'*len(p_mode_name_msg) + '  ' + '-'*len(p_mode_status_msg))
    for mode_name, mode_status, mode_index in zip(mode_name_list, mode_status_list, range(0, len(mode_name_list))):
        p_mode_name_msg = mode_name + ' '*(max_mode_name_len-len(mode_name))
        p_mode_status_msg = str(mode_status) + ' '*(max_mode_status_len-len(str(mode_status)))
        print(p_mode_name_msg + '  ' + p_mode_status_msg)
    print('-'*len(p_mode_title_msg)+'\n')

    if mode_check_sum % 5 == 0: # mode選択が無かった場合
        print('Mode was not selected. Start in standard mode.')
        uninput_mode = 'game'
        mode_cog_list.extend([
            11, # 競馬版wordle(ウマ娘含む)
            12  # ウマ娘x実在馬クイズ
        ])


    # bot cog処理 =============================================================================================
    DiscordBot_Cogs = [ DiscordBot_Cogs_list[x] for x in mode_cog_list] # 実行するcogの設定
    
    cog_function_name_len = [ len(p_cog[0]) for p_cog in DiscordBot_Cogs ]   # cogの名前のlen
    cog_function_help_len = [ len(p_cog[1]) for p_cog in DiscordBot_Cogs ]   # cogのヘルプのlen]

    p_cog_title_1 = 'Cog Function Name'                     # cogの名前のタイトル
    cog_function_name_len.insert(0, len(p_cog_title_1))     # cogの名前のタイトルlen
    p_cog_title_2 = 'Cog Function Help'                     # cogのヘルプのタイトル
    cog_function_help_len.insert(0, len(p_cog_title_2))     # cogのヘルプのタイトルlen

    max_cog_function_name_len = max(cog_function_name_len)
    max_cog_function_help_len = max(cog_function_help_len)
    
    p_cog_title_1 = p_cog_title_1 + ' '*(max_cog_function_name_len-len(p_cog_title_1))
    p_cog_title_2 = p_cog_title_2 + ' '*2*(max_cog_function_help_len-len(p_cog_title_2))
    title_msg = p_cog_title_1 + '  ' + p_cog_title_2
    p_cog_title_under = '-'*len(p_cog_title_1) + '  ' + '-'*2*len(p_cog_title_2)
    
    print(title_msg)
    print(p_cog_title_under)
    for p_cog in DiscordBot_Cogs:
        msg_p_cog_1 = p_cog[0] + ' '*(max_cog_function_name_len-len(p_cog[0]))
        msg_p_cog_2 = p_cog[1] + ' '*2*(max_cog_function_help_len-len(p_cog[1]))
        print(msg_p_cog_1 + '  ' + msg_p_cog_2)
    print('-'*len(p_cog_title_under)+'\n')

    # botの起動 ================================================================================================
    if test_mode == 'True':
        Dict_Setup(mode='test')
    
    elif game_mode == 'True':
        if vote_mode == 'True':
            Dict_Setup()
        else:
            pass
    
    else:
        Dict_Setup()
        
    time.sleep(3)

    # botの設定    
    bot = CounterBot()
    
    # botの起動
    bot.run(bot_TOKEN)



