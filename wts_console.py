import re
import time
import datetime
import threading
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

#Setting
default_receiver = 'Mum'
refresh_interval = 0.5

wts_url = 'https://web.whatsapp.com/'
input_box_xpath = '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]'
name_xpath = "//span[@title='{}']"
msg_div_class = 'message-in'
msg_span_class = 'invisible-space'
name_div_class = 'copyable-text'

#Load WhatsApp
driver = webdriver.Chrome()
driver.get(wts_url)

#Scan QR code
name_input = input("(1) Scan QR code\n(2) Input receiver's name (default: {}): ".format(default_receiver))
if name_input=='':
    name_input = default_receiver
try:
    name = driver.find_element_by_xpath(name_xpath.format(name_input))
except NoSuchElementException:
    name = driver.find_element_by_xpath(name_xpath.format(default_receiver))
name.click()
confirm_input = input("(3) Confirm receiver's name and press enter to read message\n")

#Main function
def send_wts(msg):
    global driver
    input_box = driver.find_element_by_xpath(input_box_xpath)
    input_box.send_keys(msg+'\n')

def has_new_msg():
    global driver, last_msg
    new_msg = get_new_msg()
    if new_msg != last_msg:
        last_msg = new_msg
        return True
    return False

def get_new_msg():
    global driver
    try:
        new_msg_elements = driver.find_elements_by_class_name(msg_div_class)
        if len(new_msg_elements)>0:
            new_msg_span = new_msg_elements[-1].find_element_by_class_name(msg_span_class)
            name_div = new_msg_elements[-1].find_element_by_class_name(name_div_class).get_attribute('data-pre-plain-text')
            name = name_div[name_div.find(']')+2:]
            return name+new_msg_span.text
    except NoSuchElementException:
        pass
    return ''

def read_input():
    your_input = input('')
    while True:
        if your_input!='':
            send_wts(your_input)
            print(datetime.datetime.now().strftime("%H:%M:%S")+'\tYou: '+your_input)
        your_input = input('')

def read_msg():
    global last_msg
    while True:
        if has_new_msg() and last_msg!='':
            print(datetime.datetime.now().strftime("%H:%M:%S"), last_msg)
        time.sleep(refresh_interval)
    
#Start reading message and input
last_msg = get_new_msg()
t1 = threading.Thread(target=read_msg)
t2 = threading.Thread(target=read_input)

t1.start()
t2.start()
