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