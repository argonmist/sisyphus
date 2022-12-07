import os
from gravel import readyaml
from pebble import pebble

class summit:
   
    def body(self, feature_file, body_list, step):
        for k, v in body_list[0].items():
            insert = '    ' + step + ':  ' + v + '\n'
            feature_file.write(insert)
 
    def feature_generate(self, featrue_num, features, yaml_path):
        feature_file = open("test.feature", "a")
        for i in yaml_path['bdd'][featrue_num]:
            for k, v in i.items():
                if k == 'feature':
                    insert = 'Feature:  ' + v + '\n'
                    feature_file.write(insert)
                if k == 'scenario':
                    insert = '  Scenario:  ' + v + '\n'
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
                insert = '@given("' + v + '")'
            if step == 'when':
                insert = '@when("' + v + '")'
            if step == 'then':
                insert = '@then("' + v + '")'
        python_code.write(insert)
        python_code.write('\n')

    def write_step(self, code_class, testcase, python_code, step_list):
        step_list.pop(0)
        python_code.write('def step(self):\n')
        for i in step_list:
            number = i.strip('step')
            if i != step_list[-1]:
                step_code =  '    ' + code_class + '().push((' + testcase + ', ' + number + '))'
            else:
                step_code = '    assert ' + code_class + '().push((' + testcase + ', ' + number + '))' 
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

    def bdd(self, platform): 
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

        with open('../template/import.template','r') as template, open('steps.py','a') as python_code:
            for line in template:
                python_code.write(line)
            python_code.write('\n')

        for i in features: 
            self.feature_generate(i, features, yaml_path)
            self.python_code_generate(platform, i, features, yaml_path)

        for k, v in yaml_path.items():
            if k != 'bdd':
                if not os.path.exists(k):
                    os.mkdir(k)
                    os.mkdir(k + '/steps')
                new_path = k + '/test.featue'
                os.replace('test.feature', new_path)
                os.replace('steps.py', k + '/steps/steps.py')
      
        template.close()
        python_code.close()
 