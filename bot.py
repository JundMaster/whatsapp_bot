from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import quopri


class Bot:
    def __init__(self):
        self.driver = webdriver.Firefox()
        # message to be sent
        self.message = "Esta é uma mensagem de teste para o programa. Vamos ver se funciona"
        # list that will contain the contacts/groups
        self.name_list = []
        self.temp_list = []
        self.utf_list = []
        self.specials_list = []
        self.specials_str = []
        self.encoded_list = []
        self.encoded_name = ""

        # opens the file with the contact/group's names in it
        with open('contacts.vcf', 'r') as name_file:
            for line in name_file:
                # appends the lines (without the '\n' character) to a temporary list          
                self.temp_list.append(line.strip())

        for i in range(0, len(self.temp_list)):
            if self.temp_list[i].find("FN:") == 0:
                self.name_list.append(self.temp_list[i].replace("FN:",""))
            elif self.temp_list[i].find("FN;") == 0:
                if self.temp_list[i][-1] == '=':
                    
                    self.encoded_list.append(self.temp_list[i])
                    self.encoded_list.append(self.temp_list[i+1])
                    self.encoded_list[-1] = self.encoded_list[-1][1::]
                    self.encoded_name = (''.join(self.encoded_list)).replace("FN;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:", "")
                    self.specials_str.append((quopri.decodestring(self.encoded_name)).decode('utf-8'))
                    self.encoded_name = ""
                    self.encoded_list = []
                else:
                    self.utf_list.append(self.temp_list[i].replace("FN;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:", ""))
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
        # opens the Web Whatsapp
        self.driver.get('https://web.whatsapp.com/')
        # waits for 15 seconds, before executing the next instructions
        time.sleep(15)
        # reads the list of contacts/groups one by one
        for name in self.name_list:
            search_box = self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/div[1]/div/label/input')
            search_box.click()
            search_box.send_keys(f'{name}')
            name = self.driver.find_element_by_xpath(f'//*[@title="{name}"]')
            # opens the contact/group chat
            name.click()
            time.sleep(1)
            # looks for the chatbox
            chat_box = self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]')
            # clicks on chat box in order to write the message
            chat_box.click()
            time.sleep(1)
            # tipes the message in the chatbox
            chat_box.send_keys(self.message)
            time.sleep(2)
            # looks for the send button 
            send_button = self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[3]/button')
            # send the message
            send_button.click()
            time.sleep(2)
            # in case the bot doesn't find the button to close the search tab, it should continue
            # and if the send button is clicked, i'll never find this one
            try:
                close_search = self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/div[1]/div/span/button')
                close_search.click()
            except:
                continue
            time.sleep(1)
        time.sleep(2)
        # looks for the option button and then the exit button to make the logout
        options = self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/header/div[2]/div/span/div[3]/div')
        options.click()
        exit_button = self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/header/div[2]/div/span/div[3]/span/div/ul/li[6]')
        exit_button.click()
        

# runs the bot
bot = Bot()
bot.send_message()