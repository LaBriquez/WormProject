from KeyBoardManager import KeyBoard
from World.Physics import *
from GameLoader.Loader import load


pygame.init()
pygame.display.set_caption("Worms")
screen = pygame.display.set_mode((1280, 720))

GameObject.all = load(screen)
colliders = list[Collider]([c.get_component(Collider) for c in GameObject.all if c.get_component(Collider) is not None])
Time.update_clock()

KeyBoard.init()

background = pygame.image.load("./Map/bg.jpg")

while True:
    KeyBoard.update_key()

    for c in colliders:
        c.self_collisions.clear()

    screen.fill((0, 0, 0))
    screen.blit(background, background.get_rect())

    for g in GameObject.all:
        g.update(screen)

    pygame.display.flip()
    Time.update_clock()
