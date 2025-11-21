import pygame
import asyncio
from classes.Dashboard import Dashboard
from classes.Level import Level
from classes.Menu import Menu
from classes.Sound import Sound
from classes.TouchControls import TouchControls
from entities.Mario import Mario


windowSize = 640, 480


async def main():
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
        await asyncio.sleep(0)  # Allow browser to stay responsive

    mario = Mario(0, 0, level, virtual_screen, dashboard, sound, display_surface=display_screen)
    clock = pygame.time.Clock()
    
    # Initialize touch controls for mobile
    touch_controls = TouchControls(windowSize[0], windowSize[1])

    while not mario.restart:
        pygame.display.set_caption("Super Mario running with {:d} FPS".format(int(clock.get_fps())))
        
        # Get events once
        events = pygame.event.get()
        
        # Process touch events and add simulated keyboard events
        additional_events = []
        for event in events:
            simulated = touch_controls.handle_event(event)
            additional_events.extend(simulated)
        
        # Combine original events with simulated ones
        all_events = events + additional_events
        
        # Handle resize events
        for event in all_events:
             if event.type == pygame.VIDEORESIZE:
                 display_screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
             if event.type == pygame.QUIT:
                 pygame.quit()
                 return

        if mario.pause:
            mario.pauseObj.update(all_events)
        else:
            level.drawLevel(mario.camera)
            dashboard.update()
            mario.update(all_events)
        
        # Draw touch controls on top (only visible on mobile)
        touch_controls.draw(virtual_screen)
            
        # Scale and blit to display
        scaled = pygame.transform.scale(virtual_screen, display_screen.get_size())
        display_screen.blit(scaled, (0, 0))
        pygame.display.update()
        await asyncio.sleep(0)  # Allow browser to stay responsive
        
        clock.tick(max_frame_rate)
    return 'restart'


if __name__ == "__main__":
    exitmessage = 'restart'
    while exitmessage == 'restart':
        exitmessage = asyncio.run(main())
