import pyray as rl
import random

import utils

import ship
import asteroid
import bullet
import explosion

rl.init_window(utils.SCREEN_W, utils.SCREEN_H, "Asteroids")

fps = utils.TARGET_FPS
if utils.DEBUG:
    fps = utils.DEBUG_FPS
rl.set_target_fps(fps)

x = utils.SCREEN_W // 2
y = utils.SCREEN_H // 2
rot = 270

# Obiekty w grze
spaceship = ship.Ship(x,y,rot)
asteroids = []
for i in range(7):
    asteroids.append(asteroid.Asteroid(random.randint(0,utils.SCREEN_W),random.randint(0,utils.SCREEN_H),random.uniform(10,60),utils.EDGES,0.25))
bullets = []
explosions = []

# Dźwięki
rl.init_audio_device()
sounds = {
  "shoot": rl.load_sound("assets/shoot.wav"),
  "hurt": rl.load_sound("assets/hurt.wav"),
  "explode": rl.load_sound("assets/explode.wav")
}

# Obraz tła
background = rl.load_texture("assets/stars.png")

while not rl.window_should_close():
    dt = rl.get_frame_time()

    rl.begin_drawing()
    rl.clear_background(rl.BLACK)
    rl.draw_texture(background, 0, 0, rl.WHITE)

    spaceship.update(dt)
    spaceship.wrap()
    spaceship.draw()

    for asteroid in asteroids:
        asteroid.update(dt)
        asteroid.wrap()
        asteroid.draw()

    # Strzelanie
    if (rl.is_key_pressed(32) and len(bullets) < utils.MAX_BULLETS): # Spacja
        if utils.DEBUG:
            print("STRZAŁ")
        bullet_pos = spaceship.get_nose()
        bullets.append(bullet.Bullet(bullet_pos.x,bullet_pos.y,spaceship.rot,utils.BULLET_SPEED,utils.BULLET_RAD,utils.BULLET_TTL))
        rl.play_sound(sounds["shoot"])

    for b in bullets:
        b.update(dt)
        b.wrap()
        b.draw()

    for a in asteroids:
        # Kolizja asteroidy-pociski
        for b in bullets:
            if utils.check_circle_collision(rl.Vector2(b.x,b.y),b.radius,rl.Vector2(a.x,a.y),a.radius):
                b.alive = False
                a.alive = False
                rl.play_sound(sounds["explode"])
                explosions.append(explosion.Explosion(a.x,a.y,a.radius*1.5))
        # Kolizja asteroidy-statek
        if utils.check_circle_collision(rl.Vector2(spaceship.x, spaceship.y), 15, rl.Vector2(a.x, a.y), a.radius):
            rl.play_sound(sounds["hurt"])
            explosions.append(explosion.Explosion(spaceship.x, spaceship.y, 30))
            spaceship.reset()


    for e in explosions:
        e.update(dt)
        e.draw()

    # Czyszczenie ,,martwych'' obiektów
    bullets = utils.clear_corpses(bullets)
    asteroids = utils.clear_corpses(asteroids)
    explosions = utils.clear_corpses(explosions)

    rl.end_drawing()

# Zwolnij dźwięki
for snd in sounds:
    rl.unload_sound(sounds[snd])
rl.close_audio_device()

# Zwolnij teksturę
rl.unload_texture(background)

rl.close_window()
