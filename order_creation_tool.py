
import sys
import csv
import json
import os
import traceback
import time

# Change to the windows folder that the ripping software watches for new rip orders.
AUTORIP_XML_IN_DIRECTORY = r'C:\Users\17044\Desktop\test automation\hotfolder'

# Change "X:" to the location of the directory holding new order .csv files
PRE_RIP_ORDERS_CSV_DIR = r'C:\Users\17044\Downloads'

# For each line in each .csv file, the ItemCode
# column will be read + this directory will be searched for a
# .png or .jpg file containing "ItemCode" anywhere in the name.
PRE_RIP_ORDERS_IMAGES_DIR = r'C:\Users\17044\Downloads'

# For testing
if 'AUTORIP_XML_IN_DIRECTORY' in os.environ:
  AUTORIP_XML_IN_DIRECTORY = os.environ['AUTORIP_XML_IN_DIRECTORY']

# For testing
if 'PRE_RIP_ORDERS_CSV_DIR' in os.environ:
  PRE_RIP_ORDERS_CSV_DIR = os.environ['PRE_RIP_ORDERS_CSV_DIR']

# For testing
if 'PRE_RIP_ORDERS_IMAGES_DIR' in os.environ:
  PRE_RIP_ORDERS_IMAGES_DIR = os.environ['PRE_RIP_ORDERS_IMAGES_DIR']


def clear_screen():
  os.system('cls' if os.name=='nt' else 'clear')

def get_user_input(prompt='> '):
  if sys.version_info[0] < 3:
    return raw_input(prompt)
  else:
    return input(prompt)

def get_user_file_pick():
  if sys.version_info[0] < 3:
    import Tkinter, tkFileDialog
    root = Tkinter.Tk()
    root.withdraw()
    return tkFileDialog.askopenfilename()
  else:
    import tkinter
    from tkinter import filedialog
    return filedialog.askopenfilename()

def search_for_prerip_image(name):
  """
  Searches PRE_RIP_ORDERS_IMAGES_DIR and returns the first file ending in .png or .jpg
  which contains "name" in its filename.
  """
  for dirpath, dirnames, filenames in os.walk(PRE_RIP_ORDERS_IMAGES_DIR):
    for file in filenames:
      if name in file.lower() and (file.lower().endswith('.png') or file.lower().endswith('.jpg')):
        # We found it!
        return os.path.join(dirpath, file)

  return None

