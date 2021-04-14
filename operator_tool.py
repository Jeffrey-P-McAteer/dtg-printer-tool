
# Code is designed to run on windows 10,
# 3rd-party libraries will have a comment to install
# them using pip.

import sys
import os
import traceback
import datetime
import time

# Change "Y:" to the windows drive that has the network share mounted for the printer's "jobs" directory
JOBS_DIRECTORY = 'Y:\\'

# Use this folder if we are on the printer
if os.path.exists("/home/aeoon/AeoonPrint/jobs"):
  JOBS_DIRECTORY = "/home/aeoon/AeoonPrint/jobs"

# For testing
if 'JOBS_DIRECTORY' in os.environ:
  JOBS_DIRECTORY = os.environ['JOBS_DIRECTORY']

# Change "X:" to the windows drive that has the network share mounted for the printer's "orders" directory
PRINT_ORDERS_HOTFOLDER = 'X:\\'

# Use this folder if we are on the printer
if os.path.exists("/home/aeoon/AeoonPrint/orders"):
  PRINT_ORDERS_HOTFOLDER = "/home/aeoon/AeoonPrint/orders"

# For testing
if 'PRINT_ORDERS_HOTFOLDER' in os.environ:
  PRINT_ORDERS_HOTFOLDER = os.environ['PRINT_ORDERS_HOTFOLDER']


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

      upc = raw_input('Scan/Enter barcode: ')

      # Sanity check so hitting enter doesn't select some random file
      if len(upc) < 3:
        continue

      prn_file = search_for_prn(upc)

      if not prn_file:
        print('[error] Could not find a matching PRN file, has this been ripped yet?')
        raw_input('Press Enter to continue...')
        continue

      prn_file_basename = os.path.basename(prn_file)
      job_name = prn_file_basename.replace('.prn', '')
      job_xml_file = os.path.join(PRINT_ORDERS_HOTFOLDER, job_name+'.xml')

      print("Inserting job {} from {} into {}".format(job_name, prn_file, job_xml_file))

      with open(job_xml_file, 'w') as fd:
        fd.write('''
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


      raw_input('Press Enter to continue...')

    except Exception as e:
      traceback.print_exc()
      # We will exit on ctrl+c events
      if isinstance(e, KeyboardInterrupt):
        break
      else:
        raw_input('Press Enter after reporting error to continue...')


if __name__ == '__main__':
  main()


