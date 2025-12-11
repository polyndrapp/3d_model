import math

class Point:
    def __init__(self, point):
        self.x, self.y, self.z = point 

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @staticmethod
    def construct(p1, p2):
        vx = p2.x - p1.x
        vy = p2.y - p1.y
        vz = p2.z - p1.z
        return Vector(vx, vy, vz)

def getN(v1, v2):
    return Vector(v1.y*v2.z - v1.z*v2.y,
                  v1.z*v2.x - v1.x*v2.z,
                  v1.x*v2.y - v1.y*v2.x)

def MdotM(M1, M2):
    M = []
    for i in range(4):
        M.append([0]*4)
    for i in range(4):
        for j in range(4):
            for k in range(4):
                M[i][j] += M1[i][k]*M2[k][j]

    return M

def MdotV(M, V):
    R = [0]*4
    for i in range(4):
        for j in range(4):
            R[i] += M[i][j]*V[j]

    return R
