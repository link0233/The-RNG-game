import math

class BigNumber:
    def __init__(self, value):
        """
        初始化大數，接受數字或字串形式。
        :param value: 數字或字串 (如 "1.23e500000" 或 1.23e500)
        """
        if isinstance(value, (int, float)):  # 直接給數字
            if value == 0:
                self.mantissa = 0
                self.exponent = 0
            else:
                self.exponent = int(math.floor(math.log10(abs(value))))
                self.mantissa = value / (10 ** self.exponent)
        elif isinstance(value, str):  # 字串形式
            if "e" in value:  # 科學記號格式
                mantissa, exponent = value.split("e")
                self.mantissa = float(mantissa)
                self.exponent = int(exponent)
            else:  # 一般數字
                value = float(value)
                self.exponent = int(math.floor(math.log10(abs(value))))
                self.mantissa = value / (10 ** self.exponent)
        else:
            raise ValueError("不支援的輸入類型")

        # 只保留前 10 位有效數字
        self.mantissa = round(self.mantissa, 10)

    def __repr__(self):
        """ 以科學記號顯示數值 """
        return f"{self.mantissa}e{self.exponent}"

    def normalize(self):
        """ 確保 mantissa 在 1 ≤ x < 10 之間 """
        if self.mantissa == 0:
            self.exponent = 0
        else:
            while abs(self.mantissa) >= 10:
                self.mantissa /= 10
                self.exponent += 1
            while abs(self.mantissa) < 1 and self.mantissa != 0:
                self.mantissa *= 10
                self.exponent -= 1
        self.mantissa = round(self.mantissa, 10)  # 只保留前 10 位有效數字

    def __add__(self, other):
        """ 加法運算 """
        if not isinstance(other, BigNumber):
            other = BigNumber(other)

        # 讓兩數指數對齊
        if self.exponent > other.exponent:
            adjusted_mantissa = other.mantissa / (10 ** (self.exponent - other.exponent))
            result_mantissa = self.mantissa + adjusted_mantissa
            result_exponent = self.exponent
        else:
            adjusted_mantissa = self.mantissa / (10 ** (other.exponent - self.exponent))
            result_mantissa = other.mantissa + adjusted_mantissa
            result_exponent = other.exponent

        result = BigNumber(f"{result_mantissa}e{result_exponent}")
        result.normalize()
        return result

    def __sub__(self, other):
        """ 減法運算 """
        if not isinstance(other, BigNumber):
            other = BigNumber(other)
        return self + BigNumber(f"{-other.mantissa}e{other.exponent}")

    def __mul__(self, other):
        """ 乘法運算 """
        if not isinstance(other, BigNumber):
            other = BigNumber(other)

        result_mantissa = self.mantissa * other.mantissa
        result_exponent = self.exponent + other.exponent

        result = BigNumber(f"{result_mantissa}e{result_exponent}")
        result.normalize()
        return result

    def __truediv__(self, other):
        """ 除法運算 """
        if not isinstance(other, BigNumber):
            other = BigNumber(other)

        if other.mantissa == 0:
            raise ZeroDivisionError("不能除以 0")

        result_mantissa = self.mantissa / other.mantissa
        result_exponent = self.exponent - other.exponent

        result = BigNumber(f"{result_mantissa}e{result_exponent}")
        result.normalize()
        return result

    def __eq__(self, other):
        """ 判斷相等 """
        if not isinstance(other, BigNumber):
            other = BigNumber(other)
        return self.exponent == other.exponent and self.mantissa == other.mantissa

    def __lt__(self, other):
        """ 小於比較 """
        if not isinstance(other, BigNumber):
            other = BigNumber(other)
        if self.exponent < other.exponent:
            return True
        if self.exponent > other.exponent:
            return False
        return self.mantissa < other.mantissa

    def __le__(self, other):
        """ 小於等於 """
        return self < other or self == other

    def __gt__(self, other):
        """ 大於比較 """
        if not isinstance(other, BigNumber):
            other = BigNumber(other)
        if self.exponent > other.exponent:
            return True
        if self.exponent < other.exponent:
            return False
        return self.mantissa > other.mantissa

    def __ge__(self, other):
        """ 大於等於 """
        return self > other or self == other

    def __ne__(self, other):
        """ 不等於 """
        return not self == other
    
    def __pow__(self, other):
        """ 指數運算 """
        if not isinstance(other, (int, float, BigNumber)):
            raise TypeError("指數必須是數字或 BigNumber")

        if isinstance(other, BigNumber):
            other = other.mantissa * (10 ** other.exponent)  # 轉回普通數字

        if self.mantissa == 0:
            if other == 0:
                raise ValueError("0 的 0 次方未定義")
            return BigNumber(0)

        # 運算公式：(a × 10^b) ^ n = a^n × 10^(b * n)
        new_mantissa = self.mantissa ** other
        new_exponent = self.exponent * other

        result = BigNumber(f"{new_mantissa}e{new_exponent}")
        result.normalize()
        return result