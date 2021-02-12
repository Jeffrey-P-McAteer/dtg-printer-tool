
# DTG Printer Tool

## Usage

Ensure [python 3](https://wiki.python.org/moin/BeginnersGuide/Download) is installed.

Download [dtg_tool.py](dtg_tool.py) to any location.

Double-click on it or open `cmd.exe` and type:

```
python %HOMEPATH%\Downloads\dtg_tool.py
```

Where `%HOMEPATH%\Downloads\dtg_tool.py` is the location of the downloaded file (eg `C:\Users\JSmith\Downloads\dtg_tool.py`)

The tool will then prompt for a barcode, which should be entered using a USB scanner.
Press enter after the barcode is typed in and the script will begin creating .xml job files on a network drive.

TODO should the script wait and scan the orders directory to know when the printer completed a job (we expect the .xml file to be removed from the orders directory)?

## Configuration

The script begins with several variables which may need to be changed:

```
# Change to the printer's IP address or hostname (eg my-printer.local if using apple networks)
# Note that non-static IPs may change over time
PRINTER_HOSTNAME = "192.168.101"
```



