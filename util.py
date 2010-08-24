
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


def PKCS7_pad(string, block):
  '''Returns a PKCS7-style padded string. See RFC 2315.
  The padding byte used is the value of the number of bytes of padding.
  '''
  bytes_to_pad = block - len(string) % block
  byte = chr(bytes_to_pad)
  return string + bytes_to_pad * byte

def PKCS7_unpad(string):
  '''Returns a PKCS7-style unpadded string. See RFC 2315.
  The value of padding bytes removed must equal the number of padding bytes.
  '''
  bytes_to_consider = ord(string[-1])
  for byte in string[-bytes_to_consider:]:
    if ord(byte) != bytes_to_consider:
      return string # not PKCS7 padded.
  return string[:-bytes_to_consider]