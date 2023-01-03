import sys
import os
import shutil
import subprocess
home = os.getenv('HOME')
main_path = home + '/sisyphus/boulder'
sys.path.insert(0, main_path)
from gravel import readyaml
from pebble import pebble

class summit:
   
    def body(self, feature_file, body_list, step):
        for k, v in body_list[0].items():
            insert = '    ' + step + ' ' + v + '\n'
            feature_file.write(insert)
 
    def feature_generate(self, featrue_num, features, yaml_path):
        feature_file = open("test.feature", "a")
        for i in yaml_path['bdd'][featrue_num]:
            for k, v in i.items():
                if k == 'feature':
                    insert = 'Feature: ' + v + '\n'
                    feature_file.write(insert)
                if k == 'scenario':
                    feature_file.write('\n')
                    insert = '  Scenario: ' + v + '\n'
                    feature_file.write(insert)
                if k == 'given':
                    self.body(feature_file, v, 'Given')
                if k == 'when':
                    self.body(feature_file, v, 'When')
                if k == 'then':
                    self.body(feature_file, v, 'Then')
        feature_file.write('\n')
        feature_file.close()

    def write_property(self, python_code, step_list, step):
        for k, v in step_list[0].items():
            if step == 'given':
                python_code.write('\n')
                insert = '@given("' + v + '")'
            if step == 'when':
                python_code.write('\n')
                insert = '@when("' + v + '")'
            if step == 'then':
                python_code.write('\n')
                insert = '@then("' + v + '")'
        python_code.write(insert)
        python_code.write('\n')

    def write_step(self, code_class, testcase, python_code, step_list):
        step_list.pop(0)
        python_code.write('def step(self):\n')
        for i in step_list:
            number = i.strip('step')
            if i != step_list[-1]:
                step_code =  '    ' + code_class + '().push((\'' + testcase + '\', ' + number + '))'
            else:
                step_code = '    assert ' + code_class + '().push((\'' + testcase + '\', ' + number + '))' 
            python_code.write(step_code)
            python_code.write('\n')

    def python_code_generate(self, platform, featrue_num, features, yaml_path):
        python_code = open('steps.py','a')
        for i in yaml_path:
            if i != 'bdd':
                testcase = i
        if platform == 'ios':
            code_class = 'pebble'
        if platform == 'android':
            code_class = 'rock'
        if platform == 'webc':
            code_class = 'stone'
        for i in yaml_path['bdd'][featrue_num]:
            for k, v in i.items():
                if k == 'given':
                    self.write_property(python_code, v, 'given')
                    self.write_step(code_class, testcase, python_code, v)
                if k == 'when':
                    self.write_property(python_code, v, 'when')
                    self.write_step(code_class, testcase, python_code, v)
                if k == 'then':
                    self.write_property(python_code, v, 'then')
                    self.write_step(code_class, testcase, python_code, v)

    def quit_app(self, platform):
        python_code = open('steps.py','a')
        if platform == 'ios':
            code_class = 'pebble'
        if platform == 'android':
            code_class = 'rock'
        if platform == 'webc':
            code_class = 'stone'
        quit_code = '    ' + code_class + '().quit()'
        python_code.write(quit_code)

    def report_generate(self, platform, testcase):
        os.chdir(home + '/sisyphus/bdd/' + platform)
        behave_cmd = 'behave -f allure_behave.formatter:AllureFormatter -o report --capture ./' + testcase
        p = subprocess.Popen(behave_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            print(line)
        retval = p.wait()

    def report_service(self, platform, report_ip):
        os.chdir(home + '/sisyphus/bdd/' + platform)
        report_cmd = 'allure serve -h '+ report_ip + ' -p 8883 ./report'
        subprocess.call(report_cmd, shell=True)

    def bdd(self, platform, report_ip, report_gen, report_serve): 
        if os.path.exists('test.feature'):
            os.remove('test.feature')
        if os.path.exists('steps.py'):
            os.remove('steps.py')
        features = []
        yaml_setting = platform + '.yaml'
        settings = readyaml.read(yaml_setting)
        yaml_path = readyaml.read(settings['pathFile']) 
        if yaml_path['bdd']['enable'] == 'yes':
            for i in yaml_path['bdd']:
                if i != 'enable':
                    features.append(i)

        with open(home + '/sisyphus/template/import.template','r') as template, open('steps.py','a') as python_code:
            for line in template:
                python_code.write(line)
            python_code.write('\n')

        for i in features: 
            self.feature_generate(i, features, yaml_path)
            self.python_code_generate(platform, i, features, yaml_path)

        self.quit_app(platform)

        for k, v in yaml_path.items():
            if k != 'bdd':
                testcase = k
                if not os.path.exists(k):
                    os.mkdir(k)
                    os.mkdir(k + '/steps')
                new_path = k + '/test.feature'
                os.replace('test.feature', new_path)
                os.replace('steps.py', k + '/steps/steps.py')
                if not os.path.exists(home + '/sisyphus/bdd'):
                    os.mkdir(home + '/sisyphus/bdd')
                if not os.path.exists(home + '/sisyphus/bdd/' + platform):
                    os.mkdir(home + '/sisyphus/bdd/' + platform)
                if os.path.exists(home + '/sisyphus/bdd/' + platform + '/' + k):
                    shutil.rmtree(home + '/sisyphus/bdd/' + platform + '/' + k)
                    os.replace(k, home + '/sisyphus/bdd/' + platform + '/' + k)
                else:
                    os.replace(k, home + '/sisyphus/bdd/' + platform + '/' + k)
      
        template.close()
        python_code.close()

        if yaml_path['bdd']['enable'] == 'yes':
            if report_gen == "yes":
                print('Generate report only')
                self.report_generate(platform, testcase)
            elif report_serve == "yes":
                print('Report serve only')
                self.report_service(platform, report_ip)
            else:
                print('Generate report and serve the report')
                self.report_generate(platform, testcase)
                self.report_service(platform, report_ip)

 
