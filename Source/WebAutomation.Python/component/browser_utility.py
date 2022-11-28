from selenium.webdriver import ChromeOptions

class BrowserUtility():
    def __init__(self):
        self.executable_path = r"C:\Projects\ATK_WebAutomation\Driver\chromedriver.exe"

    def get_chrome_options(self):
        options = ChromeOptions();
        options.page_load_strategy = 'none'
        options.add_argument('--enable-automation')
        options.add_argument('--disable-infobars') #
        options.add_argument('--incognito') # 無痕模式
        options.add_argument('--disable-gpu') # 關閉使用顯示卡(降低錯誤)
        options.add_argument('--no-sandbox')
        options.add_argument('--ignore-certificate-errors') # 忽略憑證錯誤
        options.add_argument('--allow-insecure-localhost')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-browser-side-navigation')
        options.add_argument('--mute-audio') # 靜音
        options.add_argument('--force-device-scale-factor=1') # 縮放比例
        options.add_argument(f'--window-size=1366,768')
        return options;

    def get_headers(self):
        return {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                    'Cache-Control': 'no-cache',
                    'Connection': 'keep-alive',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Pragma': 'no-cache',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'same-origin',
                    'Sec-Fetch-User': '?1',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
                    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                };

    def set_cookies(self, driver, session):
        cookies = driver.get_cookies()
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])