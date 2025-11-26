from PIL import Image
from random import randint
from Bresenham import draw_line, draw
import time


class point2:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class polygon:
    def __init__(self, vertexes):
        self.vertexes = vertexes

    def cyruse_beck(self, a, b):
        normal = lambda p1, p2: point2(- (p1.y - p2.y), - (p2.x - p1.x))
        direction = lambda p1, p2: point2(p2.x - p1.x, p2.y - p1.y)
        scalar = lambda p1, p2: p1.x * p2.x + p1.y * p2.y

        t_begin = 0
        t_end = 1
        ab_vec = direction(a, b)

        new_a = point2(a.x, a.y)
        new_b = point2(b.x, b.y)
        for i in range(len(vertexes)):
            p1 = vertexes[i]
            p2 = vertexes[(i + 1) % len(vertexes)]
            p12_vec = direction(p1, p2)
            p12_norm = normal(p1, p2)

            p1a = direction(p1, a)

            scalar_abn = scalar(ab_vec, p12_norm)
            scalar_p1an = scalar(p1a, p12_norm)

            if scalar_abn == 0:
                if scalar_p1an > 0:
                    return None, None
                else:
                    return new_a, new_b
            elif scalar_abn > 0:
                t = -  scalar_p1an / scalar_abn
                if t > t_end:
                    continue
                t_begin = max(t_begin, t)
            elif scalar_abn < 0:
                t = - scalar_p1an / scalar_abn
                if t < t_begin:
                    continue
                t_end = min(t_end, t)

        if t_end > t_begin:
            if t_begin > 0:
                new_a.x = int(a.x + t_begin * ab_vec.x)
                new_a.y = int(a.y + t_begin * ab_vec.y)
            if t_end < 1:
                new_b.x = int(a.x + t_end * ab_vec.x)
                new_b.y = int(a.y + t_end * ab_vec.y)
        else:
            return None, None

        return new_a, new_b


if __name__ == '__main__':
    vertexes = [
        point2(250, 250),
        point2(250, 350),
        point2(350, 450),
        point2(450, 450),
        point2(550, 350),
        point2(550, 250),
        point2(450, 150),
        point2(350, 150)
    ]

    center = point2(400, 300)
    segment = polygon(vertexes)
    pol_points = []

    with Image.open('CyrusBeck.png') as im:
        im.paste((0, 0, 0), (0, 0, im.size[0], im.size[1]))

        for i in range(len(vertexes)):
            pol_points += draw_line(vertexes[i].x, vertexes[i].y,
                                    vertexes[(i + 1) % len(vertexes)].x,
                                    vertexes[(i + 1) % len(vertexes)].y)
        draw(im, pol_points, (0, 255, 0))

        start = time.time()
        for i in range(500):
            b = point2(randint(0, 799), randint(0, 599))
            a, b = segment.cyruse_beck(center, b)
            if a is not None and b is not None:
                line_points = draw_line(a.x, a.y, b.x, b.y)
                draw(im, line_points, (255, 0, 0))
        end = time.time()
        im.save('CyrusBeck.png')
        print(end - start)

# РЕЗУЛЬТАТ: 0.040863037109375 для 500 прямых
