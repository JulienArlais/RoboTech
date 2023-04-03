from .constante import  *
import numpy as np
from .toolbox import distance
import cv2
from .camera import detect, BaliseException


class StrategieAvance():
	def __init__(self, distance, vitesse, proxy):
		"""constructeur de la stratégie pour avancer d'une distance voulu
		Args:
			distance (float): distance
			vitesse (int): vitesse des roues ( degré par seconde )
			robot (Robot): robot
		"""
		self.distance = distance
		self.vitesse = vitesse
		self.proxy = proxy
		self.on_off=False
		
	def update(self):
		"""itération de la stratégie
		"""
		if self.stop():
			return
		self.proxy.set_vitesse(self.vitesse, self.vitesse)
		self.proxy.dist_parcourue()
		self.proxy.set_led(1,self.on_off)	#pour nous permettre d'alterner la couleur de la led à chaque update
		not self.on_off
			
	def stop(self):
		"""condition d'arrêt
		Returns:
			boolean: arrêt ou non
		"""
		if (self.proxy.distance_parcourue >= self.distance):
			self.proxy.set_vitesse(0, 0)
			self.proxy.reset_distance()
			return True
		return False


class StrategieAngle():
	def __init__(self, angle, dps, proxy):
		"""constructeur de la stratégie pour tourner d'un angle voulu
		Args:
			angle (int): angle souhaité ( en degré )
			dps (int): degré par seconde
			proxy (Robot): proxy
		"""
		self.angle = angle
		self.dps = dps
		self.proxy = proxy

	def update(self):
		"""itération de la stratégie
		"""
		if self.stop():
			return
		self.proxy.tourner(self.dps * dt)
		self.proxy.ang_parcouru()

	def stop(self):
		"""condition d'arrêt
		Returns:
			boolean: arrêt ou non
		"""
		if np.abs(self.proxy.angle_parcouru) >= np.abs(self.angle):
			self.proxy.set_vitesse(0, 0)
			self.proxy.reset_angle()
			return True
		else:
			return False


class StrategieArretMur():
	def __init__(self, proxy, env, vitesse):
		"""constructeur de la stratégie pour s'arrêter à un mur
		Args:
			robot (Robot): robot
			env (Environnement): environnement
			vitesse (int): vitesse des roues ( degré par seconde )
		"""
		self.proxy = proxy
		self.env = env
		self.stavance = StrategieAvance(self.env.width*2, vitesse, self.proxy)
	
	def stop(self):
		"""condition d'arrêt
		Returns:
			boolean: arrêt ou non
		"""
		return (self.proxy.get_distance() < 2*self.proxy.rayon)

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
		self.liste[self.indlist].update()
		if self.liste[self.indlist].stop():
			self.indlist += 1
		
	def stop(self):
		"""condition d'arrêt
		Returns:
			boolean: arrêt ou non
		"""
		return self.indlist >= len(self.liste)

class StrategieSuivreBalise():
	def __init__(self, data, proxy):
		self.data = data
		self.proxy = proxy
		self.stangle1 = StrategieAngle(45, 45, self.proxy)
		self.stangle2 = StrategieAngle(-45, -45, self.proxy)

	def update(self):
		if self.stop():
			return

		if (detect(self.data) <= -5 or detect(self.data) >= 5): # si la balise se situe plus de ±5% du centre
			if detect(self.data) <= 0:
				self.stangle1.update()
				if self.stangle1.stop():
					StrategieAvance(5, 45, self.proxy).update()
			else:
				self.stangle2.update()		
				if self.stangle2.stop():
					StrategieAvance(5, 45, self.proxy).update()	
		else:
			StrategieAvance(15, 45, self.proxy).update()

	def stop(self):
		try:
			detect(self.data)
		except BaliseException as e:
			return True
		return False




