from statistics import mode
from main_sub_func import json_func as jf
import datetime
import os

# レースjsonの読み込み
def race_jsons(race_id=None):

    flag_path = r'user_record\mode_flag' + '\\' + 'test_mode_flag_.flag'
    if not os.path.exists(flag_path):
        dt_now = datetime.datetime.now()
        today_data = str(dt_now.year) + str(dt_now.month).zfill(2) + str(dt_now.day).zfill(2)
        race_data_path = r'..\keiba_race_getting_prog\getting_uma_info\saved_race_jsons' + '\\' + str(today_data) + r'\vote_race_datas.json'
    else:   # テストモード
        race_data_path = r'..\keiba_race_getting_prog\getting_uma_info\saved_race_jsons\TEST_RACE\vote_race_datas.json'


    race_dict = jf.READ_JSON(race_data_path)

    # 登録されてるレースIDの取得
    races_ids = list(race_dict.keys())
    
    # レース情報リスト
    
    # race_idのキャスト
    race_id = str(race_id)

    # 特定のレースの情報の取得
    race_infos = race_dict[race_id]
    race_info_list = [ race_infos['race_name'], race_infos['race_number'], race_infos['race_place'], race_infos['race_distance'], race_infos['race_times'], race_infos['race_hold_info'] ]

    # 特定のレースの出走馬の取得
    horse_infos = race_dict[race_id]['register_horse']
    horse_ids_list = list(horse_infos.keys())

    horse_info_list = []    # 馬の情報
    horse_etc_info_list = []    # 騎手などの情報
    horse_parent_list = []
    for horse_id in horse_ids_list:
        horse_info = horse_infos[horse_id]  # 個別に馬を取得

        horse_name = horse_info['horse_name']
        horse_waku = horse_info['horse_waku']
        horse_number = horse_info['horse_number']

        horse_str_info = str(horse_waku) + ',' + str(horse_number) + ',' + str(horse_name)
        horse_info_list.append(horse_str_info)

        horse_ages = horse_info['horse_ages']
        kinryo = horse_info['kinryo']
        jockey = horse_info['jockey']
        kyusya = horse_info['kyusya']

        horse_etc_tuple = (horse_ages, kinryo, jockey, kyusya)
        horse_etc_info_list.append(horse_etc_tuple)

        boba = horse_info['horse_parent']['boba']
        hinba = horse_info['horse_parent']['hinba']
        hahachichi = horse_info['horse_parent']['hahachichi']
        horse_parent_list.append([boba, hinba, hahachichi])

    # レース名の取得
    race_name_list = []
    for race_id in races_ids:
        race_infos = race_dict[race_id]
        race_name_list.append(race_infos['race_name'])
    race_name_id_dict = dict(zip(race_name_list, races_ids))


    return race_dict, race_info_list, horse_info_list, horse_etc_info_list, horse_parent_list, race_name_id_dict


def race_json_data(mode=None):

    if mode != 'test':
        dt_now = datetime.datetime.now()
        today_data = str(dt_now.year) + str(dt_now.month).zfill(2) + str(dt_now.day).zfill(2)
        race_data_path = r'..\keiba_race_getting_prog\getting_uma_info\saved_race_jsons' + '\\' + str(today_data) + r'\vote_race_datas.json'
    else:
        race_data_path = r'..\keiba_race_getting_prog\getting_uma_info\saved_race_jsons\TEST_RACE\vote_race_datas.json'
    race_dict = jf.READ_JSON(race_data_path)

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