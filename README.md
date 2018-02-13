# pyWhatsAppLog
A Python3 class to parse and analyse WhatsApp logs (sent via the "Email chat" option)

Use with 

```
from whatsapplog import WhatsAppLog

parser = WhatsAppLog(source)
parser.parse()
```

The `source` can wither be a filepath or a raw string. `parser.parsed` is True after a `parse()` has succeeded.

`parser.filter(criteria)` returns a filtered lisk of messages. The filters take the form...

* DateTime beforedatetime: Any message sent on or before this date/time will be returned
* DateTime afterdatetime: Any message sent on or after this date/time will be returned
* String sendercontains: Returns any message where the sender name contains this string.
* String textcontains: Returns any message where the message text contains this string.

