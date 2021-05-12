import sys
import os
import traceback
import datetime
import time
import socket
import json

COMM_PORT = 4001
JOBS_DIRECTORY = '/home/aeoon/AeoonPrint/jobs'
if 'JOBS_DIRECTORY' in os.environ:
  JOBS_DIRECTORY = os.environ['JOBS_DIRECTORY']

PRINT_ORDERS_HOTFOLDER = '/home/aeoon/AeoonPrint/orders'
if 'PRINT_ORDERS_HOTFOLDER' in os.environ:
  PRINT_ORDERS_HOTFOLDER = os.environ['PRINT_ORDERS_HOTFOLDER']

def get_local_ip_addr():
  addr = '127.0.0.1'
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    addr = s.getsockname()[0]
    s.close()
  except Exception as e:
    print(e)
  return addr

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


if __name__ == '__main__':
  while True:
    try:
      # Setup server
      server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      server_socket.bind(('', COMM_PORT))
      print('Listening on {} port {}'.format(get_local_ip_addr(), COMM_PORT))
      
      while True:
        message_bytes, address = server_socket.recvfrom(4096)
        message = json.loads(message_bytes)
        
        print("Received message from {}".format(address))
        #print("Received from {}: {}".format(address, message))

        if message['cmd'] == 'find_prn_file':
          upc = message['upc']
          prn_file = search_for_prn(upc)

          print('Found prn for upc {} at {}'.format(upc, prn_file))
          
          server_socket.sendto(json.dumps({
            'filename': prn_file,
          }).encode('utf-8'), address)

        elif message['cmd'] == 'insert_job':
          job_xml_filename = os.path.join(PRINT_ORDERS_HOTFOLDER, message['job_xml_filename'])
          job_xml_content = message['job_xml_content']

          with open(job_xml_filename, 'w') as fd:
            fd.write(job_xml_content)

          print('Created order .xml from {} at {}'.format(address, job_xml_filename))

          server_socket.sendto(json.dumps({
            'done': 'done',
          }).encode('utf-8'), address)
        else:
          print('[ error ] unknown cmd == {}'.format(message['cmd']))

      time.sleep(1)

    except Exception as e:
      traceback.print_exc()
      # We will exit on ctrl+c events
      if isinstance(e, KeyboardInterrupt):
        break
      else:
        time.sleep(5)



