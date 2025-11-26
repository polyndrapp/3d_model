from PIL import Image
from Bresenham import draw_line, draw
from CyrusBeck import point2

def del_seq(arr):
	i = len(arr) - 1
	while i > 0:

		if arr[i] == arr[i - 1] + 1:
			arr.pop(i)
			break
		i -= 1
	if len(arr) % 2 == 1:
		arr.pop(len(arr) - 2)
	return arr


def fill2D(vertexes):
	points = dict()
	for i in range(len(vertexes)):
		x1, y1 = vertexes[i].x, vertexes[i].y
		x2 = vertexes[(i + 1) % len(vertexes)].x
		y2 = vertexes[(i + 1) % len(vertexes)].y

		if y2 == y1:
			continue

		line = draw_line(x1, y1, x2, y2)
		if y2 > y1:
			line.remove((x1, y1))
		else:
			line.remove((x2, y2))

		for point in line:
			if point[1] in points:
				points[point[1]].append(point[0])
			else:
				points[point[1]] = [point[0]]

	line = []
	for y in points:
		points[y].sort()
		if len(points[y]) % 2 == 1:
			points[y] = del_seq(points[y])
		for i in range(len(points[y]) // 2):
			line += [(k, y) for k in range(points[y][2 * i], points[y][2 * i + 1] + 1)]
	return line

if __name__ == '__main__':
	vertexes = [
		point2(250, 250),
		point2(250, 350),
	 	point2(350, 450),
	 	point2(450, 300),
	 	point2(550, 350),
	 	point2(550, 250),
	 	point2(450, 150),
	 	point2(400, 150),
	 	point2(350, 350)
	]

	pol_points = []
	with Image.open('fill.png') as im:
		im.paste((0, 0, 0), (0, 0, im.size[0], im.size[1]))

		points = fill2D(vertexes)
		draw(im, points, (0, 255, 0))

		im.save('fill.png')
