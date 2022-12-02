import time
import logging
import threading
import traceback
import ddddocr
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from component.browser_utility import BrowserUtility
from component.common_utility import CommonUtility
from hehuanline.config import Config

class Bot():
    def __init__(self):
        self.config = Config();

        self.commonUtility = CommonUtility();
        log_path = self.commonUtility.log_path;

        self.browser_utility = BrowserUtility();
        chrome_options = self.browser_utility.get_chrome_options();
        executable_path = self.browser_utility.executable_path;
        self.driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options);

        self.is_while = True;
        self.judging_success_thread: threading.Thread = None;
        self.judgment_failed_thread: threading.Thread = None;

        fileHandler = logging.FileHandler(log_path, mode='a')
        fileHandler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'));
        self.logger = logging.getLogger("Bot");
        self.logger.addHandler(fileHandler);

        self.terminate_judging_flag();

    def terminate_judging_flag(self):
        try:
            self.is_judging_success = False;
            self.is_judging_success_while = False;
            self.is_judgment_failed = False;
            self.is_judgment_failed_while = False;
        except Exception as e:
            self.logger.error(f"terminate_judging_flag error: {e}")

    def judging_success(self):
        while self.is_judging_success_while:
            try:
                if "check_ok" in self.driver.current_url:
                    self.is_judging_success = True; 
                    self.is_judging_success_while = False;
                    self.is_while = False;
                    self.logger.debug(f"judging_success: success")
            except Exception as e:
                self.logger.error(f"judging_success error: {e}")
            
    def judgment_failed(self):
        while self.is_judgment_failed_while:
            try:
                element = self.driver.find_element_by_class_name('jconfirm-title')
                if element.text != '':
                    self.is_judgment_failed = True;
                    self.is_judgment_failed_while = False;
                    self.logger.debug(f"judgment_failed: {element.text}")
            except Exception as e:
                self.logger.error(f"judgment_failed error: {e}")

    def judgment_login(self):
        if "login" in self.driver.current_url:
            return False;
        else:
            return True;

    def action_login(self):
        self.driver.get(f"https://hehuanline.forest.gov.tw/user/?mode=login")

        # 帳號密碼的登入
        account_element = self.driver.find_element_by_xpath('//*[@id="is_uu"]')
        account_element.clear()
        account_element.send_keys(self.config.account)
        password_element = self.driver.find_element_by_xpath('//*[@id="is_pp"]')
        password_element.clear()
        password_element.send_keys(self.config.password)
        self.driver.find_element_by_xpath('//*[@id="login-form-submit"]').click()

        self.driver.get(r'https://hehuanline.forest.gov.tw/room/')
        return;

    def input_verify_code(self):
        verify_code_element = WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.ID, "verify_code")))
        verify_code_element.click();

        self.logger.debug(f"驗證碼解析");
        image_element = WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//img[@id="siimage"]')))
        while len(image_element.screenshot_as_png) < 800:
            self.logger.debug(f"len(image_element.screenshot_as_png): {len(image_element.screenshot_as_png)}");
            time.sleep(1)
        
        with open(self.commonUtility.captcha_path, 'wb') as file:
            file.write(image_element.screenshot_as_png)

        ocr = ddddocr.DdddOcr()
        with open(self.commonUtility.captcha_path, 'rb') as f:
            img_bytes = f.read()
        verify_code = ocr.classification(img_bytes)
        verify_code = ''.join(ch for ch in verify_code if ch.isalnum())

        if verify_code == '最澄碉':
            raise Exception('驗證碼無法載入，趕快重新再跑一次看看')

        verify_code_element.send_keys(verify_code)
        self.logger.debug(f"驗證碼:{verify_code}");

    def execution(self):
        now = datetime.now();
        open_date = datetime.strptime(f"{self.config.open_date}","%Y-%m-%d %H:%M:%S")
        while now < open_date:
            now = datetime.now();
            time.sleep(1);
        
        self.driver.implicitly_wait(1);
        self.driver.set_page_load_timeout(15);
        self.driver.set_script_timeout(15);

        while self.is_while:
            try:
                self.driver.get(f'https://hehuanline.forest.gov.tw/room/?mode=add&date_start={self.config.ticket_date}')

                while not self.judgment_login():
                    self.action_login();

                self.terminate_judging_flag();

                element = WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.NAME, f"num[{self.config.room_type}]")))
                select = Select(element)
                select.select_by_visible_text(f'{self.config.room_count}')
                select.select_by_value(f'{self.config.room_count}')

                self.driver.find_element(By.ID, "button_roomsubmit").click()

                self.input_verify_code();

                self.logger.debug(f"驗證用戶解析");
                recaptcha_response = ''
                while recaptcha_response == '':
                    recaptcha_response_element = self.driver.find_element_by_xpath('//*[@id="recaptchaResponse"]')
                    recaptcha_response = recaptcha_response_element.get_attribute('value');
                self.logger.debug(f"驗證用戶:{recaptcha_response}");

                self.logger.debug(f"update_button click");
                self.driver.find_element(By.CSS_SELECTOR, ".update_button").click()

                self.logger.debug(f"judging success/failed");

                self.is_judging_success_while = True;
                self.judging_success_thread = threading.Thread(target=self.judging_success)
                self.judging_success_thread.start()

                self.is_judgment_failed_while = True;
                self.judgment_failed_thread = threading.Thread(target=self.judgment_failed)
                self.judgment_failed_thread.start()

                self.logger.debug(f"wating result....");
                while self.is_judging_success == self.is_judgment_failed:
                    continue;
                self.logger.debug(f"success: {self.is_judging_success}、failed: {self.is_judgment_failed}");

                self.terminate_judging_flag();
                self.logger.debug(f"end....");
            except Exception as e:
                self.logger.error(f"is_while error: {e}")
                self.logger.error(traceback.format_exc())
                self.terminate_judging_flag();
                time.sleep(1);