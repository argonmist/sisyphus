from gravel import readyaml
from gravel.android import DriverClient
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from appium.webdriver.common.appiumby import AppiumBy
from typing import Dict, NoReturn, Tuple, List, Union, Optional
from loguru import logger
import time

LAST_WINDOW = ''
WINDOW_SIZE = 0
class rock:

    def __init__(self):
        self.driver = DriverClient().getDriver()
        self.settings = readyaml.read('android.yaml')
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
                        if m == 'xpath':
                            input_box = self.find_element(('xpath', self.yaml_path[block_name][title][k]['input']['xpath']))
                            self.send_keys(input_box, input_text)
                        if m == 'webview_xpath':
                            input_box = self.find_element_in_all_windows(block_name, title, k, 'input')
                            self.send_keys(input_box, input_text)
                            self.swith_to_native()
                        if m == 'class':
                            input_box = self.find_element_by_class(block_name, title, k, 'input')
                            self.send_keys(input_box, input_text)
                if j == 'click':
                    print(self.yaml_path[block_name][title][k]['click']['desc'])
                    for m in self.yaml_path[block_name][title][k]['click']:
                        if m == 'xpath':
                            click_btn = self.find_element(('xpath', self.yaml_path[block_name][title][k]['click']['xpath']))
                            click_btn.click()
                        if m == 'webview_xpath':
                            click_btn = self.find_element_in_all_windows(block_name, title, k, 'click')
                            click_btn.click()
                            self.swith_to_native()
                        if m == 'class':
                            click_btn = self.find_element_by_class(block_name, title, k, 'click')
                            click_btn.click()
                if j == 'scroll':
                    print(self.yaml_path[block_name][title][k]['scroll']['desc'])
                    self.scroll_to_text(self.yaml_path[block_name][k]['scroll']['text'])
                if j == 'snapshot':
                    if self.yaml_path[block_name][title][k]['snapshot']['enable'] == 'yes':
                        print(self.yaml_path[block_name][title][k]['snapshot']['desc'])
                        pic_name = block_name + "_" + title
                        self.save_screenshot(pic_name)
                if j == 'sleep':
                    sleep_second = int(self.yaml_path[block_name][title][k][j])
                    info = 'sleep ' + str(sleep_second) + ' seconds'
                    print(info)
                    time.sleep(sleep_second)
                if j == 'check':
                    print(self.yaml_path[block_name][title][k]['check']['desc'])
                    for m in self.yaml_path[block_name][title][k]['check']:
                        if m == 'xpath':
                            result = self.is_element_exist(('xpath', self.yaml_path[block_name][title][k]['check']['xpath']))
                        if m == 'webview_xpath':
                            result = self.is_element_exist_in_all_windows(block_name, title, k, 'check')
                            self.swith_to_native()
                        if m == 'class':
                            result = self.is_class_element_exist_by_class(block_name, title, k, 'check')
                    print(result)
                    return result
                if j == 'keyboard':
                    print(self.yaml_path[block_name][title][k]['keyboard']['desc'])
                    input_string = self.yaml_path[block_name][title][k]['keyboard']['text']
                    self.press_keyboard(input_string)
                if j == 'check_disapear':
                    print(self.yaml_path[block_name][title][k]['check_disapear']['desc'])
                    for m in self.yaml_path[block_name][title][k]['check_disapear']:
                        if m == 'xpath':
                            result = self.is_element_not_exist(('xpath', self.yaml_path[block_name][title][k]['check_disapear']['xpath']))
                        if m == 'webview_xpath':
                            result = self.is_element_not_exist_in_current_window(block_name, title, k, 'check_disapear')
                            self.swith_to_native()
                        if m == 'class':
                            result = self.is_class_element_not_exist_by_class(block_name, title, k, 'check_disapear')
                    print(result)
                    return result
            k = k + 1

    def save_screenshot(self, picture_name: str):
        picture_name = "/root/sisyphus/pics/" + picture_name + ".png"
        self.driver.get_screenshot_as_file(picture_name)

    def swith_to_native(self):
        contexts = self.driver.contexts
        self.driver.switch_to.context(contexts[0])

    def get_contexts(self):
        webview_class = 'android.webkit.WebView'
        WebDriverWait(self.driver, 20, 1).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, webview_class)))
        contexts = self.driver.contexts
        return contexts

    def get_all_window(self):
        contexts = self.get_contexts()
        context_name = contexts[1]
        self.driver.switch_to.context(context_name)
        window_handles = self.driver.window_handles
        return window_handles

    def find_element_in_all_windows(self, block_name, title, k, ele_type):
        global LAST_WINDOW
        global WINDOW_SIZE
        window_handles = self.get_all_window()
        value = self.yaml_path[block_name][title][k][ele_type]['webview_xpath']
        if LAST_WINDOW != '':
            print('Switch to window last time: ' + LAST_WINDOW)
            self.driver.switch_to.window(LAST_WINDOW)
            if not self.is_element_not_exist(('webview_xpath', value)):
                WINDOW_SIZE = len(window_handles)
                return self.driver.find_element(By.XPATH, value)
            print('Element not found')
        for i in window_handles:
            print('Switch to all windows')
            print('Switch to ' + i)
            self.driver.switch_to.window(i)
            if not self.is_element_not_exist(('webview_xpath', value)):
                LAST_WINDOW = i
                WINDOW_SIZE = len(window_handles)
                print('Find element in window: ' + i)
                print('Latest window renew to: ' + i)
                return self.driver.find_element(By.XPATH, value)
            print('Element not found')

    def is_element_exist_in_all_windows(self, block_name, title, k, ele_type):
        global LAST_WINDOW
        global WINDOW_SIZE
        window_handles = self.get_all_window()
        value = self.yaml_path[block_name][title][k][ele_type]['webview_xpath']
        if LAST_WINDOW != '':
            print('Switch to window last time ' + LAST_WINDOW)
            self.driver.switch_to.window(LAST_WINDOW)
            if self.is_element_exist(('webview_xpath', value)):
                WINDOW_SIZE = len(window_handles)
                return True
            print('Element not found')
        for i in window_handles:
            print('Switch to all windows')
            print('Switch to ' + i)
            self.driver.switch_to.window(i)
            if self.is_element_exist(('webview_xpath', value)):
                WINDOW_SIZE = len(window_handles)
                LAST_WINDOW = i
                print('Find element in window: ' + i)
                print('Latest window renew to: ' + i)
                print(LAST_WINDOW)
                return True
        print('Element not found')
        return False

    def is_element_not_exist_in_current_window(self, block_name, title, k, ele_type):
        global LAST_WINDOW
        global WINDOW_SIZE
        if self.is_new_window_not_exist():
            print('No webview in current page')
            return True
        window_handles = self.get_all_window()
        origin_len = WINDOW_SIZE
        value = self.yaml_path[block_name][title][k][ele_type]['webview_xpath']
        if self.is_new_window_open(window_handles, origin_len):
            WINDOW_SIZE = len(window_handles)
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

    def find_element_by_class(self, block_name, title, k, ele_action):
        class_type = self.yaml_path[block_name][title][k][ele_action]['class']
        for l in self.yaml_path[block_name][title][k][ele_action]:
            if l == 'class_text' or l == 'class_resource-id':
                att_type = l.strip('class_')
                att_compare = self.yaml_path[block_name][title][k][ele_action][l]                
        class_elements = self.find_element(('class', class_type))
        for element in class_elements:
            if element.get_attribute(att_type) == att_compare:
                return element

    def is_class_element_exist_by_class(self, block_name, title, k, ele_action):
        class_type = self.yaml_path[block_name][title][k][ele_action]['class']
        for l in self.yaml_path[block_name][title][k][ele_action]:
            if l == 'class_text' or l == 'class_resource-id':
                att_type = l.strip('class_')
                att_compare = self.yaml_path[block_name][title][k][ele_action][l]
        class_elements = self.find_element(('class', class_type))
        for element in class_elements:
            if element.get_attribute(att_type) == att_compare:
                return True
        return False
   
    def is_class_element_not_exist_by_class(self, block_name, title, k, ele_action):
        class_type = self.yaml_path[block_name][title][k][ele_action]['class']
        for l in self.yaml_path[block_name][title][k][ele_action]:
            if l == 'class_text' or l == 'class_resource-id':
                att_type = l.strip('class_')
                att_compare = self.yaml_path[block_name][title][k][ele_action][l]
        class_elements = self.find_element(('class', class_type))
        for element in class_elements:
            if element.get_attribute(att_type) == att_compare:
                print('Element still in the current page')
                return False
        print('Element not found')
        return True
                
    def get_current_window(self):
        self.get_all_window()
        return self.driver.current_window_handle

    def swith_to_current_window(self):
        current_window = self.get_current_window()
        print(current_window)
        self.driver.switch_to.window(current_window)

    def dump_current_window(self):
        web_static = open('current_window.html', 'w')
        web_static.write(self.driver.page_source)

    def send_keys(self, element, value):
        element.send_keys(value)

    def scroll_to_text(self, text):
        uiautomator_cmd = "new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView(new UiSelector().text(\"%s\").instance(0))" % text
        self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, uiautomator_cmd)

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
                else:
                    raise NameError("Please enter the correct targeting elements,'id','name','class','text','xpath','css'.")
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
            else:
                raise NameError("Please enter the correct targeting elements,'id','name','class','text','xpath','css'.")
        except Exception:
            return False
        return True

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
            else:
                raise NameError("Please enter the correct targeting elements,'id','name','class','text','xpath','css'.")
        except Exception:
            return False
        return True

    def is_new_window_open(self, window_handles, origin_len) -> bool:
        if len(window_handles) > origin_len:
            return True
        else:
            return False

    def is_new_window_not_exist(self) -> bool:
        if self.is_element_not_exist(('class', 'android.webkit.WebView')):
            return True
        else:
            return False

    def string_to_keycode(self, argument):
        switcher = {
            '0': 7,
            '1': 8,
            '2': 9,
            '3': 10,
            '4': 11,
            '5': 12,
            '6': 13,
            '7': 14,
            '8': 15,
            '9': 16
        }
        return switcher.get(argument, "nothing")

    def press_keyboard(self, input_string):
        for i in [*input_string]:
            keycode = self.string_to_keycode(i)
            self.driver.press_keycode(keycode)

    def quit(self):
        self.driver.quit()
