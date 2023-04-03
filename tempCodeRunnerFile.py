def read_pos(string):
    ls = string.split(',')
    return int(ls[0]), int(ls[1])

def write_pos(tup):
    return f'{str(tup[0])},{str(tup[1])}'