import time
import datetime
from selenium import webdriver

#Setting
ai_url = 'https://www.eviebot.com/en/'
ai_input_xpath = '//*[@id="avatarform"]/input[1]'
ai_reply_xpath = '//*[@id="line1"]/span'
ai_reply_refresh = 0.5

#Load AI page in background
option = webdriver.ChromeOptions()
option.add_argument('headless')
driver= webdriver.Chrome(options=option)
driver.get(ai_url)

#Main function
def get_ai_msg(msg):
    global driver
    ai_input = driver.find_element_by_xpath(ai_input_xpath)
    ai_input.send_keys(msg+'\n')
    last_reply = driver.find_element_by_xpath(ai_reply_xpath).text
    while True:
        time.sleep(ai_reply_refresh)
        ai_reply = driver.find_element_by_xpath(ai_reply_xpath).text
        if last_reply.strip()!='' and last_reply==ai_reply:
            break
        else:
            last_reply = ai_reply
    return last_reply

#Start chatbot
your_input = input('ChatBot start...\nType \"quit\" to stop the program\n\n')
while your_input!='quit':
    print('\n'+datetime.datetime.now().strftime("%H:%M:%S")+' You: '+your_input)
    print(datetime.datetime.now().strftime("%H:%M:%S")+'  AI: '+get_ai_msg(your_input)+'\n')
    your_input = input('')
driver.quit()
print('\nChatBot end\n')
