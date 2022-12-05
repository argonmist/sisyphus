import sys
import os
import getopt
home = os.getenv('HOME')
main_path = home + '/sisyphus/boulder'
sys.path.insert(0, main_path)
from gravel import readyaml
from pebble import pebble

def auto_run(argv):
    type = ''
    try:
        opts, args = getopt.getopt(argv,"ht:",["type="])
    except getopt.GetoptError:
        print('sisyphus -t <test_type>')
        sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print('sisyphus -t <test_type>')
         sys.exit()
      elif opt in ("-t", "--type"):
         type = arg

    type_yaml = type + '.yaml'
    settings = readyaml.read(type_yaml)
    path_yaml = readyaml.read(settings['pathFile'])
    
    for k, v in path_yaml.items(): 
        task = k

    lastNum = ''
    for k, v in path_yaml[task].items():
        for num in k.split("step"):
            if num.isdigit():
                lastNum = num

    if type == 'ios':
        for testNum in range(1, int(lastNum)+1):
            pebble().push((task, testNum)) 

if __name__ == '__main__':
    auto_run(sys.argv[1:])

