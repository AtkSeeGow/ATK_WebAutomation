import logging
import threading
import traceback
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from component.browser_utility import BrowserUtility
from component.common_utility import CommonUtility
from redmine.config import Config

class Bot():
    def __init__(self):
        self.config = Config();

        browser_utility = CommonUtility();
        log_path = browser_utility.log_path;

        browser_utility = BrowserUtility();
        chrome_options = browser_utility.get_chrome_options();
        executable_path = browser_utility.executable_path;
        self.driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options);

        fileHandler = logging.FileHandler(log_path, mode='a')
        fileHandler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'));
        self.logger = logging.getLogger("Bot");
        self.logger.addHandler(fileHandler);

    def execution(self):
        self.driver.implicitly_wait(5);
        self.driver.set_page_load_timeout(15);
        self.driver.set_script_timeout(15);

        self.driver.get(f"https://angelia.citystate.com.tw/login")

        # 帳號密碼的登入
        account_element = self.driver.find_element_by_xpath('//*[@id="username"]')
        account_element.clear()
        account_element.send_keys(self.config.account)
        password_element = self.driver.find_element_by_xpath('//*[@id="password"]')
        password_element.clear()
        password_element.send_keys(self.config.password)
        self.driver.find_element_by_xpath('//*[@id="login-submit"]').click()

        # 讀取要建立資料清單(主旨、工時、日期、分類、標籤)
        with open(self.config.csv_path, newline='', encoding="utf-8") as csv_file:
            rows = csv.reader(csv_file)
            for row in rows:
                try:
                    self.driver.get(f'https://angelia.citystate.com.tw/projects/pscs-2019-operation-management-project/issues/new')
                    
                    # 主旨
                    element = self.driver.find_element_by_xpath('//*[@id="issue_subject"]')
                    element.clear()
                    element.send_keys(row[0])

                    # 狀態
                    element = WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.NAME, f"issue[status_id]")))
                    select = Select(element)
                    select.select_by_visible_text(f'已解決')

                    # 被分派者
                    time.sleep(2)
                    element = WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.NAME, f"issue[assigned_to_id]")))
                    select = Select(element)
                    select.select_by_visible_text(f'Webster Chen')

                    # 開始日期
                    element = self.driver.find_element_by_xpath('//*[@id="issue_start_date"]')
                    element.clear()
                    element.send_keys(row[2])
                    element.send_keys('\t')
                    element.send_keys(row[3])
                    element.send_keys(row[4])

                    # 完成日期
                    element = self.driver.find_element_by_xpath('//*[@id="issue_due_date"]')
                    element.clear()
                    element.send_keys(row[2])
                    element.send_keys('\t')
                    element.send_keys(row[3])
                    element.send_keys(row[4])

                    # 分類
                    element = WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.NAME, f"issue[category_id]")))
                    select = Select(element)
                    select.select_by_visible_text(row[5])

                    # 預估工時
                    element = self.driver.find_element_by_xpath('//*[@id="issue_estimated_hours"]')
                    element.clear()
                    element.send_keys(row[1])

                    # 標籤
                    if row[6] != '':
                        element = self.driver.find_element_by_xpath('//*[@id="issue_tags"]/span/span[1]/span/ul/li/input')
                        element.clear()
                        element.send_keys(row[6])
                        time.sleep(1)
                        element = self.driver.find_element_by_xpath('//*[@id="select2-issue_tag_list-results"]/li')
                        element.click()

                    # 完成度
                    element = WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.NAME, 'issue[done_ratio]')))
                    select = Select(element)
                    select.select_by_value('100')

                    # 建立
                    element = self.driver.find_element_by_xpath('//*[@id="issue-form"]/input[3]')
                    element.click()

                    # 記錄時間
                    element = self.driver.find_element_by_xpath('//*[@id="content"]/div[2]/a[2]')
                    element.click()

                    # 日期
                    element = self.driver.find_element_by_xpath('//*[@id="time_entry_spent_on"]')
                    element.clear()
                    element.send_keys(row[2])
                    element.send_keys('\t')
                    element.send_keys(row[3])
                    element.send_keys(row[4])

                    # 小時
                    element = self.driver.find_element_by_xpath('//*[@id="time_entry_hours"]')
                    element.clear()
                    element.send_keys(row[1])

                    # 活動
                    element = WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.NAME, 'time_entry[activity_id]')))
                    select = Select(element)
                    select.select_by_visible_text('Support')

                    # 建立
                    element = self.driver.find_element_by_xpath('//*[@id="new_time_entry"]/input[4]')
                    element.click()

                    time.sleep(1);
                except Exception as e:
                    self.logger.error(f"{e}")
                    self.logger.error(traceback.format_exc())