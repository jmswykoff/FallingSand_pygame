import pygame

from simulation import Simulation

# pygame boilerplate
pygame.init()
pygame.mouse.set_visible(False)

#game window width, these are supposed to be constant, so all caps
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 800

#how many pixels on the screen one particle takes up
CELL_SIZE = 6
FPS = 120
GREY = (29, 29, 29)

#creates a window and sets the header
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Falling Sand")

clock = pygame.time.Clock()

# instantiate the simulation
sim = Simulation(WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE)

#Simulation Loop
while True:
    # 1. Event handling
    sim.handle_controls()
    sim.handle_mouse()

    # 2. Updating state
    sim.update()

    # 3. Drawing
    window.fill(GREY)
    sim.draw(window)

    pygame.display.flip()
    clock.tick(FPS)