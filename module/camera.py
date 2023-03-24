import cv2
import numpy as np
from module.controleur import StrategieAvance, StrategieAngle, StrategieArretMur, StrategieSeq

class BaliseException(Exception):
	def __init__(self, message):
		"""constructeur de l'exception

		Args:
			message (string): message de l'exception
		"""
		self.message = message
		
def detect(data):
	# lecture + dimensions de l'image
	image = cv2.imread(data)
	height = image.shape[0]
	width = image.shape[1]

	# conversion en niveau de gris + algorithme de détection de contour
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	edged = cv2.Canny(gray, 30, 200)

	contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	for contour in contours:

		# périmètre du contour
		perimeter = cv2.arcLength(contour, True)

		# approximation en une forme plus simple
		approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
			
		# condition : 4 coté et aire suffisante
		if len(approx) == 4 and cv2.contourArea(contour) > 1000:

			x, y, w, h = cv2.boundingRect(contours[0])
			cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

			# Trouver le plus grand contour
			c = max(contours, key=cv2.contourArea) # inutile pour le moment

			# Trouver le centre de la balise dans l'image
			M = cv2.moments(c)
			object_center_x = int(M['m10'] / M['m00'])
			image_center_x = width//2

			# distance entre le centre de l'image et le centre de l'objet
			dist_x = np.abs(image_center_x - object_center_x)

			# distance de l'objet en % par rapport au centre de l'image
			dist_percent = dist_x/image_center_x * 100

			if object_center_x < image_center_x:
					dist_percent = -dist_percent
			print(f"L'objet est à {dist_percent}% du centre de l'image.")
			return dist_percent
	raise BaliseException("Balise non trouvé")

def capture():
	cap = cv2.VideoCapture(1) # 1 si camera externe, 0 sinon 
	ret, frame = cap.read()
	cv2.imwrite('camera_test/photo.jpg', frame)
	cap.release()

class StrategieSuivreBalise():
	def __init__(self, data, robot):
		self.data = data
		self.robot = robot
		self.stangle1 = StrategieAngle(45, 45, self.robot)
		self.stangle2 = StrategieAngle(-45, -45, self.robot)

	def update(self):
		if self.stop():
			return

		if (detect(self.data) <= -5 or detect(self.data) >= 5): # si la balise se situe plus de ±5% du centre
			if detect(self.data) <= 0:
				self.stangle1.update()
				if self.stangle1.stop():
					StrategieAvance(5, 45, self.robot).update()
			else:
				self.stangle2.update()		
				if self.stangle2.stop():
					StrategieAvance(5, 45, self.robot).update()	
		else:
			StrategieAvance(15, 45, self.robot).update()

	def stop(self):
		try:
			detect(self.data)
		except BaliseException as e:
			return True
		return False
