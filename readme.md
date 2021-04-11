
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

The rconn tool works by running 2 processes: one on the printer to create .xml files in `TODO ORDERS DIR`,
and one on the operator's PC to read in scanned UPC codes and send them to the printer process over the network.

1. Install `python` on the printer by running `sudo apt-get install -y python` on the printer.
2. Copy `rconn_printer_tool.py` to the printer and run it by typing `python rconn_printer_tool.py`




