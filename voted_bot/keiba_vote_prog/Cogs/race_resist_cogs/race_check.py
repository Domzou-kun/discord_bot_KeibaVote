from discord.ext import commands
import discord
import json
import datetime
import os

class Regist_Race_Cmd_Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # 日付の取得
        dt_now = datetime.datetime.now()
        self.today_data = str(dt_now.year) + str(dt_now.month).zfill(2) + str(dt_now.day).zfill(2)

    @commands.command()
    async def registed_races(self, ctx):

        flag_path = r'user_record\mode_flag' + '\\' + 'test_mode_flag_.flag'
        if not os.path.exists(flag_path):
            # 日付の取得
            today_data = self.today_data
            #today_data = '20220220'
            # レース情報の読み込み
            race_dict, race_name_id_dict = race_json_data(race_hold_day=today_data)
        
        else:   # testモードの場合
            race_dict, race_name_id_dict = race_json_data(race_hold_day='TEST_RACE')
        


        # embedの生成
        races_embed = discord.Embed(title="登録レース一覧", color=0x00ff00, description="投票できるレース一覧です。\n投票したいレースの番号を「$vote_start レース番号」のように送信すると\nDMにて投票が開始されます")   #テスト版

        # レース名とIDの取得
        race_names = list(race_name_id_dict.keys())
        race_ids = list(race_name_id_dict.values())

        for race_name, race_id in zip(race_names, race_ids):
            value_str = 'レースID:' + race_id
            name_str = race_dict[race_id]['race_place'] + race_dict[race_id]['race_number'] + " : " + race_name
            races_embed.add_field(name=name_str ,value=value_str, inline=False)

        await ctx.channel.send(embed=races_embed)




def race_json_data(race_hold_day):
    race_data_path = r'..\keiba_race_getting_prog\getting_uma_info\saved_race_jsons' + '\\' + race_hold_day + r'\vote_race_datas.json'
    
    race_dict = READ_JSON(race_data_path)

    # 登録されてるレースIDの取得
    races_ids = list(race_dict.keys())
    print(races_ids)
    
    # レース名の取得
    race_name_list = []
    for race_id in races_ids:
        race_infos = race_dict[race_id]
        race_name_list.append(race_infos['race_name'])
    race_name_id_dict = dict(zip(race_name_list, races_ids))

    return race_dict, race_name_id_dict

# jsonの読み込み関数
def READ_JSON(json_f_path):

    # jsonを辞書型に変換
    with open(json_f_path, mode='rt', encoding='utf-8') as js_file:

        # 辞書オブジェクト(dictionary)を取得
        json_dict = json.load(js_file)
        
    # return
    return json_dict




def setup(bot):
    bot.add_cog(Regist_Race_Cmd_Cog(bot))