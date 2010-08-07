
import datetime

ISO_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"

def strptime(val):
  if '.' not in val:
    return datetime.datetime.strptime(val, ISO_DATE_FORMAT)

  nofrag, frag = val.split(".")
  date = datetime.datetime.strptime(nofrag, ISO_DATE_FORMAT)

  frag = frag[:6]  # truncate to microseconds
  frag += (6 - len(frag)) * '0'  # add 0s
  return date.replace(microsecond=int(frag))
