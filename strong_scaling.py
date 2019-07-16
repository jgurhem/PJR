import sys
import json
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import core.DictHelper as dh

input_res = []

def filter_dict(md):
  if md["machine"] != "Poincare": return False
#  if md["datasize"] != "8192": return False
  if md["datasize"] != "16384": return False
  if md["test"] != "blockLU": return False
  if md["success"] != "true": return False
  return True

def conv_list_el_to_int(ml):
  for i in range(len(ml)):
    ml[i] = int(ml[i])

with open(sys.argv[1]) as fp:
  for cnt, line in enumerate(fp):
    line=line.strip()
    if not line.startswith("{"): continue
    mydict=json.loads(line)
    if filter_dict(mydict):
      input_res.append(mydict)

lang_set = dh.extract_set(input_res, "lang")

op_type = "min"

lang_v = dict()
for lang in lang_set:
  lang_v[lang] = dict()

nb_node_set = set()
for d in input_res:
  lang = d["lang"]
  nnodes = int(d["nb_nodes"])
  if lang == "YML+XMP":
    if nnodes < 2:
      print("error : YML+XMP number of nodes < 2")
      sys.exit(1)
    dh.add_val(lang_v[lang], d["time_io"], nnodes - 1)
    nb_node_set.add(nnodes - 1)
  else:
    dh.add_val(lang_v[lang], d["time_calc"], nnodes)
    nb_node_set.add(nnodes)


plt.style.use('dark_background')
fig = plt.figure()
ax = fig.gca()

for lang in lang_set:
  v = dict()
  v2 = dict()
  for i in sorted(lang_v[lang].keys()):
    v[str(i)] = dh.get_val(lang_v[lang], i, op_type)
    v2[str(i)] = v[str(1)] / v[str(i)]
#  ax.plot(v.keys(), v.values(), label=lang, marker='o')
  ax.plot(v2.keys(), v2.values(), label=lang, marker='*')

ideal = dict()
incr = 1
for i in sorted(nb_node_set):
  ideal[str(i)] = i
  incr += 1
ax.plot(ideal.keys(), ideal.values(), label='Ideal Speedup')

ax.set_yscale('log', basey=2)
ax.set_ylabel("Speedup")
ax.set_xlabel("Nodes")

plt.legend()
plt.savefig("fig_strong_scaling.pdf")
plt.close()