class Strategieloop():
	#la detection de la collisions se fera automatiquement par la méthode run de element_simulation qui vérifie à chaque pas de temps si ol eeeeeeeeeeeeeeeeeeeeeeeee
	def __init__(self, strategie,proxy):
		"""Constructeur de la stratégie loop, prend en paramètre la strategie a repéter et le proxy à qui donner les ordres
		Args:
		strategie: la stratégie à répéter en boucle
		"""
		self.strategie = strategie
		self.proxy=proxy

	def update(self):
		"""Itération de la stratégie"""
		#if (self.proxy.get_distance() < 2*self.proxy.rayon): #on teste si le robot va etre en collision pres d'un obstacle/mur
			#self.strategie.liste.reverse() #on inverse la liste pour pouvoir refaire le même motif mais en arrière
			#self.strategie.indlist=0 #on remet l'indice à 0 pour repartir du debut du fin de la fin de la liste

		if self.strategie.stop():
			self.strategie.indlist=0
			#On remet l'indice de la liste d'instuctions à 0 pour la reparcourir entièrement
		self.strategie.update()

	def stop(self):
		"""Condition d'arrêt"""
		#if (self.proxy.get_distance() < 2*self.proxy.rayon):
			#print("OHOHOHOHO")
		return False



class StrategieTriangleEq():
	def __init__(self,proxy_v,dist):
		"""constructeur de la stratégie TriangleEq
		Args:
			proxy_v:robot_virtuel à qui donner les ordres
		"""
		self.liste = [StrategieAngle(30,stan_dps_pos, proxy_v), StrategieAvance(dist, stav_vit, proxy_v),StrategieAngle(-120, stan_dps_neg, proxy_v), StrategieAvance(dist, stav_vit, proxy_v),StrategieAngle(-120, stan_dps_neg, proxy_v), StrategieAvance(dist, stav_vit, proxy_v)]
		self.indlist = 0
		self.proxy_v=proxy_v
		self.angle=60
		
	def update(self):
		"""itération de la stratégie
		"""
		self.liste[self.indlist].update()
		if self.liste[self.indlist].stop():
			self.indlist += 1
		
	def stop(self):
		"""condition d'arrêt
		Returns:
			boolean: arrêt ou non
		"""
		
		if self.indlist >= len(self.liste):
			self.indlist=0
			return True
		return False



class StrategieHexagone():
	def __init__(self,dist,angle,proxy):
		"""constructeur de la stratégie séquentielle 1 du TME SOLO
		Args:
			liste (_type_): liste de stratégies
		"""
		self.proxy=proxy
		self.liste = [StrategieAngle(angle,angle,self.proxy),StrategieAvance(dist, stav_vit, self.proxy),StrategieAngle(-angle,-angle,self.proxy),StrategieAvance(dist, stav_vit, self.proxy),StrategieAngle(-angle,-angle,self.proxy),StrategieAvance(dist, stav_vit, self.proxy),StrategieAngle(-90,-45,self.proxy),StrategieAvance(dist, stav_vit, self.proxy),StrategieAngle(-angle,-angle,self.proxy),StrategieAvance(dist, stav_vit, self.proxy),StrategieAngle(-angle,-angle,self.proxy),StrategieAvance(dist, stav_vit, self.proxy)]
		self.indlist = 0
		
		
	def update(self):
		"""itération de la stratégie
		"""
		self.liste[self.indlist].update()
		if self.liste[self.indlist].stop():
			self.indlist += 1
		
	def stop(self):
		"""condition d'arrêt
		Returns:
			boolean: arrêt ou non
		"""
		
		if self.indlist >= len(self.liste):
			self.indlist=0
			return True
		return False







class Strategie1():
	def __init__(self,proxy_v,dist):
		"""constructeur de la stratégie TriangleEq
		Args:
			proxy_v:robot_virtuel à qui donner les ordres
		"""
		self.proxy=proxy_v
		self.strat =StrategieAvance(dist, stav_vit, proxy_v)
		
		
	def update(self):
		"""itération de la stratégie
		"""
		#if self.proxy.abaisser=True:
		self.strat.update()
	
		
	def stop(self):
		"""condition d'arrêt
		Returns:
			boolean: arrêt ou non
		"""
		return self.strat.stop()


