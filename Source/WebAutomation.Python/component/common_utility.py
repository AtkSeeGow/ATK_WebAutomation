import os
from datetime import datetime
from selenium.webdriver import ChromeOptions


class CommonUtility():
    def __init__(self):
        now = datetime.now();
        strftime = now.strftime("%Y%m%d")
        self.folder_path = rf"C:\Projects\ATK_WebAutomation\Data\{strftime}"
        if not os.path.isdir(self.folder_path):
            os.makedirs(self.folder_path)

        self.log_path = rf"{self.folder_path}\log.txt"
        self.captcha_path = rf"{self.folder_path}\captcha.png"