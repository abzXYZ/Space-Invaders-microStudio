import pyray as rl
import math

class Ship:
    points = [rl.Vector2(0, -15),rl.Vector2(-10, 10),rl.Vector2(10, 10)]
    flame_points = [rl.Vector2(-7, 10), rl.Vector2(7, 10), rl.Vector2(0, 20)]
    velocity = 0
    thrusting = False
    debug_mode = False
    THRUST = 1      # Siła przyspieszenia. Wartość 1 skutkuje umiarkowanym, mało gwałtownym rozpędem. 
    MAX_SPEED = 50  # Maksymalna prędkość. Wartość 50 nie jest za szybka, ale na ten moment nie widzę potrzeby na większą.
    ROT_SPEED = 3   # Szybkość obrotu. Wartość 3 pozwala na kontrolowane sterowanie.
    FRICTION = 1    # Tarcie. Wartość 1 sprawia, że hamuje gładko, ale zdecydowanie.

    def __init__(self, x = 0, y = 0, rot = 0):
        self.x = x
        self.y = y
        self.rot = rot
        self.direction = rl.Vector2(math.cos(math.radians(rot - 90)),math.sin(math.radians(rot - 90)))

    # Metoda pomocnicza do limitowania wartości (Teraz się nie przyda ale jest na potem może)
    def clamp(n, min, max):
        if n < min:
            return min
        elif n > max:
            return max
        else:
            return n

    # Funkcja do obrotu punktu tym macierzowym sposobem
    def rotate_point(self, point):
        cos_a = math.cos(math.radians(self.rot))
        sin_a = math.sin(math.radians(self.rot))
        return rl.Vector2(point.x * cos_a - point.y * sin_a, point.x * sin_a + point.y * cos_a)

    # Funkcja do otrzymywania globalnej pozycji punktu
    def point_pos(self, point):
        return rl.Vector2(point.x + self.x, point.y + self.y)

    def update(self, dt):
        if (rl.is_key_down(265)): # Strzałka w górę
            self.thrusting = True
            if self.velocity < self.MAX_SPEED:
                self.velocity += self.THRUST
                if self.velocity > self.MAX_SPEED:
                    self.velocity = self.MAX_SPEED
        else:
            self.thrusting = False
            if (self.velocity > 0): # Mechanika tarcia
                self.velocity -= self.FRICTION
                if self.velocity < 0:
                    self.velocity = 0
        if (rl.is_key_down(263) or rl.is_key_down(262)):
            # Strzałka w lewo
            if (rl.is_key_down(263)):
                self.rot -= self.ROT_SPEED
                if self.rot < 0:
                    self.rot = 360 + self.rot
            # Strzałka w prawo
            else:
                self.rot += self.ROT_SPEED
                if self.rot > 360:
                    self.rot = self.rot - 360
            self.direction = rl.Vector2(math.cos(math.radians(self.rot - 90)),math.sin(math.radians(self.rot - 90)))

        self.x += self.velocity * self.direction.x * dt
        self.y += self.velocity * self.direction.y * dt



    def draw(self):
        p1 = self.point_pos(self.rotate_point(self.points[0]))
        p2 = self.point_pos(self.rotate_point(self.points[1]))
        p3 = self.point_pos(self.rotate_point(self.points[2]))
        rl.draw_triangle(p1,p2,p3,rl.MAGENTA)
        # Ogień za statkiem
        if self.thrusting:
            f1 = self.point_pos(self.rotate_point(self.flame_points[0]))
            f2 = self.point_pos(self.rotate_point(self.flame_points[1]))
            f3 = self.point_pos(self.rotate_point(self.flame_points[2]))
            rl.draw_triangle(f1,f2,f3,rl.ORANGE)
        if self.debug_mode:
            tip = rl.Vector2(self.x + self.direction.x * self.velocity,self.y + self.direction.y * self.velocity)
            rl.draw_line_v(rl.Vector2(self.x, self.y), tip, rl.YELLOW)