from gravel import readyaml
from gravel.ios import DriverClient
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from appium.webdriver.common.appiumby import AppiumBy
from typing import Dict, NoReturn, Tuple, List, Union, Optional
import time

LAST_WEBVIEW = ''
WINDOW_SIZE = ''
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
                            input_box = self.find_element_in_all_webview(block_name, title, k, 'input')
                            self.clear_box(input_box, block_name, title, k)
                            self.send_keys(input_box, input_text)
                            self.swith_to_native()
                        if m == 'type':
                            input_box = self.find_element_by_type(block_name, title, k, 'input')
                            self.clear_box(input_box, block_name, title, k)
                            self.send_keys(input_box, input_text)
                if j == 'click':
                    print(self.yaml_path[block_name][title][k]['click']['desc'])
                    for m in self.yaml_path[block_name][title][k]['click']:
                        if m == 'ios-class-chain':
                            click_btn = self.find_element(('ioscc', self.yaml_path[block_name][title][k]['click']['ios-class-chain']))
                            click_btn.click()
                        if m == 'webview_xpath':
                            click_btn = self.find_element_in_all_webview(block_name, title, k, 'click')
                            click_btn.click()
                            self.swith_to_native()
                        if m == 'type':
                            click_btn = self.find_element_by_type(block_name, title, k, 'click')
                            click_btn.click()
                if j == 'scroll':
                    print(self.yaml_path[block_name][title][k]['scroll']['desc'])
                    self.scroll_to_name(self.yaml_path[block_name][title][k]['scroll']['name'])
                if j == 'snapshot':
                    if self.yaml_path[block_name][k]['snapshot']['enable'] == 'yes':
                        print(self.yaml_path[block_name][title][k]['snapshot']['desc'])
                        pic_name = "~/sisyphus/pics" + block_name + "_" + title + ".png"
                        self.driver.get_screenshot_as_file(pic_name)
                if j == 'sleep':
                    sleep_second = int(self.yaml_path[block_name][title][k][j])
                    info = 'sleep ' + str(sleep_second) + ' seconds'
                    print(info)
                    time.sleep(sleep_second)
                if j == 'check':
                    print(self.yaml_path[block_name][title][k]['check']['desc'])
                    for m in self.yaml_path[block_name][title][k]['check']:
                        if m == 'ios-class-chain':
                            result = self.is_element_exist(('ioscc', self.yaml_path[block_name][title][k]['check']['ios-class-chain']))
                        if m == 'webview_xpath':
                            result = self.is_element_exist_in_all_webview(block_name, title, k, 'check')
                            self.swith_to_native()
                        if m == 'type':
                            result = self.is_type_element_exist_by_type(block_name, title, k, 'check')
                    print(result)
                    return result
                if j == 'check_disapear':
                    print(self.yaml_path[block_name][title][k]['check_disapear']['desc'])
                    for m in self.yaml_path[block_name][title][k]['check_disapear']:
                        if m == 'ios-class-chain':
                            result = self.is_element_not_exist(('ioscc', self.yaml_path[block_name][title][k]['check_disapear']['ios-class-chain']))
                        if m == 'webview_xpath':
                            result = self.is_element_not_exist_in_current_window(block_name, title, k, 'check_disapear')
                            self.swith_to_native()
                        if m == 'type':
                            result = self.is_type_element_not_exist_by_type(block_name, title, k, 'check_disapear')
                    print(result)
                    return result
            k = k + 1

    def find_element_in_all_webview(self, block_name, title, k, ele_type):
        global LAST_WEBVIEW
        global WINDOW_SIZE
        webview_type = 'XCUIElementTypeWebView'
        WebDriverWait(self.driver, 20, 1).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, webview_type)))
        contexts = self.driver.contexts
        value = self.yaml_path[block_name][title][k][ele_type]['webview_xpath']
        if LAST_WEBVIEW != '':
            print('Switch to webview last time: ' + LAST_WEBVIEW)
            self.driver.switch_to.context(LAST_WEBVIEW)
            if self.is_element_exist(('webview_xpath', value)):
                WINDOW_SIZE = len(contexts)
                return self.driver.find_element(By.XPATH, value)
            print('Element not found')
        for i in range(1, len(contexts)):
            print(contexts[i])
            print('Switch to all webview')
            print('Switch to ' + contexts[i])
            self.driver.switch_to.context(contexts[i])
            if self.is_element_exist(('webview_xpath', value)):
                LAST_WEBVIEW = contexts[i]
                WINDOW_SIZE = len(contexts)
                print('Find element in webview: ' + contexts[i])
                print('Latest webview renew to: ' + contexts[i])
                return self.driver.find_element(By.XPATH, value)
            print('Element not found')

    def is_element_exist_in_all_webview(self, block_name, title, k, ele_type):
        global LAST_WEBVIEW
        global WINDOW_SIZE
        webview_type = 'XCUIElementTypeWebView'
        WebDriverWait(self.driver, 20, 1).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, webview_type)))
        contexts = self.driver.contexts
        value = self.yaml_path[block_name][title][k][ele_type]['webview_xpath']
        if LAST_WEBVIEW != '':
            print('Switch to webview last time: ' + LAST_WEBVIEW)
            self.driver.switch_to.context(LAST_WEBVIEW)
            if self.is_element_exist(('webview_xpath', value)):
                return True
            print('Element not found')
        for i in range(1, len(contexts)):
            print(contexts[i])
            print('Switch to all webview')
            print('Switch to ' + contexts[i])
            self.driver.switch_to.context(contexts[i])
            if self.is_element_exist(('webview_xpath', value)):
                WINDOW_SIZE = len(contexts)
                LAST_WEBVIEW = contexts[i]
                print('Find element in webview: ' + contexts[i])
                print('Latest webview renew to: ' + contexts[i])
                return True
            print('Element not found')
            return False

    def is_element_not_exist_in_current_window(self, block_name, title, k, ele_type):
        global LAST_WINDOW
        global WINDOW_SIZE
        if self.is_new_window_not_exist():
            print('No webview in current page')
            return True
        contexts = self.driver.contexts
        origin_len = WINDOW_SIZE
        value = self.yaml_path[block_name][title][k][ele_type]['webview_xpath']
        if self.is_new_window_open(contexts, origin_len):
            WINDOW_SIZE = len(contexts)
            print('New window opened')
            return True
        else:
            print('Still in the same page, Switch to window last time ' + LAST_WINDOW)
            self.driver.switch_to.window(LAST_WINDOW)
            if self.is_element_not_exist(('webview_xpath', value)):
                print('Element not found')
                return True
            else:
                print('Element still exist')
                return False

    def clear_box(self, element, block_name, title, k):
        back_count = 0
        for m in self.yaml_path[block_name][title][k]['input']:
            if m == 'backspace':
                back_count = int(self.yaml_path[block_name][title][k]['input']['backspace'])
        element.send_keys(back_count * Keys.BACKSPACE)

    def send_keys(self, element, value):
        element.send_keys(value)
        if self.is_element_exist(('xpath', '//XCUIElementTypeButton[@name="Done"]')):
            done_btn = self.find_element(('xpath', '//XCUIElementTypeButton[@name="Done"]'))
            done_btn.click()

    def scroll_exist(self, value):
        try:
            WebDriverWait(self.driver, 3, 1).until(expected_conditions.visibility_of_element_located((By.NAME, value)))
        except:
            return False
        return True

    def scroll_to_name(self, name):
        found = False
        while not found:
            if not self.scroll_exist(name):
                self.driver.swipe(150, 400, 150, 200, 1000)
            else:
                found = True

    def find_element_by_type(self, block_name, title, k, ele_action):
        element_type = self.yaml_path[block_name][title][k][ele_action]['type']
        WebDriverWait(self.driver, 10, 2).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, element_type)))
        for l in self.yaml_path[block_name][title][k][ele_action]:
            if l == 'value' or l == 'name':
                att_type = l
                att_compare = self.yaml_path[block_name][title][k][ele_action][l]
        type_elements = self.find_element(('class', element_type))
        for element in type_elements:
            if element.get_attribute(att_type) == att_compare:
                return element

    def is_type_element_exist_by_type(self, block_name, title, k, ele_action):
        element_type = self.yaml_path[block_name][title][k][ele_action]['type']
        for l in self.yaml_path[block_name][title][k][ele_action]:
            if l == 'value' or l == 'name':
                att_type = l
                att_compare = self.yaml_path[block_name][title][k][ele_action][l]
        type_elements = self.find_element(('class', element_type))
        for element in type_elements:
            if element.get_attribute(att_type) == att_compare:
                return True
        return False

    def is_type_element_not_exist_by_type(self, block_name, title, k, ele_action):
        element_type = self.yaml_path[block_name][title][k][ele_action]['type']
        for l in self.yaml_path[block_name][title][k][ele_action]:
            if l == 'value' or l == 'name':
                att_type = l
                att_compare = self.yaml_path[block_name][title][k][ele_action][l]
        type_elements = self.find_element(('class', element_type))
        for element in type_elements:
            if element.get_attribute(att_type) == att_compare:
                return False
        return True

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

    def swith_to_native(self):
        contexts = self.driver.contexts
        self.driver.switch_to.context(contexts[0])

    def is_element_not_exist(self, element: Tuple[str, Union[str, Dict]], wait_seconds: int = 20) -> bool:
        by = element[0]
        value = element[1]
        try:
            if by == "id":
                WebDriverWait(self.driver, wait_seconds, 1).until(expected_conditions.invisibility_of_element_located((By.ID, value)))
            elif by == "name":
                WebDriverWait(self.driver, wait_seconds, 1).until(expected_conditions.invisibility_of_element_located((By.NAME, value)))
            elif by == "class":
                WebDriverWait(self.driver, wait_seconds, 1).until(expected_conditions.invisibility_of_element_located((By.CLASS_NAME, value)))
            elif by == "text":
                WebDriverWait(self.driver, wait_seconds, 1).until(expected_conditions.invisibility_of_element_located((By.LINK_TEXT, value)))
            elif by == "partial_text":
                WebDriverWait(self.driver, wait_seconds, 1).until(expected_conditions.invisibility_of_element_located((By.PARTIAL_LINK_TEXT, value)))
            elif by == "xpath":
                WebDriverWait(self.driver, wait_seconds, 1).until(expected_conditions.invisibility_of_element_located((By.XPATH, value)))
            elif by == "webview_xpath":
                WebDriverWait(self.driver, wait_seconds, 1).until(expected_conditions.invisibility_of_element_located((By.XPATH, value)))
            elif by == "css":
                WebDriverWait(self.driver, wait_seconds, 1).until(expected_conditions.invisibility_of_element_located((By.CSS_SELECTOR, value)))
            elif by == "tag":
                WebDriverWait(self.driver, wait_seconds, 1).until(expected_conditions.invisibility_of_element_located((By.TAG_NAME, value)))
            elif by == "ioscc":
                WebDriverWait(self.driver, wait_seconds, 1).until(expected_conditions.invisibility_of_element_located((AppiumBy.IOS_CLASS_CHAIN, value)))
            else:
                raise NameError("Please enter the correct targeting elements,'id','name','class','text','xpath','css','ioscc'.")
        except Exception:
            return False
        return True

    def is_new_window_open(self, contexts, origin_len) -> bool:
        if len(contexts) > origin_len:
            return True
        else:
            return False

    def is_new_window_not_exist(self) -> bool:
        if self.is_element_not_exist(('class', 'XCUIElementTypeWebView')):
            return True
        else:
            return False
