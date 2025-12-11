# icosahedron.py
# Полный пример: строит icosahedron или dodecahedron и рисует видимые ребра (алгоритм Робертса)
# Требует: linalg.py в той же папке. :contentReference[oaicite:1]{index=1}

import math
import linalg
from PIL import Image, ImageDraw
import os

# ---------- Параметры ----------
MODE = "dodeca"   # "icosa" или "dodeca"
IMG_SIZE = (600, 600)
SCALE = 2.2       # масштаб общей фигуры (подгоняй)
OFFSET = (300, 300)  # сдвиг центра в пикселях
# ---------------------------------

phi = (1.0 + math.sqrt(5.0)) / 2.0

# --- helper: нормализация и векторные операции (локально) ---
def normalize(v):
    nx = math.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])
    return (v[0]/nx, v[1]/nx, v[2]/nx)

def add(a,b): return (a[0]+b[0], a[1]+b[1], a[2]+b[2])
def sub(a,b): return (a[0]-b[0], a[1]-b[1], a[2]-b[2])
def mul(a, s): return (a[0]*s, a[1]*s, a[2]*s)
def dot(a,b): return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]
def cross(a,b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])

# --- Построение икосаэдра (вершины + 20 треугольных граней) ---
def build_icosahedron(radius=60.0):
    # стандартная конфигурация (12 вершин)
    verts = [
        (-1,  phi,  0),
        ( 1,  phi,  0),
        (-1, -phi,  0),
        ( 1, -phi,  0),
        ( 0, -1,  phi),
        ( 0,  1,  phi),
        ( 0, -1, -phi),
        ( 0,  1, -phi),
        ( phi,  0, -1),
        ( phi,  0,  1),
        (-phi,  0, -1),
        (-phi,  0,  1)
    ]
    # нормализуем и масштабируем
    vlist = []
    for v in verts:
        nv = normalize(v)
        vlist.append((nv[0]*radius, nv[1]*radius, nv[2]*radius))

    # faces — стандартный набор 20 треугольников (0-based индексы)
    faces = [
        (0, 11, 5),
        (0, 5, 1),
        (0, 1, 7),
        (0, 7, 10),
        (0, 10, 11),
        (1, 5, 9),
        (5, 11, 4),
        (11, 10, 2),
        (10, 7, 6),
        (7, 1, 8),
        (3, 9, 4),
        (3, 4, 2),
        (3, 2, 6),
        (3, 6, 8),
        (3, 8, 9),
        (4, 9, 5),
        (2, 4, 11),
        (6, 2, 10),
        (8, 6, 7),
        (9, 8, 1)
    ]

    return vlist, faces

# --- Построение додекаэдра как двойственного к икосаэдру ---
# Мы используем центроиды граней икосаэдра как вершины додекаэдра.
# Грани додекаэдра соответствуют исходным вершинам икосаэдра:
# для каждой исходной вершины берем соседние грани (должно быть 5) и упорядочиваем их по углу.
def build_dodecahedron_from_icosa(radius=60.0):
    icosa_v, icosa_f = build_icosahedron(radius)
    # 1) центроиды всех граней (всего 20) -> это вершины додекаэдра
    centroids = []
    for f in icosa_f:
        a = icosa_v[f[0]]
        b = icosa_v[f[1]]
        c = icosa_v[f[2]]
        centroid = ((a[0]+b[0]+c[0])/3.0, (a[1]+b[1]+c[1])/3.0, (a[2]+b[2]+c[2])/3.0)
        # нормализуем и масштабируем немного — чтобы модель выглядела аккуратно
        centroids.append(centroid)

    # 2) Для каждой вершины икосаэдра найдём индексы граней, которые её содержат
    vertex_to_faces = [[] for _ in range(len(icosa_v))]
    for fi, f in enumerate(icosa_f):
        for vi in f:
            vertex_to_faces[vi].append(fi)

    # 3) Для каждой вершины получим порядок её смежных центроидов (пятиугольник)
    dodeca_faces = []
    for vi, face_indices in enumerate(vertex_to_faces):
        # face_indices должно содержать 5 элементов
        if len(face_indices) != 5:
            # На всякий случай — но для правильного икоса это не случится
            # print("Warning: vertex", vi, "has", len(face_indices), "adjacent faces")
            pass

        # центр исходной фигуры (0,0,0) — икоса у нас центрирован
        center = (0.0, 0.0, 0.0)
        # опорный вектор — направление от центра к вершине vi
        vpos = icosa_v[vi]
        n = normalize(vpos)

        # создаём локальную плоскость: берем произвольный вектор, не коллинеарный n
        arbitrary = (1.0, 0.0, 0.0)
        if abs(dot(n, arbitrary)) > 0.9:
            arbitrary = (0.0, 1.0, 0.0)
        # basis u,v ортонормированны и лежат в плоскости, перпендикулярной n
        u = normalize(cross(arbitrary, n))
        v = cross(n, u)

        # собираем центроиды и вычисляем углы в этой плоскости
        items = []
        for fi in face_indices:
            c = centroids[fi]
            vec = sub(c, vpos)  # вектор от вершины к центроиду
            # проекция на basis (u,v)
            xu = dot(vec, u)
            yv = dot(vec, v)
            ang = math.atan2(yv, xu)
            items.append((ang, fi))

        # сортируем по углу (чтобы грани шли по окружности)
        items.sort(key=lambda x: x[0])
        ordered_face_indices = [fi for (_, fi) in items]
        # dodeca face — последовательность индексов центроидов (0-based)
        dodeca_faces.append(tuple(ordered_face_indices))

    # centroids — 20 точек; dodeca_faces — 12 граней (по одной на каждую вершину икосаедра)
    # Однако сейчас dodeca_faces будут иметь по 5 индексов, но они ссылаются на индексы центроидов 0..19
    # Переведём к 1-based индексации, используемой в основном коде
    dodeca_vertices = centroids
    dodeca_faces_1based = [tuple(fi+1 for fi in face) for face in dodeca_faces]  # 1-based

    return dodeca_vertices, dodeca_faces_1based

