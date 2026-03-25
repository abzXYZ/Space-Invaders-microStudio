import pyray as rl

import ship

DEBUG = False

SCREEN_W = 800
SCREEN_H = 600

rl.init_window(SCREEN_W, SCREEN_H, "Tiddlywinks")
rl.set_target_fps(60)

x = SCREEN_W // 2
y = SCREEN_H // 2
rot = 270

spaceship = ship.Ship(x,y,rot)

if DEBUG:
    rl.set_target_fps(120)
    spaceship.debug_mode = True

while not rl.window_should_close():
    rl.begin_drawing()
    rl.clear_background(rl.BLACK)
    spaceship.update(rl.get_frame_time())
    spaceship.draw()
    rl.draw_text(f"x={spaceship.x}  y={spaceship.y} rot={rot}", 10, 10, 18, rl.GRAY)
    rl.end_drawing()

rl.close_window()
