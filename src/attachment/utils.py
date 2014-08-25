import os
from uuid import uuid4


def get_attachment_filename(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (str(uuid4()), ext)
    file_path = 'attachment/%s/' % instance.user
    return os.path.join(file_path, filename)