from discord.ext import commands
import discord
import unicodedata
import datetime
from main_sub_func import json_func as jf


class Reaction_Off_Cmd_Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot_id = '925385144150409226'
        
        # 日付の取得
        dt_now = datetime.datetime.now()
        self.today_data = str(dt_now.year) + str(dt_now.month).zfill(2) + str(dt_now.day).zfill(2)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):

        # idの取得
        bot_id = self.bot_id
        # 日付の取得
        today_data = self.today_data

        # ボットの判別。ボットでない場合のみdict処理へ
        if str(payload.user_id) != bot_id:
            # DM channel以外でのreactionの検出
            if type(payload.channel_id) != discord.DMChannel:

                # リアクションが外されたチャンネルの取得
                channel = self.bot.get_channel(payload.channel_id)
                # メッセージidの取得とメッセージ文の取得
                message_id = payload.message_id
                msg_content = await channel.fetch_message(message_id)
                main_uma = msg_content.embeds[0].title
                # 外されたリアクションの取得と変換
                emoji = payload.emoji
                # リアクションを推した人の確認
                user_id = payload.user_id
                user_name = await self.bot.fetch_user(user_id)

                del_date_dict(emoji_code=emoji, user=user_name, unvoted_uma=main_uma, user_id=user_id, today_data=today_data)
            else:
                print('DM以外でのリアクションを検出')
                print('削除版')
                pass
        # botの場合
        else:
            pass

# 辞書からの削除関数
def del_date_dict(emoji_code, user, unvoted_uma, user_id, today_data):

    # 投票用jsonファイル
    user_temp_json_path = r'user_record\user_records' + '\\' + str(user_id) + '\\' + str(today_data) + '\\' + r'temp' + r'\res_temp.json'

    # pythonで扱える絵文字に変換
    emoji_name = unicodedata.name(emoji_code.name)
    py_emoji = unicodedata.lookup(emoji_name)
    emoji_hex = hex(ord(py_emoji))  # 16進数変換

    # user名から"#"の削除
    user_name_list = str(user).split('#')
    user_name = user_name_list[0]

    # 馬情報から":"の削除
    un_uma_name_str = str(unvoted_uma)
    un_uma_name_list = un_uma_name_str.split(':')

    # 投票結果格納のdictの取得
    #uma_res_dict = poll_res[user_name]['res']
    uma_res_dict = jf.READ_JSON(json_f_path=user_temp_json_path)
    
    # 更新処理
    try:
        now_emoji = uma_res_dict[un_uma_name_list[1]]
    except:
        print('=== 現在投票プールは空です。 ===')
        pass
    if now_emoji == str(emoji_hex):    # もし格納されてる絵文字が同じ場合は削除
        uma_res_dict.pop(un_uma_name_list[1])
    else:                               # 違う絵文字ならそのまま放置
        pass
    #uma_res_dict[str(emoji_hex)] = 0

    print(f'========== <== {user_name}:投票削除 ==> ==========')
    print(uma_res_dict)

    # 更新結果のセーブ
    jf.SAVE_JSON(json_f_save_path=user_temp_json_path, saved_dict=uma_res_dict)

def setup(bot):
    bot.add_cog(Reaction_Off_Cmd_Cog(bot))