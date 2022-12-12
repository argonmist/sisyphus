import sys
import os
import getopt
home = os.getenv('HOME')
main_path = home + '/sisyphus/boulder'
sys.path.insert(0, main_path)
from summit import summit

if __name__ == '__main__':
    type = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:],"ht:r:",["type=","rip="])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         sys.exit()
      elif opt in ("-t", "--type"):
         type = arg
      elif opt in ("-r", "--rip"):
         report_ip = arg
    summit().bdd(type, report_ip)

