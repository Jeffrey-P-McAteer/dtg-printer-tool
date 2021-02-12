
# Code is designed to run on windows 10,
# 3rd-party libraries will have a comment to install
# them using pip.


import sys
import os

# Change to the printer's IP address or hostname
PRINTER_HOSTNAME = "192.168.101"

# Python supports UNC paths on windows using forward slashes
# Reddit discusson about the topic: https://www.reddit.com/r/learnpython/comments/k7mkg/python_32_and_accessing_a_network_location/
JOBS_DIRECTORY = r'\\{}\jobs'.format(PRINTER_HOSTNAME)
ORDERS_DIRECTORY = r'\\{}\orders'.format(PRINTER_HOSTNAME)

def main(args=sys.argv):

  while True:
    order_id = input('Scan/Enter barcode: ')
    
    new_job_file = ORDERS_DIRECTORY+r'\{}.xml'.format(order_id)
    
    print('Creating new job at {new_job_file}'.format(new_job_file=new_job_file))

    # Search for a matching order .xml file to pull data from
    # order_xml = None
    # for order_file in os.listdir(JOBS_DIRECTORY):
    #   # Make file an absolute path we can read + write to
    #   order_file = JOBS_DIRECTORY+r'\\'+order_file
    #   if order_file.lower().endswith('.xml'):
    #     # Check if this is the order we just scanned
    #     with open(order_file) as fd:
    #       contents = fd.read()
    #       if '<id>{}'.format(order_id) in contents.lower():
    #         print('Found matching order at {order_file}'.format(order_file=order_file))
    #         order_xml = contents

    # if not order_xml:
    #   print('Cannot find an order in {order_file} for  {order_id}'.format(
    #     order_file=order_file,
    #     order_id=order_id
    #   ))
    #   continue

    # Do we need to parse order_xml for jobs or ask the operator which job to submit?
    # The current assumption is we can copy the order file verbatim to the new job .xml file

    # Also before we write the new_job_file should we handle this requirement from the windows box?
    # "In order to print some images from the automatic print queue, first the ripped images have to be copied to the printer into its "jobs" folder (/home/aeoon/AeoonPrint/jobs). "

    

    with open(new_job_file, 'w') as fd:
      fd.write("""
<?xml version="1.0"?>
<Order>
  <Id>14SB1201008714</Id>
  <Images>
    <Image>
      <Id>14SB1201008714-0</Id>
      <SourceImage>/home/aeoon/AeoonPrint/jobs/cat.png</SourceImage>
      <RipedImage>cat.rip</RipedImage>
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
    <Image>
      <Id>14SB1201008714-1</Id>
      <SourceImage>/home/aeoon/AeoonPrint/jobs/Apples.png</SourceImage>
      <RipedImage>Apples.rip</RipedImage>
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
      <Id>14SB1201008714-p1</Id>
      <DesiredCount>1</DesiredCount>
      <Material>AAA of the Loom white, L</Material>
      <Prints>
        <Print>
          <Id>14SB1201008714 -print1</Id>
          <ImageId>14SB1201008714-0</ImageId>
          <PrintArea>front</PrintArea>
          <Position>
            <X>0</X>
            <Y>0</Y>
          </Position>
        </Print>
      </Prints>
    </Product>
    <Product>
      <Id>14SB1201008714-p2</Id>
      <DesiredCount>1</DesiredCount>
      <CurrentCount>1</CurrentCount>
      <Material>CCC of the Loom white, L</Material>
      <Prints>
        <Print>
          <Id>14SB1201008714-print2</Id>
          <ImageId>14SB1201008714-0</ImageId>
          <PrintArea>front</PrintArea>
          <Position>
            <X>30</X>
            <Y>0</Y>
          </Position>
        </Print>
      </Prints>
    </Product>
  </Products>
</Order>

""".strip())

    print('Job submitted!')


if __name__ == '__main__':
  main()
