from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import quopri


class Bot:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.message = "Esta é uma mensagem de teste para o programa. Vamos ver se funciona"
        self.name_list = []
        self.temp_list = []
        self.utf_list = []
        self.specials_list = []
        self.specials_str = []
        self.encoded_list = []
        self.encoded_name = ""

        with open('contacts.vcf', 'r', encoding="utf-8") as name_file:
            for line in name_file:            
                self.temp_list.append(line.strip())

        for i in range(0, len(self.temp_list)):
            if self.temp_list[i].find("FN:") == 0:
                self.name_list.append(self.temp_list[i].replace("FN:",""))
            elif self.temp_list[i].find("FN;") == 0:
                self.utf_list.append(self.temp_list[i].replace("FN;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:", ""))
                if self.temp_list[i][-1] == '=':
                    
                    self.encoded_list.append(self.temp_list[i])
                    self.encoded_list.append(self.temp_list[i+1])
                    self.encoded_list[-1] = self.encoded_list[-1][1::]
                    self.encoded_name = (''.join(self.encoded_list)).replace("FN;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:", "")
                    self.specials_str.append((quopri.decodestring(self.encoded_name)).decode('utf-8'))
                    self.encoded_name = ""
                    self.encoded_list = []
                else:
                    self.specials_str.append((quopri.decodestring(self.utf_list[-1])).decode('utf-8'))
                for j in range (0, len(self.specials_str[-1])):
                    self.specials_list.append(self.specials_str[-1][j])
                if self.specials_str[-1][-1] == '️':
                    del self.specials_list[-1]
                self.name = ''.join(map(str, self.specials_list))
                self.name_list.append(self.name)
                self.specials_list = []
                self.specials_str = []
                self.name = ""
                self.utf_list = []
            elif self.temp_list[i].find("FN_GROUP:") == 0:
                self.name_list.append(self.temp_list[i].replace("FN_GROUP:", ""))
                self.specials_str.append((quopri.decodestring(self.name_list[-1])).decode('utf-8'))
    def send_message(self):
        self.driver.get('https://web.whatsapp.com/')
        time.sleep(15)
        # <span dir="auto" title="Sara" class="_19RFN _1ovWX _F7Vk">Sara</span>
        for name in self.name_list:
            name = self.driver.find_element_by_xpath(f'//*[@title="{name}"]')
            name.click()
            time.sleep(1)
            chat_box = self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]')
            chat_box.click()
            time.sleep(1)
            chat_box.send_keys(self.message)
            time.sleep(2)
            # send_button = self.driver.find_element_by_xpath('//*[@data-icon="send"]') 
            send_button = self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[3]/button')
            # send_button.click()
            time.sleep(1)
        time.sleep(2)
        options = self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/header/div[2]/div/span/div[3]/div')
        options.click()
        exit_button = self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/header/div[2]/div/span/div[3]/span/div/ul/li[6]')
        exit_button.click()
        


bot = Bot()
bot.send_message()