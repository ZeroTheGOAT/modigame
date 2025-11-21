import pygame
import cv2
import sys

from classes.Animation import Animation
from classes.Camera import Camera
from classes.Collider import Collider
from classes.EntityCollider import EntityCollider
from classes.Input import Input
from classes.Sprites import Sprites
from entities.EntityBase import EntityBase
from entities.Mushroom import RedMushroom
from traits.bounce import bounceTrait
from traits.go import GoTrait
from traits.jump import JumpTrait
from classes.Pause import Pause

spriteCollection = Sprites().spriteCollection
smallAnimation = Animation(
    [
        spriteCollection["mario_run1"].image,
        spriteCollection["mario_run2"].image,
        spriteCollection["mario_run3"].image,
    ],
    spriteCollection["mario_idle"].image,
    spriteCollection["mario_jump"].image,
)
bigAnimation = Animation(
    [
        spriteCollection["mario_big_run1"].image,
        spriteCollection["mario_big_run2"].image,
        spriteCollection["mario_big_run3"].image,
    ],
    spriteCollection["mario_big_idle"].image,
    spriteCollection["mario_big_jump"].image,
)

happyAnimation = Animation(
    [
        spriteCollection["mario_happy_run1"].image,
        spriteCollection["mario_happy_run2"].image,
        spriteCollection["mario_happy_run3"].image,
    ],
    spriteCollection["mario_happy_idle"].image,
    spriteCollection["mario_happy_jump"].image,
)
bigHappyAnimation = Animation(
    [
        spriteCollection["mario_big_happy_run1"].image,
        spriteCollection["mario_big_happy_run2"].image,
        spriteCollection["mario_big_happy_run3"].image,
    ],
    spriteCollection["mario_big_happy_idle"].image,
    spriteCollection["mario_big_happy_jump"].image,
)


