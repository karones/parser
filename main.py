import telebot
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.chrome.options import Options 

bot = telebot.TeleBot('1605853735:AAGYGN3uWIGJO4MY3vCTMX1qnAjNL80U8UY')

week_name = 0
group_name = '0'
count = 0

def get_rez(week_name, group_name, message):
    global count
    if count == 1:
        week_name = week_name+1
        link = f'https://www.polessu.by/ruz/term2/?q={group_name}'
        option = webdriver.ChromeOptions()
        GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
        CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
        option.add_argument('headless')
        option.add_argument('--disable-gpu')
        option.add_argument('--no-sandbox')
        browser = webdriver.Chrome(execution_path=CHROMEDRIVER_PATH, options=option)
        browser.get(link)
        browser.set_window_size(1000,1200)
        browser.find_element_by_xpath('/html/body/section/div/div/div[2]/div/button').click()
        browser.find_element_by_xpath(f'//*[@id="weeks-menu"]/li[{week_name}]/a').click()
        with open('page.txt', 'w') as f:
            f.write(browser.page_source)
            screenshot = browser.save_screenshot("my_screenshot.png")
        browser.quit()
        count = 0
        bot.send_photo(message.chat.id, open('/home/jabka/parser/my_screenshot.png', 'rb'))
        message.text = ''
        bot.register_next_step_handler(message, start_message)

@bot.message_handler(commands=['start'])
def start_message(message):
    global count 
    count = 1
    bot.send_message(message.chat.id, 'Hi! Enter group or week(1-18)')
    bot.register_next_step_handler(message, get_message)

def get_message(message):
    global week_name
    global group_name
    if week_name == 0 or group_name == '0':
        try:
            week_name = int(message.text)
            bot.register_next_step_handler(message, get_message)
        except Exception:
            group_name = message.text
            bot.register_next_step_handler(message, get_message)
    if week_name != 0 and group_name != '0':
        get_rez(week_name, group_name, message)
        week_name = 0 
        group_name = 0
bot.polling(none_stop=True, interval=0)
