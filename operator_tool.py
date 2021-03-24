
# Code is designed to run on windows 10,
# 3rd-party libraries will have a comment to install
# them using pip.

# Change to the max # of prints possible at one time.
# Operators will be asked to confirm that old jobs can be moved to
# PRIMARY_QUEUE_COMPLETED_DIRECTORY after we have this many in PRIMARY_QUEUE_DIRECTORY
PRIMARY_QUEUE_SIZE = 5


import sys
import os
import traceback
import datetime
import time
from pathlib import Path

# Change "Y:" to the windows drive that has the network share mounted for the printer's jobs directory
JOBS_DIRECTORY = '\\Y:\\'

# For testing
if 'JOBS_DIRECTORY' in os.environ:
  JOBS_DIRECTORY = os.environ['JOBS_DIRECTORY']


def clear_screen():
  os.system('cls' if os.name=='nt' else 'clear')


def search_for_prn(upc):
  """
  Searches through JOBS_DIRECTORY for a file ending in .prn that contains the value of upc,
  and returns the first match
  """
  for dirpath, dirnames, filenames in os.walk(JOBS_DIRECTORY):
    # Do not search in already-printing items
    
    for file in filenames:
      if upc in file.lower() and file.lower().endswith('.prn'):
        # We found it!
        return os.path.join(dirpath, file)

  return None


def main(args=sys.argv):
  
  while True:
    try:
      time.sleep(0.4)
      clear_screen()

      upc = input('Scan/Enter barcode: ')

      # Sanity check so hitting enter doesn't select some random file
      if len(upc) < 3:
        continue

      prn_file = search_for_prn(upc)

      if not prn_file:
        print('[error] Could not find a matching PRN file, has this been ripped yet?')
        input('Press Enter to continue...')
        continue

      print("Inserting {} into the printer's primary queue".format(os.path.basename(prn_file)))

      # TODO reverse-engineer network message to tell printer to print prn_file next in line
      


      input('Press Enter to continue...')

    except Exception as e:
      traceback.print_exc()
      # We will exit on ctrl+c events
      if isinstance(e, KeyboardInterrupt):
        break
      else:
        time.sleep(3)


if __name__ == '__main__':
  main()


