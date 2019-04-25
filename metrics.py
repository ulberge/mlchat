from pandas import *
import matplotlib.pyplot as plt


def filter(arr, name):
    maxVal = max(arr)
    minVal = min(arr)
    # totVar = maxVal - minVal
    newArr = []
    for i, item in enumerate(arr):
        # newVal = (item - minVal) / totVar
        newVal = item
        newArr.append([i, newVal, name])

    return newArr


def readArrayFile(file_in_name):
    file = open(file_in_name)
    data = file.read()
    lines = data.split('\n')

    if lines[-1] == '':
        del lines[-1]

    data_array = []

    attr_map = dict([])
    wofeature_map = dict([])
    wfeature_map = dict([])
    # attr_hs_map = dict([])
    # attr_hl_map = dict([])

    for t, line in enumerate(lines):
        parts = line.split('/')
        if parts[-1] == '':
            del parts[-1]

        for j, part in enumerate(parts):
            pieces = part.split(',')
            # idx, attr, attr_hs, attr_hl = part.split(',')
            idx = pieces[0]
            attr = pieces[1]

            if idx in attr_map:
                attr_map[idx].append(float(attr))
            else:
                attr_map[idx] = [float(attr)]

            if (t % 2) == 0:
                if idx in wofeature_map:
                    wofeature_map[idx].append(float(attr))
                else:
                    wofeature_map[idx] = [float(attr)]
            else:
                if idx in wfeature_map:
                    wfeature_map[idx].append(float(attr))
                else:
                    wfeature_map[idx] = [float(attr)]

            # if idx in attr_hs_map:
            #     attr_hs_map[idx].append(float(attr_hs))
            # else:
            #     attr_hs_map[idx] = [float(attr_hs)]

            # if idx in attr_hl_map:
            #     attr_hl_map[idx].append(float(attr_hl))
            # else:
            #     attr_hl_map[idx] = [float(attr_hl)]

    # print wofeature_map
    # print wfeature_map
    # dirty = []
    # clean = []
    # for idx, arr in attr_map.iteritems():
    #     dist = min(wfeature_map[idx]) - max(wofeature_map[idx])
    #     if dist > 0:
    #         # is clean
    #         # positive distane between signals of with and without feature
    #         clean.append((idx, dist))
    #     else:
    #         # not clean, get rid of
    #         dirty.append(idx)

    # clean.sort(key=lambda x: x[1], reverse=True)

    # clean_attr_map = dict([])
    # for item in clean[:7]:
    #     idx, dist = item
    #     clean_attr_map[idx] = attr_map[idx]
    # for idx in dirty:
    #     del attr_map[idx]
    clean_attr_map = attr_map

    count = 0
    data_arr = []
    for idx, arr in clean_attr_map.iteritems():
        print 'append', idx
        f_arr = filter(arr, count)
        data_arr.append(('Attr ' + str(idx), f_arr))
        count += 1

    # for idx, arr in attr_hs_map.iteritems():
    #     f_arr = filter(arr, count)
    #     data_arr.append(('Attr W=5 ' + str(idx), f_arr))
    #     count += 1

    # for idx, arr in attr_hl_map.iteritems():
    #     f_arr = filter(arr, count)
    #     data_arr.append(('Attr W=20 ' + str(idx), f_arr))
    #     count += 1

    return data_arr


data_arr = readArrayFile('data.txt')

print 'render!', data_arr
name0, arr0 = data_arr[0]
df0 = DataFrame(arr0, columns=['time', 'norm val', 'type'])
ax = df0.plot.line(x='time', y='norm val', label=name0)

for i in range(1, len(data_arr)):
    print 'render', i
    name, arr = data_arr[i]
    df = DataFrame(arr, columns=['time', 'norm val', 'type'])
    df.plot.line(x='time', y='norm val', label=name, ax=ax)

plt.ylabel('Value')

plt.show()
