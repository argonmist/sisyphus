from selenium import webdriver
from gravel import readyaml

class Singleton(object):
    driver = None
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            settings = readyaml.read('webc.yaml')
            HOST = settings['selenoidIP']
            orig = super(Singleton, cls)

            capabilities = {
                "browserName": "chrome",
                "browserVersion": "107.0",
                "selenoid:options": {
                "enableVideo": False,
                "enableVNC": True
                }
            }
            cls._instance = orig.__new__(cls, *args, **kw)
            cls._instance.driver = webdriver.Remote(command_executor='http://{}:4444/wd/hub'.format(HOST), desired_capabilities=capabilities)
        return cls._instance

class DriverClient(Singleton):

    def getDriver(self):
        return self.driver
