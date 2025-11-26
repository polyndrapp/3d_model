import matplotlib.pyplot as plt
import numpy as np

# Функция для рисования прямой линии с использованием алгоритма Брезенхема
def draw_line(x1, y1, x2, y2, image):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    steep = dy > dx
    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    error = int(dx / 2)
    y_step = 1 if y1 < y2 else -1
    y = y1
    for x in range(x1, x2 + 1):
        coord = (y, x) if steep else (x, y)
        image[coord] = 1
        error -= dy
        if error < 0:
            y += y_step
            error += dx

# Запрос размера изображения у пользователя
width = 50
height = 50

# Создаем изображение с заданными размерами
image = np.zeros((height, width), dtype=np.uint8)

# Запрос координат начальной и конечной точек у пользователя
x1 = 10
y1 = 10
x2 = 30
y2 = 20

# Вызываем функцию для рисования линии
draw_line(x1, y1, x2, y2, image)

# Отображаем изображение
plt.imshow(image, cmap='gray')
plt.axis('off')
plt.show()
