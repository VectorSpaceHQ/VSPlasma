VSPlasma is an open source, 2D CAM program specifically for plasma cutters. It's scope is intentionally narrow with the purpose of doing a great job at performing a specific purpose while allowing other software to meet different goals.

# Goals
  - Run natively on Linux. Development and testing is specifically performed in Debian Stable.
  - Generate gcode for LinuxCNC (Plasmac).
  - Focus on functionality before features.
  - Provide a traditional, simple, and intuitive interface. Think XFCE not Unity.

# Requirements
    To install requirements, run the following:

  $ make init
  $ apt install pyqt5-dev-tools python3-pyqt5 python3-configobj qtcreator




# Troubleshooting

## PyQt5 error
ImportError: /lib/x86_64-linux-gnu/libQt5Core.so.5: version `Qt_5.15' not found

solved by removing pip3 version and using Debian's version.
https://stackoverflow.com/questions/63903441/python3-importerror-lib-x86-64-linux-gnu-libqt5core-so-5-version-qt-5-15-n

# Thanks
Much of this project relies on the work of the DXF2GCODE authors.
