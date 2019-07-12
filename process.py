import sys
import json
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import core.DictHelper as dh

input_res = []

def filter_dict(md):
  if md["machine"] != "Poincare": return False
  if md["datasize"] != "128": return False
  if md["test"] != "blockLU": return False
  if md["nb_cores"] != "129" and md["nb_cores"] != "128": return False
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

nb_block_set = dh.extract_set(input_res, "nb_blocks")
blocksize_set = dh.extract_set(input_res, "blocksize")
nb_proc_per_task_set = dh.extract_set(input_res, "nb_proc_per_task")
lang_set = dh.extract_set(input_res, "lang")

conv_list_el_to_int(nb_block_set)
conv_list_el_to_int(nb_proc_per_task_set)

op_type = "min"

ymlxmp_data = dict()
for nbb in nb_block_set:
  ymlxmp_data[nbb] = dict()

lang_v = dict()
for lang in lang_set:
  lang_v[lang] = dict()

for d in input_res:
  lang = d["lang"]
  if lang == "YML+XMP":
    nppt = int(d["nb_proc_per_task"])
    nbb = int(d["nb_blocks"])
    if nppt in nb_proc_per_task_set and nbb in ymlxmp_data.keys():
      dh.add_val(ymlxmp_data[nbb], d["time_io"], nppt)
  else:
    dh.add_val(lang_v[lang], d["time_io"], d["nb_cores"])


plt.style.use('dark_background')
fig = plt.figure()
ax = fig.gca()

for it in ymlxmp_data.keys():
  v = dict()
  for i in sorted(nb_proc_per_task_set):
    v[str(i)] = dh.get_val(ymlxmp_data[it], i, op_type)
  label = str(it) + " x " + str(it) + " blocks"
  ax.plot(v.keys(), v.values(), label=label, marker="o")


for lang in lang_set:
  if lang == "YML+XMP": continue
  v = dict()
  for i in sorted(lang_v[lang].keys()):
    v[str(i)] = dh.get_val(lang_v[lang], i, op_type)
  ax.plot(v.keys(), v.values(), label=lang, marker='x')

ax.set_xlabel("#core/task")
ax.set_ylabel("time (s)")

plt.legend()
plt.savefig("fig.pdf")
