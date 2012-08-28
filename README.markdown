500px Python SDK
================
This a python version for [500px](http://500px.com/ "500px") api, http://developer.500px.com/  

**Warning:** This SDK is still in active development. 
If you would like to get involved feel free to contact
zachaysan or arthurnn on github or at 500px.com.

Installation
------------

### To install:
1.  ```python setup.py build ```
2.  ```sudo python setup.py install ```
3.  ```sudo pip install git+git://github.com/simplegeo/python-oauth2.git ``` (oauth users only)
To try without installing
-------------------------	
```python -m examples.fetchphotos ```

### Or for some magic object fun:
```python -m examples.magic_photos ```

To run test suite
-----------------
1. Turn on oauth testing by editing config/test_settings.json (requires chrome browser)
2. ```python -m discover ````
