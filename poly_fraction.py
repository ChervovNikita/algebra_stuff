M = 3

def mul(a, b):
    c = [0 for _ in range(len(a) + len(b) - 1)]
    for i in range(len(a)):
        for j in range(len(b)):
            c[i + j] += a[i] * b[j]
            c[i + j] = c[i + j] % M
    return c

def val(a, x):
    res = 0
    coef = 1
    for i in a:
        res += i * coef
        coef *= x
    res %= M
    return res

def generate(deg, first):
    if deg == 0:
        for i in range(M):
            yield [i]
    else:
        for i in range(M):
            if i == 0 and first: continue
            for other in generate(deg - 1, False):
                t = other.copy()
                t.append(i)
                yield t

good = {}

for deg in range(1, 4 + 1):
    print('=========================')
    good[deg] = []
    if deg == 1:
        for i in range(M):
            good[deg].append([i, 1])
    else:
        for poly in generate(deg, True):
            ok = True
            for i in range(1, deg):
                j = deg - i
                for poly1 in generate(i, True):
                    for poly2 in generate(j, True):
                    	if ok and mul(poly1, poly2) == poly: 
                    		print(f'{poly} = {poly1} * {poly2}')
                    		ok = False
            if ok: good[deg].append(poly)
    counter = 0
    for poly in good[deg]:
        if poly[-1] == 1:
        	print(poly)
        	counter += 1
    print(counter)

