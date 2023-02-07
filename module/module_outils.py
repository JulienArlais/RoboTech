import numpy as np

def format(nb):
	return "{:.2f}".format(nb)

def distance(x1, y1, x2, y2):
		"""donne la distance entre (x1, y1) et (x2, y2)
		Args:
			x1 (float): coordonnée x réelle
			y1 (float): coordonnée y réelle
			x2 (float): coordonnée x réelle
			y2 (float): coordonnée y réelle
		Returns:
			float: distance
		"""
		dist = np.sqrt(np.square(x2 - x1)+np.square(y2 - y1))
		#print("Distance entre (", format(x1), ",", format(y1), ") et (", format(x2), ",", format(y2), ") :", format(dist))
		return dist

def create_circle(x, y, r, canvas, color): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_oval(x0, y0, x1, y1, fill = color)