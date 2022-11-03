def binaryInsert(list, item, selectFunc):
    l = 0
    r = len(list)
    idx = (l + r)//2
    while l != r:
        if selectFunc(list[idx]) < selectFunc(item):
            l = idx + 1
        else:
            r = idx
        idx = (l + r)//2
    list.insert(l, item)