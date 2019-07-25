from optparse import OptionParser


class InputError(Exception):
  """Exception raised for errors in the input.

  Attributes:
     expression -- input expression in which the error occurred
     message -- explanation of the error
  """

  def __init__(self, message):
    self.message = message


def get_comma_separated_args(option, opt, value, parser):
  my_dict = getattr(parser.values, option.dest)
  split = value.split(':')
  if len(split) != 2:
    raise InputError(f'Got "-f {value}" as input value but expect -f filter_key:filter_value1,filter_value2')
  my_dict[split[0]] = split[1].split(',')


def parse_input_arg():
  parser = OptionParser()
  parser.add_option('-f', '--foo', type='string', action='callback', callback=get_comma_separated_args, dest="filter_dict", default=dict())
  (options, args) = parser.parse_args()
  return options