def create_order_rip_xml_request(order_csv_file):
  print('Reading orders from {}'.format(order_csv_file))
  with open(order_csv_file, 'r') as fd:
    reader = csv.DictReader(fd)
    for row in reader:
      try:
        # Debugging
        # print(json.dumps(row, sort_keys=True, indent=4))
        
        item_code = row['ItemCode']
        item_name = row['ItemName']
        
        # Handle error case from the .csv having 2x headers.
        if item_name.strip() == 'ItemName':
          continue

        print('Creating rip order for item "{}" ()'.format(item_name, item_code))

        lead_time = row.get('LeadTime', '')
        print_category = row.get('U_ARGNS_CATEGORY', '')
        columns = row.get('U_ARGNS_COL', '')
        art_type = row.get('U_ARGNS_ART_TYPE', '')
        graphic_category = row.get('U_ARGNS_GRAPHIC_CAT', '')
        graphic_type = row.get('U_ARGNS_GRAPHIC_TYPE', '')
        number_of_colors = row.get('U_ARGNS_NUM_COLORS', '')
        material = row.get('U_ARGNS_MATERIAL', '')
        height = row.get('U_ARGNS_ART_TYPE_SIZE_HEIGHT', '')
        width = row.get('U_ARGNS_ART_TYPE_SIZE_WIDTH', '')

        print('Lead Time = {}'.format(lead_time))
        print('Category = {}'.format(print_category))
        print('Columns = {}'.format(columns))
        print('Art Type = {}'.format(art_type))
        print('Graphic Category = {}'.format(graphic_category))
        print('Graphic Type = {}'.format(graphic_type))
        print('# of colors = {}'.format(number_of_colors))

        if not material:
          print('Material is empty! Please input material manually (eg "AAA of the Loom white, L" w/o quotes):')
          material = get_user_input('material: ')

        print('material = {}'.format(material))

        if not width:
          print('Width is empty! Please input rip width manually:')
          width = get_user_input('width: ')

        if not height:
          print('Height is empty! Please input rip height manually:')
          height = get_user_input('height: ')

        print('width = {}'.format(width))
        print('height = {}'.format(height))

        # TODO auto-map x and y from some known profiles
        x = row.get('y', '')
        if not x:
          print('X is empty! Please input x manually (0=left of shirt, ???=right):')
          x = get_user_input('x: ')

        y = row.get('y', '')
        if not y:
          print('Y is empty! Please input y manually (0=top of shirt, ???=bottom):')
          y = get_user_input('y: ')
        
        # TODO map this from a .csv file or something
        rip_profile = row.get('rip-profile', '')
        if not rip_profile:
          print('Could not determine rip profile, please enter one manually (eg shirt-white):')
          rip_profile = get_user_input('rip_profile: ')

        image_file = search_for_prerip_image(item_code)
        if image_file:
          print('Press enter to use the image {} for print code {}'.format(os.path.basename(image_file), item_code))
          get_user_input()
        else:
          print('No image file found within {} for print code {}'.format(PRE_RIP_ORDERS_IMAGES_DIR, item_code))

        while not image_file or not os.path.exists(image_file):
          print('Press enter to select an image file for this rip')
          get_user_input()
          try:
            image_file = get_user_file_pick()
          except:
            traceback.print_exc()
                
        request_xml_file = os.path.join(AUTORIP_XML_IN_DIRECTORY, '{}.xml'.format(item_code))
        with open(request_xml_file, 'w') as fd:
          fd.write('''
<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<Order>
  <Id>{item_code}</Id>
  <Images>
    <Image>
      <Id>{item_code}-i0</Id>
      <SourceImage>{image_file}</SourceImage>
      <RipProfile>{rip_profile}</RipProfile>
      <ColorPasses>3</ColorPasses>
      <Size>
        <Width>{width}</Width>
        <Height>{height}</Height>
      </Size>
      <Rotation>0</Rotation>
    </Image>
  </Images>
  <Products>
    <Product>
      <Id>{item_code}-p0</Id>
      <DesiredCount>1</DesiredCount>
      <Material>{material}</Material>
      <Prints>
        <Print>
          <Id>{item_code}-p0p1</Id>
          <ImageId>{item_code}-i0</ImageId>
          <PrintArea>front</PrintArea>
          <Position>
            <X>{x}</X>
            <Y>{y}</Y>
          </Position>
        </Print>
      </Prints>
    </Product>
  </Products>
</Order>
'''.format(
  item_code=item_code,
  image_file=image_file,
  width=width,
  height=height,
  material=material,
  rip_profile=rip_profile,
  x=x,
  y=y,

).strip())

        print('Created rip request {}'.format(request_xml_file))

        # Poll for 15 seconds to ensure file is accepted by auto-rip SW
        print('Polling request until accepted')
        accepted = False
        for _ in range(0, 10 * 2):
          print('.', end='', flush=True)
          time.sleep(0.5)
          if not os.path.exists(request_xml_file):
            accepted = True
            break

        if accepted:
          print('Auto-rip process started!')

        print('Press enter to continue...')
        get_user_input()
        clear_screen()

      except:
        traceback.print_exc()
        print('=' * 25)
        print(' Error in spreadsheet row, please check for missing data. ')
        print(' Continuing to next row in 5 seconds... ')
        print('=' * 25)
        time.sleep(5)





def main(args=sys.argv):
  
  for dirpath, dirnames, filenames in os.walk(PRE_RIP_ORDERS_CSV_DIR):
    for file in filenames:
      if file.lower().endswith('.csv'):
        create_order_rip_xml_request( os.path.join(dirpath, file) )



if __name__ == '__main__':
  main()
