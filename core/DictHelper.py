from .Value import Value
import json

def extract_set(md, val_name):
  s=set()
  for d in md:
    v = d.get(val_name, None)
    if v != None:
      s.add(v)
  s = sorted(s)
#  print(val_name + " : " + str(s))
  return s

def add_val(md_out, val_from, val_to):
  new = float(val_from)
  prev = md_out.get(val_to, None)
  if prev == None:
    md_out[val_to] = Value(new)
  else:
    md_out[val_to].add(new)

def get_val(md, el, op_type):
    r = md.get(el, None)
    if r == None:
      return r
    else:
      return getattr(r, 'get_' + op_type)()


def __filter_tuple(v, tup):
  for i in tup:
    if v == i: return True
  return False

def __filter(md, fd):
  for k in fd.keys():
    if not __filter_tuple(md[k], fd[k]): return False
  return True

def read_json_file(filename, filter_dict):
  input_res = []
  with open(filename) as fp:
    for cnt, line in enumerate(fp):
      line=line.strip()
      if not line.startswith("{"): continue
      mydict=json.loads(line)
      if __filter(mydict, filter_dict):
        input_res.append(mydict)
  return input_res
