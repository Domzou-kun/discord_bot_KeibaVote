
import numpy as np


def poll_score(vote_res, regist_horse, race_id):

    # スコアdictの作成
    initial_score = [ 0 for _ in range(0, int(len(regist_horse)))]
    score_dict = dict(zip(regist_horse, initial_score))

    # 絵文字変換
    reaction_buttons = [ '🧿', '⭕', '🔼', '🔽', '⭐', '❌' ] 
    hex_ord_list = [ hex(ord(_rect)) for _rect in reaction_buttons ]


    # 投票結果の辞書key
    poll_dict_key_list = list(vote_res.keys())

    print(vote_res)
    print(hex_ord_list)
    print(regist_horse)
    print(vote_res)
    
    
    

    for poll_dict_key in poll_dict_key_list:
        poll_horse_res = vote_res[poll_dict_key][race_id]['res']
        
        for poll_horse_tuple in poll_horse_res.items():
            # (horse_name, emoji_code)
            # スコア加算
            if hex_ord_list[0] == poll_horse_tuple[1]:
                poll_score = score_dict[poll_horse_tuple[0]]
                poll_score = poll_score + 10
                score_dict[poll_horse_tuple[0]] = poll_score

            elif hex_ord_list[1] == poll_horse_tuple[1]:
                poll_score = score_dict[poll_horse_tuple[0]]
                poll_score = poll_score + 7
                score_dict[poll_horse_tuple[0]] = poll_score

            elif hex_ord_list[2] == poll_horse_tuple[1]:
                poll_score = score_dict[poll_horse_tuple[0]]
                poll_score = poll_score + 5
                score_dict[poll_horse_tuple[0]] = poll_score

            elif hex_ord_list[3] == poll_horse_tuple[1]:
                poll_score = score_dict[poll_horse_tuple[0]]
                poll_score = poll_score + 3
                score_dict[poll_horse_tuple[0]] = poll_score

            elif hex_ord_list[4] == poll_horse_tuple[1]:
                poll_score = score_dict[poll_horse_tuple[0]]
                poll_score = poll_score + 2
                score_dict[poll_horse_tuple[0]] = poll_score

            elif hex_ord_list[5] == poll_horse_tuple[1]:
                poll_score = score_dict[poll_horse_tuple[0]]
                poll_score = poll_score + (-6)
                score_dict[poll_horse_tuple[0]] = poll_score
            

    # dictに記録されたスコアの確認
    print('========== <== スコア集計 ==> ==========')
    print(score_dict)

    # 標準化処理
    poll_score_value_list = list(score_dict.values())   # valueの取得
    poll_score_key_list = list(score_dict.keys())   # keyの取得

    # np arrayに変換    
    poll_score_ndarray = np.array(poll_score_value_list)
    flat_poll_score = normalize(v=poll_score_ndarray)

    new_poll_score = flat_poll_score.tolist()
    new_poll_score_list = [x*100 for x in new_poll_score]   # 0~100%に設定する


    # 最終的なスコアdictへのマージ
    new_poll_score_dict = dict(zip(poll_score_key_list, new_poll_score_list))
    print('========== <== 最終的な新しいスコア辞書 ==> ==========')
    print(new_poll_score_dict)


    return new_poll_score_dict


def normalize(v, axis=-1, order=2):
    l2 = np.linalg.norm(v, ord = order, axis=axis, keepdims=True)
    l2[l2==0] = 1
    return v/l2

