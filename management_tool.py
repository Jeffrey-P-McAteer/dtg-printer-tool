
# Code is designed to run on windows 10,
# 3rd-party libraries will have a comment to install
# them using pip.

import os
import sys
import shutil

JOB_BACKUP_DIRECTORY = os.path.normpath(os.path.expanduser("~/Desktop/JOB_BACKUPS"))

# For testing
if 'JOB_BACKUP_DIRECTORY' in os.environ:
  JOB_BACKUP_DIRECTORY = os.environ['JOB_BACKUP_DIRECTORY']

# Change to the printer's IP address or hostname
PRINTER_HOSTNAME = "192.168.1.193"

JOBS_DIRECTORY = '\\\\{}\\'.format(PRINTER_HOSTNAME)
# For testing
if 'JOBS_DIRECTORY' in os.environ:
  JOBS_DIRECTORY = os.environ['JOBS_DIRECTORY']

PRIMARY_QUEUE_DIRECTORY = os.path.join(JOBS_DIRECTORY, 'PRIMARY_QUEUE')

# This holds "completed" jobs
PRIMARY_QUEUE_COMPLETED_DIRECTORY = os.path.join(JOBS_DIRECTORY, 'PRIMARY_COMPLETED')

DAILY_JOB_HISTORY_CSV = os.path.join(JOBS_DIRECTORY, 'daily_job_history.csv')

def main(args=sys.argv):

  if not os.path.exists(JOB_BACKUP_DIRECTORY):
    os.makedirs(JOB_BACKUP_DIRECTORY)

  print('Completed jobs:')
  for file in os.listdir(PRIMARY_QUEUE_COMPLETED_DIRECTORY):
    print('> {}'.format(file))

  print('')
  yn = input('Move all to {}? '.format(JOB_BACKUP_DIRECTORY))
  if 'y' in yn.lower():
    for file in os.listdir(PRIMARY_QUEUE_COMPLETED_DIRECTORY):
      shutil.move(
        os.path.join(PRIMARY_QUEUE_COMPLETED_DIRECTORY, file),
        JOB_BACKUP_DIRECTORY,
      )

  print('Files copied!')



if __name__ == '__main__':
  main()

