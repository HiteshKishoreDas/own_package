import numpy as np


def coloumb(sigma, x):
    E = []
    for i in range(len(x)):
        r = x - x[i]
        cond = r != 0
        E_i = np.trapz(-np.sign(r[cond]) * sigma[cond] / r[cond] ** 2, x=x[cond])
        E.append(E_i)

    E = np.array(E)

    return E
