import pygame
from classes.Dashboard import Dashboard
from classes.Level import Level
from classes.Menu import Menu
from classes.Sound import Sound
from entities.Mario import Mario


windowSize = 640, 480


def main():
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()
    
    # Real window (resizable)
    display_screen = pygame.display.set_mode(windowSize, pygame.RESIZABLE)
    
    # Virtual screen (fixed resolution)
    virtual_screen = pygame.Surface(windowSize)
    
    max_frame_rate = 60
    dashboard = Dashboard("./img/font.png", 8, virtual_screen)
    sound = Sound()
    level = Level(virtual_screen, sound, dashboard)
    menu = Menu(virtual_screen, dashboard, level, sound)

    while not menu.start:
        # Get events once
        events = pygame.event.get()
        
        # Handle resize events
        for event in events:
             if event.type == pygame.VIDEORESIZE:
                 display_screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
             if event.type == pygame.QUIT:
                 pygame.quit()
                 return

        menu.update(events)
        
        # Scale and blit to display
        scaled = pygame.transform.scale(virtual_screen, display_screen.get_size())
        display_screen.blit(scaled, (0, 0))
        pygame.display.update()

    mario = Mario(0, 0, level, virtual_screen, dashboard, sound, display_surface=display_screen)
    clock = pygame.time.Clock()

    while not mario.restart:
        pygame.display.set_caption("Super Mario running with {:d} FPS".format(int(clock.get_fps())))
        
        # Get events once
        events = pygame.event.get()
        
        # Handle resize events
        for event in events:
             if event.type == pygame.VIDEORESIZE:
                 display_screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
             if event.type == pygame.QUIT:
                 pygame.quit()
                 return

        if mario.pause:
            mario.pauseObj.update(events)
        else:
            level.drawLevel(mario.camera)
            dashboard.update()
            mario.update(events)
            
        # Scale and blit to display
        scaled = pygame.transform.scale(virtual_screen, display_screen.get_size())
        display_screen.blit(scaled, (0, 0))
        pygame.display.update()
        
        clock.tick(max_frame_rate)
    return 'restart'


if __name__ == "__main__":
    exitmessage = 'restart'
    while exitmessage == 'restart':
        exitmessage = main()
