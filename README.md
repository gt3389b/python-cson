python-cson
===========

Python library for CSON (schema-compressed JSON)


Authors
-------
*  Russell Leake, http://www.leakerlabs.com/, gt3389b@gmail.com

Source
------
* Documentation: <https://github.com/lifthrasiir/cson>
* Python Package Index: <http://pypi.python.org/pypi/cson>
* GitHub: <https://github.com/gt3389b/python-cson>

##Install
```bash
easy_install python-cson
```

##Examples
```python
#! /usr/bin/python
import cson,json,optparse,os

parser = optparse.OptionParser('Usage: %prog')
parser.add_option('-c', '--config', dest='config',  type='string')

(options, args) = parser.parse_args()

# Assign new names to constants passed in from CLI options. 
config  = options.config


if config:
   print "Processing "+config
   outName = os.path.splitext(config)[0]
   outFile = outName+".json"
   with open (config, "r") as infile:
      example=infile.readlines()
      text = json.dumps(cson.loads(''.join(example)))
      print "Creating "+outFile
      with open (outFile, "w") as outfile:
         outfile.write(text)
```
