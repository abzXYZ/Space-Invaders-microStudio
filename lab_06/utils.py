import pyray as rl

DEBUG = False
DEBUG_FPS = 60

SCREEN_W = 800
SCREEN_H = 600

# Dane asteroidy
EDGES = 9 # Ilość kątów wielokąta

# Dane statku
THRUST = 1      # Siła przyspieszenia. Wartość 1 skutkuje umiarkowanym, mało gwałtownym rozpędem. 
MAX_SPEED = 50  # Maksymalna prędkość. Wartość 50 nie jest za szybka, ale na ten moment nie widzę potrzeby na większą.
ROT_SPEED = 3   # Szybkość obrotu. Wartość 3 pozwala na kontrolowane sterowanie.
FRICTION = 1    # Tarcie. Wartość 1 sprawia, że hamuje gładko, ale zdecydowanie.

def ghost_positions(x, y, size):
    ghosts = []

    near_right = x + size > SCREEN_W
    near_left = x < size
    near_bottom = y + size > SCREEN_H
    near_top = y < size

    if near_right:
        gx = x - SCREEN_W
    elif near_left:
        gx = x + SCREEN_W
    else:
        gx = None

    if near_bottom:
        gy = y - SCREEN_H
    elif near_top:
        gy = y + SCREEN_H
    else:
        gy = None

    if gx is not None:
        ghosts.append(rl.Vector2(gx, y))   # prawo/lewo
    if gy is not None:
        ghosts.append(rl.Vector2(x, gy))   # góra/dół
    if gx is not None and gy is not None:
        ghosts.append(rl.Vector2(gx, gy))  # rogi

    return ghosts