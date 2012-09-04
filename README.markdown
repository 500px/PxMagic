500px Python Magical API Client
===============================
This a Python version for [500px](http://500px.com/ "500px") API, http://developer.500px.com/  

**Warning:** This project is still in active development. 
If you would like to get involved feel free to contact
@zachaysan or @arthurnn on github or at 500px.com.

Installation
------------

### To install:
1.  ```[sudo] python setup.py build ```
2.  ```[sudo] python setup.py install ```
3.  ```[sudo] pip install git+git://github.com/simplegeo/python-oauth2.git ``` (oauth users only)

To try without installing
-------------------------	
```python -m fhp.examples.fetchphotos ```

### Or for some magic object fun:
```python -m examples.magic_photos ```

To run test suite
-----------------
1. Turn on oauth testing by editing config/test_settings.json (requires chrome browser)
2. ```python -m discover ```
