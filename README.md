py-static-types
==========
A utility for adding typechecking to annotated functions in python  


Installation
-----------
currently in testing, but once enough tests have been made it will be added to the package manager  

future:
`python3 -m pip install pystatictypes`  


current:
`git clone https://github.com/Seamooo/py-static-types.git` and add the pystatictypes.py file to any codebase you wish to use it in

Usage
------
To use the library there is a single, exposed decorator `typed` meant for use
simply add the decorator to any annotated function to add typechecking
```python
from pystatictypes import typed
@typed
def add(a:int, b:int) -> int:
    return a + b
```
This would now ensure that if an attempt was made to call this function with, for example, a pair of strings, instead of returning the concatenation of those strings, which is undesirable, a TypeError will be raised
```python
foo('a', 'string')
```

Known Limitations
-------
Currently does not allow for extending annotations with typing, but will accept the container type as an annotation
