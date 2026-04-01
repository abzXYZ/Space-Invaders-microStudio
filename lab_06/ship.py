import pyray as rl
import math
import utils

class Ship:
    points = [rl.Vector2(0, -15),rl.Vector2(-10, 10),rl.Vector2(10, 10)]
    flame_points = [rl.Vector2(-7, 10), rl.Vector2(7, 10), rl.Vector2(0, 20)]

    def __init__(self, x = 0, y = 0, rot = 0):
        self.x = x
        self.y = y
        self.rot = rot
        self.direction = rl.Vector2(math.cos(math.radians(rot - 90)),math.sin(math.radians(rot - 90)))
        self.thrusting = False
        self.velocity = 0

    # Funkcja do obrotu punktu tym macierzowym sposobem
    def rotate_point(self, point):
        cos_a = math.cos(math.radians(self.rot))
        sin_a = math.sin(math.radians(self.rot))
        return rl.Vector2(point.x * cos_a - point.y * sin_a, point.x * sin_a + point.y * cos_a)

    # Funkcja do otrzymywania globalnej pozycji punktu
    def point_pos(self, point, x, y):
        return rl.Vector2(point.x + x, point.y + y)

    # Wrapowanie przy krawędziach okna z wykorzystaniem operatora modulo
    def wrap(self):
        self.x = self.x % utils.SCREEN_W
        self.y = self.y % utils.SCREEN_H

    # Funkcja do rysowania statku (żeby nie kopiować kodu)
    def draw_ship(self,x,y):
        p1 = self.point_pos(self.rotate_point(self.points[0]),x,y)
        p2 = self.point_pos(self.rotate_point(self.points[1]),x,y)
        p3 = self.point_pos(self.rotate_point(self.points[2]),x,y)
        rl.draw_triangle(p1,p2,p3,rl.MAGENTA)

    def update(self, dt):
        if (rl.is_key_down(265)): # Strzałka w górę
            self.thrusting = True
            if self.velocity < utils.MAX_SPEED:
                self.velocity += utils.THRUST
                if self.velocity > utils.MAX_SPEED:
                    self.velocity = utils.MAX_SPEED
        else:
            self.thrusting = False
            if (self.velocity > 0): # Mechanika tarcia
                self.velocity -= utils.FRICTION
                if self.velocity < 0:
                    self.velocity = 0
        if (rl.is_key_down(263) or rl.is_key_down(262)):
            # Strzałka w lewo
            if (rl.is_key_down(263)):
                self.rot -= utils.ROT_SPEED
                if self.rot < 0:
                    self.rot = 360 + self.rot
            # Strzałka w prawo
            else:
                self.rot += utils.ROT_SPEED
                if self.rot > 360:
                    self.rot = self.rot - 360
            self.direction = rl.Vector2(math.cos(math.radians(self.rot - 90)),math.sin(math.radians(self.rot - 90)))

        self.x += self.velocity * self.direction.x * dt
        self.y += self.velocity * self.direction.y * dt

    def draw(self):
        # Rysuj statek
        self.draw_ship(self.x,self.y)

        # Rysuj odbicia lustrzane statku (rozmiar ok. 25)
        for g in utils.ghost_positions(self.x,self.y,25):
            self.draw_ship(g.x,g.y)

        # Ogień za statkiem
        if self.thrusting:
            f1 = self.point_pos(self.rotate_point(self.flame_points[0]),self.x,self.y)
            f2 = self.point_pos(self.rotate_point(self.flame_points[1]),self.x,self.y)
            f3 = self.point_pos(self.rotate_point(self.flame_points[2]),self.x,self.y)
            rl.draw_triangle(f1,f2,f3,rl.ORANGE)
        if utils.DEBUG:
            tip = rl.Vector2(self.x + self.direction.x * self.velocity,self.y + self.direction.y * self.velocity)
            rl.draw_line_v(rl.Vector2(self.x, self.y), tip, rl.YELLOW)