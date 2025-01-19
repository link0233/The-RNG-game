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