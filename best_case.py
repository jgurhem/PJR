import sys
import core.DictHelper as dh
import core.ParseInputArg as pia
import core.JsonToCmd as jtc

parser = pia.Parser()
parser.add_filter()
parser.add_not_show()
parser.add_option('--best_case', action='store', dest="best_case_value", default="time_calc", help='time value used to sort the cases')
parser.add_option('--cmd', action='store_true', dest="to_cmd", default=False, help='print commands to perform the test')
parser.add_option('--add-cmd', action='store_true', dest="add_cmd", default=False, help='print supplementary commands to perform the test')
parser.add_option('-N', '--number_show', action='store', dest="number_values_shown", type=int, default=0, help="show N best cases, default : show all (N=0)")
parser.add_option('--prefix', action='store', dest="prefix", type=str, default="", help="command prefix")
parser.add_option('--suffix', action='store', dest="suffix", type=str, default="", help="command suffix")
in_var = parser.get_options()

def my_key(i):
  t = []
  t.append(i["lang"])
  t.append(float(i["nb_nodes"]))
  t.append(float(i[in_var.best_case_value].get_mean()))
  i["tmp_key_sort_best_case"] = (i["lang"], i["nb_nodes"])
  return t

def isCasePerformed(in_md, case):
  for d in in_md:
    if (d["lang"], d["nb_nodes"], d["datasize"], d["nb_blocks"]) == (case["lang"], case["nb_nodes"], case["datasize"], case["nb_blocks"]):
      return True
  return False


input_res = dh.read_json_file(sys.argv[1], in_var.filter_dict, "val")
input_res = sorted(input_res, key = my_key)

in_var.not_show.append("tmp_key_sort_best_case")

old_d = None
counter = dict()
for d in input_res:
  new_d = dict()
  counter[d["tmp_key_sort_best_case"]] = counter.get(d["tmp_key_sort_best_case"], 0) + 1
  if in_var.number_values_shown != 0 and counter.get(d["tmp_key_sort_best_case"], 0) > in_var.number_values_shown: continue
  for k, v in d.items():
    if k in in_var.not_show: continue
    new_d[k] = v
  print(new_d)
  if in_var.to_cmd:
    print(in_var.prefix + jtc.dict_to_cmd(d) + in_var.suffix)
  if in_var.add_cmd and old_d !=None and d["tmp_key_sort_best_case"] == old_d["tmp_key_sort_best_case"]:
    d_copy = dict()
    for k, v in d.items():
      d_copy[k] = v
    d_copy["nb_blocks"] = str(int((int(d["nb_blocks"]) + int(old_d["nb_blocks"])) / 2))
    if not isCasePerformed(input_res, d_copy):
      print(in_var.prefix + jtc.dict_to_cmd(d_copy) + in_var.suffix)
  old_d = d
