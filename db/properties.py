
from google.appengine.ext import db
import pickle

class DictProperty(db.StringListProperty):
  '''Support for creating Dictionary Properties in Google's App Engine.
  Authors:
    peej <Paul James>
    jbenet <Juan Batiz-Benet>
  '''
  data_type = dict
  data_value_type = str

  def __init__(self, value_type=None, **kwds):
    ''' Constructs this property.

    Args:
      value_type: the class that all values should be an instance of. Values
      will be passed in to the constructor of this class.
    '''
    db.StringListProperty.__init__(self, **kwds)
    if value_type:
      self.data_value_type = value_type

  def get_value_for_datastore(self, model_instance):
    ''' Returns the pickled value for the datastore. '''
    value = super(DictProperty, self).get_value_for_datastore(model_instance)
    return db.Blob(pickle.dumps(value))
    #TODO(jbenet) reconsider not pickling for base types.
    # This would make the dictionaries editable via datastore viewer.

  def make_value_from_datastore(self, value):
    ''' Returns the unpickled value from the datastore. '''
    if value is None:
      return dict()
    return pickle.loads(value)

  def default_value(self):
    ''' Returns the default value for this property, or an empty dictionary.'''
    if self.default is None:
      return dict()
    else:
      return super(DictProperty, self).default_value().copy()

  def validate(self, value):
    ''' Checks whether value is a valid value for this property.

    Args:
      value: the input value to check.

    Returns:
      value, if it is valid. Otherwise, a BadValueError is raised.
    '''
    if not isinstance(value, dict):
      raise db.BadValueError('Property %s needs to be convertible '
                  'to a dict instance (%s) of class dict' % (self.name, value))

    for key in value:
      if not isinstance(value[key], self.data_value_type):
        raise db.BadValueError('Value for key %s of property %s needs to be '
                'an instance of class %s', key, self.name, self.data_value_type)

    return value

  def empty(self, value):
    ''' Returns whether the value is empty. '''
    return value is None

  def get_value_for_form(self, instance):
    '''Converts the property value to the form value

    Args:
      instance: the property instance.

    Returns:
      A multiline string, where each line is a comma separated key-value pair.
      Each value is passed to str().
    '''
    value = super(DictProperty, self).get_value_for_form(instance)
    if not value:
      pass
    elif isinstance(value, dict):
      value = map(lambda k: "%s,%s" % (k, str(value[k])), value)
      value = '\n'.join(value)
    return value

  def make_value_from_form(self, form_input):
    '''Converts a form value to the property value.

    Args:
      form_input: multiline string, where each line is a comma separated
      key-value pair.

    Returns:
      The dictionary to store in the datastore. Each the value is passed in to
      the constructor of data_value_type.
    '''
    result = {}
    if not form_input:
      pass
    elif isinstance(form_input, basestring):
      lines = form_input.splitlines()
      form_input = {}
      for line in lines:
        line = line.split(',')
        result[line[0]] = self.data_value_type(line[1])
    return result

