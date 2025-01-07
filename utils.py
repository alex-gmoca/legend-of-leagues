from constants import SPAWN_INTERVAL
from minion import Minion
import pygame

def is_pointing_enemy(mouse_position, objects):
	for obj in objects:
		if obj.team != 'red':
			distance = obj.position.distance_to(mouse_position)
			if distance < obj.radius:
				return True
	return False

def create_minion(team, lane):
	minion = Minion(team=team, lane=lane)
	return minion

def manage_waves(current_time, minions_count, last_spawn_time):
	new_minions = None
	if minions_count > 4:
		if current_time - last_spawn_time >= SPAWN_INTERVAL:
			minions_count = 0
			last_spawn_time = current_time
	else:
		new_minions = []
		new_minions.append(create_minion('blue', 'top'))
		new_minions.append(create_minion('blue', 'bot'))
		new_minions.append(create_minion('blue', 'mid'))
		minions_count += 1
	return new_minions, minions_count, last_spawn_time

def get_mouse_position():
	mouse = pygame.mouse.get_pos()
	return mouse

def sprite_frames(frame_limit, frame_rate=5):
	value = 0
	frames = 0
	while True:
		yield value
		frames += 1
		if frames == frame_rate:
			value += 1
			frames = 0
			if value > frame_limit:
				value = 0

def get_game_over_sprite():
	sprite = pygame.image.load('sprites/victory.png')
	return sprite