import numpy as np
from PIL import Image
from Bresenham import draw, draw_line
from z_buffer import point3, fill3D, draw_buffer, update_buffer 

def rotate3D(points, angle, axis=1): # 1-z, 2-x, 3-y
	new_points = to_numpy(points)
	if axis == 1:
		M = np.array([
			[np.cos(angle), -np.sin(angle), 0, 0],
			[np.sin(angle),  np.cos(angle), 0, 0],
			[0, 0, 1, 0],
			[0, 0, 0, 1]
		])
	elif axis == 2:
		M = np.array([
			[1, 0, 0, 0],
			[0, np.cos(angle), -np.sin(angle), 0],
			[0, np.sin(angle),  np.cos(angle), 0],
			[0, 0, 0, 1]
		])
	elif axis == 3:
		M = np.array([
			[np.cos(angle), 0, -np.sin(angle), 0],
			[0, 1, 0, 0],
			[np.sin(angle), 0,  np.cos(angle), 0],
			[0, 0, 0, 1]
		])

	for i in range(len(points)):
		new_points[i] = new_points[i] @ M.T

	return to_point3(new_points)

def shift3D(points, dx, dy, dz):
	new_points = to_numpy(points)
	M = np.array([
			[1, 0, 0, dx],
			[0, 1, 0, dy],
			[0, 0, 1, dz],
			[0, 0, 0, 1]
		])

	for i in range(len(points)):
		new_points[i] = new_points[i] @ M.T

	return to_point3(new_points)

def scale3D(points, sx, sy, sz):
	new_points = to_numpy(points)
	M = np.array([
			[sx, 0, 0, 0],
			[0, sy, 0, 0],
			[0, 0, sz, 0],
			[0, 0, 0, 1]
		])

	for i in range(len(points)):
		new_points[i] = new_points[i] @ M.T

	return to_point3(new_points)

def reflect3D(points, line, axis=1): # 1-z, 2-x, 3-y
	new_points = to_numpy(points)
	if axis == 1:
		M = np.array([
				[1, 0, 0, 0],
				[0, 1, 0, 0],
				[0, 0, -1, 2 * line],
				[0, 0, 0, 1]
			])
	elif axis == 2:
		M = np.array([
				[-1, 0, 0, 2 * line],
				[0, 1, 0, 0],
				[0, 0, 1, 0],
				[0, 0, 0, 1]
			])
	elif axis == 3:
		M = np.array([
				[1, 0, 0, 0],
				[0, -1, 0, 2 * line],
				[0, 0, 1, 0],
				[0, 0, 0, 1]
			])

	for i in range(len(points)):
		new_points[i] = new_points[i] @ M.T

	return to_point3(new_points)

def to_numpy(points):
	new_points = []
	for point in points:
		new_points.append(np.array([[point.x, point.y, point.z, 1]]))
	return new_points

def to_point3(points):
	new_points = []
	for point in points:
		new_points.append(point3(int(point[0][0]), int(point[0][1]), int(point[0][2])))
	return new_points

if __name__ == '__main__':
	vertexes1 = [
		point3(300, 300, 100),
		point3(350, 400, 100),
	 	point3(500, 150, 300)
	]

	vertexes2 = [
		point3(200, 100, 0),
		point3(400, 400, 200),
		point3(500, 200, 200)
	]

	with Image.open('3D.png') as im:
		im.paste((0, 0, 0), (0, 0, im.size[0], im.size[1]))
		
		z_buffer = [1000] * 800 * 600

		points1 = fill3D(vertexes1)
		points2 = fill3D(vertexes2)

		points1 = reflect3D(points1, 400, 2)
		points2 = reflect3D(points2, 400, 2)

		update_buffer(points1, z_buffer)
		update_buffer(points2, z_buffer)

		draw_buffer(im, points2, z_buffer, (0, 0, 255))
		draw_buffer(im, points1, z_buffer, (255, 0, 0))
		
		im.save('3D.png')
