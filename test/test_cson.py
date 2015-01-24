from __future__ import print_function
from __future__ import unicode_literals
import pytest, cson, json
def compare(a, b):
   if ( a == b ):
      return True
   else:
      return False

def parseTest(input, expected, message=""):
    __tracebackhide__ = True
    #message = typeof message == 'undefined' ?
    #    input : message.toUpperCase() + ':';
    if len(message):
      print("")
      print('\x1B[1m\x1B[33m' + message + '\x1B[22m')
    actual = cson.loads(input)
    if not compare(expected,actual):
       pytest.fail('\x1B[1m\x1B[31mFAILED\x1B[39m\x1B[22m', ': expected(', expected, ") actual(", actual,")")
       #pytest.fail("not configured: %s" %(x,))
    print('\x1B[1m\x1B[32mPASS\x1B[39m\x1B[22m', ': expected(', expected, ") actual(", actual,")")

#
# Primitive Types
#
def test_true():
   parseTest('true', True, 'true');

def test_false():
   parseTest('false', False, 'false');

def test_null():
   parseTest('null', None, 'null');

def test_zero():
   parseTest('0', 0, 'zero');

def test_one():
   parseTest('1', 1, 'one');

def test_ten():
   parseTest('10', 10, 'ten');

def test_MinusOne():
   parseTest('-1', -1, 'minus one');

def test_IeeeFloat():
   parseTest('-1.23e45', -1.23e45, 'ieee float');


#
# Strings
#
def test_EmptyDoubleQuoteString():
   parseTest('""', '', 'empty double quote string');

def test_EmptySingleQuoteString():
   parseTest("''", '', 'empty single quote string');

def test_SingleQuoteInDoubltQuoteString():
   parseTest('"\'"', "'", 'single quote in double quote string');

def test_DoubeQuoteInDoubltQuoteString():
   parseTest("'\"'", '"', 'double quote in single quote string');


#
# Arrays
#
def test_array():
   parseTest('[]', [], 'array');

def test_OneLengthArray():
   parseTest('[0]', [0], 'one length array');

def test_twoLengthArray():
   parseTest('[0, 1]', [0, 1], 'two length array');

def test_MultitypeArray():
   parseTest('[true, null, 0, \'string\']', [True, None, 0, 'string'], 'multitype array');

def test_NewlineInsteadOfComma():
   parseTest('[0\n1\n2]', [0, 1, 2], 'newline instead of comma');

def test_TrailingComma():
   parseTest('[1, 2, 3, ]', [1, 2, 3], 'trailing comma');

def test_Series():
   parseTest('1, 2', [1, 2], 'series with comma');

def test_SeriesTrailingComma():
   parseTest('3, 4, ', [3, 4], 'series with trailing comma');

def test_SeriesWithNewline():
   parseTest('true\nfalse', [True, False], 'series with newline');


#
# Object
#
def test_object():
   parseTest('{}', {}, 'object');

def test_ObjectDoubleQuoteKey():
   parseTest('{"a": 0}', json.loads('{"a": 0}'), 'ensure object double quote key');

def test_ObjectSingleQuoteKey():
   parseTest('{\'b\': true}', json.loads('{"b": true}'), 'ensure unquoted bool does not get quoted');

def test_ObjectValueString():
   parseTest('{"b": True}', json.loads('{"b": "True"}'), 'ensure True does not get quoted');

def test_UnquotedNullNotGetQuoted():
   parseTest('{c: null}', json.loads('{"c": null}'), 'ensure unquoted null does not get quoted');

def test_UnquotedCapNullGetQuoted():
   parseTest('{c: Null}', json.loads('{"c": "Null"}'), 'ensure Null gets quoted');

def test_QuotedStringStaysQuoted():
   parseTest('d: "string"', json.loads('{"d": "string"}'), 'ensure qutoed string stays quoted');

def test_UnquotedValuesGetQutoed():
   parseTest('d:  string', json.loads('{"d": "string"}'), 'ensure unquoted values get quoted');

def test_UnquotedKeysGetQutoed():
   parseTest('e = []', json.loads('{"e": []}'), 'ensure unquoted keys get quoted');


#
# Complex
#
def test_complex():
   parseTest('# CSON example\npi: 3.141592\ne = 2.718281828, \'foo\': \'bar\'\n"nested" = ["JSON array",\n{and = "JSON object"},\n"with a trailing comma", # yes!\n# yes, the comment can be inside JSON arrays/objects as well\n]\n"verbatim": |a verbatim string\n|  keeps the preceding whitespace\n|    and joins all lines with `\\n`\n|      as you see, no escape sequence is processed\n|        and this string does not have a trailing \\n -->\n',json.loads('{"pi":3.141592,"e":2.718281828,"foo":"bar","nested":["JSON array",{"and":"JSON object"},"with a trailing comma"],"verbatim":"a verbatim string\\n  keeps the preceding whitespace\\n    and joins all lines with `\\\\n`\\n      as you see, no escape sequence is processed\\n        and this string does not have a trailing \\\\n -->"}'), 'complex');
