import numpy as np

def dot_product (A, B):
    A_dot_B  = A[0]*B[0]
    A_dot_B += A[1]*B[1]
    A_dot_B += A[2]*B[2]

    A_mag = A[0]**2 + A[1]**2 + A[2]**2
    B_mag = B[0]**2 + B[1]**2 + B[2]**2

    A_mag = np.sqrt(A_mag)
    B_mag = np.sqrt(B_mag)

    AB_cos = A_dot_B/(A_mag*B_mag)

    return A_dot_B, AB_cos 

def gradient(A):
    return np.gradient(A)

def magnitude(A):

    dim = len(A)

    A_mag = 0.0

    for i in range(dim):
        A_mag += A[i]**2

    return np.sqrt(A_mag)

def radial_vector(A_list):

    L = np.array(np.shape(A_list[0]))
    dim = len(L)

    mid = (L/2).astype(int)

    r  = [ np.array(range(L[i])) - mid[i] for i in range(dim)]

    # print(len(r))
    # print(tuple(r))

    R_mesh = np.meshgrid(*r)

    # print(np.shape(R_mesh))

    R = 0
    for i in range(dim):
        R += R_mesh[i]**2
    R = np.sqrt(R)

    AdotR = 0
    for i in range(dim):
        if i==0:
            AdotR += A_list[0]*R_mesh[1]
        elif i==1:
            AdotR += A_list[1]*R_mesh[0]
        else:
            AdotR += A_list[i]*R_mesh[i]

    AdotR = AdotR/R

    return AdotR