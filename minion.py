from artifact_interface import ArtifactInterface
import uuid
import pygame
from constants import HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT

class Minion(ArtifactInterface):
	def __init__(
			self,
			x=40,
			y=800,
			radius=10,
			color=(0, 0, 255),
			hp=2000,
			damage=5,
			artifact_range=0,
			velocity=1.5,
			team=None,
			artifact_type = 'minion',
			sprite = 'sprites/blue_minion.png',
			shoot_position = (-10, 3)
		):
		self.id = uuid.uuid4()
		self.position = pygame.Vector2(x, y)
		self.radius = radius
		self.color = color
		self.hp = hp
		self.current_hp = hp
		self.damage = damage
		self.range = radius + artifact_range
		self.velocity = velocity
		self.team = team
		self.artifact_type = artifact_type
		self.sprite = sprite
		self.shoot_position = pygame.Vector2(shoot_position)

	def __repr__(self):
		return f'{self.artifact_type}-{self.id} {self.current_hp}'

	def __str__(self):
		return f'[{self.artifact_type}] {self.id}'

	def draw(self, surface):
		life_bar_value = self.current_hp * 100 / self.hp / 100
		#quitar esto
		if self.sprite:
			sprite = pygame.image.load(self.sprite)
			surface.blit(sprite, (self.position.x - self.radius, self.position.y - self.radius))
			pygame.draw.rect(surface, (0, 255, 0), pygame.Rect(self.position.x
							 + self.radius+10, self.position.y + self.radius - 30,
							 HEALTH_BAR_WIDTH * life_bar_value,
							 HEALTH_BAR_HEIGHT))
		else:
			pygame.draw.circle(surface, self.color, self.position, self.radius)
			pygame.draw.rect(surface, (0, 255, 0), pygame.Rect(self.position.x
							 + self.radius, self.position.y + self.radius - 10,
							 HEALTH_BAR_WIDTH * life_bar_value,
							 HEALTH_BAR_HEIGHT))

	def move(self, x_inc=0, y_inc=0):
		self.position += pygame.Vector2(x_inc, -y_inc)

	def in_range(self, objects):
		objects_in_range = []
		for obj in objects:
			if obj.id != self.id:
				distance = self.position.distance_to(obj.position)
				if distance < self.range + obj.radius:
					objects_in_range.append(obj)
		return sorted(objects_in_range, key=lambda artifact: artifact.artifact_type, reverse=True)

	def hit(self, surface, target):
		pygame.draw.line(surface, self.color, self.position - self.shoot_position, target.position, 2)
		self.draw(surface)

	def collision(self, objects):
		for obj in objects:
			if obj.id != self.id and obj.team != self.team:
				distance = self.position.distance_to(obj.position)
				if distance < self.radius + obj.radius:
					if obj.position.y <= self.position.y:
						return True
		return False