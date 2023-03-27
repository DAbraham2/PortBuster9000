To download certs:
```
POST http://152.66.249.144/
```

with added body:
```json
{
  "neptun": "DASGYJ",
  "password": "crysys"
}
```

important to save session cookie!

Then to download cert & key:
```
GET http://152.66.249.144/getcert.php

GET http://152.66.249.144/getkey.php
```

Make sure to include cookie to the request