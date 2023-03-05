import pygame
import math

from KeyBoardManager import KeyBoard
from World.GameObject import GameComponent, GameObject, Camera
from World.Physics import Time, CircleCollider, Rigidbody, Collider
from Transform.Transform import Vector2


class Player(GameComponent):
    team = []
    cpt = 0
    temps = 0.0

    def __init__(self, g: GameObject):
        self.weapon = [Grenade(), Rocket()]
        self.chow = 0
        super().__init__(g)
        self.speed = 10.0
        self._hp = 100.0
        self.image = None

    @property
    def hp(self) -> float:
        return self._hp

    @property
    def speed(self) -> float:
        return self._speed

    @speed.setter
    def speed(self, v: float):
        if isinstance(v, float) or isinstance(v, int):
            self._speed = v
        else:
            raise AttributeError("speed must be a float")

    def first_update(self):
        if Player.temps > 0:
            Player.temps -= Time.deltatime()

    def update(self):
        if Player.temps > 0:
            return
        if self is not Player.team[Player.cpt]:
            return

        if KeyBoard.key_down[pygame.K_i]:
            Player.temps += 1
            Player.cpt += 1
            if Player.cpt >= len(Player.team):
                Player.cpt = 0

        if KeyBoard.key_pressed[pygame.K_s]:
            a = self.weapon[self.chow].angle + 100 * Time.deltaTime()
            self.weapon[self.chow].angle = min(90, max(-90, a))
        if KeyBoard.key_pressed[pygame.K_z]:
            a = self.weapon[self.chow].angle - 100 * Time.deltaTime()
            self.weapon[self.chow].angle = min(90, max(-90, a))

        if KeyBoard.key_pressed[pygame.K_d]:
            self.transform.position.x += self.speed * Time.deltatime()
            for w in self.weapon:
                w.left = True

        if KeyBoard.key_pressed[pygame.K_q]:
            self.transform.position.x -= self.speed * Time.deltatime()
            for w in self.weapon:
                w.left = False

        if KeyBoard.key_down[pygame.K_h]:
            self.chow += 1
            if self.chow >= len(self.weapon):
                self.chow = 0

        if KeyBoard.key_down[pygame.K_SPACE]:
            self.weapon[self.chow].fire(self)
            Player.temps += 1
            Player.cpt += 1
            if Player.cpt >= len(Player.team):
                Player.cpt = 0

    def draw(self, screen: pygame.Surface):
        p = Camera.main.world2screen(self.transform.position)

        screen.blit(pygame.transform.rotate(pygame.transform.scale(pygame.transform.flip(self.image,
                                                                                         self.weapon[self.chow].left,
                                                                                         False),
                                                                   (self.transform.scale.x,
                                                                    self.transform.scale.y)),
                                            self.transform.rotation), (p.x, p.y))
        screen.blit(pygame.transform.rotate(pygame.transform.scale(pygame.transform.flip(self.weapon[self.chow].image,
                                                                                         self.weapon[self.chow].left,
                                                                                         False),
                                                                   (self.transform.scale.x * 0.7,
                                                                    self.transform.scale.y * 0.7)),
                                            self.weapon[self.chow].angle), (p.x, p.y))

        hp = Camera.main.world2screen(self.transform.local2world(Vector2(0, 0.05)))
        screen.blit(pygame.font.SysFont(None, 24)
                    .render('hp : ' + str(int(self._hp)),
                            True, (255, 255, 0)),
                    (hp.x, hp.y))

    def damage(self, d):
        self._hp -= d


class Weapon:
    def fire(self, p: Player):
        pass


class GrenadeLau(GameComponent):
    def __init__(self, g: GameObject):
        super().__init__(g)
        self.timer = 3.0
        self.image = None
        self.radius = 10
        self.dmg = 40

    def update(self):
        self.timer -= Time.deltaTime()
        if self.timer < 0:
            g = self.gameobject
            GameObject.remove(g)
            for p in Player.team:
                d = (p.transform.position - self.transform.position).magnitude()
                if d < self.radius:
                    p.damage(self.dmg * (1 - d / self.radius))

    def draw(self, screen: pygame.Surface):
        p = Camera.main.world2screen(self.transform.position)
        screen.blit(pygame.transform.scale(self.image, (
            self.transform.scale.x * 20,
            self.transform.scale.y * 20
        )), (p.x, p.y))


class RockLau(GameComponent):
    def __init__(self, g: GameObject):
        super().__init__(g)
        self.collider = self.gameobject.get_component(Collider)
        self.timer = 3.0
        self.image = None
        self.radius = 10
        self.dmg = 40

    def update(self):
        self.timer -= Time.deltaTime()
        if self.timer < 0 or len(self.collider.self_collisions) != 0:
            g = self.gameobject
            GameObject.remove(g)
            for p in Player.team:
                d = (p.transform.position - self.transform.position).magnitude()
                if d < self.radius:
                    p.damage(self.dmg * (1 - d / self.radius))

    def draw(self, screen: pygame.Surface):
        p = Camera.main.world2screen(self.transform.position)
        screen.blit(pygame.transform.scale(self.image, (
            self.transform.scale.x * 20,
            self.transform.scale.y * 20
        )), (p.x, p.y))


class Grenade(Weapon):
    def __init__(self):
        self.angle = 0
        self.left = False
        self.image = pygame.image.load("./Weapon/grenade.png")

    def fire(self, p: Player):
        g = GameObject("grenade")
        g.transform.position = Vector2(p.transform.position.x, p.transform.position.y)
        g.addcomponent(CircleCollider)
        g.addcomponent(GrenadeLau).image = pygame.image.load("./Weapon/grenade.png")
        rb = g.addcomponent(Rigidbody)
        rb.gravity = 70
        rb.add_velocity(Vector2(40 if self.left else -40, 0).rotate(self.angle))
        GameObject.all.append(g)


class Rocket(Weapon):
    def __init__(self):
        self.angle = 0
        self.left = False
        self._dmg = 50
        self.image = pygame.image.load("./Weapon/roquette.png")

    def fire(self, p: Player):
        g = GameObject("rocket")
        g.transform.position = Vector2(p.transform.position.x, p.transform.position.y)
        g.addcomponent(CircleCollider)
        g.addcomponent(RockLau).image = pygame.image.load("./Weapon/grenade.png")
        rb = g.addcomponent(Rigidbody)
        rb.gravity = 70
        rb.add_velocity(Vector2(40 if self.left else -40, 0).rotate(self.angle))
        GameObject.all.append(g)


'''class Team(GameComponent):
    def __init__(self, g: GameObject):
        super().__init__(g)
        self._players = list[Player]()
        self._index = 0
        self.color = pygame.Color(255, 0, 0)

    def add_player(self, p: Player):
        self._players.append(p)

    def update(self):
        if KeyBoardManager.KeyBoard.key_pressed[pygame.K_d]:
            p = self._players[self._index]
            p.transform.position.x += p.speed * Time.deltatime()
        if KeyBoardManager.KeyBoard.key_pressed[pygame.K_q]:
            p = self._players[self._index]
            p.transform.position.x -= p.speed * Time.deltatime()'''
