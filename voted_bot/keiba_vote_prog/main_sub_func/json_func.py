import json

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

