#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
import sys
import time

from pygame.locals import *

#import classes
from tower import Tower
from champion import Champion
from minion import Minion

#import functions
from utils import is_pointing_enemy, manage_waves

#import constants
from constants import TARGET_FPS

# Set up pygame.
pygame.init()
surface = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Legend of leagues!')
running = True
color = [0, 0, 0]
pygame.display.get_surface().fill(color)
pygame.display.update()
cursor_img = pygame.image.load('sprites/normal.png')
attack_cursor_img = pygame.image.load('sprites/text.png')
clock = pygame.time.Clock()

objects = []

champion = Champion(sprite_sheet='sprites/champion.png', team='blue')
objects.append(Tower(y=400, team='red'))
objects.append(Tower(y=100, team='red'))
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
mouse_target_position = pygame.Vector2(400, 780)

while running:
	#check for quit event
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	#restart surface
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
		if obj.artifact_type != 'champion':
			if not obj.collision(objects):
				obj.move(0, obj.velocity)

	#manage champion movement
	click = pygame.mouse.get_pressed()
	direction, mouse_target_position = champion.move(click, direction, mouse_target_position)

	#manage waves
	current_time = time.time()
	if minion_spacer > 50:
		new_minion = None
		new_minion, minions_count, last_spawn_time = manage_waves(current_time, minions_count, last_spawn_time)
		if new_minion:
			new_objects.append(new_minion)
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
