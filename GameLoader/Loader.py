from Player import Player
from World.Physics import *
from World.GameObject import *


def load(screen: pygame.Surface) -> list[GameObject]:
    gameobjects = []

    Camera(screen.get_width(), screen.get_height(), 10)

    g = GameObject("secondSquare")
    c = g.addcomponent(SquareCollider)
    c.size = Vector2(200, 7)
    gameobjects.append(g)
    g.transform.rotation = 0
    g.transform.position = Vector2(0, -30)

    g = GameObject("p1")
    g.transform.position = Vector2(20, -18)
    p = g.addcomponent(Player)
    p.image = pygame.image.load("./Worm/worm.png")
    p.transform.scale = Vector2(50, 50)
    Player.team.append(p)

    gameobjects.append(g)

    g = GameObject("p2")
    g.transform.position = Vector2(-20, -18)

    p = g.addcomponent(Player)
    p.image = pygame.image.load("./Worm/worm.png")
    p.transform.scale = Vector2(50, 50)
    Player.team.append(p)

    gameobjects.append(g)

    Rigidbody.drawer = False

    return gameobjects
