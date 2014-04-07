#! /usr/bin/python
#
# coding: utf8
#
# cson (schema-compessed json)
#
# author: Russell Leake, http://leakerlabs.com, gt3389b@gmail.com
import json

__all__ = ("loads", )

def isName(char):
   return not ((char == ',') | \
               (char == '=') | \
               (char == '"') | \
               (char == '\'') | \
               (char == '[') | \
               (char == '{') | \
               (char == ']') | \
               (char == '}') | \
               (char == ' ') | \
               (char == '#') | \
               (char == '\n') | \
               (char == ':'));
    
def isWS(char):
   return (char == ' ')

def isCRLF(char, nextChar):
   return (char == '\r') & (nextChar == '\n');

def isNameSeparator(char):
   return (char == ':') | (char == '=');

def isEndOfDQuote(prevChar, char):
   return (prevChar != '\\') & (char == '\"');

def isEndOfSQuote(prevChar, char):
   return (prevChar != '\\') & (char == '\'');

def isBeginOfBracket(char):
   return (char == '[') | (char == '{');

def isEndOfBracket(char):
   return (char == ']') | (char == '}');

def isBracket(char):
   return isBeginOfBracket(char) | isEndOfBracket(char);

def stringToLiteral(string):
   string = string.replace('\\', '\\\\');
   string = string.replace('\b', '\\b');
   string = string.replace('\f', '\\f');
   string = string.replace('\n', '\\n');
   string = string.replace('\r', '\\r');
   string = string.replace('\t', '\\t');
   string = string.replace('\"', '\\\"');
   return string;

def get_iterable(text):
     if type(text) == list:
        iterable = range(len(text))
     elif type(text) == dict:
        iterable = cson_data.keys()
     else:
        iterable = len(list(text))
     return iterable

def tokenize(text):
   tokens = [];
   iterable = get_iterable(text)
   i=0
   while i < iterable:
      currentChar = text[i]
      if i < iterable-1:
         nextChar = text[i+1]
      else:
         nextChar = None

      if (isBracket(currentChar)):
         tokens.append(currentChar)
         i+=1
      elif (currentChar == ',') | (currentChar == '\n'):
         i+=1
      elif (nextChar != None) & (isCRLF(currentChar, nextChar)):
         i+=1
      elif (isNameSeparator(currentChar)):
         tokens.append(':')
         i+=1
      # Address Quotes
      elif (currentChar == '\"') | (currentChar == '\''):
         buffer = ''
         isSQuote = currentChar == '\''
         escapeCount = 0
         i+=1
         currentChar = text[i]
         prevChar = text[i - 1]

         while (not (isEndOfSQuote(prevChar, currentChar) if isSQuote else isEndOfDQuote(prevChar, currentChar))) & (i < iterable):
            if (isSQuote & (currentChar == '\"') & ((escapeCount % 2) == 0)):
               buffer += '\\';
            buffer += currentChar
            escapeCount = escapeCount + 1 if (currentChar == '\\') else 0
            i+=1
            if i < iterable:
               currentChar = text[i];
               if (i < iterable - 1):
                  prevChar = text[i - 1];
         tokens.append('\"' + buffer + '\"');
         i+=1
      # Address Verbatim
      elif (currentChar == '|'):
         buffer = '';
         verbatimBuffer = [];
         verbatimExit = False;
         i+=1
         while(i < iterable):
            currentChar = text[i];
            if(i < iterable - 1):
               nextChar = text[i + 1];
            if (verbatimExit): 
               if (currentChar == '|'):
                  verbatimExit = False;
                  i+=1
                  continue;
               elif (isCRLF(currentChar, nextChar)):
                     i+=1;
                     break;
               elif (currentChar == '\n'):
                     break;
               elif (not isWS(currentChar)):
                     i-=1;
                     break;
            elif (isCRLF(currentChar, nextChar)):
               i+=1
               verbatimBuffer.append(stringToLiteral(buffer))
               buffer = ''
               verbatimExit = True
            elif (currentChar == '\n'):
               verbatimBuffer.append(stringToLiteral(buffer))
               buffer = ''
               verbatimExit = True;
            else:
               buffer += currentChar;
            i+=1
         if (not verbatimExit):
            verbatimBuffer.append(stringToLiteral(buffer))
         buffer = ''
         tokens.append('\"' + '\\n'.join(verbatimBuffer) + '\"')
      # Address comments
      elif (currentChar == '#'):
         while (i < iterable):
            currentChar = text[i];
            if ( i < iterable - 1):
               nextChar = text[i + 1];
            if (currentChar == '\n'):
               break
            elif (isCRLF(currentChar, nextChar)):
               i+=1
               break
            i+=1
      # Address extraneous WS
      elif isWS(currentChar):
         while (isWS(currentChar)) & (i < iterable):
            i+=1
            if (i < iterable):
               currentChar = text[i]
      else:
         if (not isName(nextChar)):
            tokens.append(currentChar)
            i+=1
            continue
         buffer = currentChar
         i+=1
         while (i < iterable):
            currentChar = text[i]
            if (i < iterable - 1):
               nextChar = text[i+1]
            i+=1
            buffer += currentChar
            if (not isName(nextChar)): 
               break
         #buffer = buffer.encode('utf16','ignore')
         tokens.append("".join(buffer))
         #print tokens[-1:][0].decode('utf16','ignore')
   return tokens

def toJSON(text, indent=0):
   tokens = tokenize(text);
   indentLevel = 0;
   if (indent != '0'):
      if isinstance(indent, int):
         indent = '    ' * indent

   def newline():
      global ident
      global identLevel
      result = '\n';
      if (indent == '0'):
         return result;
      i = 0
      while ( i < indentLevel ):
         result += indent;
         i+=1
      return result;
   
   if (not isBeginOfBracket(tokens[0])):
      if len(tokens) > 1:
         if (tokens[1] == ':'):
            tokens.insert(0,'{');
            tokens.append('}');
         else: 
            tokens.insert(0,'[');
            tokens.append(']');

   i=0
   while(i < len(tokens)):
      token = tokens[i];

      if ( i < len(tokens) - 1):
         nextToken = tokens[i + 1];
      else:
         nextToken = None;

      if indent:
         if (token == ':'):
            tokens[i] += ' ';
         if (isBeginOfBracket(token[0])):
            indentLevel+=1;
         if (isEndOfBracket(token[0])):
            indentLevel-=1;

      if (isName(token[0]) & (nextToken == ':')):
         tokens[i] = '\"' + tokens[i] + '\"';

      if nextToken:
         if not (isNameSeparator(token[0]) | isNameSeparator(nextToken[0]) | isBeginOfBracket(token[0]) | isEndOfBracket(nextToken[0])):
            tokens[i] += ',';
            if (indent):
               tokens[i] += newline();
      i+=1

   if (indent):
      i=0
      while(i < len(tokens)):
         token = tokens[i];
         if i > 0:
            prevToken = tokens[i - 1];
         else:
            prevToken = None
         if i < len(tokens)-1:
            nextToken = tokens[i + 1];
         else:
            nextToken = None;

         if isBeginOfBracket(token[0]):
            indentLevel+=1;
            if nextToken:
               if not isEndOfBracket(nextToken[0]):
                  tokens[i] += newline();
         if isEndOfBracket(token[0]):
            indentLevel-=1;
            if prevToken:
               if not isBeginOfBracket(prevToken[0]):
                  tokens[i] = newline() + token;
         i+=1

   return ''.join(tokens)

def cson2json(csonString):
   return json.loads(toJSON(csonString))

loads = cson2json
