
# Code is designed to run on windows 10,
# 3rd-party libraries will have a comment to install
# them using pip.


# Change to the printer's IP address or hostname
PRINTER_HOSTNAME = "192.168.1.193"

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

JOBS_DIRECTORY = '\\\\{}\\'.format(PRINTER_HOSTNAME)
# For testing
if 'JOBS_DIRECTORY' in os.environ:
  JOBS_DIRECTORY = os.environ['JOBS_DIRECTORY']

PRIMARY_QUEUE_DIRECTORY = os.path.join(JOBS_DIRECTORY, 'PRIMARY_QUEUE')

# This holds "completed" jobs
PRIMARY_QUEUE_COMPLETED_DIRECTORY = os.path.join(JOBS_DIRECTORY, 'PRIMARY_COMPLETED')

def clear_screen():
  os.system('cls' if os.name=='nt' else 'clear')


def search_for_prn(upc):
  """
  Searches through JOBS_DIRECTORY for a file ending in .prn that contains the value of upc,
  and returns the first match
  """
  for dirpath, dirnames, filenames in os.walk(JOBS_DIRECTORY):
    # Do not search in already-printing items
    if PRIMARY_QUEUE_DIRECTORY in dirpath or PRIMARY_QUEUE_COMPLETED_DIRECTORY in dirpath:
      continue

    for file in filenames:
      if upc in file.lower() and file.lower().endswith('.prn'):
        # We found it!
        return os.path.join(dirpath, file)

  return None

def get_primary_queue_path(prn_file):
  return os.path.join(PRIMARY_QUEUE_DIRECTORY, os.path.basename(prn_file))

def get_primary_queue_overflow_path(prn_file):
  return os.path.join(PRIMARY_QUEUE_COMPLETED_DIRECTORY, os.path.basename(prn_file))

def get_oldest_f(directory):
  all_files = [os.path.join(directory, x) for x in os.listdir(directory)]
  return min(all_files, key=os.path.getctime)

def move_oldest_primary_to_completed():
  while len(os.listdir(PRIMARY_QUEUE_DIRECTORY)) > PRIMARY_QUEUE_SIZE:
    oldest_in_queue_prn = get_oldest_f(PRIMARY_QUEUE_DIRECTORY)
    name = os.path.basename(oldest_in_queue_prn)
    yn = input('Has {} completed printing? '.format(name))
    if 'y' in yn.lower():
      overflow_path_prn = get_primary_queue_overflow_path(oldest_in_queue_prn)
      print('[info] Moving {} to {}'.format(oldest_in_queue_prn, overflow_path_prn))
      os.rename(oldest_in_queue_prn, overflow_path_prn)
      print('[info] Moved completed.')


def main(args=sys.argv):
  
  if not os.path.exists(PRIMARY_QUEUE_DIRECTORY):
    os.makedirs(PRIMARY_QUEUE_DIRECTORY)

  if not os.path.exists(PRIMARY_QUEUE_COMPLETED_DIRECTORY):
    os.makedirs(PRIMARY_QUEUE_COMPLETED_DIRECTORY)

  while True:
    try:
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

      print('[info] found {}, moving file...'.format(prn_file))
      primary_queue_file = get_primary_queue_path(prn_file)
      os.rename(prn_file, primary_queue_file)
      # This ensures the modification timestamps are updated
      Path(primary_queue_file).touch()

      print('[info] {} moved to {}'.format(prn_file, primary_queue_file))
      print("Go select {} from the printer's primary queue".format(os.path.basename(prn_file)))
      

      # Finally, move oldest files out of primary queue
      items_in_primary_queue = len(os.listdir(PRIMARY_QUEUE_DIRECTORY))
      if items_in_primary_queue > PRIMARY_QUEUE_SIZE:
        print('[info] There are {} items in the queue'.format(items_in_primary_queue))
        yn = input('Would you like to move completed items into the overflow area? ')
        if 'y' in yn.lower():
          move_oldest_primary_to_completed()

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


