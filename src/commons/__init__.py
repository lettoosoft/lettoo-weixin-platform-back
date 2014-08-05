import hmac

from datetime import datetime
import os
from time import mktime
from uuid import uuid4

try:
    from hashlib import sha1
except ImportError:
    import sha

    sha1 = sha.sha


def get_epoch():
    dt = datetime.utcnow()
    sec_since_epoch = mktime(dt.timetuple()) + dt.microsecond / 1000000.0
    millis_since_epoch = sec_since_epoch * 1000
    return millis_since_epoch


def get_filename(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (str(uuid4()), ext)
    return os.path.join(instance._meta.model_name, filename)


def generate_key():
    # Get a random UUID.
    new_uuid = uuid4()
    # Hmac that beast.
    return hmac.new(str(new_uuid), digestmod=sha1).hexdigest()