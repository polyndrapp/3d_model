import numpy as np
from PIL import Image
from Bresenham import draw, draw_line


def scale2D(points, sx, sy):
    new_points = []
    M = np.array([
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ])
    for i in range(len(points)):
        new_points.append(points[i] @ M.T)

    return new_points


def reflect2D(points, line, axis=1):
    new_points = []
    if axis == 1:
        M = np.array([
            [1, 0, 0],
            [0, -1, 2 * line],
            [0, 0, 1]
        ])
    else:
        M = np.array([
            [-1, 0, 2 * line],
            [0, 1, 0],
            [0, 0, 1]
        ])
    for i in range(len(points)):
        new_points.append(points[i] @ M.T)

    return new_points


def rotate2D(points, angle):
    new_points = []
    M = np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle), np.cos(angle), 0],
        [0, 0, 1]
    ])
    for i in range(len(points)):
        new_points.append(points[i] @ M.T)

    return new_points


def shift2D(points, dx, dy):
    new_points = []
    M = np.array([
        [1, 0, dx],
        [0, 1, dy],
        [0, 0, 1]
    ])
    for i in range(len(points)):
        new_points.append(points[i] @ M.T)

    return new_points


if __name__ == '__main__':
    vertexes2D = [
        np.array([[250, 250, 1]]),
        np.array([[250, 350, 1]]),
        np.array([[350, 450, 1]]),
        np.array([[450, 300, 1]]),
        np.array([[550, 350, 1]]),
        np.array([[550, 250, 1]]),
        np.array([[450, 150, 1]]),
        np.array([[400, 150, 1]]),
        np.array([[350, 350, 1]])
    ]

    with Image.open('2D.png') as im:
        im.paste((0, 0, 0), (0, 0, im.size[0], im.size[1]))

        pol_points = []
        for i in range(len(vertexes2D)):
            pol_points += draw_line(vertexes2D[i][0][0], vertexes2D[i][0][1],
                                    vertexes2D[(i + 1) % len(vertexes2D)][0][0],
                                    vertexes2D[(i + 1) % len(vertexes2D)][0][1])
        draw(im, pol_points, (255, 0, 0))

        vertexes2D = rotate2D(vertexes2D, 0.1)
        pol_points = []
        for i in range(len(vertexes2D)):
            pol_points += draw_line(int(vertexes2D[i][0][0]), int(vertexes2D[i][0][1]),
                                    int(vertexes2D[(i + 1) % len(vertexes2D)][0][0]),
                                    int(vertexes2D[(i + 1) % len(vertexes2D)][0][1]))
        draw(im, pol_points, (0, 255, 0))

        vertexes2D = shift2D(vertexes2D, 50, 50)
        pol_points = []
        for i in range(len(vertexes2D)):
            pol_points += draw_line(int(vertexes2D[i][0][0]), int(vertexes2D[i][0][1]),
                                    int(vertexes2D[(i + 1) % len(vertexes2D)][0][0]),
                                    int(vertexes2D[(i + 1) % len(vertexes2D)][0][1]))
        draw(im, pol_points, (0, 0, 255))

        vertexes2D = scale2D(vertexes2D, 0.2, 0.2)
        pol_points = []
        for i in range(len(vertexes2D)):
            pol_points += draw_line(int(vertexes2D[i][0][0]), int(vertexes2D[i][0][1]),
                                    int(vertexes2D[(i + 1) % len(vertexes2D)][0][0]),
                                    int(vertexes2D[(i + 1) % len(vertexes2D)][0][1]))
        draw(im, pol_points, (255, 0, 0))

        vertexes2D = reflect2D(vertexes2D, 300, 1)
        pol_points = []
        for i in range(len(vertexes2D)):
            pol_points += draw_line(int(vertexes2D[i][0][0]), int(vertexes2D[i][0][1]),
                                    int(vertexes2D[(i + 1) % len(vertexes2D)][0][0]),
                                    int(vertexes2D[(i + 1) % len(vertexes2D)][0][1]))
        draw(im, pol_points, (255, 0, 0))

        vertexes2D = reflect2D(vertexes2D, 400, 0)
        pol_points = []
        for i in range(len(vertexes2D)):
            pol_points += draw_line(int(vertexes2D[i][0][0]), int(vertexes2D[i][0][1]),
                                    int(vertexes2D[(i + 1) % len(vertexes2D)][0][0]),
                                    int(vertexes2D[(i + 1) % len(vertexes2D)][0][1]))
        draw(im, pol_points, (255, 0, 0))

        im.save('2D.png')
