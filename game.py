#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
import sys
import time
import copy

from pygame.locals import *

#import classes
from tower import Tower
from champion import Champion
from minion import Minion
from nexus import Nexus

#import functions
from utils import is_pointing_enemy, manage_waves, get_game_over_sprite

#import constants
from constants import TARGET_FPS

# Set up pygame.
pygame.init()
surface = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Legend of leagues!')
running = True
cursor_img = pygame.image.load('sprites/normal.png')
attack_cursor_img = pygame.image.load('sprites/text.png')
clock = pygame.time.Clock()

objects = []

champion = Champion(sprite_sheet='sprites/champion.png', team='blue')
#nexus
red_nexus = Nexus(x=745, y=80, team='red')
objects.append(red_nexus)
#1 tier tower
objects.append(Tower(x=40, y=380, team='red'))
objects.append(Tower(x=420, y=710, team='red'))
objects.append(Tower(x=296, y=480, team='red'))
#2 tier tower
objects.append(Tower(x=40, y=60, team='red'))
objects.append(Tower(x=760, y=710, team='red'))
objects.append(Tower(x=460, y=300, team='red'))
#inhib tower
objects.append(Tower(x=450, y=60, team='red'))
objects.append(Tower(x=760, y=250, team='red'))
objects.append(Tower(x=586, y=170, team='red'))
#nexus towers
objects.append(Tower(x=665, y=60, team='red'))
objects.append(Tower(x=760, y=110, team='red'))


objects.append(champion)

pygame.display.flip()
pygame.mouse.set_visible(False)
current_time = time.time()
minions_count = 0
minion_spacer = 0
new_objects = []
delete_objects = []
last_spawn_time = time.time()
direction = pygame.Vector2(0, 0)
mouse_target_position = pygame.Vector2(champion.position.x, champion.position.y)

while running:
	#check for quit event
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	#check for game ending
	if red_nexus.current_hp <= 0:
		print('You win!')
		game_over_sprite = get_game_over_sprite()
		#show game over screen with transition effect
		for x in range(1020):
			if x % 4 == 0:
				game_over_sprite.set_alpha(x//4)
				surface.blit(game_over_sprite, (145, 280))
				pygame.display.update()
			else:
				time.sleep(0.01)
		time.sleep(15)
		running = False

	#restart surface
	#background = pygame.image.load("sprites/background2.png")
	#surface.blit(background, (0, 0))
	#no background
	surface.fill((0, 0, 0))

	#move and draw objects, hit enemies
	for obj in list(objects):
		objects_in_range = None
		objects_in_range = obj.in_range(objects)
		if objects_in_range:
			if obj.team != objects_in_range[0].team:
				obj.hit(surface, objects_in_range[0])
				objects_in_range[0].current_hp -= obj.damage
				if objects_in_range[0].current_hp <= 0:
					delete_objects.append(objects_in_range[0])
			else:
				obj.draw(surface)
		else:
			obj.draw(surface)
		if obj.artifact_type == 'minion':
			if not obj.collision(objects):
				obj.move()

	#manage champion movement
	click = pygame.mouse.get_pressed()
	direction, mouse_target_position = champion.move(click, direction, mouse_target_position)
	#manage keyboard events
	keys = pygame.key.get_pressed()
	if keys[pygame.K_d] and champion.summoner_spell_d.last_execution is None:
		last_summoner_spell_d_position = copy.deepcopy(champion.position)
		animation_gradient = 700
		champion = champion.summoner_spell_d.cast(mouse_target_position, champion)
	if champion.summoner_spell_d.last_execution and champion.summoner_spell_d.last_execution > time.time() - champion.summoner_spell_d.animation_duration:
		champion.summoner_spell_d.draw_animation(surface, last_summoner_spell_d_position, animation_gradient)
		animation_gradient -= 10

	#draw champion summoners spells uid
	champion.summoner_spell_d.draw(surface)
	#champion.summoner_spell_f.draw(surface)

	#manage waves
	current_time = time.time()
	if minion_spacer > 50:
		new_minions = None
		new_minions, minions_count, last_spawn_time = manage_waves(current_time, minions_count, last_spawn_time)
		if new_minions:
			new_objects.extend(new_minions)
			minion_spacer = 0
	else:
		minion_spacer += 1

	#update objects
	objects.extend(new_objects)
	new_objects = []
	for del_obj in delete_objects:
		if del_obj in objects:
			objects.remove(del_obj)
	delete_objects = []

	#mouse and cursor
	if is_pointing_enemy(pygame.mouse.get_pos(), objects):
		surface.blit(attack_cursor_img, pygame.mouse.get_pos())
	else:
		surface.blit(cursor_img, pygame.mouse.get_pos())

	#update display
	pygame.display.update()
	#limit frames per second
	clock.tick(TARGET_FPS)

print('Thanks for playing.')
