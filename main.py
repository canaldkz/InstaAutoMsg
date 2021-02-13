from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import random
import pickle
import random
import user_data as udata


class InstaSamka():
    def __init__(self):
        super().__init__()
        self.URL = 'https://instagram.com'
        self.msg_text_list = ['Мм)','Аа)','Хах','лол','Дадааа)','лол)']
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 YaBrowser/20.12.3.138 Yowser/2.5 Safari/537.36')
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        #self.options.add_argument('--headless')
        self.browser = webdriver.Chrome(r'./chromedriver/chromedriver.exe',options=self.options)

    def start(self):
        self.browser.get(self.URL)
        user_list = udata.get_user_list()
        print('Сохраненные пользователи:')
        for user in user_list:
            print(f'{user_list.index(user)} - {user}')
        print('new - Новый пользователь')
        uid = input('ID> ')
        if uid == 'new':
            username = input('username>')
            password = input('password>')
            self.login(username, password)
        elif type(uid) == type(int(uid)):
            print(f'Выбран {user_list[int(uid)]}')
            for cookie in udata.get_cookies(user_list[uid]):
                self.browser.add_cookie(cookie)
        self.browser.refresh()
        time.sleep(5)
        self.browser.find_element_by_xpath('//button[text()="Не сейчас"]').click()

    def login(self, username, password):
        self.browser.get(self.URL)
        time.sleep(5)
        username_field = self.browser.find_element_by_name('username')
        username_field.clear()
        username_field.send_keys(username)
        time.sleep(1)
        passw_field = self.browser.find_element_by_name('password')
        passw_field.clear()
        passw_field.send_keys(password)
        time.sleep(1)
        passw_field.send_keys(Keys.ENTER)
        time.sleep(5)
        udata.save_cookies(self.browser.get_cookies(),username)
        
    def send_msg(self,target_names):
        self.browser.get(self.URL+'/direct/inbox/')
        time.sleep(5)
        for target_name in target_names:
            chat = self.browser.find_element_by_xpath(f'//div[text() = "{target_name}"]').click()
            time.sleep(1)
            text_area = self.browser.find_element_by_xpath('//textarea[@placeholder="Напишите сообщение..."]')
            random_msg = random.choice(self.msg_text_list)
            text_area.send_keys(f'{random_msg}')
            text_area.send_keys(Keys.ENTER)
            print(f'Сообщение "{random_msg}" отправлено {target_name}!')
            time.sleep(1.5)
        
    def check_msg(self):
        print('Проверка новых сообщений...')
        self.browser.get(self.URL+'/direct/inbox/')
        time.sleep(5)
        unread_list = self.browser.find_elements_by_xpath('//div[@style= "height: 8px; width: 8px;"]/../../div[2]/div/div/div/div/div')
        print(f'Новые сообщения от {len(unread_list)} людей')
        user_list = []
        for user in unread_list:
            user_list.append(user.get_attribute('innerHTML'))
        if len(user_list) == 0:
            print('Ничего не найдено')
            raise IndexError
        else:
            return user_list
        #print(unread_list)

    def automsg(self):
        try:
            send_msg(check_msg())
        except IndexError:
            pass
        finally:
            print('фсё')
            
    def shutdown(self):
        self.browser.close()
        self.browser.quit()

if __name__ == '__main__':
    app = InstaSamka()
    app.start()
