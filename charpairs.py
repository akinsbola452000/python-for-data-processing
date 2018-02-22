import sys
paircounts = {}
for w in sys.argv[1:]:
    for i in range(1, len(w)):
        p = w[i-1:i+1]
        if p not in paircounts:
          paircounts[p] = 0
        paircounts[p] += 1
for p in sorted(paircounts):
  print '%s: %d occurrences' % (p, paircounts[p])
