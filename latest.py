import sys
import core.DictHelper as dh
import core.ParseInputArg as pia
import core.JsonToCmd as jtc

parser = pia.Parser()
parser.add_filter()
parser.add_not_show()
parser.add_option('-N', '--number_show', action='store', dest="number_values_shown", type=int, default=0, help="show N best cases, default : show all (N=0)")
in_var = parser.get_options()

def my_key(i):
  t = []
  t.append(i["date"])
  return t

input_res = dh.read_json_file_raw(sys.argv[1], in_var.filter_dict, "val")
input_res = sorted(input_res, key = my_key, reverse=True)

in_var.not_show.append("tmp_key_sort_best_case")

incr = 0
for d in input_res:
  new_d = dict()
  if in_var.number_values_shown != 0 and incr > in_var.number_values_shown: break
  for k, v in d.items():
    if k in in_var.not_show: continue
    new_d[k] = v
  print(new_d)
  incr += 1