# ---------- Figure wrapper ----------
class Figure:
    def __init__(self, which="icosa"):
        if which == "icosa":
            verts, faces = build_icosahedron(radius=60.0)
            # faces в 0-based -> преобразуем к 1-based и к тому формату, что в основном коде (любой размер граней)
            self.points = [(x, y, z) for (x, y, z) in verts]
            self.faces = [tuple(i+1 for i in face) for face in faces]
        elif which == "dodeca":
            verts, faces = build_dodecahedron_from_icosa(radius=60.0)
            self.points = [(x, y, z) for (x, y, z) in verts]
            self.faces = faces
        else:
            raise ValueError("Unknown figure: " + str(which))

# ---------- Матричные преобразования (как в твоём коде) ----------
def transform(M, figure):
    f = Figure()  # временный, будем перезаписывать точки
    f.points = list(figure.points)  # копируем
    for i in range(len(figure.points)):
        x, y, z, _ = linalg.MdotV(M, [figure.points[i][0], figure.points[i][1], figure.points[i][2], 1])
        f.points[i] = (x, y, z)
    return f

# ---------- Рендер и отрисовка (Roberts: N.z > 0 visible) ----------
def render(figure, filename="img.png"):
    img = Image.new('RGB', IMG_SIZE, (255,255,255))
    draw = ImageDraw.Draw(img)

    # базовая матрица: перенос + масштабирование + центрирование
    # сделаем сначала повороты (для наглядности), затем масштаб и перенос
    alpha = 30 * math.pi/180.0
    beta = 25 * math.pi/180.0

    Mrx = [
        [1, 0, 0, 0],
        [0, math.cos(alpha), -math.sin(alpha), 0],
        [0, math.sin(alpha), math.cos(alpha), 0],
        [0, 0, 0, 1]
    ]

    Mry = [
        [math.cos(beta), 0, math.sin(beta), 0],
        [0, 1, 0, 0],
        [-math.sin(beta), 0, math.cos(beta), 0],
        [0, 0, 0, 1]
    ]

    # масштаб+перенос
    Mscale = [
        [SCALE, 0, 0, OFFSET[0]],
        [0, SCALE, 0, OFFSET[1]],
        [0, 0, SCALE, 0],
        [0, 0, 0, 1]
    ]

    M = linalg.MdotM(Mscale, linalg.MdotM(Mry, Mrx))
    f1 = transform(M, figure)

    # --- автокоррекция ориентации граней (для выпуклых/правильных многогранников)
    cx = sum(p[0] for p in f1.points) / len(f1.points)
    cy = sum(p[1] for p in f1.points) / len(f1.points)
    cz = sum(p[2] for p in f1.points) / len(f1.points)

    fixed_faces = []
    for face in f1.faces:
        # берем первые три вершины для вычисления нормали
        pA = linalg.Point(f1.points[face[0]-1])
        pB = linalg.Point(f1.points[face[1]-1])
        pC = linalg.Point(f1.points[face[2]-1])

        v1 = linalg.Vector.construct(pA, pB)
        v2 = linalg.Vector.construct(pA, pC)
        N = linalg.getN(v1, v2)

        # центр грани
        fx = sum(f1.points[i-1][0] for i in face) / len(face)
        fy = sum(f1.points[i-1][1] for i in face) / len(face)
        fz = sum(f1.points[i-1][2] for i in face) / len(face)

        vx = fx - cx
        vy = fy - cy
        vz = fz - cz

        dotp = N.x*vx + N.y*vy + N.z*vz
        if dotp < 0:
            fixed_faces.append(tuple(reversed(face)))
        else:
            fixed_faces.append(face)

    f1.faces = fixed_faces
    # --- конец автокоррекции

    # рисуем видимые ребра
    for face in f1.faces:
        # вычисляем нормаль трёх точек
        p1 = linalg.Point(f1.points[face[0]-1])
        p2 = linalg.Point(f1.points[face[1]-1])
        p3 = linalg.Point(f1.points[face[2]-1])

        v1 = linalg.Vector.construct(p1, p3)
        v2 = linalg.Vector.construct(p1, p2)
        N = linalg.getN(v1, v2)

        # Roberts: видимая грань если N.z > 0
        if N.z > 0:
            size = len(face)
            for i in range(size):
                pa = f1.points[face[i]-1]
                pb = f1.points[face[(i+1)%size]-1]
                draw.line((round(pa[0]), round(pa[1]), round(pb[0]), round(pb[1])), fill=(0,0,0), width=2)

    img.save(filename)
    try:
        img.show()
    except Exception:
        print("Image saved to:", os.path.abspath(filename))

# ---------- Запуск ----------
if __name__ == "__main__":
    fig = Figure(which = "icosa" if MODE == "icosa" else "dodeca")

    print(f"Figure: {MODE}")
    print("Vertices:", len(fig.points), "Faces:", len(fig.faces))
    # небольшая инфа про первые несколько точек/граней
    print("first 6 vertices (x,y,z):")
    for i, p in enumerate(fig.points[:6], start=1):
        print(i, p)

    render(fig, "img.png")
    print("Saved img.png in", os.path.abspath("img.png"))
