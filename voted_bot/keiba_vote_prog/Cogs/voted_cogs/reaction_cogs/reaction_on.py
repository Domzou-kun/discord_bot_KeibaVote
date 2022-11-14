from importlib import import_module
from discord.ext import commands
import discord
import datetime
import unicodedata
from main_sub_func import json_func as jf


class Reaction_On_Cmd_Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot_id = '925385144150409226'

        # 日付の取得
        dt_now = datetime.datetime.now()
        self.today_data = str(dt_now.year) + str(dt_now.month).zfill(2) + str(dt_now.day).zfill(2)


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        # idの取得
        bot_id = self.bot_id
        # 日付の取得
        today_data = self.today_data
        

        # ボットの判別。ボットでない場合のみdict処理へ
        if str(payload.user_id) != bot_id:
            # DM channel以外でのreactionの検出
            if type(payload.channel_id) != discord.DMChannel:

                """
                
                特定のチャンネルの特定のメッセージを取得する方法
                channel = bot.get_channel(payload.channel_id)
                message_id = payload.message_id
                msg_content = await channel.fetch_message(message_id)
                main_uma = msg_content.embeds[0].title

                """

                # リアクションが押されたチャンネルの取得
                channel = self.bot.get_channel(payload.channel_id)
                # メッセージidの取得とメッセージ文の取得
                message_id = payload.message_id
                msg_content = await channel.fetch_message(message_id)   #####
                main_uma = msg_content.embeds[0].title
                # 押されたリアクションの取得と変換
                emoji = payload.emoji      #####
                emoji_name = unicodedata.name(emoji.name)  # pythonで扱える絵文字に変換
                py_emoji = unicodedata.lookup(emoji_name)
                emoji_hex = hex(ord(py_emoji))  # 16進数変換
                # リアクションを推した人の確認
                user_id = payload.user_id
                user_info = self.bot.get_user(payload.user_id)   #####
                user_name = await self.bot.fetch_user(user_id)

                update_dict(emoji_code=emoji_hex, user=user_name, voted_uma=main_uma, user_id=user_id, today_data=today_data)
            else:
                print('dm以外でのリアクションを検出')
                print('追加版')
                pass
        # botの場合
        else:
            pass


# 辞書の更新関数
def update_dict(emoji_code, user, voted_uma, user_id, today_data):

    # 投票用jsonファイル
    user_temp_json_path = r'user_record\user_records' + '\\' + str(user_id) + '\\' + str(today_data) + '\\' + r'temp' + r'\res_temp.json'
    
    # user名から"#"の削除
    user_name_list = str(user).split('#')
    user_name = user_name_list[0]

    # 馬情報から":"の削除
    uma_name_str = str(voted_uma)
    uma_name_list = uma_name_str.split(':')


    # 投票結果格納のdictの取得
    #uma_res_dict = poll_res[user_name]['res']
    uma_res_dict = jf.READ_JSON(json_f_path=user_temp_json_path)
    
    # 更新処理
    uma_res_dict.setdefault(uma_name_list[1], str(emoji_code))
    #uma_res_dict[str(emoji_code)] = uma_name_list[1]

    print(f'========== <== {user_name}:投票追加 ==> ==========')
    print(uma_res_dict)

    # 更新結果のセーブ
    jf.SAVE_JSON(json_f_save_path=user_temp_json_path, saved_dict=uma_res_dict)


def setup(bot):
    bot.add_cog(Reaction_On_Cmd_Cog(bot))