#!python3.9

import os
import re
import sys
import time
import requests
import json
from bs4 import BeautifulSoup


"""

races_holds = { # 土曜日のレース情報まとめ

    race_id = {
        race_place : レース会場
        race_name : レース名
        race_number : レース番号
        race_distance : レース距離
        race_times : 発走時間

        register_horse : {
            horse_id : {
                horse_name : 馬の名前
                horse_waku : 枠番号
                horse_number : 馬番号
                horse_parent = {
                    hinba : 母馬
                    boba : 父馬
                }
                horse_ages : 性齢
                kinryo : 斤量
                jockey : 騎手
                kyusya : 厩舎
            }
        
            horse_id : {
                horse_name : 馬の名前
                horse_waku : 枠番号
                horse_number : 馬番号
                horse_parent = {
                    hinba : 母馬
                    boba : 父馬
                }
                horse_ages : 性齢
                kinryo : 斤量
                jockey : 騎手
                kyusya : 厩舎
            }

            horse_id : {
                horse_name : 馬の名前
                horse_waku : 枠番号
                horse_number : 馬番号
                horse_parent = {
                    hinba : 母馬
                    boba : 父馬
                }
                horse_ages : 性齢
                kinryo : 斤量
                jockey : 騎手
                kyusya : 厩舎
            }
        }

        /// 以下続く ///
    
    }

    race_id = {
        race_place : レース会場
        race_name : レース名
        race_number : レース番号
        race_distance : レース距離
        race_times : 発走時間

        register_horse = {
            horse_id = {
                horse_name : 馬の名前
                horse_waku : 枠番号
                horse_number : 馬番号
                horse_parent = {
                    hinba : 母馬
                    boba : 父馬
                }
                horse_ages : 性齢
                kinryo : 斤量
                jockey : 騎手
                kyusya : 厩舎
            }
        }

    /// 以下続く ///
}




"""



def make_json(race_id, race_info, horse_ids, horse_infos, bld_lists):
    race_holds = dict([(race_id, make_races_json(race_infos_list=race_info, horse_ids=horse_ids, horse_infos=horse_infos, bld_lists=bld_lists))])

    return race_holds

def make_races_json(race_infos_list, horse_ids, horse_infos, bld_lists):
    races_keys = [ 'race_place', 'race_name', 'race_number', 'race_distance', 'race_times', 'register_horse']
    races_values = [ race_infos_list[0], race_infos_list[1], race_infos_list[2], race_infos_list[3], race_infos_list[4], make_horse_info_json_A(horse_id_list=horse_ids, horse_infos_list=horse_infos, bld_lists=bld_lists) ]

    return dict(zip(races_keys, races_values))

def make_horse_info_json_A(horse_id_list, horse_infos_list, bld_lists):
    horse_infos_dict_values = []
    for horse_info, bld_tuple in zip(horse_infos_list, bld_lists):
        horse_infos_dict_values.append(make_horse_info_json_B(horse_infos_list=horse_info, bld_tuple=bld_tuple))
    
    return dict(zip(horse_id_list, horse_infos_dict_values))

def make_horse_info_json_B(horse_infos_list, bld_tuple):
    horse_keys = [ 'horse_name', 'horse_waku', 'horse_number', 'horse_parent', 'horse_ages', 'kinryo', 'jockey', 'kyusya' ]
    horse_values = [horse_infos_list[0], horse_infos_list[1], horse_infos_list[2], make_horse_info_json_C(horse_parent_list=bld_tuple), horse_infos_list[3], horse_infos_list[4], horse_infos_list[5], horse_infos_list[6]]

    return dict(zip(horse_keys, horse_values))

def make_horse_info_json_C(horse_parent_list):
    parent_keys = [ 'boba', 'hinba', 'hahachichi' ]
    parent_values = [ horse_parent_list[0], horse_parent_list[1], horse_parent_list[2] ]
    return dict(zip(parent_keys, parent_values))




