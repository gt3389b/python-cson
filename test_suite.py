#! /usr/bin/python
import cson,json

def compare(a, b):
   if ( a == b ):
      return True
   else:
      return False

def parseTest(input, expected, message=""):
    #message = typeof message == 'undefined' ?
    #    input : message.toUpperCase() + ':';
    if len(message):
      print ""
      print '\x1B[1m\x1B[33m' + message + '\x1B[22m'
    json_string=cson.loads(input, 1)
    actual = json.loads(json_string)
    if not compare(expected,actual):
       print '\x1B[1m\x1B[31mFAILED\x1B[39m\x1B[22m', ': expected(', expected, ") actual(", actual,")"
       assert(0)
    print '\x1B[1m\x1B[32mPASS\x1B[39m\x1B[22m', ': expected(', expected, ") actual(", actual,")"

def printSubject(subject):
    print ''
    print '*****'
    print '\x1B[33m' + subject + '\x1B[39m'
    print '*****'


printSubject('Primitive types');

parseTest('true', True, 'true');
parseTest('false', False, 'false');
parseTest('null', None, 'null');
parseTest('0', 0, 'zero');
parseTest('1', 1, 'one');
parseTest('10', 10, 'ten');
parseTest('-1', -1, 'minus one');
parseTest('-1.23e45', -1.23e45, 'ieee float');


printSubject('String');

parseTest('""', '', 'empty double quote string');
parseTest("''", '', 'empty single quote string');
parseTest('"\'"', "'", 'single quote in double quote string');
parseTest("'\"'", '"', 'double quote in single quote string');


printSubject('Array');

parseTest('[]', [], 'array');
parseTest('[0]', [0], 'one length array');
parseTest('[0, 1]', [0, 1], 'two length array');
parseTest('[true, null, 0, \'string\']', [True, None, 0, 'string'], 'multitype');
parseTest('[0\n1\n2]', [0, 1, 2], 'newline instead of comma');
parseTest('[1, 2, 3, ]', [1, 2, 3], 'trailing comma');
parseTest('1, 2', [1, 2]);
parseTest('3, 4, ', [3, 4]);
parseTest('true\nfalse', [True, False]);


printSubject('Object');

parseTest('{}', {}, 'object');
parseTest('{"a": 0}', json.loads('{"a": 0}'));
parseTest('{\'b\': true}', json.loads('{"b": true}'));
parseTest('{c: null}', json.loads('{"c": null}'));
parseTest('d: "string"', json.loads('{"d": "string"}'));
parseTest('d:  string', json.loads('{"d": "string"}'), 'ensure unquoted values get quoted');
parseTest('e = []', json.loads('{"e": []}'), 'ensure unquoted keys get quoted');


printSubject('Complex');
parseTest('# CSON example\npi: 3.141592\ne = 2.718281828, \'foo\': \'bar\'\n"nested" = ["JSON array",\n{and = "JSON object"},\n"with a trailing comma", # yes!\n# yes, the comment can be inside JSON arrays/objects as well\n]\n"verbatim": |a verbatim string\n|  keeps the preceding whitespace\n|    and joins all lines with `\\n`\n|      as you see, no escape sequence is processed\n|        and this string does not have a trailing \\n -->\n',json.loads('{"pi":3.141592,"e":2.718281828,"foo":"bar","nested":["JSON array",{"and":"JSON object"},"with a trailing comma"],"verbatim":"a verbatim string\\n  keeps the preceding whitespace\\n    and joins all lines with `\\\\n`\\n      as you see, no escape sequence is processed\\n        and this string does not have a trailing \\\\n -->"}'));
