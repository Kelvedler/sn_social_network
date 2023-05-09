import math
from datetime import datetime
from django.utils import timezone


def get_now():
    return timezone.now()


def to_timestamp(value: datetime, as_milliseconds=True):
    return math.ceil(value.timestamp() * (1000 if as_milliseconds else 1)) if value else None
