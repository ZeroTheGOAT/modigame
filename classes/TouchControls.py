import pygame
import sys

class TouchControls:
    """Handle mobile touch controls for web version"""
    
    def __init__(self, screen_width=640, screen_height=480):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.button_size = 60
        self.button_padding = 20
        
        # Detect if running on mobile (in browser, this will be set by platform check)
        self.is_mobile = self._detect_mobile()
        
        # Button positions
        # Left button (left side, bottom)
        self.left_button = pygame.Rect(
            self.button_padding,
            screen_height - self.button_size - self.button_padding,
            self.button_size,
            self.button_size
        )
        
        # Forward button (right side, bottom)
        self.forward_button = pygame.Rect(
            screen_width - self.button_size - self.button_padding,
            screen_height - self.button_size - self.button_padding,
            self.button_size,
            self.button_size
        )
        
        # Jump button (above forward button)
        self.jump_button = pygame.Rect(
            screen_width - self.button_size - self.button_padding,
            screen_height - (self.button_size * 2) - self.button_padding - 10,
            self.button_size,
            self.button_size
        )
        
        # Track which buttons are currently pressed
        self.left_pressed = False
        self.forward_pressed = False
        self.jump_pressed = False
        
        # Button colors
        self.button_color = (100, 100, 100, 180)
        self.button_pressed_color = (150, 150, 200, 220)
        self.button_border_color = (255, 255, 255, 200)
        
    def _detect_mobile(self):
        """Detect if running on mobile device"""
        # In web browser, we can check sys.platform
        # Pygbag sets platform to 'emscripten' when running in browser
        if sys.platform == 'emscripten':
            # In browser, assume mobile if touch is available
            # For now, we'll show controls in browser by default
            return True
        return False
    
    def handle_event(self, event):
        """
        Process touch events and return simulated keyboard events
        Returns list of pygame events to inject
        """
        simulated_events = []
        
        if event.type == pygame.FINGERDOWN:
            # Convert normalized coordinates to screen coordinates
            x = int(event.x * self.screen_width)
            y = int(event.y * self.screen_height)
            pos = (x, y)
            
            # Check which button was pressed
            if self.left_button.collidepoint(pos):
                self.left_pressed = True
                # Simulate LEFT key press
                simulated_events.append(
                    pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT})
                )
            elif self.forward_button.collidepoint(pos):
                self.forward_pressed = True
                # Simulate RIGHT key press
                simulated_events.append(
                    pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT})
                )
            elif self.jump_button.collidepoint(pos):
                self.jump_pressed = True
                # Simulate SPACE key press
                simulated_events.append(
                    pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_SPACE})
                )
                
        elif event.type == pygame.FINGERUP:
            # Release all buttons (simplified approach)
            if self.left_pressed:
                self.left_pressed = False
                simulated_events.append(
                    pygame.event.Event(pygame.KEYUP, {'key': pygame.K_LEFT})
                )
            if self.forward_pressed:
                self.forward_pressed = False
                simulated_events.append(
                    pygame.event.Event(pygame.KEYUP, {'key': pygame.K_RIGHT})
                )
            if self.jump_pressed:
                self.jump_pressed = False
                simulated_events.append(
                    pygame.event.Event(pygame.KEYUP, {'key': pygame.K_SPACE})
                )
        
        return simulated_events
    
    def draw(self, surface):
        """Draw touch control buttons on screen (only if mobile)"""
        if not self.is_mobile:
            return
        
        # Create semi-transparent surface for buttons
        button_surface = pygame.Surface((self.button_size, self.button_size), pygame.SRCALPHA)
        
        # Draw left button (arrow pointing left)
        color = self.button_pressed_color if self.left_pressed else self.button_color
        button_surface.fill((0, 0, 0, 0))
        pygame.draw.circle(button_surface, color, (self.button_size//2, self.button_size//2), self.button_size//2)
        pygame.draw.circle(button_surface, self.button_border_color, (self.button_size//2, self.button_size//2), self.button_size//2, 2)
        
        # Draw arrow (left)
        arrow_color = (255, 255, 255, 255)
        center = self.button_size // 2
        pygame.draw.polygon(button_surface, arrow_color, [
            (center - 10, center),
            (center + 5, center - 10),
            (center + 5, center + 10)
        ])
        surface.blit(button_surface, self.left_button.topleft)
        
        # Draw forward button (arrow pointing right)
        color = self.button_pressed_color if self.forward_pressed else self.button_color
        button_surface.fill((0, 0, 0, 0))
        pygame.draw.circle(button_surface, color, (self.button_size//2, self.button_size//2), self.button_size//2)
        pygame.draw.circle(button_surface, self.button_border_color, (self.button_size//2, self.button_size//2), self.button_size//2, 2)
        
        # Draw arrow (right)
        pygame.draw.polygon(button_surface, arrow_color, [
            (center + 10, center),
            (center - 5, center - 10),
            (center - 5, center + 10)
        ])
        surface.blit(button_surface, self.forward_button.topleft)
        
        # Draw jump button (up arrow)
        color = self.button_pressed_color if self.jump_pressed else self.button_color
        button_surface.fill((0, 0, 0, 0))
        pygame.draw.circle(button_surface, color, (self.button_size//2, self.button_size//2), self.button_size//2)
        pygame.draw.circle(button_surface, self.button_border_color, (self.button_size//2, self.button_size//2), self.button_size//2, 2)
        
        # Draw arrow (up)
        pygame.draw.polygon(button_surface, arrow_color, [
            (center, center - 10),
            (center - 10, center + 5),
            (center + 10, center + 5)
        ])
        surface.blit(button_surface, self.jump_button.topleft)
