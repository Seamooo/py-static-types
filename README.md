py-static-types
==========
A library for adding typechecking to annotated functions in python
Installation
-----
`python3 -m pip install pystatictypes`
Usage
------
To use the library there is a single, exposed decorator `typed` meant for use
simply add the decorator to any annotated function to add typechecking
```
from pystatictypes import typed
@typed
def add(a:int, b:int) -> int:
    return a + b
```
This would now ensure that if an attempt was made to call this function with, for example, a pair of strings, instead of returning the concatenation of those strings, which is undesirable, a TypeError will be raised
```
foo('a', 'string')
```
