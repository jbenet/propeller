
from google.appengine.ext.webapp import template
from google.appengine.ext.db.djangoforms import forms

class DateTimeField(forms.DateTimeField):
  def clean(self, value):
    microseconds = 0
    if value and '.' in value:
      value, frag = value.rsplit('.', 1)
      frag = frag[:6]  # truncate to microseconds
      frag += (6 - len(frag)) * '0'  # add 0s
      try:
        microseconds = int(frag)
      except ValueError:
        raise ValidationError('invalid microseconds entered')

    value = super(DateTimeField, self).clean(value)
    if value:
      value = value.replace(microsecond=microseconds)
    return value