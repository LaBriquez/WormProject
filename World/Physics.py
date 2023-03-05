from __future__ import annotations

from math import degrees

from World.GameObject import *
from time import time_ns


class Time:
    _deltatime = 0.0
    _clock = time_ns()

    @staticmethod
    def update_clock():
        c = time_ns()
        Time._deltatime = (c - Time._clock) / 1000000000.0 + 0.000000000001
        Time._clock = c

    @staticmethod
    def deltatime() -> float:
        return Time._deltatime

    @classmethod
    def deltaTime(cls):
        return Time._deltatime


class Collision:
    def __init__(self, p=Vector2(), n=Vector2(), c: Collider = None):
        self._point = p
        self._normal = n
        self._collider = c

    @property
    def point(self) -> Vector2:
        return self._point

    @property
    def normal(self) -> Vector2:
        return self._normal

    @property
    def collider(self) -> Collider:
        return self._collider


class Collider(GameComponent):
    colliders = []

    def __init__(self, g: GameObject):
        super().__init__(g)
        Collider.colliders.append(self)
        self.self_collisions = list[Collision]()

    def get_collision(self, c: Collider) -> Collision:
        pass

    def closest_point(self, p: Vector2) -> Collision:
        pass

    def remove(self):
        Collider.colliders.remove(self)


class SquareCollider(Collider):
    def __init__(self, g: GameObject):
        super().__init__(g)
        self.size = Vector2(1, 1)

    @property
    def size(self) -> Vector2:
        return self._size

    @size.setter
    def size(self, v: Vector2):
        if isinstance(v, Vector2):
            self._size = v
        else:
            raise AttributeError("size must be a Vector2")

    def draw(self, screen: pygame.Surface):
        if not Rigidbody.drawer:
            return

        p1 = Camera.main.world2screen(self.transform.local2world(self._size))
        p2 = Camera.main.world2screen(self.transform.local2world(Vector2(-self._size.x, self._size.y)))
        p3 = Camera.main.world2screen(self.transform.local2world(-self._size))
        p4 = Camera.main.world2screen(self.transform.local2world(Vector2(self._size.x, -self._size.y)))
        pygame.draw.lines(screen, (255, 255, 255), False,
                          [(p1.x, p1.y), (p2.x, p2.y), (p3.x, p3.y), (p4.x, p4.y), (p1.x, p1.y)])

    def get_collision(self, c: Collider) -> Collision:
        ccp = c.closest_point(self.transform.position)
        cp = self.closest_point(c.transform.position)
        mid = Vector2.lerp(ccp.point, cp.point, 0.5)

        for i in range(20):
            ccp = c.closest_point(mid)
            cp = self.closest_point(mid)
            mid = Vector2.lerp(ccp.point, cp.point, 0.5)

        lp = self.transform.world2local(mid)

        size = Vector2(self._size.x * self.transform.scale.x, self._size.y * self.transform.scale.y)

        return Collision(mid, ccp.normal, self) \
            if abs(lp.x) < size.x + 0.025 and abs(lp.y) < size.y + 0.025 else \
            Collision()

    def closest_point(self, p: Vector2) -> Collision:
        local = self.transform.world2local(p)
        size = self._size
        angle = degrees(Vector2.angle(local, Vector2(1, 0)))

        f_ang = degrees(Vector2.angle(size, Vector2(1, 0)))
        s_ang = degrees(Vector2.angle(-size, Vector2(1, 0)))

        if angle < f_ang:
            point = Vector2(size.x, size.y if local.y > size.y else max(local.y, -size.y))
            normal = Vector2(1, 0)
        elif angle < s_ang:
            if local.y > 0:
                point = Vector2(size.x if local.x > size.x else max(local.x, -size.x), size.y)
                normal = Vector2(0, 1)
            else:
                point = Vector2(size.x if local.x > size.x else max(local.x, -size.x), -size.y)
                normal = Vector2(0, -1)
        else:
            point = Vector2(-size.x, size.y if local.y > size.y else max(local.y, -size.y))
            normal = Vector2(-1, 0)

        if abs(local.x) < size.x and abs(local.y) < size.y:
            return Collision(p, normal.rotate(self.transform.rotation), self)

        return Collision(self.transform.local2world(point), normal.rotate(self.transform.rotation), self)


class CircleCollider(Collider):
    def __init__(self, g: GameObject):
        super().__init__(g)
        self._radius = 1

    def draw(self, screen: pygame.Surface):
        if not Rigidbody.drawer:
            return
        p = Camera.main.world2screen(self.transform.position)
        pygame.draw.circle(screen, (255, 255, 255), (p.x, p.y), Camera.main.scale * self._radius)

    def get_collision(self, c: Collider) -> Collision:
        p = c.closest_point(self.transform.position)
        return p if (p.point - self.transform.position).magnitude() < self._radius else Collision()

    def closest_point(self, p: Vector2) -> Collision:
        direction = (p - self.transform.position)
        mag = direction.magnitude()
        if mag < self._radius:
            return Collision(p, direction / mag, self)
        return Collision(direction / mag * self._radius, direction / mag, self)


class Rigidbody(GameComponent):
    drawer = True

    def __init__(self, g: GameObject):
        super().__init__(g)
        self._collider = g.get_component(Collider)
        self._velocity = Vector2()
        self.gravity = 10.0
        self._bounce = .5
        self.n = Vector2()
        self.frottement = .5

    @property
    def bounce(self) -> float:
        return self._bounce

    @bounce.setter
    def bounce(self, v: float):
        if isinstance(v, float) or isinstance(v, int):
            self._bounce = min(1.0, max(0.0, v))
        else:
            raise AttributeError("bounce must be a float")

    @property
    def gravity(self) -> float:
        return self._gravity

    @gravity.setter
    def gravity(self, v: float):
        if isinstance(v, float) or isinstance(v, int):
            self._gravity = float(v)
        else:
            raise AttributeError("gravity must be a float")

    def update(self):
        pos = self.transform.position

        self.transform.position = Vector2(self._velocity.x * Time.deltatime() + self.transform.position.x,
                                          -self._gravity * 0.5 * Time.deltatime() * Time.deltatime() +
                                          self._velocity.y * Time.deltatime() +
                                          self.transform.position.y)

        self._velocity = (self.transform.position - pos) / Time.deltatime()
        for r in Collider.colliders:
            if r is self._collider:
                continue
            c = self._collider.get_collision(r)

            if c.point != Vector2(0, 0):
                self._velocity = (-Vector2.proj(c.normal, self._velocity) * 2.0 + self._velocity) * self._bounce
                self.transform.position += c.normal * Time.deltatime()
                self.n = self._velocity
                self._collider.self_collisions.append(c)
                r.self_collisions.append(c)

    def add_velocity(self, v: Vector2):
        self._velocity += v

    def draw(self, scene: pygame.Surface):
        if not Rigidbody.drawer:
            return

        s = Camera.main.world2screen(self.transform.position)
        e = Camera.main.world2screen(self.transform.position + self.n)
        pygame.draw.line(scene, (255, 255, 255), (s.x, s.y), (e.x, e.y))
