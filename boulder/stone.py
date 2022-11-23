from gravel import readyaml
from gravel.webc import DriverClient
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from typing import Dict, NoReturn, Tuple, List, Union, Optional

class stone:

    def __init__(self):
        self.driver = DriverClient().getDriver()
        self.settings = readyaml.read('webc.yaml')
        self.yaml_path = readyaml.read(self.settings['pathFile'])

    def outset(self):
        url = self.settings['url']
        self.driver.get(url)

    def push(self, steps: Tuple[str, Union[str, Dict]]):
        block_name = steps[0]
        index = steps[1]
        title = 'step' + str(index)
        k = 0
        for i in self.yaml_path[block_name][title]:
            for j in i:
                if j == 'input':
                    print(self.yaml_path[block_name][title][k]['input']['desc'])
                    input_box = self.find_element(('xpath', self.yaml_path[block_name][title][k]['input']['xpath']))
                    input_text = self.yaml_path[block_name][title][k]['input']['text']
                    self.send_keys(input_box, input_text)
                if j == 'click':
                    print(self.yaml_path[block_name][title][k]['click']['desc'])
                    click_btn = self.find_element(('xpath', self.yaml_path[block_name][title][k]['click']['xpath']))
                    click_btn.click()
                if j == 'check':
                    print(self.yaml_path[block_name][title][k]['check']['desc'])
                    result = self.is_element_exist(('xpath', self.yaml_path[block_name][title][k]['check']['xpath']))
                    print(result)
                    return result
            k = k + 1

    def send_keys(self, element, value):
        element.send_keys(value)

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
            elif by == "css":
                WebDriverWait(self.driver, wait_seconds, 1).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, value)))
            elif by == "tag":
                WebDriverWait(self.driver, wait_seconds, 1).until(expected_conditions.presence_of_element_located((By.TAG_NAME, value)))
            else:
                raise NameError("Please enter the correct targeting elements,'id','name','class','text','xpath','css'.")
        except Exception:
            return False
        return True
