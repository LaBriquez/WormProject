from __future__ import annotations
import pygame

from Transform.Transform import *


class GameComponent:
    def __init__(self, g: GameObject):
        self._transform = g.transform
        self._gameobject = g

    def __str__(self):
        return f"{self._gameobject}, {type(self)}"

    @property
    def transform(self) -> Transform:
        return self._transform

    @property
    def gameobject(self) -> GameObject:
        return self._gameobject

    def remove(self):
        pass

    def first_update(self):
        pass

    def update(self):
        pass

    def draw(self, scene: pygame.Surface):
        pass


class GameObject:
    all = list["GameObject"]()

    @staticmethod
    def remove(g: GameObject):
        GameObject.all.remove(g)
        for c in g._gameComponents:
            c.remove()

    def __init__(self, n: str = "gameobject"):
        self._name = n
        self._transform = Transform()
        self._gameComponents = []

    def __str__(self):
        return f"{self._name}"

    @property
    def transform(self) -> Transform:
        return self._transform

    def update(self, scene: pygame.Surface):
        for c in self._gameComponents:
            c.first_update()
            c.update()
            c.draw(scene)

    def addcomponent(self, c) -> GameComponent:
        if issubclass(c, GameComponent):
            self._gameComponents.append(c(self))
            return self._gameComponents[len(self._gameComponents) - 1]
        return None

    def get_component(self, c: type) -> GameComponent:
        return next((x for x in self._gameComponents if issubclass(type(x), c)), None)


class Camera:
    main: Camera = None

    def __init__(self, w: float, h: float, s=10.0):
        self._transform = Transform()
        self._width = w
        self._height = h
        self.scale = s
        Camera.main = self

    @property
    def transform(self) -> Transform:
        return self._transform

    @property
    def scale(self) -> float:
        return self._scale

    @scale.setter
    def scale(self, v: float):
        if isinstance(v, float) or isinstance(v, int):
            self._scale = float(v)
        else:
            raise AttributeError("scale must be a float")

    def world2screen(self, v: Vector2) -> Vector2:
        p = self._transform.world2local(v)
        return Vector2(p.x * self.scale + self._width / 2.0,
                       -p.y * self.scale + self._height / 2.0)

    def screen2world(self, v: Vector2) -> Vector2:
        p = self._transform.local2world(v)
        return Vector2(p.x / self.scale + self._width / 2.0,
                       -p.y / self.scale + self._height / 2.0)
