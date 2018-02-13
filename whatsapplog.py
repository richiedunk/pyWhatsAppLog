import os
from datetime import datetime

class WhatsAppLog:

     def __init__(self, text):
          self.loadstring(text)

     def loadstring(self, text):
          # If text is a path, read it. If text is a string, use it.
          if os.path.isfile(text):
               with open(text, encoding="utf-8") as myfile:
                    self.rawtext = myfile.read()
          elif isinstance(text, str):
                    self.rawtext = text
          else:
                    raise ValueError('Not a valid filename or string')
          self.parsed = False

     def parse(self):
          # Take the raw input text and parse it to an array
          # Each item is [DateTime date&time, utf8 sender, utf8 text]
          stringarray = self.rawtext.split("\n")
          self.messages = []
          i = 0
          for line in stringarray:
               metadata1 = line.split(" - ")
               try:
                    msgdate = datetime.strptime(metadata1[0], "%d/%m/%Y, %H:%M")
               except ValueError:
                    # This isn't a new message, it's the second half of a multiline one. Add it to the previous msgtext.
                    self.messages[i-1][2] += ("\n" + line).encode("utf-8")
                    continue
               metadata2 = " - ".join(metadata1[1:]).split(": ")
               msgsender = metadata2[0].encode("utf-8")
               msgtext = ": ".join(metadata2[1:]).encode("utf-8")
               self.messages.append([msgdate, msgsender, msgtext])
               i += 1
          self.parsed = True

     def filter(self, beforedatetime = None, afterdatetime = None, sendercontains = None, textcontains = None):
          filtered = []
          for message in self.messages:
               add = False
               if beforedatetime and message[0] <= beforedatetime: add = True
               if afterdatetime  and message[0] >= beforedatetime: add = True
               if sendercontains and sendercontains.encode("utf-8") in message[1]: add = True
               if textcontains and textcontains.encode("utf-8") in message[2]: add = True
               if add: filtered.append(message)
          return filtered
