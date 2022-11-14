import json
from main_sub_func import json_func as jf

def marge_vote_res(race_id, today_data):

    # 取得するレースのpath
    vote_user_record_path = r'vote_user_record' + '\\' + str(today_data) + '\\' + str(race_id) + r'_vote_user_record.json'

    print('========== <== レース投票者の結果の統合 ==> ==========')
    print('投票者jsonパス : {}'.format(vote_user_record_path))

    # jsonの取得
    vote_user_record_json = jf.READ_JSON(json_f_path=vote_user_record_path)

    # 投票されているかの有無
    if len(vote_user_record_json) != 0:
        # jsonのvalueの取得
        voted_user_name_list = list(vote_user_record_json.keys())
        voted_user_id_list = list(vote_user_record_json.values())

        # 各個別投票結果jsonの取得
        user_res_dict = {}  # このdictにマージしていきreturnする
        for voted_user_id in voted_user_id_list:
            voted_user_res_path = r'user_record\user_records' + '\\' + str(voted_user_id) + '\\' + str(today_data) + '\\' + str(voted_user_id) + '_' + str(race_id) + '.json'
            voted_user_res_json = jf.READ_JSON(json_f_path=voted_user_res_path)

            # 取得した投票結果をupdate
            user_res_dict.update(voted_user_res_json)

        
        print('========== <== 投票結果のマージ完了 ==> ==========')
        print('マージdict')
        print(user_res_dict)
        print('マージ対象のユーザー')
        for marge_user in voted_user_name_list:
            print(marge_user)
        print('=================================================')

        return user_res_dict
    
    # 投票されていない場合
    else:
        return_msg = 'のレースは投票がありませんでした。'
        return return_msg



    










