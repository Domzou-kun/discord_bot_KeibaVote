from discord.ext import commands
import discord
import requests
import json
import datetime
import cv2
import os
from PIL import Image, ImageDraw, ImageFont





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

# dictからjsonでの保存処理
def SAVE_JSON(json_f_save_path, saved_dict):

    with open(json_f_save_path, 'w', encoding='utf-8') as fp:
        json.dump(saved_dict, fp, indent=4)

    print('complete json file')



def main():

    # jsonの読み込み
    json_p = r"D:\keiba_bot\voted_bot\getting_uma_info\saved_race_jsons\20220219\vote_race_datas.json"
    race_json = READ_JSON(json_f_path=json_p)

    race_hold_name = race_json["202209010311"]['race_name']     # レース名
    race_hold_info = race_json["202209010311"]['race_hold_info']        # レース情報
    race_hold_time = race_json["202209010311"]['race_times']        # レース時間
    race_hold_distance = race_json["202209010311"]['race_distance'] # レース距離

    
    # 曜日
    dt_now = datetime.datetime.now()
    hold_today_data = str(dt_now.year) + '年' + str(dt_now.month).zfill(2) + '月' + str(dt_now.day).zfill(2) + '日' + '開催競争レース'


    # フォントpath
    hold_info_font_path = r'C:\Windows\Fonts\HGRGY.TTC'
    hold_info_sub_font_path = r'C:\Windows\Fonts\HGRME.TTC'
    text_color = (0,0,0,255)

    # holdなどの情報
    hold_info_font_size = 30
    hold_info_font = ImageFont.truetype(hold_info_sub_font_path, hold_info_font_size)
    hold_place_info_font_size = 65
    hold_place_info_font = ImageFont.truetype(hold_info_font_path, hold_place_info_font_size)
    hold_day_info_font_size = 20
    hold_day_info_font = ImageFont.truetype(hold_info_sub_font_path, hold_day_info_font_size)

    hold_info_name_p = r"D:\keiba_bot\voted_bot\test_logo\logo_2.jpg"
    hold_info_name_im = Image.open(hold_info_name_p)
    hold_info_name_img = ImageDraw.Draw(hold_info_name_im)

    # 文字の入力
    str_place = (20, 33)
    hold_info_name_img.text(str_place, race_hold_name, font=hold_place_info_font, fill=text_color)    # レース名

    str_place = (20, 10)
    hold_info_name_img.text(str_place, hold_today_data, font=hold_day_info_font, fill=text_color)    # レース開催日
    

    str_place = (15, 130)
    race_start_info = race_hold_time + ' ' + race_hold_distance
    hold_info_name_img.text(str_place, race_start_info, font=hold_info_font, fill=text_color)    # レースの時間と距離

    str_place = (15, 165)
    race_hold_info_1 = ''
    for hold_i in range(0, 3):
        race_hold_info_1 = race_hold_info_1 + race_hold_info[hold_i] + ' '
    hold_info_name_img.text(str_place, race_hold_info_1, font=hold_info_font, fill=text_color)    # レースhold 1


    str_place = (15, 200)
    race_hold_info_2 = ''
    for hold_i in range(3, 5):
        race_hold_info_2 = race_hold_info_2 + race_hold_info[hold_i] + ' '
    hold_info_name_img.text(str_place, race_hold_info_2, font=hold_info_font, fill=text_color)    # レースhold 2

    str_place = (15, 235)
    race_hold_info_3 = ''
    for hold_i in range(5, 7):
        race_hold_info_3 = race_hold_info_3 + race_hold_info[hold_i] + ' '
    hold_info_name_img.text(str_place, race_hold_info_3, font=hold_info_font, fill=text_color)    # レースhold 3


    str_place = (15, 270)
    race_hold_info_4 = ''
    for hold_i in range(7, 8):
        race_hold_info_4 = race_hold_info_4 + race_hold_info[hold_i] + ' '
    hold_info_name_img.text(str_place, race_hold_info_4, font=hold_info_font, fill=text_color)    # レースhold 4


    str_place = (15, 305)
    race_hold_info_5 = ''
    for hold_i in range(8, 9):
        race_hold_info_5 = race_hold_info_5 + race_hold_info[hold_i] + ' '
    hold_info_name_img.text(str_place, race_hold_info_5, font=hold_info_font, fill=text_color)    # レースhold 4

    

    # 保存
    saved_p = r'D:\keiba_bot\voted_bot\test_logo\logo_test_hold.png'
    hold_info_name_im.save(saved_p)
    print('saved ok')



if __name__ == '__main__':
    main()


