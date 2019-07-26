import sys
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import core.DictHelper as dh
import core.ParseInputArg as pia

in_var = pia.parse_input_arg()
input_res = dh.read_json_file(sys.argv[1], in_var.filter_dict, "val")

for d in input_res:
  new_d = dict()
  for k, v in d.items():
    if k in in_var.not_show: continue
    new_d[k] = v
  print(new_d)
