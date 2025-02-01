def format_to_two_decimal_places(number_str):
    """
    保留兩位小數的整數字符串。
    :param number_str: 表示數字的字符串
    :return: 格式化後的字符串
    """
    try:
        # 將字符串轉換為浮點數
        number = float(number_str)
        # 格式化為保留兩位小數的字符串
        formatted_number = f"{number:.2f}"
        return formatted_number
    except ValueError:
        return "輸入無效，請提供有效的數字字符串。"
    
def returnTrue(): return True

def draw_text(screen, text, font, color, rect, line_height, antialias=True):
    """
    繪製自動換行文字
    :param screen: 畫布
    :param text: 要顯示的文字
    :param font: Pygame 字型對象
    :param color: 字體顏色 (RGB)
    :param rect: 限制的繪製範圍 (x, y, w, h)
    :param line_height: 每行的高度
    :param antialias: 是否使用抗鋸齒
    """
    words = text.split(' ')  # 按空格分割文字
    x, y, w, h = rect
    line = ""
    space_width, _ = font.size(" ")  # 空格的寬度

    for word in words:
        word_width, word_height = font.size(word)
        # 檢查當前行的長度
        if font.size(line + word)[0] <= w:
            line += word + " "
        else:
            # 繪製當前行文字
            text_surface = font.render(line, antialias, color)
            screen.blit(text_surface, (x, y))
            y += line_height  # 移到下一行
            line = word + " "

        # 如果超出高度限制，停止繪製
        if y + line_height > h:
            print("error")
            break

    # 繪製最後一行
    if line:
        text_surface = font.render(line, antialias, color)
        screen.blit(text_surface, (x, y))

def closest_smaller(a, b):
    """
    :param a: 一個清單
    :param b: 一個數字
    回傳a 中 最接近b且小於b的數字
    """
    smaller_numbers = [x for x in a if x <= b]  # 過濾出小於 b 的數字
    return max(smaller_numbers, default=None)  # 找最大值（最接近 b），如果沒有則回傳 None