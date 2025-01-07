import abc
import pygame
import time
from utils import get_mouse_position
class SummonerSpellInterface(metaclass=abc.ABCMeta):
	@classmethod
	def __subclasshook__(cls, subclass):
		return (hasattr(subclass,__init__) and
				hasattr(subclass, __repr__) and
				hasattr(subclass, __str__) and
				hasattr(subclass, cast) and
				hasattr(subclass, update_cooldown) and
				callable(subclass.__init__) and
				callable(subclass.__repr__) and
				callable(subclass.__str__) and
				callable(subclass.cast) and
				callable(subclass.update_cooldown) and
				NotImplemented)

	POSITION = pygame.Vector2(360, 760)
	FONT_COLOR = (255, 255, 255)
	BACKGROUND = (4,37,89)
	FLASH_DISTANCE = 60

	@abc.abstractmethod
	def __init__():
		"""Constructor"""
		raise NotImplementedError

	def __repr__():
		"""Representation"""
		raise NotImplementedError

	def __str__():
		"""String representation"""
		raise NotImplementedError

	def cast():
		"""Cast the spell"""
		raise NotImplementedError

	@abc.abstractmethod
	def draw():
		"""Update the cooldown"""
		raise NotImplementedError

class Flash(SummonerSpellInterface):
	def __init__(self):
		self.name = 'Flash'
		self.duration = 0
		self.cooldown = 6
		self.last_execution = None
		self.sprite = 'sprites/flash.jpg'
		self.animation_sprite = 'sprites/flash_animation.png'
		self.animation_duration = 3

	def __repr__(self):
		return f'{self.name}'

	def __str__(self):
		return f'{self.name}'

	def cast(self, mouse_target_position, champion):
		if self.last_execution is None:
			self.last_execution = time.time()
			mouse_target_position = pygame.Vector2(get_mouse_position())
			direction = mouse_target_position - champion.position
			#move instantly champion 10 pixels into the direcition
			champion.position += direction.normalize() * self.FLASH_DISTANCE
		return champion

	def draw(self, surface):
		if self.last_execution is None:
			sprite = pygame.image.load(self.sprite)
			sprite = pygame.transform.scale(sprite, (40, 40))
			surface.blit(sprite, (self.POSITION.x, self.POSITION.y))
		else:
			cooldown_timer = int(self.cooldown - (time.time() - self.last_execution))
			if cooldown_timer < 0:
				self.last_execution = None
			font = pygame.font.Font(None, 36)
			text_surface = font.render(str(cooldown_timer), True, self.FONT_COLOR)
			rect = pygame.Rect(self.POSITION.x, self.POSITION.y, 40, 40)
			text_rect = text_surface.get_rect(center=rect.center)
			pygame.draw.rect(surface, self.BACKGROUND, rect)
			surface.blit(text_surface, text_rect)

	def draw_animation(self, surface, position, gradient):
		sprite = pygame.image.load(self.animation_sprite)
		sprite = pygame.transform.scale(sprite, (40, 40))
		sprite.set_alpha(gradient)
		surface.blit(sprite, (position.x-10, position.y-45))
