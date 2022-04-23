import os
import hashlib
s = hashlib.sha1(os.urandom(24)).hexdigest()
print(s)

import hmac
import base64
val = 'cb01b64fce16b2092e30a593879c8bd192184a05'
hashed = hmac.new('liukun'.encode("utf-8"), 'Helloworld!'.encode("utf-8"), 'sha1')
a = hashed.hexdigest()
print(a)