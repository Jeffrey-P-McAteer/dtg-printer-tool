import sys
import os
import traceback
import datetime
import time
import socket
import json

PRINTER_IP = '192.168.1.193'
if 'PRINTER_IP' in os.environ:
  PRINTER_IP = os.environ['PRINTER_IP']

COMM_PORT = 4001


def clear_screen():
  os.system('cls' if os.name=='nt' else 'clear')

def msg_to_printer(msg, timeout=3):
  response = {}
  try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    sock.sendto(json.dumps(msg).encode('utf-8'), (PRINTER_IP, COMM_PORT))
    # wait timeout seconds for a reply...
    reply_bytes = sock.recv(4096)
    response = json.loads(reply_bytes)
  except Exception as e:
    traceback.print_exc()
  return response


def ask_printer_to_find_prn_file(upc):
  return msg_to_printer({
    'cmd': 'find_prn_file',
    'upc': upc
  })['filename']

def tell_printer_to_insert_job(job_xml_filename, job_xml_content):
  return msg_to_printer({
    'cmd': 'insert_job',
    'job_xml_filename': job_xml_filename,
    'job_xml_content': job_xml_content
  })

if __name__ == '__main__':

  while True:
    try:
      time.sleep(0.4)
      clear_screen()

      upc = input('Scan/Enter barcode: ')

      # Sanity check so hitting enter doesn't select some random file
      if len(upc) < 3:
        continue

      prn_file = ask_printer_to_find_prn_file(upc)

      if not prn_file:
        print('[error] Could not find a matching PRN file, has this been ripped yet?')
        input('Press Enter to continue...')
        continue

      prn_file_basename = os.path.basename(prn_file)
      job_name = prn_file_basename.replace('.prn', '')
      job_xml_file = job_name+'.xml'

      print("Inserting job {} from {} into {}".format(job_name, prn_file, job_xml_file))

      tell_printer_to_insert_job(job_xml_file, '''
<Order>
  <Id>{job_name}</Id>
  <Images>
    <Image>
      <Id>{job_name}-i0</Id>
      <SourceImage>/home/aeoon/AeoonPrint/jobs/{job_name}.png</SourceImage>
      <RipedImage>{prn_file_basename}</RipedImage>
      <RipProfile>shirt-white</RipProfile>
      <ColorPasses>3</ColorPasses>
      <Size>
        <Width>100</Width>
        <Height>240</Height>
      </Size>
      <Rotation>0</Rotation>
      <RipStatus>
        <StatusCode>1</StatusCode>
        <Message>Ok</Message>
      </RipStatus>
    </Image>
  </Images>
  <Products>
    <Product>
      <Id>{job_name}-p0</Id>
      <DesiredCount>1</DesiredCount>
      <Material>AAA of the Loom white, L</Material>
      <Prints>
        <Print>
          <Id>{job_name}-p0p1</Id>
          <ImageId>{job_name}-i0</ImageId>
          <PrintArea>front</PrintArea>
          <Position>
            <X>0</X>
            <Y>0</Y>
          </Position>
        </Print>
      </Prints>
    </Product>
  </Products>
</Order>
'''.format(
  job_name=job_name,
  prn_file_basename=prn_file_basename,
  # TODO future parameters I see needing:
  # print resolution (width x height)
  # print location (x,y)
  # RipProfile and ColorPasses
  # Possibly Material, though this looks like it's purely for humans to read and would not be processed by the printer
).strip())

      input('Press Enter to continue...')

    except Exception as e:
      traceback.print_exc()
      # We will exit on ctrl+c events
      if isinstance(e, KeyboardInterrupt):
        break
      else:
        time.sleep(5)


