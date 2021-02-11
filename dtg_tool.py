
# Code is designed to run on windows 10,
# 3rd-party libraries will have a comment to install
# them using PIP.


import sys
import os

XML_OUTPUT_FILE = "x:\\file.xml"

def main(args=sys.argv):

  while True:
    barcode = input('Scan/Enter barcode: ')
    with open(XML_OUTPUT_FILE, 'w') as fd:
      fd.write("""
""".format(barcode=barcode))



if __name__ == '__main__':
  main()
