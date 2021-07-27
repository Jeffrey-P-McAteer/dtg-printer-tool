
# Code is designed to run on windows 10,
# 3rd-party libraries will have a comment to install
# them using pip.

import sys
import os
import traceback
import datetime
import time
import shutil

# Change "Y:" to the windows folder that contains already-ripped .xml files.
RIPPED_XML_OUT_DIRECTORY = r'C:\Users\17044\Desktop\test automation\done'

# Change "X:" to the windows drive that has the network share mounted for the printer's "orders" directory
PRINT_ORDERS_HOTFOLDER = 'X:\\'

# For testing
if 'RIPPED_XML_OUT_DIRECTORY' in os.environ:
  RIPPED_XML_OUT_DIRECTORY = os.environ['RIPPED_XML_OUT_DIRECTORY']

# For testing
if 'PRINT_ORDERS_HOTFOLDER' in os.environ:
  PRINT_ORDERS_HOTFOLDER = os.environ['PRINT_ORDERS_HOTFOLDER']


def clear_screen():
  os.system('cls' if os.name=='nt' else 'clear')

def get_user_input(prompt='> '):
  if sys.version_info[0] < 3:
    return raw_input(prompt)
  else:
    return input(prompt)

def search_for_rip_xml(upc):
  """
  Searches through RIPPED_XML_OUT_DIRECTORY for a file ending in .xml that contains the value of upc,
  and returns the first match
  """
  for dirpath, dirnames, filenames in os.walk(RIPPED_XML_OUT_DIRECTORY):
    for file in filenames:
      if upc in file.lower() and file.lower().endswith('.xml'):
        # We found it!
        return os.path.join(dirpath, file)

  return None


def main(args=sys.argv):
  
  while True:
    try:
      time.sleep(0.4)
      if not 'DEBUG' in args:
        clear_screen()

      upc = get_user_input('Scan/Enter barcode: ')

      # Sanity check so hitting enter doesn't select some random file
      if len(upc) < 3:
        continue

      xml_file = search_for_rip_xml(upc)

      if not xml_file:
        print('[error] Could not find a matching rip .xml output file, has this been ripped yet?')
        get_user_input('Press Enter to continue...')
        continue

      xml_file_basename = os.path.basename(xml_file)
      job_xml_file = os.path.join(PRINT_ORDERS_HOTFOLDER, xml_file_basename)

      print("Inserting job {} from {} into {}".format(xml_file_basename, xml_file, job_xml_file))

      shutil.copy(xml_file, job_xml_file)

      print('Wrote job to {}, polling for 10s to see if Aeoon accepts it...'.format(job_xml_file))
      aeoon_accepted_xml = False
      num_checks = 10
      while num_checks > 0:
        num_checks -= 1
        time.sleep(1)
        if not os.path.exists(job_xml_file):
          aeoon_accepted_xml = True
          break

      if aeoon_accepted_xml:
        print('Aeoon accepted XML order!')
      else:
        print('Order XML {} still exists, orders hotfolder must not be monitored by Aeoon.'.format(job_xml_file))

      get_user_input('Press Enter to continue...')

    except Exception as e:
      traceback.print_exc()
      # We will exit on ctrl+c events
      if isinstance(e, KeyboardInterrupt):
        break
      else:
        get_user_input('Press Enter after reporting error to continue...')


if __name__ == '__main__':
  main()


