from artifact_interface import ArtifactInterface
import uuid
import pygame
from utils import get_mouse_position, sprite_frames
from constants import (HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT, CHAMPION_WALKING_1, CHAMPION_WALKING_2, 
CHAMPION_WALKING_3, CHAMPION_WALKING_4, CHAMPION_WALKING_5, CHAMPION_WALKING_6, CHAMPION_STANDING,
CHAMPION_ATTACKING_1, CHAMPION_ATTACKING_2, CHAMPION_ATTACKING_3, CHAMPION_ATTACKING_4, 
CHAMPION_ATTACKING_5, CHAMPION_ATTACKING_6)
from sprite_sheet import SpriteSheet

class Champion(ArtifactInterface):

	def __init__(
			self,
			x=400,
			y=780,
			radius=20,
			color=(0, 255, 0),
			hp=10000,
			damage=5,
			artifact_range=10,
			velocity=2,
			team=None,
			artifact_type = 'champion',
			sprite_sheet = None,
			sprite = None,
			shoot_position = (-5, -5)
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
		self.sprite_sheet = SpriteSheet(sprite_sheet)
		self.sprite = None
		self.shoot_position = pygame.Vector2(shoot_position)
		self.standing_frame_r = None
		self.standing_frame_l = None
		self.walking_frames_l = []
		self.walking_frames_r = []
		self.attacking_frames_l = []
		self.attacking_frames_r = []
		self.current_orientation = 'R'
		self.last_orientation = 'R'
		self.current_walking_frame = sprite_frames(5,5)
		self.current_attacking_frame = sprite_frames(5,5)
		self.generate_sprites()

	def generate_sprites(self):
		#standing sprites
		image = self.sprite_sheet.get_image(*CHAMPION_STANDING)
		self.standing_frame_r = image
		image = pygame.transform.flip(image, True, False)
		self.standing_frame_l = image
		#walking sprites
		image = self.sprite_sheet.get_image(*CHAMPION_WALKING_1)
		self.walking_frames_r.append(image)
		image = self.sprite_sheet.get_image(*CHAMPION_WALKING_2)
		self.walking_frames_r.append(image)
		image = self.sprite_sheet.get_image(*CHAMPION_WALKING_3)
		self.walking_frames_r.append(image)
		image = self.sprite_sheet.get_image(*CHAMPION_WALKING_4)
		self.walking_frames_r.append(image)
		image = self.sprite_sheet.get_image(*CHAMPION_WALKING_5)
		self.walking_frames_r.append(image)
		image = self.sprite_sheet.get_image(*CHAMPION_WALKING_6)
		self.walking_frames_r.append(image)
		for image in self.walking_frames_r:
			image = pygame.transform.flip(image, True, False)
			self.walking_frames_l.append(image)
		#attacking sprites
		image = self.sprite_sheet.get_image(*CHAMPION_ATTACKING_1)
		self.attacking_frames_r.append(image)
		image = self.sprite_sheet.get_image(*CHAMPION_ATTACKING_2)
		self.attacking_frames_r.append(image)
		image = self.sprite_sheet.get_image(*CHAMPION_ATTACKING_3)
		self.attacking_frames_r.append(image)
		image = self.sprite_sheet.get_image(*CHAMPION_ATTACKING_4)
		self.attacking_frames_r.append(image)
		image = self.sprite_sheet.get_image(*CHAMPION_ATTACKING_5)
		self.attacking_frames_r.append(image)
		image = self.sprite_sheet.get_image(*CHAMPION_ATTACKING_6)
		self.attacking_frames_r.append(image)
		for image in self.attacking_frames_r:
			image = pygame.transform.flip(image, True, False)
			self.attacking_frames_l.append(image)

	def __repr__(self):
		return f'{self.artifact_type}-{self.id} {self.current_hp}'

	def __str__(self):
		return f'[{self.artifact_type}] {self.id}'

	def draw_life_bar(self, surface):
		life_bar_value = self.current_hp * 100 / self.hp / 100
		pygame.draw.rect(surface, (0, 255, 0), pygame.Rect(self.position.x
				 + self.radius+10, self.position.y + self.radius - 80,
				 HEALTH_BAR_WIDTH * life_bar_value,
				 HEALTH_BAR_HEIGHT))

	def draw(self, surface):
		if self.current_orientation == 'R':
			sprite = self.walking_frames_r[next(self.current_walking_frame)]
		elif self.current_orientation == 'L':
			sprite = self.walking_frames_l[next(self.current_walking_frame)]
		else:
			if self.last_orientation == 'R':
				sprite = self.standing_frame_r
			else:
				sprite = self.standing_frame_l
		surface.blit(sprite, (self.position.x - self.radius, self.position.y - self.radius -30))
		self.draw_life_bar(surface)

	def move(self, click, direction, mouse_target_position):
		if click[0]:
			mouse_target_position = pygame.Vector2(get_mouse_position())
			direction = mouse_target_position - self.position
			if direction.length() != 0:
				direction = direction.normalize() * self.velocity
		if (mouse_target_position - self.position).length() > self.velocity:
			self.position += direction
			if self.position.x < mouse_target_position.x:
				self.current_orientation = 'R'
			else:
				self.current_orientation = 'L'
		else:
			self.position = mouse_target_position
			if self.current_orientation:
				self.last_orientation = self.current_orientation
			self.current_orientation = None
			direction = pygame.Vector2(0, 0)

		return direction, mouse_target_position

	def in_range(self, objects):
		objects_in_range = []
		for obj in objects:
			if obj.id != self.id:
				distance = self.position.distance_to(obj.position)
				if distance < self.range + obj.radius:
					objects_in_range.append(obj)
		return sorted(objects_in_range, key=lambda artifact: artifact.artifact_type, reverse=True)

	def hit(self, surface, target):
		if self.current_orientation == 'R':
			sprite = self.attacking_frames_r[next(self.current_attacking_frame)]
		else:
			sprite = self.attacking_frames_l[next(self.current_attacking_frame)]
		surface.blit(sprite, (self.position.x - self.radius, self.position.y - self.radius -30))
		self.draw_life_bar(surface)

	def collision(self, objects):
		for obj in objects:
			if obj.id != self.id and obj.team != self.team:
				distance = self.position.distance_to(obj.position)
				if distance < self.radius + obj.radius:
					if obj.position.y <= self.position.y:
						return True
		return False