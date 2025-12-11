import open3d as o3d
from pathlib import Path


def triangulate_obj(in_path: str, out_path: str):
    """
    Преобразует многоугольные грани (с 4+ вершинами) в набор треугольников.
    Всё остальное (v, vt, vn, usemtl, mtllib и т.п.) просто копируется.
    Поддерживает форматы вершин в грани:
      f v1 v2 v3 v4
      f v1/vt1 v2/vt2 v3/vt3 v4/vt4
      f v1//vn1 v2//vn2 v3//vn3 ...
      f v1/vt1/vn1 ...
    """
    in_path = Path(in_path)
    out_path = Path(out_path)

    with in_path.open("r", errors="ignore") as fin, out_path.open("w") as fout:
        for line in fin:
            # если это не строка с гранью – просто копируем
            if not line.startswith("f "):
                fout.write(line)
                continue

            # парсим вершины грани
            parts = line.strip().split()[1:]  # всё после 'f'

            # если грань уже треугольная (или меньше) – не трогаем
            if len(parts) <= 3:
                fout.write(line)
                continue

            # фан-триангуляция: (v0, v1, v2), (v0, v2, v3), ...
            v0 = parts[0]
            for i in range(1, len(parts) - 1):
                tri = [v0, parts[i], parts[i + 1]]
                fout.write("f " + " ".join(tri) + "\n")


def main():
    # Имена файлов можно поменять под себя
    src_obj = "sandal.obj"       # исходный файл
    tri_obj = "sandal1.obj"   # файл только с треугольниками

    print(f"Триангуляция {src_obj} → {tri_obj} ...")
    triangulate_obj(src_obj, tri_obj)
    print("Готово, загружаем в Open3D...")

    # Загружаем уже триангулированную модель
    mesh = o3d.io.read_triangle_mesh(tri_obj)

    if not mesh.has_vertex_normals():
        mesh.compute_vertex_normals()

    print(mesh)  # короткая инфа о модели в консоли

    # Показываем окно с 3D моделью
    o3d.visualization.draw_geometries([mesh])


if __name__ == "__main__":
    main()
