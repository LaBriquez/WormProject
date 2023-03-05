from __future__ import annotations
from math import sqrt, acos, cos, sin, radians


class Vector2:
    def __init__(self, _x=0.0, _y=0.0):
        self.x, self.y = _x, _y

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, v: float):
        if isinstance(v, float) or isinstance(v, int):
            self._x = float(v)
        else:
            raise AttributeError("x must be a float")

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, v: float):
        if isinstance(v, float) or isinstance(v, int):
            self._y = float(v)
        else:
            raise AttributeError("y must be a float")

    def __add__(self, v: Vector2) -> Vector2:
        return Vector2(self.x + v.x, self.y + v.y)

    def __neg__(self) -> Vector2:
        return Vector2(-self.x, -self.y)

    def __sub__(self, v: Vector2) -> Vector2:
        return Vector2(self.x - v.x, self.y - v.y)

    def __mul__(self, v: float) -> Vector2:
        return Vector2(self.x * v, self.y * v)

    def __truediv__(self, v: float) -> Vector2:
        return Vector2(self.x / v, self.y / v)

    def __floordiv__(self, v: float) -> Vector2:
        return Vector2(self.x // v, self.y // v)

    def __ne__(self, o: Vector2):
        return self.x != o.x or self.y != o.y

    def __eq__(self, o: Vector2):
        return self.x == o.x and self.y == o.y

    def magnitude(self) -> float:
        return sqrt(self.x * self.x + self.y * self.y)

    def normalize(self) -> Vector2:
        return self / self.magnitude()

    def rotate(self, angle: float) -> Vector2:
        cz = cos(radians(angle))
        sz = sin(radians(angle))
        return Vector2(self.x * cz - self.y * sz, self.x * sz + self.y * cz)

    def __str__(self):
        return f"(x : {self.x}, y : {self.y})"

    @staticmethod
    def dot(a: Vector2, b: Vector2) -> float:
        return a.x * b.x + a.y * b.y

    @staticmethod
    def angle(a: Vector2, b: Vector2) -> float:
        return acos(Vector2.dot(a, b) / (a.magnitude() * b.magnitude()))

    @staticmethod
    def proj(u: Vector2, v: Vector2) -> Vector2:
        return u * (Vector2.dot(u, v) / u.magnitude()**2)

    @staticmethod
    def lerp(a: Vector2, b: Vector2, t: float) -> Vector2:
        t = max(0.0, min(t, 1.0))
        return Vector2(a.x * (1 - t) + b.x * t, a.y * (1 - t) + b.y * t)


class Transform:
    def __init__(self):
        self.position = Vector2()
        self.scale = Vector2(1, 1)
        self.rotation = 0.0

    @property
    def position(self) -> Vector2:
        return self._position

    @position.setter
    def position(self, v: Vector2):
        if isinstance(v, Vector2):
            self._position = v
        else:
            raise AttributeError("position must be a Vector2")

    @property
    def scale(self) -> Vector2:
        return self._scale

    @scale.setter
    def scale(self, v: Vector2):
        if isinstance(v, Vector2):
            self._scale = v
        else:
            raise AttributeError("scale must be a Vector2")

    @property
    def rotation(self) -> float:
        return self._rotation

    @rotation.setter
    def rotation(self, v: float):
        if isinstance(v, float) or isinstance(v, int):
            self._rotation = float(v)
        else:
            raise AttributeError("rotation must be a float")

    def local2world(self, p: Vector2) -> Vector2:
        return Vector2(p.x * self.scale.x, p.y * self.scale.y).rotate(self.rotation) + self.position

    def world2local(self, p: Vector2) -> Vector2:
        return (Vector2(p.x / self.scale.x, p.y / self.scale.y) - self.position).rotate(-self.rotation) \
            if self.scale.x != 0 and self.scale.y != 0 else Vector2()
    