class  Strategie0():
	def __init__(self, dist,proxy):
		"""constructeur de la stratégie séquentielle 1 du TME SOLO
		Args:
			liste (_type_): liste de stratégies
		"""
		self.proxy=proxy
		self.liste = [StrategieAngle(90,90,self.proxy),StrategieAvance(dist/2, stav_vit, self.proxy),StrategieAngle(-90,-90,self.proxy),StrategieAvance(dist, stav_vit, self.proxy),StrategieAngle(-90,-90,self.proxy),StrategieAvance(dist/2, stav_vit, self.proxy),StrategieAngle(-90,-45,self.proxy),StrategieAvance(dist, stav_vit, self.proxy),StrategieAngle(90,-90,self.proxy),StrategieAvance(dist, stav_vit, self.proxy)]

		self.indlist = 0
		
	def update(self):
		"""itération de la stratégie
		"""
		self.liste[self.indlist].update()
		if self.liste[self.indlist].stop():
			self.indlist += 1
		
	def stop(self):
		"""condition d'arrêt
		Returns:
			boolean: arrêt ou non
		"""
		
		if self.indlist >= len(self.liste):
			self.indlist=0
			return True
		return False



class StrategieLoopSeq():
	def __init__(self, liste_strat, proxy):
		"""Constructeur de la stratégie loop, prend en paramètre la liste de strategie a repéter et le proxy 
		Args:
			strategie: la liste de stratégie à répéter en boucle
		"""
		self.tab = liste_strat
		self.index = 0
		self.proxy = proxy

	def update(self):
		if (self.index >= len(self.tab)): #Pour recommencer à l'infinni sur la même ligne des 1 et des 0
			self.index = 0

		if self.tab[self.index].stop():
			self.index += 1
			
		self.tab[self.index].update()
		

	def stop(self):
		"""Condition d'arrêt"""
		return False


class StrategieBinaire():
	def __init__(self, liste, proxy,dist):
		"""Constructeur de la stratégie loop, prend en paramètre la liste de strategie a repéter et le proxy 
		Args:
			strategie: la liste de stratégie à répéter en boucle
		"""
		self.tab = liste
		self.res=[]
		self.index = 0
		self.proxy_v = proxy
		self.dist=dist

	def update(self):

		#fonction de conversion à mettre en dehors de la fonction update 
		for nombre in self.tab:
			if nombre==1:
				self.res.append(Strategie0(self.dist,self.proxy_v))
			if nombre==0:
				self.res.append(Strategie1(self.proxy_v,self.dist))
		
		self.res.reverse() #Pour avoir la liste res dans le bon order voulu

		if self.res[self.index].stop():
			self.index += 1
			
		self.res[self.index].update()


		#if (self.proxy.get_distance() < 2*self.proxy.rayon):): il y a alors une collision
			#self.proxy_v.x=50
			#self.proxy_v.y=50

			#on remet le position en haut à gauche et il contunue alors à écrire 

		

	def stop(self):
		"""Condition d'arrêt"""
		return False


class StrategieEmeteur():
	def __init__(self,proxy_v):
		"""constructeur de la stratégie TriangleEq
		Args:
			proxy_v:robot_virtuel à qui donner les ordres
		"""
		self.proxy=proxy_v
		self.emeteur=self.proxy_v.env.éméteur[0]
		#On recupere la distance du robot pour y aller directement en ligne droite

		self.strat =StrategieAvance(self.proxy_v.getSignal(self.proxy_v.env), stav_vit,self.proxy_v)
		
		
	def update(self):
		"""itération de la stratégie
		"""
		#if self.proxy.abaisser=True:
		self.strat.update()
	
		
	def stop(self):
		"""condition d'arrêt
		Returns:
			boolean: arrêt ou non
		"""
		return self.strat.stop()


