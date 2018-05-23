# gerber_cli
A CLI application for interacting with gerber files, work in progress.

# Setup
 - Have a python 2 environment and pip on your system
 - Install [pcb-tools](https://github.com/curtacircuitos/pcb-tools)

# Usage
```bash
$ python load_daemon.py --help
usage: load_daemon.py [-h] [-f FORMAT] [-v] directory

CLI for working with gerber files.

positional arguments:
  directory             Directory containing the gerber files you'll work
                        with.

optional arguments:
  -h, --help            show this help message and exit
  -f FORMAT, --format FORMAT
                        Gerber folder structure format, specific to the
                        software used to export the gerber files. Is either
                        eagle, kicad, ...
  -v, --verbose         Changes logging level to the most output possible
```

Example:
```bash
$ python /path/to/my/gerbers/ -f kicad -v
2018-05-23 18:39:34,201 - gerber_parsing - INFO - Main entry in test file
2018-05-23 18:39:34,203 - gerber_parsing - INFO - Creating an instance of gerber_daemon
2018-05-23 18:39:34,203 - gerber_parsing.gerber_daemon - INFO - Filtering files
2018-05-23 18:39:34,203 - gerber_parsing.gerber_daemon - INFO - Found 5 of the 7 expected gerber files
2018-05-23 18:39:34,203 - gerber_parsing.gerber_daemon - INFO - Rejected 1 files, which were ['arduino_Uno_Rev3-02-TH.gpi']
2018-05-23 18:39:34,203 - gerber_parsing.gerber_daemon - INFO - Creating wrapper for top_copper
2018-05-23 18:39:34,203 - gerber_parsing.gerber_daemon - INFO - Creating wrapper for bottom_copper
2018-05-23 18:39:34,203 - gerber_parsing.gerber_daemon - INFO - Creating wrapper for bottom_soldermask
2018-05-23 18:39:34,206 - gerber_parsing.gerber_daemon - INFO - Creating wrapper for top_soldermask
2018-05-23 18:39:34,207 - gerber_parsing.gerber_daemon - INFO - Creating wrapper for top_silkscreen
2018-05-23 18:39:34,207 - gerber_parsing - INFO - Starting a render dump of the loaded files
2018-05-23 18:39:34,208 - gerber_parsing.gerber_daemon - INFO - Rendering frame for top_copper
2018-05-23 18:39:37,184 - gerber_parsing.gerber_daemon - INFO - Rendering frame for top_silkscreen
2018-05-23 18:39:37,986 - gerber_parsing.gerber_daemon - INFO - Rendering frame for bottom_soldermask
2018-05-23 18:39:38,046 - gerber_parsing.gerber_daemon - INFO - Rendering frame for bottom_copper
2018-05-23 18:39:38,893 - gerber_parsing.gerber_daemon - INFO - Rendering frame for top_soldermask
```


