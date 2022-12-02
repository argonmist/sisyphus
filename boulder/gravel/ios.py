from appium import webdriver
from gravel import readyaml

class Singleton(object):
    driver = None
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            settings = readyaml.read('ios.yaml')
            caps = {}
            caps['platformName'] = settings['platformName']
            caps['platformVersion'] = settings['platformVersion']
            caps['deviceName'] = settings['deviceName']
            caps['automationName'] = settings['automationName']
            caps['xcodeOrgId'] = settings['xcodeOrgId']
            caps['xcodeSigningId'] = settings['xcodeSigningId']
            caps['udid'] = settings['udid']
            caps['bundleId'] = settings['bundleId']
            caps['webviewConnectTimeout'] = settings['webviewConnectTimeout']
            cls._instance = orig.__new__(cls, *args, **kw)
            cls._instance.driver = webdriver.Remote(settings['appiumServer'],caps)
        return cls._instance

class DriverClient(Singleton):

    def getDriver(self):
        return self.driver
