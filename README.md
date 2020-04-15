# cfc-tools-windows

CFC Tools for Windows for the Business Office.  Tools that must run on Windows (not web).

## Developer Setup

* Python: a 32-bit version is required by the 32-bit MS-Access drivers
  (which are required by the CFC's MS-Access files are 32-bit):
  * `py -3.8-32 -m venv venv`
  * `venv\scripts\activate`
* Python Packages: to install the required packages:
  * `python -m pip install -r requirements.txt`
  