# レースのスクレイピング
def race_scrape(race_ids, place_checker, saved_path):


    # 漢字変換リスト
    NumberToKanji = {
        '0' : '〇',
        '1' : '一',
        '2' : '二',
        '3' : '三',
        '4' : '四',
        '5' : '五',
        '6' : '六',
        '7' : '七',
        '8' : '八',
        '9' : '九'
    }
    # レース会場名
    race_places_name = ['札幌', '函館', '福島', '中山', '東京', '新潟', '中京', '京都', '阪神', '小倉', '大井', '笠松', '姫路', '高知', '佐賀', '浦和', '名古屋', '船橋', '帯広(ば)', '水沢', '金沢', '園田', '盛岡', '川崎', '門別']


    #race_idをkeyにしてDataFrame型を格納
    race_results = {}

    for race_id in race_ids:
        
        time.sleep(5)
        if place_checker == 0:  # 中央
            url = "https://race.netkeiba.com/race/shutuba.html?race_id=" + race_id
        elif place_checker == 1:    # 地方
            url = "https://nar.netkeiba.com/race/shutuba.html?race_id=" + race_id
        else:
            pass
        
        #メインとなるテーブルデータを取得
        #df = pd.read_html(url)[0]

        print('=================================================================================================')
        print('取得するURL')
        print(url)
        print('=================================================================================================')

        html = requests.get(url)
        html.encoding = "EUC-JP"
        soup = BeautifulSoup(html.text, "html.parser")

        time.sleep(5)
        print('=================================================================================================')
        print('取得しました')
        print('=================================================================================================')
        time.sleep(5)

        # 保存用リスト
        race_info_list = []

        # レース会場
        race_data = soup.find_all('div', class_='RaceData02')
        
        temp_data2 = []
        for a in race_data:
            temp_data2.append(a.text.replace("\n","").replace(" ",""))
        
        print(temp_data2)


        for race_place_name in race_places_name:
            if race_place_name in temp_data2[0]:
                race_info_list.append(race_place_name)


        #################### 詳しいレース情報 ########################
        race_hold_info_list = []
        race_hold_info_span = race_data[0]
        race_hold_infos = race_hold_info_span.find_all('span')
        
        for race_hold_info in race_hold_infos:
            print(race_hold_info.text)
            race_hold_info_list.append(race_hold_info.text)
        
        print(race_hold_info_list)

        #############################################################


        # レース名取得
        race_name = soup.find_all('div', class_='RaceName')
        race_info_list.append(race_name[0].text.replace("\n","").replace(" ",""))
        print(race_name[0].text.replace("\n","").replace(" ",""))

        # レース番号の取得
        if place_checker == 0:  # 中央
            race_num = soup.find_all('span', class_='RaceNum')
            race_info_list.append(race_num[0].text.replace("\n","").replace(" ","").replace("R",""))
        elif place_checker == 1:   # 地方
            race_num = soup.find_all('div', class_='Race_Num')
            race_info_list.append(race_num[0].text.replace("\n","").replace(" ","").replace("R",""))
        else:
            pass

        # 発走時間、レース距離取得
        race_infos = soup.find_all('div', class_='RaceData01')
        temp_infos_a = race_infos[0].text.replace("\n","").replace(" ","")
        infos_lists = temp_infos_a.split('/')   # [発走時刻, 距離]

        # 距離の漢字変換]
        keys_list = list(NumberToKanji.keys())
        new_dist_str = ''
        for race_str in infos_lists[1]:
            if (race_str in keys_list):
                new_dist_str = new_dist_str+NumberToKanji[race_str]
            elif (race_str == '芝') or (race_str == 'ダ'):
                new_dist_str = new_dist_str+race_str
            else:
                pass

        # リストに追加
        race_info_list.append(new_dist_str)
        race_info_list.append(infos_lists[0])

        print(race_info_list)



        if place_checker == 0:  # 中央
            # 出走馬名取得テスト
            b = soup.find_all('td', class_='HorseInfo')
            temp_a = []
            for bb in b:
                temp_a.append(bb.text.replace("\n","").replace(" ",""))
            print(temp_a)
        elif place_checker == 1:    # 地方
            # 出走馬名取得テスト
            b = soup.find_all('span', class_='HorseName')
            temp_a = []
            for bb in b:
                temp_a.append(bb.text.replace("\n","").replace(" ",""))
            temp_a.remove('馬名')
            print(temp_a)
        else:
            pass
        
        # 馬id取得テスト
        temp_ids = []
        if place_checker == 0:  # 中央
            c = soup.find_all('img')
            for cc in c:
                try:
                    ccc = cc['id'].split('_')
                    if ccc[0] == 'myhorse':
                        temp_ids.append(ccc[1])
                except:
                    pass
        elif place_checker == 1:    # 地方
            links = soup.find_all('a')
            for link in links:
                tags = link.get('id')
                if tags is not None:
                    id_tag = tags.split('_')
                    if id_tag[0] != 'Bamei':
                        temp_ids.append(str(id_tag[1]))
        else:
            pass

        print(temp_ids)



        if place_checker == 0:  # 中央
            # 性齢取得テスト
            temp_barei = []
            d = soup.find_all('td', class_='Barei Txt_C')
            for dd in d:
                temp_barei.append(dd.text.replace("\n","").replace(" ","").replace("**",""))
            print(temp_barei)
        elif place_checker == 1:   # 地方
            # 性齢取得テスト
            temp_barei = []
            d = soup.find_all('span', class_='Age')
            for dd in d:
                temp_barei.append(dd.text.replace("\n","").replace(" ","").replace("**",""))
            print(temp_barei)
        else:
            pass

        # 斤量取得テスト
        temp_kinryo = []
        e = soup.find_all('td', class_='Txt_C')
        for eee in e:
            ee = eee.text.replace("\n","").replace(" ","").replace("**","")
            if (len(ee) == 0):
                pass
            elif '牡' in ee:
                pass
            elif '牝' in ee:
                pass
            elif len(ee) <= 3:
                pass
            else:
                temp_kinryo.append(eee.text.replace("\n","").replace(" ","").replace("**",""))
        print(temp_kinryo)


        # 騎手取得テスト
        temp_kisyu = []
        f = soup.find_all('td', class_='Jockey')
        for ff in f:
            temp_kisyu.append(ff.text.replace("\n","").replace(" ","").replace("○○","未 定"))
        print(temp_kisyu)

        # 厩舎情報の取得テスト
        temp_trainer = []
        g = soup.find_all('td', class_='Trainer')
        for gg in g:
            temp_trainer.append(gg.text.replace("\n","").replace(" ",""))
        print(temp_trainer)


        # 枠番決定方法
        if len(temp_a) == 8:
            waku = [1, 2, 3, 4, 5, 6, 7, 8]
        elif len(temp_a) == 9:
            waku = [1, 2, 3, 4, 5, 6, 7, 8, 8]
        elif len(temp_a) == 10:
            waku = [1, 2, 3, 4, 5, 6, 7, 7, 8, 8]
        elif len(temp_a) == 11:
            waku = [1, 2, 3, 4, 5, 6, 6, 7, 7, 8, 8]
        elif len(temp_a) == 12:
            waku = [1, 2, 3, 4, 5, 5, 6, 6, 7, 7, 8, 8]
        elif len(temp_a) == 13:
            waku = [1, 2, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8]
        elif len(temp_a) == 14:
            waku = [1, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8]
        elif len(temp_a) == 15:
            waku = [1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8]
        elif len(temp_a) == 16:
            waku = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8]
        elif len(temp_a) == 17:
            waku = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 8]
        elif len(temp_a) == 18:
            waku = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 7, 8, 8, 8]

        # 馬番決定方法
        umaban = [ int(x) for x in range(1, len(temp_a)+1)]
        

        print(waku)
        print(umaban)
        
        
        # 血統の取得
        bld_lists= get_info(ids_list=temp_ids)


        # 馬情報の結合
        horse_infos_list = list(zip(temp_a, waku, umaban, temp_barei, temp_kinryo, temp_kisyu, temp_trainer))

        # 辞書の作成
        races_json = make_json(race_id=race_id, race_info=race_info_list, horse_ids=temp_ids, horse_infos=horse_infos_list, bld_lists=bld_lists)
        # 辞書にレースの詳細な開催情報データの追加
        races_json[race_id]['race_hold_info'] = race_hold_info_list
        print(races_json)

        #print(bld_lists)


        # ファイルの追加
        #f_path = r'D:\keiba_bot\voted_bot\getting_uma_info\saved_race_jsons\vote_race_datas.json'
        f_path = saved_path + r'\vote_race_datas.json'

        if os.path.exists(f_path):  # もしファイルがある場合
            open_race_json = READ_JSON(json_f_path=f_path)
            race_ids = list(open_race_json.keys())
            if race_id in race_ids:
                print('既に登録されているデータです')
                sys.exit()
            else:
                print('上書きを行います。')
                open_race_json.update(races_json)
                with open(f_path, mode='wt', encoding='utf-8') as file:
                    json.dump(open_race_json, file, ensure_ascii=False, indent=4)
        else:
            print('新規作成を行います。')
            with open(f_path, mode='wt', encoding='utf-8') as file:
                json.dump(races_json, file, ensure_ascii=False, indent=4) 

        print('json saved!')



    




