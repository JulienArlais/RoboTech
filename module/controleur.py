from .constante import dt
import numpy as np
from .toolbox import distance
import cv2

class BaliseException(Exception):
	def __init__(self, message):
		"""constructeur de l'exception

		Args:
			message (string): message de l'exception
		"""
		self.message = message

class StrategieAvance():
	def __init__(self, distance, vitesse, robot):
		"""constructeur de la stratégie pour avancer d'une distance voulu

		Args:
			distance (float): distance
			vitesse (int): vitesse des roues ( degré par seconde )
			robot (Robot): robot
		"""
		self.distance = distance
		self.vitesse = vitesse
		self.robot = robot
		self.parcouru = 0
		
	def update(self):
		"""itération de la stratégie
		"""
		if self.stop():
			return
		self.robot.set_vitesse(self.vitesse, self.vitesse)
		self.parcouru += distance(self.robot.x - self.robot.getXstep(dt), self.robot.y - self.robot.getYstep(dt), self.robot.x, self.robot.y)
		self.robot.last_update = time.time()
			
	def stop(self):
		"""condition d'arrêt

		Returns:
			boolean: arrêt ou non
		"""
		if (self.parcouru >= self.distance):
			self.robot.set_vitesse(0, 0)
			self.parcouru = 0
			return True
		return False


class StrategieAngle():
	def __init__(self, angle, dps, robot):
		"""constructeur de la stratégie pour tourner d'un angle voulu

		Args:
			angle (int): angle souhaité ( en degré )
			dps (int): degré par seconde
			robot (Robot): robot
		"""
		self.angle = angle
		self.dps = dps
		self.robot = robot
		self.angleapplique = 0

	def update(self):
		"""itération de la stratégie
		"""
		if self.stop():
			return
		self.robot.tourner(self.dps * dt)
		delta_angle = (self.robot.vitAngD - self.robot.vitAngG) * self.robot.rayon/self.robot.dist_roue * dt * 180/np.pi
		self.angleapplique += delta_angle
		self.robot.last_update = time.time()

	def stop(self):
		"""condition d'arrêt

		Returns:
			boolean: arrêt ou non
		"""
		if np.abs(self.angleapplique) >= np.abs(self.angle):
			self.robot.set_vitesse(0, 0)
			self.angleapplique = 0
			return True
		else:
			return False


class StrategieArretMur():
	def __init__(self, robot, env, objets, vitesse):
		"""constructeur de la stratégie pour s'arrêter à un mur

		Args:
			robot (Robot): robot
			env (Environnement): environnement
			objets (Objet): objets
			vitesse (int): vitesse des roues ( degré par seconde )
		"""
		self.robot = robot
		self.env = env
		self.obj = objets
		self.stavance = StrategieAvance(self.env.width*2, vitesse, self.robot)
	
	def stop(self):
		"""condition d'arrêt

		Returns:
			boolean: arrêt ou non
		"""
		return (self.robot.capteur(self.env, 10000, self.obj) < 2*self.robot.rayon)

	def update(self):
		"""itération de la stratégie
		"""
		if self.stop():
			return
		self.stavance.update()


class StrategieSeq():
	def __init__(self, liste):
		"""constructeur de la stratégie séquentielle

		Args:
			liste (_type_): liste de stratégies
		"""
		self.liste = liste
		self.indlist = 0
		
	def update(self):
		"""itération de la stratégie
		"""
		if self.liste[self.indlist].stop():
			self.indlist += 1
			if self.stop():
				return
		self.liste[self.indlist].update()
		
	def stop(self):
		"""condition d'arrêt

		Returns:
			boolean: arrêt ou non
		"""
		return self.indlist >= len(self.liste)

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
