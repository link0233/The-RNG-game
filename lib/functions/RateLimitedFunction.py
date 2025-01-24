import time

class RateLimitedFunction:
    def __init__(self, interval, condition):
        """
        初始化限速函數
        :param interval: 執行函數的最小間隔時間（秒）
        :param condition: 函數觸發的條件（可調用對象，返回布林值）
        """
        self.interval = interval
        self.condition = condition
        self.last_run = 0
        self.last_stop = 0

    def execute(self, func, *args, **kwargs):
        """
        嘗試執行函數，根據條件和間隔時間限制執行
        :param func: 要執行的函數
        :param args: 函數的位置參數
        :param kwargs: 函數的關鍵字參數
        """
        current_time = time.time()
        if current_time - self.last_run >= self.interval and self.condition():
            self.last_run = current_time
            return func(*args, **kwargs)
        else:pass
            #print("條件不滿足或尚未達到間隔時間，函數未執行。")

    def get_timeToRun(self):
        """
        回傳該程式執行的剩餘時間
        落已可以執行則回傳0
        """
        current_time = time.time()
        _time = self.interval - (current_time - self.last_run)
        if _time <= 0:
            return 0
        else:
            return _time
        
    def reset(self):
        """
        重新設定啟用時間
        """
        self.last_run = time.time()
        
    def stop(self):
        """
        暫停
        """
        self.last_stop = time.time()

    def restart(self):
        """
        暫停後重新開始
        """
        now = time.time()
        self.last_run += now - self.last_stop