# pyWhatsAppLog
A Python3 class to parse and analyse WhatsApp logs (sent via the "Email chat" option)

Use with 

```
from whatsapplog import WhatsAppLog

parser = WhatsAppLog(source)
parser.parse()
```

The `source` can either be a filepath or a raw string. `parser.parsed` is True after a `parse()` has succeeded.

`parser.filter(criteria)` returns a filtered list of messages. The filters are named arguments and take the form...

* DateTime beforedatetime: Any message sent on or before this date/time will be returned
* DateTime afterdatetime: Any message sent on or after this date/time will be returned
* String sendercontains: Returns any message where the sender name contains this string.
* String textcontains: Returns any message where the message text contains this string.

So examples might be...

```
results = parser.filter(beforedatetime = datetime(2018, 1, 31, 17, 0), afterdatetime = datetime(2018, 1, 1, 9, 0))
# returns all messages sent between 9am on 1 January 2018 and 5pm on 31 January 2018

results = parser.filter(sendercontains = "Jim")
# returns all messages where the sender name contains "Jim" - so will include Jim, Jimmy, Jimbo etc

results = parser.filter(textcontains = "dog")
# returns all messages containing the word "dog"

results = parser.filter(textcontains = "birthday", sendercontains = "Queen", afterdatetime = datetime(2019, 6, 13, 0, 0))
# returns all messages the Queen might have sent you about her birthday after it happened
```  
