from optparse import OptionParser


class InputError(Exception):
  """Exception raised for errors in the input.

  Attributes:
     expression -- input expression in which the error occurred
     message -- explanation of the error
  """

  def __init__(self, message):
    self.message = message


def add_args_to_dict(option, opt, value, parser):
  my_dict = getattr(parser.values, option.dest)
  split = value.split(':')
  if len(split) != 2:
    raise InputError(f'Got "-f {value}" as input value but expect -f filter_key:filter_value1,filter_value2')
  my_dict[split[0]] = split[1].split(',')

def get_comma_separated_args(option, opt, value, parser):
  setattr(parser.values, option.dest, value.split(','))


class Parser():
  def __init__(self):
    self.parser = OptionParser()
    self.add_option = self.parser.add_option

  def add_filter(self):
    self.add_option('-f', '--filter', type='string', action='callback', callback=add_args_to_dict, dest="filter_dict", default=dict())

  def add_not_show(self):
    self.add_option('-s', '--not_show', type='string', action='callback', callback=get_comma_separated_args, dest = 'not_show')

  def get_options(self):
   (options, args) = self.parser.parse_args()
   return options

