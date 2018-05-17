python-cson
===========
[![Build Status](https://travis-ci.org/gt3389b/python-cson.svg)](https://travis-ci.org/gt3389b/python-cson)

[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/gt3389b/python-cson?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Python library for CSON (schema-compressed JSON)


Authors
-------
*  Russell Leake, http://www.leakerlabs.com/, gt3389b@gmail.com

Source
------
* Documentation: <https://github.com/lifthrasiir/cson>
* Python Package Index: <http://pypi.python.org/pypi/python-cson>
* GitHub: <https://github.com/gt3389b/python-cson>

##Install
```bash
easy_install python-cson
```

##Examples

```bash
#Commandline usage
python-cson -f <outfile> <infile>

#Using STDIN
cat <infile> | python-cson -f <outfile>

#Printing output to STDOUT
python-cson <infile>
```

```python
#!/usr/bin/python
import cson, json, optparse, os

parser = optparse.OptionParser('Usage: %prog -i <inputfilename>')
parser.add_option('-i', '--inputfilename', dest='inputfilename', type='string')

(options, args) = parser.parse_args()

# Assign new names to constants passed in from CLI options.
inputfilename  = options.inputfilename

if inputfilename:
    print "Processing " + inputfilename
    outName = os.path.splitext(inputfilename)[0]
    outFile = outName + ".json"
    with open(inputfilename, 'r') as infile:
        cson_data = infile.readlines()

        # interpret the CSON string
        json_data = cson.csons2json(''.join(cson_data), 1)

        # write the JSON string out to
        print "Creating " + outFile
        with open(outFile, 'w') as outfile:
            outfile.write(json_data)

       # decode JSON text for verfication
       obj = json.loads(json_data)
else:
    print "Requires input filename file"
```
