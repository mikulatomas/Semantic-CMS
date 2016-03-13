from os.path import splitext
from hashlib import sha1
# Time
import datetime
from django.utils import timezone

import uuid

default_quality = 60

def upload_to_id_image(instance, filename):
    extension = splitext(filename)[1].lower()
    path = 'images/%(time_now)s_%(uuid)s' % {
                                         'time_now': timezone.now().strftime("%Y%m%d_%H%M%S"),
                                         'uuid': uuid.uuid1().time_hi_version }
    return '%(path)s%(extension)s' % {'path': path,
                                          'extension': extension}
