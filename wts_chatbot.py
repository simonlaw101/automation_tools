import re
import time
import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

#Setting
default_receiver = 'Mum'
refresh_interval = 0.5
enable_emoji = True

wts_url = 'https://web.whatsapp.com/'
input_box_xpath = '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]'
name_xpath = "//span[@title='{}']"
msg_div_class = 'message-in'
msg_span_class = 'invisible-space'

ai_url = 'https://www.eviebot.com/en/'
ai_input_xpath = '//*[@id="avatarform"]/input[1]'
ai_reply_xpath = '//*[@id="line1"]/span'
ai_reply_refresh = 0.5

emojis = ['(y)','(n)',':-)',':-(',':-p',':-|',':-\\',':-D',':-*','<3','^_^','>_<',';-)']
emoji_keywords = {'yes':0,
                  'good':0,
                  'okay':0,
                  'agree':0,
                  'no':1,
                  'nope':1,
                  "you don't":1,
                  'smile':2,
                  'smiling':2,
                  "i don't know":3,
                  "i can't":3,
                  'i hope not':3,
                  'sad':3,
                  'unhappy':3,
                  'die':3,
                  'why not':4,
                  'joke':4,
                  'hate':5,
                  'boring':5,
                  'annoying':6,
                  'annoy':6,
                  'rude':6,
                  'damnit':6,
                  'damit':6,
                  'stop':6,
                  'lying':6,
                  'happy':7,
                  'interesting':7,
                  'fine':7,
                  'positive':7,
                  'kiss':8,
                  'kisses':8,
                  'beautiful':8,
                  'favorite':9,
                  'girl':9,
                  'love':9,
                  'thank you':10,
                  'nice':10,
                  'fun':10,
                  'friend':10,
                  'friends':10,
                  'ha':11,
                  'haha':11,
                  'hahaha':11,
                  'hilarious':11,
                  'cool':12,
                  'come on':12,
                  'bye':12}
'''
thumbs up: 0
thumbs down: 1
slight smile: 2
unhappy smile: 3
stuck-out tongue: 4
indifferent: 5
annoyed: 6
happy: 7
kiss: 8
red heart: 9
happy smiling eye: 10
laugh: 11
blink eye: 12
'''

#Load WhatsApp and AI page
driver = webdriver.Chrome()
driver.get(wts_url)
driver.execute_script("window.open('{}', 'new');".format(ai_url))
driver.switch_to.window(driver.window_handles[0])

#Scan QR code
name_input = input("(1) Scan QR code\n(2) Input receiver's name (default: {}): ".format(default_receiver))
if name_input=='':
    name_input = default_receiver
try:
    name = driver.find_element_by_xpath(name_xpath.format(name_input))
except NoSuchElementException:
    name = driver.find_element_by_xpath(name_xpath.format(default_receiver))
name.click()
confirm_input = input("(3) Confirm receiver's name and press enter to start chatbot\n")

#Main function
def send_wts(msg):
    global driver
    input_box = driver.find_element_by_xpath(input_box_xpath)
    if enable_emoji:
        input_box.send_keys(msg+add_emoji(msg)+'\n')
    else:
        input_box.send_keys(msg+'\n')

def has_new_msg():
    global driver, last_msg
    cur_time = datetime.datetime.now().strftime("%H:%M:%S")
    new_msg = get_new_msg()
    if new_msg != last_msg:
        last_msg = new_msg
        print(cur_time,new_msg)
        return True
    print(cur_time)
    return False

def get_new_msg():
    global driver
    new_msg_elements = driver.find_elements_by_class_name(msg_div_class)
    if len(new_msg_elements)>0:
        new_msg_span = new_msg_elements[-1].find_element_by_class_name(msg_span_class)
        return new_msg_span.text
    return ''

def get_ai_msg(msg):
    global driver
    driver.switch_to.window(driver.window_handles[1])
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
    driver.switch_to.window(driver.window_handles[0])
    return last_reply

def add_emoji(msg):
    for emoji_keyword in emoji_keywords:
        if has_word(emoji_keyword,msg):
            return ' '+emojis[emoji_keywords[emoji_keyword]]
    return ''

def has_word(word, sentence):
    return re.compile(r'\b({0})\b'.format(word), flags=re.IGNORECASE).search(sentence)!=None

#Start chatbot    
last_msg = get_new_msg()
while True:
    if has_new_msg() and last_msg!='':
        send_wts(get_ai_msg(last_msg))
    time.sleep(refresh_interval)
