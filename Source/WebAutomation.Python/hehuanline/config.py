class Config():
    def __init__(self):
        self.account = ""
        self.password = ""
        # 住宿日期
        self.ticket_date = "2022-09-28"
        self.ticket_numbers = 1;
        # 開放時間
        self.open_date = "2022-08-30 07:55:00";
        # 房型(滑雪山莊:212、景觀雙人套房:134)
        self.room_type = "";

    def captcha_path(self):
        return rf'C:\Logs\{self.account}\captcha.png';

    def log_root_path(self):
        return rf'C:\Logs\{self.account}'
        