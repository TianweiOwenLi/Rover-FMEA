def qsort(arr, a, b):
    if (b-a) > 1:
        pivot = arr[a][1]
        i, j = a+1, b-1
        while True:
            while (i<b and arr[i][1] >= pivot): i += 1
            while (j>a and arr[j][1] <= pivot): j -= 1
            if (i > j): break
            arr[i], arr[j] = arr[j], arr[i]
        arr[a], arr[j] = arr[j], arr[a]
        qsort(arr, a, j)
        qsort(arr, i, b)

def dsort(d):
  l = list(d.items())
  qsort(l, 0, len(l))
  sd = {}
  for (lbl, idx) in l: sd[lbl] = idx
  return sd
