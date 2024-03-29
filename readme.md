
# DTG Printer Tool

## Usage (original tool)

Ensure [python 3](https://wiki.python.org/moin/BeginnersGuide/Download) is installed.

Download [operator_tool.py](operator_tool.py) to any location.

Double-click on it or open `cmd.exe` and type:

```
python %HOMEPATH%\Downloads\operator_tool.py
```

Where `%HOMEPATH%\Downloads\operator_tool.py` is the location of the downloaded file (eg `C:\Users\JSmith\Downloads\operator_tool.py`)

The tool will then prompt for a barcode, which should be entered using a USB scanner.
Press enter after the barcode is typed in and the script will move the first matching `.prn` file into a `PRIMARY_QUEUE` directory on the printer.

If the number of items in `PRIMARY_QUEUE` is > 5 the operator will be prompted to move the oldest files into a `PRIMARY_COMPLETED` directory.
This ensures long use does not leave operators searching through a growing queue.


The other script, `management_tool.py`, simply prints completed jobs and prompts to save them to the desktop (or any directory set in `JOB_BACKUP_DIRECTORY`).


## Configuration

The script begins with several variables which may need to be changed:

```
# Change to the printer's IP address or hostname (eg my-printer.local if using apple networks)
# Note that non-static IPs may change over time
PRINTER_HOSTNAME = "192.168.101"
```


## Usage (rconn tool)

The rconn tool works by running 2 processes: one on the printer to create .xml files in the printer's `/home/aeoon/AeoonPrint/orders` directory,
and one on the operator's PC to read in scanned UPC codes and send them to the printer process over the network.

### Printer setup

1. Install `python` on the printer by running `sudo apt-get install -y python` on the printer.
2. Copy `rconn_printer_tool.py` to the printer
3. Run `rconn_printer_tool.py` by typing `python rconn_printer_tool.py` into a terminal. This only needs to be done once, when the printer boots up.

### PC Setup

1. Copy `rconn_pc_tool.py` to the printer
2. Double-click on it or open `cmd.exe` and type `python %HOMEPATH%\Downloads\rconn_pc_tool.py`
3. Scan UPC codes to send orders to the printer

Where `%HOMEPATH%\Downloads\rconn_pc_tool.py` is the location of the downloaded file (eg `C:\Users\JSmith\Downloads\rconn_pc_tool.py`)



# Operation Planning

## Stage 1: bulk rip orders

Inputs:

 - `PRE_RIP_ORDERS_CSV_DIR` - a directory containing customer .csv orders with columns `ItemCode`, `ItemName`, `U_ARGNS_ART_TYPE_SIZE_HEIGHT`, and `U_ARGNS_ART_TYPE_SIZE_WIDTH`
 - `PRE_RIP_ORDERS_IMAGES_DIR` - a directory containing .jpg or .png images with names containing `ItemCode` for each input order

The operator will need to ensure the ripping SW is watching the folder `AUTORIP_XML_IN_DIRECTORY`, then run `order_creation_tool.py`.
The tool will prompt for unknown inputs (x,y,width,height,shirt profile information) all of which may be further automated by
adding the data to columns in the .csv file. Currently the following data is ingested:

 - `width = U_ARGNS_ART_TYPE_SIZE_WIDTH`
 - `height = U_ARGNS_ART_TYPE_SIZE_HEIGHT`
 - `x = x`
 - `y = y`
 - `material = U_ARGNS_MATERIAL`
 - `rip_profile = rip-profile`

If an image with a matching barcode is not found the operator will be prompted to pick one from a dialogue.

Outputs:
 - `AUTORIP_XML_IN_DIRECTORY` - directory ripping SW watches for input .xml orders.

## Stage 2: bulk print

Inputs:

 - scanned barcode
 - `RIPPED_XML_OUT_DIRECTORY` - directory rip software writes .xml to

The operator will run `operator_tool.py` and scan or type barcodes into the prompt. The tool will then find the order .xml under `RIPPED_XML_OUT_DIRECTORY` and copy it to `PRINT_ORDERS_HOTFOLDER`, at which point the printer should begin printing.

Outputs:
 - `PRINT_ORDERS_HOTFOLDER` - directory mapped to printer's "orders" directory



