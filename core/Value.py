class Value:
  def __init__(self, val):
    self.__n = 1
    self.__sum = val
    self.__min = val
    self.__max = val

  def add(self, val):
    self.__n += 1
    self.__sum += val
    self.__min = min(self.__min, val)
    self.__max = max(self.__max, val)

  def get_mean(self):
    return self.__sum / self.__n

  def get_min(self):
    return self.__min

  def get_max(self):
    return self.__max
