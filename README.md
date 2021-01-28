# cfc-tools-windows

CFC Tools for Windows for the Business Office.  Tools that must run on Windows (not web).

## Running CFC-Tools

### In Development Environment

* Run (in a Windows command prompt):
  * `cd \path\to\project\root`
  * `venv\scripts\activate`
  * `python main.py`

### In Production Environment

* Build:
  * `cd \path\to\project\root`
  * `venv\scripts\activate`
  * `python x-dev/build.py`
  * Runnable created in `x-dev/CFC-Tools.pyzw`

* Run (in a Windows command prompt):
  * Must have Python installed locally with `x-dev/requirements.txt` packages
  * `python3 CFC-Tools.pyzw`