class Mario(EntityBase):
    def __init__(self, x, y, level, screen, dashboard, sound, gravity=0.8, display_surface=None):
        super(Mario, self).__init__(x, y, gravity)
        self.display_surface = display_surface
        self.camera = Camera(self.rect, self)
        self.sound = sound
        self.input = Input(self)
        self.inAir = False
        self.inJump = False
        self.powerUpState = 0
        self.invincibilityFrames = 0
        self.traits = {
            "jumpTrait": JumpTrait(self),
            "goTrait": GoTrait(smallAnimation, screen, self.camera, self),
            "bounceTrait": bounceTrait(self),
        }

        self.levelObj = level
        self.collision = Collider(self, level)
        self.screen = screen
        self.EntityCollider = EntityCollider(self)
        self.dashboard = dashboard
        self.restart = False
        self.pause = False
        self.pauseObj = Pause(screen, self, dashboard)
        
        self.happyTimer = 0
        self.isHappy = False

    def update(self, events):
        if self.invincibilityFrames > 0:
            self.invincibilityFrames -= 1
        
        # Happy logic
        if self.happyTimer > 0:
            self.happyTimer -= 1
            if not self.isHappy:
                self.isHappy = True
                if self.powerUpState == 0:
                    self.traits['goTrait'].updateAnimation(happyAnimation)
                else:
                    self.traits['goTrait'].updateAnimation(bigHappyAnimation)
        elif self.isHappy:
            self.isHappy = False
            if self.powerUpState == 0:
                self.traits['goTrait'].updateAnimation(smallAnimation)
            else:
                self.traits['goTrait'].updateAnimation(bigAnimation)

        self.updateTraits()
        self.moveMario()
        self.camera.move()
        self.applyGravity()
        self.checkEntityCollision()
        self.input.checkForInput(events)

    def moveMario(self):
        self.rect.y += self.vel.y
        self.collision.checkY()
        self.rect.x += self.vel.x
        self.collision.checkX()

    def checkEntityCollision(self):
        for ent in self.levelObj.entityList:
            collisionState = self.EntityCollider.check(ent)
            if collisionState.isColliding:
                if ent.type == "Item":
                    self._onCollisionWithItem(ent)
                elif ent.type == "Block":
                    self._onCollisionWithBlock(ent)
                elif ent.type == "Mob":
                    self._onCollisionWithMob(ent, collisionState)
                elif ent.type == "Meloni":
                    self.winGame()

    def _onCollisionWithItem(self, item):
        self.levelObj.entityList.remove(item)
        self.dashboard.points += 100
        self.dashboard.coins += 1
        self.sound.play_sfx(self.sound.coin)
        # Trigger happy state
        self.happyTimer = 120 # 2 seconds at 60fps

    def _onCollisionWithBlock(self, block):
        if not block.triggered:
            self.dashboard.coins += 1
            self.sound.play_sfx(self.sound.bump)
        block.triggered = True

    def _onCollisionWithMob(self, mob, collisionState):
        if isinstance(mob, RedMushroom) and mob.alive:
            self.powerup(1)
            self.killEntity(mob)
            self.sound.play_sfx(self.sound.powerup)
        elif collisionState.isTop and (mob.alive or mob.bouncing):
            self.sound.play_sfx(self.sound.stomp)
            self.rect.bottom = mob.rect.top
            self.bounce()
            self.killEntity(mob)
        elif collisionState.isTop and mob.alive and not mob.active:
            self.sound.play_sfx(self.sound.stomp)
            self.rect.bottom = mob.rect.top
            mob.timer = 0
            self.bounce()
            mob.alive = False
        elif collisionState.isColliding and mob.alive and not mob.active and not mob.bouncing:
            mob.bouncing = True
            if mob.rect.x < self.rect.x:
                mob.leftrightTrait.direction = -1
                mob.rect.x += -5
                self.sound.play_sfx(self.sound.kick)
            else:
                mob.rect.x += 5
                mob.leftrightTrait.direction = 1
                self.sound.play_sfx(self.sound.kick)
        elif collisionState.isColliding and mob.alive and not self.invincibilityFrames:
            if self.powerUpState == 0:
                self.gameOver()
            elif self.powerUpState == 1:
                self.powerUpState = 0
                self.traits['goTrait'].updateAnimation(smallAnimation)
                x, y = self.rect.x, self.rect.y
                self.rect = pygame.Rect(x, y + 32, 32, 32)
                self.invincibilityFrames = 60
                self.sound.play_sfx(self.sound.pipe)

    def bounce(self):
        self.traits["bounceTrait"].jump = True

    def killEntity(self, ent):
        if ent.__class__.__name__ != "Koopa":
            ent.alive = False
        else:
            ent.timer = 0
            ent.leftrightTrait.speed = 1
            ent.alive = True
            ent.active = False
            ent.bouncing = False
        self.dashboard.points += 100
        self.sound.play_sfx(self.sound.ah)

    def gameOver(self):
        # Stop music and play death sound
        self.sound.music_channel.stop()
        self.sound.music_channel.play(self.sound.death)
        
        # Load out.png image
        try:
            out_image = pygame.image.load("./img/out.png").convert_alpha()
        except:
            out_image = pygame.image.load("./img/out.png")
        
        # Get original image dimensions
        original_width, original_height = out_image.get_size()
        
        # Calculate target size (25% of screen = 160x120 for 640x480 screen)
        screen_width, screen_height = 640, 480
        target_width = int(screen_width * 0.25)
        target_height = int(screen_height * 0.25)
        
        # Maintain aspect ratio
        aspect_ratio = original_width / original_height
        if target_width / target_height > aspect_ratio:
            target_width = int(target_height * aspect_ratio)
        else:
            target_height = int(target_width / aspect_ratio)
        
        # Animation parameters
        total_frames = 66  # 1.1 seconds at 60fps
        center_x = screen_width // 2
        center_y = screen_height // 2
        
        # Create font for "YOUR OUT" text
        font = pygame.font.Font(None, 48)
        
        clock = pygame.time.Clock()
        
        # Animate from 0% to 100% scale over 1.1 seconds
        for frame in range(total_frames + 1):
            # Calculate current scale (0 to 1)
            scale = frame / total_frames
            
            # Calculate current dimensions
            current_width = int(target_width * scale)
            current_height = int(target_height * scale)
            
            if current_width > 0 and current_height > 0:
                # Scale the image
                scaled_image = pygame.transform.scale(out_image, (current_width, current_height))
                
                # Calculate position to center the image
                image_x = center_x - current_width // 2
                image_y = center_y - current_height // 2
                
                # Fill screen with black
                self.screen.fill((0, 0, 0))
                
                # Draw the scaled image
                self.screen.blit(scaled_image, (image_x, image_y))
                
                # Draw "YOUR OUT" text below the image (fade in with the image)
                text = font.render("YOUR OUT", True, (255, 255, 255))
                text.set_alpha(int(255 * scale))
                text_rect = text.get_rect(center=(center_x, image_y + current_height + 40))
                self.screen.blit(text, text_rect)
                
                # Update display
                if self.display_surface:
                    scaled = pygame.transform.scale(self.screen, self.display_surface.get_size())
                    self.display_surface.blit(scaled, (0, 0))
                
                pygame.display.update()
                
                # Handle events
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                
                clock.tick(60)  # 60 fps
        
        # Wait for death sound to finish
        while self.sound.music_channel.get_busy():
            # Keep displaying the final frame
            if self.display_surface:
                scaled = pygame.transform.scale(self.screen, self.display_surface.get_size())
                self.display_surface.blit(scaled, (0, 0))
            pygame.display.update()
            events = pygame.event.get()
            self.input.checkForInput(events)
            clock.tick(60)
        
        self.restart = True

    def getPos(self):
        return self.camera.x + self.rect.x, self.rect.y

    def setPos(self, x, y):
        self.rect.x = x
        self.rect.y = y
        
    def powerup(self, powerupID):
        if self.powerUpState == 0:
            if powerupID == 1:
                self.powerUpState = 1
                self.traits['goTrait'].updateAnimation(bigAnimation)
                self.rect = pygame.Rect(self.rect.x, self.rect.y-32, 32, 64)
                self.invincibilityFrames = 20

    def winGame(self):
        # Stop music
        self.sound.music_channel.stop()
        
        # Show Win Screen First
        font = pygame.font.Font(None, 74)
        text = font.render("You Won!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(320, 240))
        
        # Show text for 3 seconds or until key press
        start_time = pygame.time.get_ticks()
        waiting = True
        while waiting:
            self.screen.fill((0, 0, 0))
            self.screen.blit(text, text_rect)
            
            if self.display_surface:
                scaled = pygame.transform.scale(self.screen, self.display_surface.get_size())
                self.display_surface.blit(scaled, (0, 0))
                
            pygame.display.update()
            
            if pygame.time.get_ticks() - start_time > 3000:
                waiting = False
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False

        # Play video
        cap = cv2.VideoCapture("./img/win_video.mp4")
        if not cap.isOpened():
            print("Error opening video file")
        else:
            # Play end music on loop
            self.sound.music_channel.play(self.sound.end_music, loops=-1)
            
            clock = pygame.time.Clock()
            while cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    # Convert frame to pygame surface
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    # Scale to fit screen while maintaining aspect ratio
                    h, w = frame.shape[:2]
                    screen_w, screen_h = 640, 480
                    scale = min(screen_w/w, screen_h/h)
                    new_w, new_h = int(w * scale), int(h * scale)
                    frame = cv2.resize(frame, (new_w, new_h))
                    
                    surf = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
                    
                    # Center the video
                    x_pos = (screen_w - new_w) // 2
                    y_pos = (screen_h - new_h) // 2
                    
                    self.screen.fill((0, 0, 0))
                    self.screen.blit(surf, (x_pos, y_pos))
                    
                    if self.display_surface:
                        scaled = pygame.transform.scale(self.screen, self.display_surface.get_size())
                        self.display_surface.blit(scaled, (0, 0))
                        
                    pygame.display.update()
                    
                    # Handle events to allow exit
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            cap.release()
                            self.sound.music_channel.stop()
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN: # Allow skipping video
                             cap.release()
                             break
                    
                    clock.tick(30) # Limit FPS
                else:
                    break
            cap.release()
            self.sound.music_channel.stop()
        
        self.restart = True
