from pico2d import *
import math


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FRAME_DELAY = 0.01

CIRCLE_CENTER_X = 400
CIRCLE_CENTER_Y = 300
CIRCLE_RADIUS = 200

RECTANGLE_LEFT = 50
RECTANGLE_RIGHT = 750
RECTANGLE_BOTTOM = 50
RECTANGLE_TOP = 550
RECTANGLE_START = (RECTANGLE_LEFT, RECTANGLE_TOP)
CONNECTOR_STEP = 5

TRIANGLE_A = (100, 100)
TRIANGLE_B = (700, 100)
TRIANGLE_C = (400, 500)
TRIANGLE_STEPS = 100


def draw_boy(x, y):
	clear_canvas()
	boy.draw(x, y)
	update_canvas()
	delay(FRAME_DELAY)


def move_between(start, end):
	start_x, start_y = start
	end_x, end_y = end
	distance = math.hypot(end_x - start_x, end_y - start_y)
	steps = max(1, math.ceil(distance / CONNECTOR_STEP))

	for step in range(1, steps):
		t = step / steps
		x = start_x + (end_x - start_x) * t
		y = start_y + (end_y - start_y) * t
		draw_boy(x, y)
	draw_boy(end_x, end_y)


def move_circle():
	for degree in range(360):
		theta = math.radians(degree)
		x = CIRCLE_CENTER_X + CIRCLE_RADIUS * math.cos(theta)
		y = CIRCLE_CENTER_Y + CIRCLE_RADIUS * math.sin(theta)
		draw_boy(x, y)
	draw_boy(CIRCLE_CENTER_X + CIRCLE_RADIUS, CIRCLE_CENTER_Y)


def move_top():
	for x in range(RECTANGLE_LEFT, RECTANGLE_RIGHT + 1, 5):
		draw_boy(x, RECTANGLE_TOP)


def move_right():
	for y in range(RECTANGLE_TOP, RECTANGLE_BOTTOM - 1, -5):
		draw_boy(RECTANGLE_RIGHT, y)


def move_bottom():
	for x in range(RECTANGLE_RIGHT, RECTANGLE_LEFT - 1, -5):
		draw_boy(x, RECTANGLE_BOTTOM)


def move_left():
	for y in range(RECTANGLE_BOTTOM, RECTANGLE_TOP + 1, 5):
		draw_boy(RECTANGLE_LEFT, y)


def move_rectangle():
	move_top()
	move_right()
	move_bottom()
	move_left()


def move_ab():
	start_x, start_y = TRIANGLE_A
	end_x, end_y = TRIANGLE_B

	for step in range(TRIANGLE_STEPS + 1):
		t = step / TRIANGLE_STEPS
		x = start_x + (end_x - start_x) * t
		y = start_y + (end_y - start_y) * t
		draw_boy(x, y)


def move_bc():
	start_x, start_y = TRIANGLE_B
	end_x, end_y = TRIANGLE_C

	for step in range(TRIANGLE_STEPS + 1):
		t = step / TRIANGLE_STEPS
		x = start_x + (end_x - start_x) * t
		y = start_y + (end_y - start_y) * t
		draw_boy(x, y)


def move_ca():
	start_x, start_y = TRIANGLE_C
	end_x, end_y = TRIANGLE_A

	for step in range(TRIANGLE_STEPS + 1):
		t = step / TRIANGLE_STEPS
		x = start_x + (end_x - start_x) * t
		y = start_y + (end_y - start_y) * t
		draw_boy(x, y)


def move_triangle():
	move_ab()
	move_bc()
	move_ca()


open_canvas(SCREEN_WIDTH, SCREEN_HEIGHT)
boy = load_image('character.png')

while True:
	move_circle()
	move_between(
		(CIRCLE_CENTER_X + CIRCLE_RADIUS, CIRCLE_CENTER_Y), RECTANGLE_START
	)
	move_rectangle()
	move_between(RECTANGLE_START, TRIANGLE_A)
	move_triangle()
	move_between(
		TRIANGLE_A, (CIRCLE_CENTER_X + CIRCLE_RADIUS, CIRCLE_CENTER_Y)
	)

close_canvas()
