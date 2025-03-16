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
                #print(value)
                mantissa, exponent = value.split("e")
                self.mantissa = float(mantissa)
                self.exponent = int(float(exponent))
            else:  # 一般數字
                value = float(value)
                if value != 0:
                    self.exponent = int(math.floor(math.log10(abs(value))))
                    self.mantissa = value / (10 ** self.exponent)
                if value == 0:
                    self.exponent = 0
                    self.mantissa = 0
        else:
            raise ValueError("不支援的輸入類型")

        # 只保留前 10 位有效數字
        self.mantissa = round(self.mantissa, 10)

    def __repr__(self , two_float = False):
        """ 以科學記號顯示數值 """
        if self.exponent<6:
            return f"{self.to_int()}"
        if two_float:
            return f"{self.mantissa:.2f}e{self.exponent}"   
        else:
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
        """ 加法 a + b """
        if not isinstance(other, BigNumber):
            other = BigNumber(other)

        if self.exponent > other.exponent:
            shift = self.exponent - other.exponent
            new_mantissa = self.mantissa + (other.mantissa / (10 ** shift))
            new_exponent = self.exponent
        else:
            shift = other.exponent - self.exponent
            new_mantissa = (self.mantissa / (10 ** shift)) + other.mantissa
            new_exponent = other.exponent

        return BigNumber(f"{new_mantissa}e{new_exponent}")

    def __sub__(self, other):
        """ 減法 a - b """
        return self + (-other)

    def __neg__(self):
        """ 負數 -a """
        return BigNumber(f"{-self.mantissa}e{self.exponent}")

    def __mul__(self, other):
        """ 乘法 a * b """
        if not isinstance(other, BigNumber):
            other = BigNumber(other)

        new_mantissa = self.mantissa * other.mantissa
        new_exponent = self.exponent + other.exponent

        return BigNumber(f"{new_mantissa}e{new_exponent}")

    def __truediv__(self, other):
        """ 除法 a / b """
        if not isinstance(other, BigNumber):
            other = BigNumber(other)

        if other.mantissa == 0:
            raise ZeroDivisionError("除數不能為零")

        new_mantissa = self.mantissa / other.mantissa
        new_exponent = self.exponent - other.exponent

        return BigNumber(f"{new_mantissa}e{new_exponent}")


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
        """ 修正指數運算 a ** b，支援超大 b """
        if not isinstance(other, BigNumber):
            other = BigNumber(other)

        if self.mantissa <= 0:
            raise ValueError("指數運算僅支援正數")

        log10_a = math.log10(self.mantissa) + self.exponent
        new_exponent = log10_a * (other.mantissa * (10 ** other.exponent))

        # 計算新 mantissa，避免浮點數溢出
        new_mantissa = 10 ** (new_exponent % 1)
        new_exponent = int(new_exponent)

        return BigNumber(f"{new_mantissa}e{new_exponent}")
    
    def log2(self):
        """ 計算 log2(self) """
        if self.mantissa <= 0:
            raise ValueError("log2(x) 只能計算正數")

        LOG10_2 = math.log10(2)  # ≈ 0.30102999566
        LOG10_8 = math.log10(8)  # ≈ 0.903089987

        # log10(c) = log10(mantissa) + exponent
        log10_c = math.log10(self.mantissa) + self.exponent

        # log10(c/8) = log10(c) - log10(8)
        log10_c_div_8 = log10_c #- LOG10_8

        # log2(c/8) = log10(c/8) / log10(2)
        log2_c_div_8 = log10_c_div_8 / LOG10_2

        return int(log2_c_div_8)  # 取整數
    
    def log(self, base=10):
        """ 計算 log_base(self) """
        if self.mantissa <= 0:
            raise ValueError("log(x) 只能計算正數")
        if base <= 0 or base == 1:
            raise ValueError("底數必須是正數且不能是 1")

        # 計算 log10(x) = log10(mantissa) + exponent
        log10_x = math.log10(self.mantissa) + self.exponent

        # 計算 log_base(x) = log10(x) / log10(base)
        log_base_x = log10_x / math.log10(base)

        return log_base_x  # 回傳浮點數

    def to_int(self):
        """ 轉換為整數（如果數字過大，則只取前 10 位） """
        if self.exponent < 18:  # Python 的 int 可安全儲存 10^18 以下的數字
            return int(self.mantissa * (10 ** self.exponent))
        else:
            # 只取前 10 位數字
            first_digits = int(self.mantissa * (10 ** 9))  # 9 位 mantissa（確保準確度）
            return int(f"{first_digits}" + "0" * (self.exponent - 9))  # 追加 0