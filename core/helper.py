import os


def isfloat(num):
    if num == 'nan':
        return False
    try:
        float(num)
        return True
    except ValueError:
        return False


def match(a, b):
    return [b.index(x) if x in b else None for x in a]


def check_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