def get_info(ids_list):
    #path_ = r"D:\keiba_bot\voted_bot\getting_uma_info\test_saved\umas_infos.html"
    
    # return用血統リスト
    bld_list = []
    
    
    for id_uma in ids_list:
        print('====================================================================')
        print('血統の取得の開始')
        print(id_uma)
        
        time.sleep(5)
        url = r'https://db.netkeiba.com/horse/' + str(id_uma)
        html = requests.get(url)
        html.encoding = "EUC-JP"

        
        soup_2 = BeautifulSoup(html.text, "html.parser")
        time.sleep(3)
        print('血統の取得の終了')
        print('====================================================================')
        #soup_2 = BeautifulSoup(open(path_, encoding='EUC-JP'), "html.parser")

        # 血統
        bml = soup_2.find('td', class_="b_ml", rowspan="2") # 父
        bfml = soup_2.find('td', class_="b_fml", rowspan="2")   # 母
        hahachichi = soup_2.find_all('td', class_="b_ml")
        hahachichi_bld = hahachichi[2]  # 母父
        print(bml.text.replace("\n","").replace(" ",""))
        print(bfml.text.replace("\n","").replace(" ",""))
        print(hahachichi_bld.text.replace("\n","").replace(" ",""))



        temp_tuple = (bml.text.replace("\n","").replace(" ",""), bfml.text.replace("\n","").replace(" ",""), hahachichi_bld.text.replace("\n","").replace(" ",""))

        bld_list.append(temp_tuple)
    
    return bld_list





