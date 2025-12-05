"""
Modern button UI component with hover effects
Demonstrates: Encapsulation
"""
import pygame


class Button:
    """
    Modern button with hover animations
    Encapsulation: Internal state management for hover/click
    """
    
    def __init__(self, x, y, width, height, text, font_size=32, audio_manager=None):
        """
        Initialize button
        
        Args:
            x: X position (center)
            y: Y position (center)
            width: Button width
            height: Button height
            text: Button text
            font_size: Font size for text
            audio_manager: Optional AudioManager for click sounds
        """
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._text = text
        self._font = pygame.font.Font(None, font_size)
        self._audio_manager = audio_manager
        
        # State
        self._is_hovered = False
        self._is_pressed = False
        
        # Colors
        self._normal_color = (99, 102, 241)  # Indigo
        self._hover_color = (129, 140, 248)  # Light Indigo
        self._pressed_color = (67, 56, 202)  # Dark Indigo
        self._text_color = (255, 255, 255)
        
        # Animation
        self._scale = 1.0
        self._target_scale = 1.0
    
    def update(self, mouse_pos, mouse_pressed):
        """
        Update button state
        
        Args:
            mouse_pos: Tuple of (x, y) mouse position
            mouse_pressed: Tuple of mouse button states
        """
        # Check if mouse is over button
        button_rect = self._get_rect()
        self._is_hovered = button_rect.collidepoint(mouse_pos)
        
        # Update scale for animation
        if self._is_hovered:
            self._target_scale = 1.05
            self._is_pressed = mouse_pressed[0]
        else:
            self._target_scale = 1.0
            self._is_pressed = False
        
        # Smooth scale transition
        self._scale += (self._target_scale - self._scale) * 0.2
    
    def draw(self, screen):
        """Draw the button with current state"""
        # Determine color based on state
        if self._is_pressed:
            color = self._pressed_color
        elif self._is_hovered:
            color = self._hover_color
        else:
            color = self._normal_color
        
        # Calculate scaled dimensions
        scaled_width = int(self._width * self._scale)
        scaled_height = int(self._height * self._scale)
        
        # Draw shadow
        shadow_rect = pygame.Rect(
            self._x - scaled_width // 2 + 4,
            self._y - scaled_height // 2 + 4,
            scaled_width,
            scaled_height
        )
        pygame.draw.rect(screen, (0, 0, 0, 80), shadow_rect, border_radius=12)
        
        # Draw button
        button_rect = pygame.Rect(
            self._x - scaled_width // 2,
            self._y - scaled_height // 2,
            scaled_width,
            scaled_height
        )
        pygame.draw.rect(screen, color, button_rect, border_radius=10)
        
        # Draw text
        text_surface = self._font.render(self._text, True, self._text_color)
        text_rect = text_surface.get_rect(center=(self._x, self._y))
        screen.blit(text_surface, text_rect)
    
    def is_clicked(self, mouse_pos, mouse_clicked):
        """
        Check if button was clicked
        
        Args:
            mouse_pos: Tuple of (x, y) mouse position
            mouse_clicked: True if mouse button was just released
            
        Returns:
            bool: True if button was clicked
        """
        button_rect = self._get_rect()
        clicked = button_rect.collidepoint(mouse_pos) and mouse_clicked
        
        # Play click sound if clicked
        if clicked and self._audio_manager:
            self._audio_manager.play_sound('click')
        
        return clicked
    
    def _get_rect(self):
        """Get button rectangle (encapsulated helper method)"""
        return pygame.Rect(
            self._x - self._width // 2,
            self._y - self._height // 2,
            self._width,
            self._height
        )
    
    # Properties
    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value):
        self._text = value
