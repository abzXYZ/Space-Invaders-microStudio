import pyray as rl
import random

import utils

import ship
import asteroid


rl.init_window(utils.SCREEN_W, utils.SCREEN_H, "Asteroids")
if utils.DEBUG:
    rl.set_target_fps(utils.DEBUG_FPS)
else:
    rl.set_target_fps(60)

x = utils.SCREEN_W // 2
y = utils.SCREEN_H // 2
rot = 270

spaceship = ship.Ship(x,y,rot)
asteroids = []
for i in range(5):
    asteroids.append(asteroid.Asteroid(random.randint(0,utils.SCREEN_W),random.randint(0,utils.SCREEN_H),random.uniform(10,60),utils.EDGES,0.25))

while not rl.window_should_close():
    rl.begin_drawing()
    rl.clear_background(rl.BLACK)

    spaceship.update(rl.get_frame_time())
    spaceship.wrap()
    spaceship.draw()

    for asteroid in asteroids:
        asteroid.update(rl.get_frame_time())
        asteroid.wrap()
        asteroid.draw()

    if utils.DEBUG:
        rl.draw_text(f"x={"{:.2f}".format(spaceship.x)}  y={"{:.2f}".format(spaceship.y)} rot={spaceship.rot} thrusting={spaceship.thrusting}", 10, 10, 18, rl.GRAY)
    
    rl.end_drawing()

rl.close_window()