# jsonの読み込み関数
def READ_JSON(json_f_path):
    """
    {
    "e_0": [
        5095628,
        10006310,
        6,
        "E_0"
    ],
    の読み込みと辞書型への変換
    """
    # jsonを辞書型に変換
    with open(json_f_path, mode='rt', encoding='utf-8') as js_file:

        # 辞書オブジェクト(dictionary)を取得
        json_dict = json.load(js_file)
        
    # return
    return json_dict




def main():

    # セーブ先path 
    race_saved = r'saved_race_jsons'

    # pythonのバージョンの確認
    print(sys.version)

    msg_plus = '＊'
    print(msg_plus*20 + '注意事項' + msg_plus*20)
    print('(1) : このプログラムは、レース予想用のレースを取得するプログラムです')
    print('(2) : 次に出てくる指示にしたがって入力してください(入力は全て半角数字のみ)')
    print('(3) : 各項目に簡易的なチェック機能は設けていますが、入力に失敗した場合はプログラムを終了し再度やり直してください')
    print(msg_plus*44)

    print('')
    print('')

    print('取得したいレースの開催日の日付をYYYYMMDD形式で入力してください(1日のみ指定可能)')
    print('(例えば、2022年3月19日のレースなら、20220319と入力)')
    race_hold_days = str(input())

    print(' ')

    print('中央か地方かを選択してください（中央なら0、地方なら1を入力）')
    place_num = int(input())
    if place_num == 0:
        print('【中央競馬】が選択されました.これ以降は地方競馬に関する入力は受付できません')
    elif place_num == 1:
        print('【地方競馬】が選択されました.これ以降は中央競馬に関する入力は受付できません')
    else:
        print('不正な値です.プログラムを終了します')
        sys.exit()
    print(place_num)

    print(' ')

    print('取得したいレース数を半角数字で入力してください')
    race_N = int(input())

    if race_N == 0:
        print('1以上のレースを入力してください')
        sys.exit()

    print(' ')

    print('レースIDを整数で入力してください')
    print('レースIDとは、netkeibaのレースURLである、\nhttps://race.netkeiba.com/race/shutuba.html?race_id=xxxxxxxxxxxx\nの「xxxxxxxxxxxx」のID番号になります。')
    race_id_list=[]
    for i in range(race_N):
        race_id = str(input())
        
        if len(race_id) != 12:
            print('不正な値です.プログラムを終了します')
            sys.exit()
        print('入力されたレースID : ' + race_id)

        race_id_list.append(race_id)

    print(' ')

    print('ディレクトリがあるか確認します')

    search_dir_path = race_saved + '\\' + race_hold_days

    if os.path.exists(search_dir_path):
        print('ディレクトリがありました.該当レース情報はここに保存します')
        print('保存先パス : {}'.format(search_dir_path))
    else:
        print('ディレクトリが見つかりませんでした.作成を行います')
        os.mkdir(search_dir_path)
        print('作成された保存先パス : {}'.format(search_dir_path))
    


		
    race_scrape(race_ids= race_id_list, place_checker=place_num, saved_path=search_dir_path)
    #est_html(saved_p=test_saved_path, race_id=race_id_list)


    print('全レースの取得が完了しました.3秒後にプログラムを終了します')
    time.sleep(3)
    sys.exit()



if __name__ == '__main__':
    main()
    #get_info()

