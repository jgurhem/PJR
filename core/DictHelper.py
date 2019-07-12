from .Value import Value

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

