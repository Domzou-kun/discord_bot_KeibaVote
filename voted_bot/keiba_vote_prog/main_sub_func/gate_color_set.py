
def gate_color(uma_list):

    # カラーコードリスト
    color_list = [
        0xffffff,   # 白
        0x000000,   # 黒
        0xff0000,   # 赤
        0x0000ff,   # 青
        0xffff00,   # 黄
        0x008000,   # 緑
        0xffa500,   # 橙
        0xff1493    # 桃
    ]
        
    # 出走頭数
    uma_numbers = len(uma_list)

    if uma_numbers <= 8:    # 8頭以下ならそのまま返す
        return color_list
    elif uma_numbers == 9:
        return [
        0xffffff,   # 白
        0x000000,   # 黒
        0xff0000,   # 赤
        0x0000ff,   # 青
        0xffff00,   # 黄
        0x008000,   # 緑
        0xffa500,   # 橙
        0xff1493,   # 桃
        0xff1493    # 桃
    ]
    elif uma_numbers == 10:
        return [
        0xffffff,   # 白
        0x000000,   # 黒
        0xff0000,   # 赤
        0x0000ff,   # 青
        0xffff00,   # 黄
        0x008000,   # 緑
        0xffa500,   # 橙
        0xffa500,   # 橙
        0xff1493,   # 桃
        0xff1493    # 桃
    ]
    elif uma_numbers == 11:
        return [
        0xffffff,   # 白
        0x000000,   # 黒
        0xff0000,   # 赤
        0x0000ff,   # 青
        0xffff00,   # 黄
        0x008000,   # 緑
        0x008000,   # 緑
        0xffa500,   # 橙
        0xffa500,   # 橙
        0xff1493,   # 桃
        0xff1493    # 桃
    ]
    elif uma_numbers == 12:
        return [
        0xffffff,   # 白
        0x000000,   # 黒
        0xff0000,   # 赤
        0x0000ff,   # 青
        0xffff00,   # 黄
        0xffff00,   # 黄
        0x008000,   # 緑
        0x008000,   # 緑
        0xffa500,   # 橙
        0xffa500,   # 橙
        0xff1493,   # 桃
        0xff1493    # 桃
    ]
    elif uma_numbers == 13:
        return [
        0xffffff,   # 白
        0x000000,   # 黒
        0xff0000,   # 赤
        0x0000ff,   # 青
        0x0000ff,   # 青
        0xffff00,   # 黄
        0xffff00,   # 黄
        0x008000,   # 緑
        0x008000,   # 緑
        0xffa500,   # 橙
        0xffa500,   # 橙
        0xff1493,   # 桃
        0xff1493    # 桃
    ]
    elif uma_numbers == 14:
        return [
        0xffffff,   # 白
        0x000000,   # 黒
        0xff0000,   # 赤
        0xff0000,   # 赤
        0x0000ff,   # 青
        0x0000ff,   # 青
        0xffff00,   # 黄
        0xffff00,   # 黄
        0x008000,   # 緑
        0x008000,   # 緑
        0xffa500,   # 橙
        0xffa500,   # 橙
        0xff1493,   # 桃
        0xff1493    # 桃
    ]
    elif uma_numbers == 15:
        return [
        0xffffff,   # 白
        0x000000,   # 黒
        0x000000,   # 黒
        0xff0000,   # 赤
        0xff0000,   # 赤
        0x0000ff,   # 青
        0x0000ff,   # 青
        0xffff00,   # 黄
        0xffff00,   # 黄
        0x008000,   # 緑
        0x008000,   # 緑
        0xffa500,   # 橙
        0xffa500,   # 橙
        0xff1493,   # 桃
        0xff1493    # 桃
    ]
    elif uma_numbers == 16:
        return [
        0xffffff,   # 白
        0xffffff,   # 白
        0x000000,   # 黒
        0x000000,   # 黒
        0xff0000,   # 赤
        0xff0000,   # 赤
        0x0000ff,   # 青
        0x0000ff,   # 青
        0xffff00,   # 黄
        0xffff00,   # 黄
        0x008000,   # 緑
        0x008000,   # 緑
        0xffa500,   # 橙
        0xffa500,   # 橙
        0xff1493,   # 桃
        0xff1493    # 桃
    ]
    elif uma_numbers == 17:
        return [
        0xffffff,   # 白
        0xffffff,   # 白
        0x000000,   # 黒
        0x000000,   # 黒
        0xff0000,   # 赤
        0xff0000,   # 赤
        0x0000ff,   # 青
        0x0000ff,   # 青
        0xffff00,   # 黄
        0xffff00,   # 黄
        0x008000,   # 緑
        0x008000,   # 緑
        0xffa500,   # 橙
        0xffa500,   # 橙
        0xff1493,   # 桃
        0xff1493,   # 桃
        0xff1493    # 桃
    ]
    elif uma_numbers == 18:
        return [
        0xffffff,   # 白
        0xffffff,   # 白
        0x000000,   # 黒
        0x000000,   # 黒
        0xff0000,   # 赤
        0xff0000,   # 赤
        0x0000ff,   # 青
        0x0000ff,   # 青
        0xffff00,   # 黄
        0xffff00,   # 黄
        0x008000,   # 緑
        0x008000,   # 緑
        0xffa500,   # 橙
        0xffa500,   # 橙
        0xffa500,   # 橙
        0xff1493,   # 桃
        0xff1493,   # 桃
        0xff1493    # 桃
    ]
    elif uma_numbers == 19:
        return [
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
    ]
    elif uma_numbers == 20:
        return [
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
    ]
    elif uma_numbers == 21:
        return [
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
    ]
    elif uma_numbers == 22:
        return [
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
    ]
    elif uma_numbers == 23:
        return [
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
        0xffffff,   # 白
    ]
    else:   # それ以外の例外的頭数
        return color_list[:uma_numbers]

