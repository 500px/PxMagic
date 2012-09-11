500px Python Magical API Client
===============================
Watch out! Go Daddy issues mean that this client has not been tested for many of the latest commits!

Furthermore installation documentation and overall guides are completely absent!

It is in your best interest to not install but to use without installing for now since by late tomorrow morning Eastern Time many things will be fixed.

This a Python version for [500px](http://500px.com/ "500px") API, http://developer.500px.com/  

**Warning:** This project is still in active development. 
If you would like to get involved feel free to contact
@zachaysan or @arthurnn on github or at 500px.com.

Installation
------------

### To install:


1.  ```[sudo] python setup.py build ```
2.  ```[sudo] python setup.py install ```
3.  ```[sudo] pip install requests-oauth ``` (oauth users only)

To try without installing
-------------------------	
```python -m fhp.examples.fetchphotos ```

### Or for some magic object fun:
```python -m fhp.examples.magic_photos ```

To run test suite
-----------------
1. Turn on oauth testing by editing config/test_settings.json (requires chrome browser)
2. ```python -m discover ```
