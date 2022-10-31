import logging
from use_mixed import Bot
from selenium import webdriver
from config import Config
from component.driver_tools import DriverTools

if __name__ == "__main__":
    config = Config();
    config.account = "*********"
    config.password = "*********"
    config.ticket_date = "2022-09-21"
    config.open_date = "2022-08-23 07:50:00";
    config.room_type = '212'
    config.ticket_numbers = '2'

    driver_tools = DriverTools();
    driver = webdriver.Chrome(
        executable_path=r'C:\Projects\ATK_TicketBots\Source\TicketBots.Python\driver\chromedriver.exe', 
        service_log_path=rf'{config.log_root_path()}\service.txt',
        chrome_options=driver_tools.get_chrome_options());
    
    logging.basicConfig(filename=f'{config.log_root_path()}\\common.txt', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    logging.debug("--------------------------------------開始--------------------------------------")
    bot = Bot(config, driver);
    bot.execution();
    logging.debug("--------------------------------------結束--------------------------------------");
