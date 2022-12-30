from behave import *
import sys
import os
home = os.getenv('HOME')
main_path = home + '/sisyphus/boulder'
sys.path.insert(0, main_path)
import allure
from gravel import readyaml
from pebble import pebble
from rock import rock


@given("使用者已有PGTalk帳號密碼且為登出狀態")
def step(self):
    assert rock().push(('Forgot', 1))

@when("忘記密碼頁輸入資訊並取得手機驗證碼")
def step(self):
    assert rock().push(('Forgot', 2))

@then("可取回密碼")
def step(self):
    assert rock().push(('Forgot', 3))

@then("可用新密碼登入PGTalk")
def step(self):
    assert rock().push(('Forgot', 4))
