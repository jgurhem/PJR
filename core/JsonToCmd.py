from . import DictHelper as dh

def prime_numbers_dec(N):
  primes = []
  p = 2
  while N >= p * p:
    if N % p == 0:
      primes.append(p)
      N = int(N / p)
    else:
      p = p + 1
  primes.append(N)
  return primes

def divisors(N):
  div = set()
  div.add(1)
  div.add(N)
  p = 2
  while N >= p * p:
    if N % p == 0:
      div.add(p)
      div.add(int(N / p))
    p = p + 1
  return sorted(div)

def round_multipliers(N):
  primes = prime_numbers_dec(N)
  a = 1
  b = 1
  for i in primes:
    if a < b:
      a *= i
    else:
      b *= i
  if a < b:
    tmp = a
    a = b
    b = tmp
  return (a, b)

def dict_to_cmd(md):
  if md["machine"] != "Poincare": return None
  if md["lang"] == "YML+XMP":
    s = "bash compile_in_batch.sh"
    s += " " + md["test"]
    s += " " + md["nb_blocks"]
    s += " " + md["blocksize"]
    nppt = int(md["nb_proc_per_task"])
    rm = round_multipliers(nppt)
    s += " " + str(nppt)
    s += " " + str(rm[0])
    s += " " + str(rm[1])
    s += " " + md["nb_cores"]
    s += " " + md["nb_nodes"]
    s += " Poincare LoadLeveler ~/results_scaling_tests.json 1"
    return s
  if md["lang"] == "PaRSEC" or md["lang"] == "HPX" or md["lang"] == "Regent":
    s = "bash scripts/poincare/submit.sh"
    s += " " + md["nb_nodes"]
    s += " " + md["datasize"]
    s += " " + md["nb_blocks"]
    return s
  if md["lang"] == "MPI" or md["lang"] == "XMP" or md["lang"] == "SCA":
    s = "bash scripts/poincare/submit.sh"
    s += " " + md["nb_nodes"]
    s += " " + md["datasize"]
    s += " " + md["lang"]
    s += " " + md["test"]
    return s
  return None

