import sys
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import core.DictHelper as dh
import core.ParseInputArg as pia

in_var = pia.parse_input_arg()
input_res = dh.read_json_file(sys.argv[1], in_var.filter_dict, "mean")
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
    val_key = "time_calc"
    if val_key in d.keys():
      dh.add_val(lang_v[lang], d[val_key], nnodes)
      nb_node_set.add(nnodes)

nb_node_set = sorted(nb_node_set, key=float)

plt.style.use('dark_background')

def strong_scaling_speedup(lang_set, lang_v, nb_node_set):
  fig = plt.figure()
  ax = fig.gca()

  for lang in lang_set:
    v = dict()
    v2 = dict()
    for i in sorted(lang_v[lang].keys()):
      v[str(i)] = dh.get_val(lang_v[lang], i, op_type)
      v2[str(i)] = v[str(1)] / v[str(i)]
    ax.plot(v2.keys(), v2.values(), label=lang, marker='*')

  ideal = dict()
  for i in sorted(nb_node_set):
    ideal[str(i)] = i
  ax.plot(ideal.keys(), ideal.values(), label='Ideal Speedup')

  ax.set_yscale('log', basey=2)
  ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))
  ax.set_ylabel("Speedup")
  ax.set_xlabel("Nodes")

  plt.legend()
  plt.savefig("fig_strong_scaling_speedup.pdf")
  plt.close()

def strong_scaling(lang_set, lang_v):
  fig = plt.figure()
  ax = fig.gca()

  for lang in lang_set:
    v = dict()
    for i in sorted(lang_v[lang].keys()):
      v[str(i)] = dh.get_val(lang_v[lang], i, op_type)
    ax.plot(v.keys(), v.values(), label=lang, marker='*')

  ax.set_yscale('log', basey=2)
  ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))
  plt.locator_params(axis='y', numticks=30)
  ax.set_ylabel("Time (s)")
  ax.set_xlabel("Nodes")

  plt.legend()
  plt.savefig("fig_strong_scaling.pdf")
  plt.close()

def strong_scaling_latex_table(lang_set, lang_v, nb_node_set):
  print("\\begin{table*}")
  print("\\newcolumntype{C}{>{\centering\\arraybackslash}X}")
  print("\\begin{tabularx}{\\textwidth}{", end='')
  for i in range(len(nb_node_set) + 1):
    print("C", end='')
  print("}")

  print("Lang/#Nodes", end = ' ')
  for i in sorted(nb_node_set, key=float):
      print('&', end=' ')
      print(i, end=' ')
  print('\\\\ \hline')

  for lang in lang_set:
    print(lang, end=' ')
    for i in sorted(nb_node_set, key=float):
      print('&', end=' ')
      v = dh.get_val(lang_v[lang], i, op_type)
      if v != None:
        print(f'{v:.2f}', end=' ')
    print('\\\\')

  print('\hline')
  print("\\end{tabularx}")
  print("\\end{table*}")


def strong_scaling_bar(lang_set, lang_v, nb_node_set):
  fig = plt.figure()
  ax = fig.gca()
  width = 0.7

  pos_g = 0
  len_lang = len(lang_set)
  for lang in lang_set:
    v = dict()
    pos_l = 0
    for i in sorted(lang_v[lang].keys(), key=float):
      v[pos_l] = dh.get_val(lang_v[lang], i, op_type)
      pos_l = pos_l + 1
    v_keys = []
    for i in list(v.keys()):
      v_keys.append(i + pos_g * width / len_lang - width / 2 + width / len_lang / 2)
    ax.bar(v_keys, v.values(), width /len_lang, label=lang, align='center')
    pos_g = pos_g + 1

#  ax.set_yscale('log', basey=2)
  ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))
  ax.set_ylabel("Time (s)")
  ax.set_xlabel("Nodes")
  ax.set_xticklabels(nb_node_set, ha='right')
  ax.set_xticks(range(len(nb_node_set)))

  plt.legend()
  plt.savefig("fig_strong_scaling_bar.pdf")
  plt.close()

def strong_scaling_speedup_bar(lang_set, lang_v, nb_node_set):
  fig = plt.figure()
  ax = fig.gca()
  width = 0.7

  pos_g = 1
  len_lang = len(lang_set) + 1
  for lang in lang_set:
    v = dict()
    v2 = dict()
    pos_l = 0
    for i in sorted(lang_v[lang].keys(), key=float):
      v[pos_l] = dh.get_val(lang_v[lang], i, op_type)
      v2[pos_l] = v[0] / v[pos_l]
      pos_l = pos_l + 1
    v_keys = []
    for i in list(v.keys()):
      v_keys.append(i + pos_g * width / len_lang - width / 2 + width / len_lang / 2)
    ax.bar(v_keys, v2.values(), width /len_lang, label=lang, align='center')
    pos_g = pos_g + 1

  ideal = dict()
  incr = 0
  for i in sorted(nb_node_set):
    ideal[incr - width / 2 + width / len_lang / 2] = i
    incr += 1
  ax.bar(ideal.keys(), ideal.values(), width /len_lang, label='Ideal Speedup')

  ax.set_yscale('log', basey=2)
  ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))
  ax.set_ylabel("Speedup")
  ax.set_xlabel("Nodes")
  ax.set_xticklabels(nb_node_set, ha='right')
  ax.set_xticks(range(len(nb_node_set)))

  plt.legend()
  plt.savefig("fig_strong_scaling_speedup_bar.pdf")
  plt.close()

def strong_scaling_speedup_against_previous_bar(lang_set, lang_v, nb_node_set):
  fig = plt.figure()
  ax = fig.gca()
  width = 0.7

  pos_g = 0
  len_lang = len(lang_set)
  for lang in lang_set:
    v = dict()
    v2 = dict()
    slang = sorted(lang_v[lang].keys(), key=float)
    v[0] = dh.get_val(lang_v[lang], slang[0], op_type)

    pos_l = 1
    for i in slang[1:]:
      v[pos_l] = dh.get_val(lang_v[lang], i, op_type)
      v2[pos_l] = v[pos_l - 1] / v[pos_l]
      pos_l = pos_l + 1
    v2_keys = []
    for i in list(v2.keys()):
      v2_keys.append(i + pos_g * width / len_lang - width / 2 + width / len_lang / 2)
    ax.bar(v2_keys, v2.values(), width /len_lang, label=lang, align='center')
    pos_g = pos_g + 1

  ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))
  ax.set_ylabel("Speedup")
  ax.set_xlabel("Nodes")
  slang[0] = None
  ax.set_xticklabels(slang, ha='right')
  ax.set_xticks(range(len(slang)))
  ax.axhline(1, color = 'black', lw = 0.5)
  ax.axhline(2, color = 'black', lw = 0.5)

  plt.legend()
  plt.savefig("fig_strong_scaling_speedup_against_previous_bar.pdf")
  plt.close()

strong_scaling(lang_set, lang_v)
strong_scaling_bar(lang_set, lang_v, nb_node_set)
strong_scaling_speedup_bar(lang_set, lang_v, nb_node_set)
strong_scaling_speedup(lang_set, lang_v, nb_node_set)
strong_scaling_latex_table(lang_set, lang_v, nb_node_set)
strong_scaling_speedup_against_previous_bar(lang_set, lang_v, nb_node_set)
