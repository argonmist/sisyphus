from gravel import readyaml
from gravel.ios import DriverClient
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from appium.webdriver.common.appiumby import AppiumBy
from typing import Dict, NoReturn, Tuple, List, Union, Optional
import time

class pebble:

    def __init__(self):
        self.driver = DriverClient().getDriver()
        self.settings = readyaml.read('ios.yaml')
        self.yaml_path = readyaml.read(self.settings['pathFile'])

    def push(self, steps: Tuple[str, Union[str, Dict]]):
        block_name = steps[0]
        index = steps[1]
        title = 'step' + str(index)
        k = 0
        for i in self.yaml_path[block_name][title]: 
            for j in i:
                if j == 'input':
                    print(self.yaml_path[block_name][title][k]['input']['desc'])
                    input_text = self.yaml_path[block_name][title][k]['input']['text']
                    for m in self.yaml_path[block_name][title][k]['input']:
                        if m == 'ios-class-chain':
                            input_box = self.find_element(('ioscc', self.yaml_path[block_name][title][k]['input']['ios-class-chain']))
                            self.clear_box(input_box, block_name, title, k)
                            self.send_keys(input_box, input_text)
                        if m == 'webview_xpath':
                            self.auto_webview()
                            input_box = self.find_element(('xpath', self.yaml_path[block_name][title][k]['input']['webview_xapth']))
                            self.clear_box(input_box, block_name, title, k)
                            self.send_keys(input_box, input_text)
                            self.swith_to_native()
                        if m == 'type':
                            input_box = self.find_element_by_type(block_name, title, k, 'input')
                            self.clear_box(input_box, block_name, title, k)
                            self.send_keys(input_box, input_text)
     
    def clear_box(self, element, block_name, title, k):
        back_count = 0
        for m in self.yaml_path[block_name][title][k]['input']:
            if m == 'backspace':
                back_count = int(self.yaml_path[block_name][title][k]['input']['backspace'])
        element.send_keys(back_count * Keys.BACKSPACE)

    def send_keys(self, element, value):
        element.send_keys(value)
        done_btn = self.find_element(('xpath', '//XCUIElementTypeButton[@name="Done"]'))
        done_btn.click()

    def scroll_exist(self, value):
        try:
            WebDriverWait(self.driver, 3, 1).until(expected_conditions.visibility_of_element_located((By.NAME, value)))
        except:
            return False
        return True

    def scroll_to_text(self, name):
        found = False
        while not found:
            if not self.scroll_exist(name):
                self.driver.swipe(150, 400, 150, 200, 1000)
            else:
                found = True

    def find_element_by_type(self, block_name, title, k, ele_action):
        element_type = self.yaml_path[block_name][title][k][ele_action]['type']
        print(element_type)
        WebDriverWait(self.driver, 10, 2).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, element_type)))
        for l in self.yaml_path[block_name][title][k][ele_action]:
            print(l)
            if l == 'value' or l == 'name':
                att_type = l
                att_compare = self.yaml_path[block_name][title][k][ele_action][l]
        type_elements = self.find_element(('class', element_type))
        print(att_type)
        for element in type_elements:
            print(element.get_attribute(att_type))
            if element.get_attribute(att_type) == att_compare:
                return element

    def find_element(self, element: Tuple[str, Union[str, Dict]]):
        by = element[0]
        value = element[1]
        try:
            if self.is_element_exist(element):
                if by == "id":
                    return self.driver.find_element(By.ID, value)
                elif by == "name":
                    return self.driver.find_element(By.NAME, value)
                elif by == "class":
                    return self.driver.find_elements(By.CLASS_NAME, value)
                elif by == "text":
                    return self.driver.find_element(By.LINK_TEXT, value)
                elif by == "partial_text":
                    return self.driver.find_element(By.PARTIAL_LINK_TEXT, value)
                elif by == "xpath":
                    return self.driver.find_element(By.XPATH, value)
                elif by == "webview_xpath":
                    return self.driver.find_element(By.XPATH, value)
                elif by == "css":
                    return self.driver.find_element(By.CSS_SELECTOR, value)
                elif by == "tag":
                    return self.driver.find_element(By.TAG_NAME, value)
                elif by == "ioscc":
                    return self.driver.find_element(AppiumBy.IOS_CLASS_CHAIN, value)
                else:
                    raise NameError("Please enter the correct targeting elements,'id','name','class','text','xpath','css','ioscc'.")
        except Exception as e:
            logger.error(">>>>>>>> failed to find element: %s is %s. Error: %s" % (by, value, e))

    def is_element_exist(self, element: Tuple[str, Union[str, Dict]], wait_seconds: int = 20) -> bool:
        by = element[0]
        value = element[1]
        try:
            if by == "id":
                WebDriverWait(self.driver, wait_seconds, 1).until(expected_conditions.presence_of_element_located((By.ID, value)))
            elif by == "name":
                WebDriverWait(self.driver, wait_seconds, 1).until(expected_conditions.presence_of_element_located((By.NAME, value)))
            elif by == "class":
                WebDriverWait(self.driver, wait_seconds, 1).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, value)))
            elif by == "text":
                WebDriverWait(self.driver, wait_seconds, 1).until(expected_conditions.presence_of_element_located((By.LINK_TEXT, value)))
            elif by == "partial_text":
                WebDriverWait(self.driver, wait_seconds, 1).until(expected_conditions.presence_of_element_located((By.PARTIAL_LINK_TEXT, value)))
            elif by == "xpath":
                WebDriverWait(self.driver, wait_seconds, 1).until(expected_conditions.presence_of_element_located((By.XPATH, value)))
            elif by == "webview_xpath":
                WebDriverWait(self.driver, wait_seconds, 1).until(expected_conditions.presence_of_element_located((By.XPATH, value)))
            elif by == "css":
                WebDriverWait(self.driver, wait_seconds, 1).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, value)))
            elif by == "tag":
                WebDriverWait(self.driver, wait_seconds, 1).until(expected_conditions.presence_of_element_located((By.TAG_NAME, value)))
            elif by == "ioscc":
                WebDriverWait(self.driver, wait_seconds, 1).until(expected_conditions.presence_of_element_located((AppiumBy.IOS_CLASS_CHAIN, value)))
            else:
                raise NameError("Please enter the correct targeting elements,'id','name','class','text','xpath','css','ioscc'.")
        except Exception:
            return False
        return True

    def auto_webview(self):
        contexts = self.driver.contexts
        last_index = len(contexts) - 1
        self.driver.switch_to.context(contexts[last_index])

    def swith_to_native(self):
        contexts = self.driver.contexts
        self.driver.switch_to.context(contexts[0])
