def binaryRemove(list, item, selectFunc):
    l = 0
    r = len(list)
    if r == 0: return False
    idx = (l + r)//2
    while l != r:
        if selectFunc(list[idx]) < selectFunc(item):
            l = idx + 1
        else:
            r = idx
        idx = (l + r)//2
    itemInList = list[idx] is item
    if itemInList: del list[idx]
    return itemInList