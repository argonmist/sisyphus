from appium import webdriver
from gravel import readyaml

class Singleton(object):
    driver = None
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            settings = readyaml.read('android.yaml')
            caps = {}
            caps['platformName'] = settings['platformName']
            caps['platformVersion'] = settings['platformVersion']
            caps['deviceName'] = settings['deviceName']
            caps['appPackage'] = settings['appPackage']
            caps['appActivity'] = settings['appActivity']
            caps['autoGrantPermissions'] = settings['autoGrantPermissions']
            caps['chromedriverExecutable'] = settings['chromedriverExecutable']
            cls._instance = orig.__new__(cls, *args, **kw)
            cls._instance.driver = webdriver.Remote(settings['appiumServer'],caps)
        return cls._instance

class DriverClient(Singleton):

    def getDriver(self):
        return self.driver
