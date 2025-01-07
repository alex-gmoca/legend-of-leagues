from artifact_interface import ArtifactInterface
import uuid
import pygame
from constants import HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT

class Nexus(ArtifactInterface):
	def __init__(
			self,
			x=775,
			y=40,
			radius=20,
			color=(255, 0, 0),
			hp=200000,
			damage=0,
			artifact_range=0,
			speed=0,
			team=None,
			artifact_type = 'nexus',
			sprite = 'sprites/red_nexus.png'
		):
		self.id = uuid.uuid4()
		self.position = pygame.Vector2(x, y)
		self.radius = radius
		self.color = color
		self.hp = hp
		self.current_hp = hp
		self.damage = damage
		self.range = radius + artifact_range
		self.speed = speed
		self.team = team
		self.artifact_type = artifact_type
		self.sprite = sprite

	def __repr__(self):
		return f'{self.artifact_type}-{self.id} {self.current_hp}'

	def __str__(self):
		return f'[{self.artifact_type}] {self.id}'

	def hit(self):
		pass

	def move(self):
		pass

	def draw(self, surface):
		life_bar_value = self.current_hp * 100 / self.hp / 100
		#quitar esto
		if self.sprite:
			sprite = pygame.image.load(self.sprite)
			surface.blit(sprite, (self.position.x - self.radius, self.position.y - self.radius -30))
			pygame.draw.rect(surface, (0, 255, 0), pygame.Rect(self.position.x
							 + self.radius - 25, self.position.y + self.radius - 90,
							 HEALTH_BAR_WIDTH * life_bar_value,
							 HEALTH_BAR_HEIGHT))
		else:
			pygame.draw.circle(surface, self.color, self.position, self.radius)
			pygame.draw.rect(surface, (0, 255, 0), pygame.Rect(self.position.x
							 + self.radius, self.position.y + self.radius - 10,
							 HEALTH_BAR_WIDTH * life_bar_value,
							 HEALTH_BAR_HEIGHT))

	def in_range(self, objects):
		return None

	def collision(self, objects):
		for obj in objects:
			if obj.id != self.id and obj.team != self.team:
				distance = self.position.distance_to(obj.position)
				if distance < self.radius + obj.radius:
					if obj.position.y <= self.position.y:
						return True
		return False