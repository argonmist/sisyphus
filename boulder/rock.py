from gravel import readyaml
from gravel.android import DriverClient
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from appium.webdriver.common.appiumby import AppiumBy
from typing import Dict, NoReturn, Tuple, List, Union, Optional

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
                    for m in self.yaml_path[block_name][title][k]['input']:
                        if m == 'xpath':
                            self.sendkey_to_input_box(block_name, title, k, 'xpath')
                        if m == 'webview_xpath':
                            self.sendkey_to_input_box(block_name, title, k, 'webview_xpath')
                            input_box = self.find_element_in_all_windows(block_name, title, k, 'input')
                            input_text = self.yaml_path[block_name][title][k]['input']['text']
                            self.send_keys(input_box, input_text)
                            self.swith_to_native()
                if j == 'click':
                    print(self.yaml_path[block_name][title][k]['click']['desc'])
                    for m in self.yaml_path[block_name][title][k]['click']:
                        if m == 'xpath':
                            self.click_btn_click(block_name, title, k, 'xpath')
                        if m == 'webview_xpath':
                            click_btn = self.find_element_in_all_windows(block_name, title, k, 'click')
                            click_btn.click()
                            self.swith_to_native()
                if j == 'scroll':
                    print(self.yaml_path[block_name][title][k]['scroll']['desc'])
                    self.scroll_to_text(self.yaml_path[block_name][k]['scroll']['text'])
                if j == 'snapshot':
                    if self.yaml_path[block_name][k]['snapshot']['enable'] == 'yes':
                        print(self.yaml_path[block_name][title][k]['snapshot']['desc'])
                        pic_name = "~/sisyphus/pics" + block_name + "_" + title + ".png"
                        self.driver.get_screenshot_as_file(pic_name)
                if j == 'check':
                    print(self.yaml_path[block_name][title][k]['check']['desc'])
                    for m in self.yaml_path[block_name][title][k]['check']:
                        if m == 'xpath':
                            result = self.is_element_exist(('xpath', self.yaml_path[block_name][title][k]['check']['xpath']))
                    print(result)
                    return result
            k = k + 1

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
        window_handles = self.get_all_window()
        value = self.yaml_path[block_name][title][k][ele_type]['webview_xpath']
        for i in window_handles:
            self.driver.switch_to.window(i)
            if self.is_element_exist(('webview_xpath', value)):
                return self.driver.find_element(By.XPATH, value)

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

