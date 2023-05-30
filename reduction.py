from copy import deepcopy
from time import sleep

def order(x, y):
    for i in range(len(x)):
        if x[i] < y[i]: return -1
        if x[i] > y[i]: return 1
    return 0

def mono_mul(x_, y_):
    x = deepcopy(x_)
    y = deepcopy(y_)
    c = list(x)
    for i in range(len(x)):
        c[i] += y[i]
    return tuple(c)

def mul(f_, g_):
    f = deepcopy(f_)
    g = deepcopy(g_)
    res = {}
    for mono_f, val_f in f.items():
        for mono_g, val_g in g.items():
            t = mono_mul(mono_f, mono_g)
            if t not in res: res[t] = 0
            res[t] += val_f * val_g
    return res

def add(f_, g_, x = 1):
    f = deepcopy(f_)
    g = deepcopy(g_)
    res = f
    for mono_g, val_g in g.items():
        if mono_g not in res: res[mono_g] = 0
        res[mono_g] += val_g * x
        if res[mono_g] == 0: del res[mono_g]
    return res

def tolist(f):
    listed = []
    for mono, s in f.items():
        listed.append((mono, s))
    listed.sort(reverse=True)
    # print(listed)
    return listed

def reduction(g, fs):
    print(tolist(g))
    for f in fs:
        print(f)
    ok = True
    while ok: 
        ok = False
        listed = tolist(g)
        for mono, s in listed:
            for idx, f in enumerate(fs):
                flist = tolist(f)
                coef_x = tuple([mono[i] - flist[0][0][i] for i in range(len(mono))])
                coef = {
                    coef_x: 1
                }
                if min(coef_x) < 0: continue
                x = s / flist[0][1]
                # print(g, f, coef, x)
                # print(f)
                # print(mul(f, coef))
                # print(add(g, mul(f, coef), -1))
                # print(f, coef)
                g = add(g, mul(f, coef), -int(x))
                ok = True
                print(idx + 1, ')  ', tolist(g))
                # sleep(0.2)
                break
            if ok: break
    
    # print(tolist(g))
    return g

def gcd(x, y):
    if not y: return x
    return gcd(y, x % y)

def red(x, y):
    return x // gcd(x, y), y // gcd(x, y)

def s_func(x, y):
    x_first, x_coef = tolist(x)[0]
    y_first, y_coef = tolist(y)[0]
    x_coef, y_coef = red(x_coef, y_coef)
    mono_x = tuple([max(0, y_first[i] - x_first[i]) for i in range(len(x_first))])
    mono_x = {
        mono_x: y_coef
    }
    mono_y = tuple([max(0, - y_first[i] + x_first[i]) for i in range(len(x_first))])
    mono_y = {
        mono_y: x_coef
    }
    return add(mul(mono_x, x), mul(mono_y, y), -1)

def grebners_basis(fs_):
    fs = deepcopy(fs_)
    ok = False
    while not ok:
        ok = True
        for i in range(len(fs)):
            for j in range(i + 1, len(fs)):
                s = s_func(fs[i], fs[j])
                res = reduction(s, fs)
                if res:
                    ok = False
                    fs.append(res)
                    break
            if not ok: break
    return fs

def contain(fs_, g_):
    fs = deepcopy(fs_)
    g_ = deepcopy(g_)
    fs = grebners_basis(fs)
    return not reduction(g_, fs)

# def MRBT(fs_): 
#     fs = deepcopy(fs_)
#     res = []
#     for i in range(len(fs)):
#         others = []
#         good = True
#         for j in range(len(fs)):
#             if j != i: fs.append(fs[j])
#             # check fraction
#         f = reduction(fs[i], others)
#         if f and good:
#             res.append(f)
#     return res

if __name__ == '__main__':
    f_1 = {
        (2, 0, 0): 1,
        (0, 2, 0): 2
    }
    f_2 = {
        (1, 0, 1): 1,
        (0, 1, 0): -1
    }
    print(tolist(s_func(f_1, f_2)))