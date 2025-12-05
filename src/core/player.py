"""
Player class with movement and catching mechanics
Demonstrates: Encapsulation, Composition
"""
import pygame


class Player:
    """
    Player character that catches falling items
    Encapsulation: Private movement state and position
    Composition: Used by Game class
    """
    
    def __init__(self, x, y, screen_width):
        """
        Initialize player
        
        Args:
            x: Starting x position
            y: Starting y position
            screen_width: Width of screen for boundary checking
        """
        self._x = x
        self._y = y
        self._screen_width = screen_width
        self._width = 80
        self._height = 60
        self._speed = 6
        self._velocity_x = 0
        self._max_speed = 8
        
        # Visual properties
        self._color = (251, 191, 36)  # Amber/Gold
        self._outline_color = (217, 119, 6)
    
    def move_left(self):
        """Start moving left"""
        self._velocity_x = -self._speed
    
    def move_right(self):
        """Start moving right"""
        self._velocity_x = self._speed
    
    def stop(self):
        """Stop horizontal movement"""
        self._velocity_x = 0
    
    def update(self):
        """Update player position with boundary checking"""
        self._x += self._velocity_x
        
        # Boundary checking (encapsulated logic)
        if self._x < self._width // 2:
            self._x = self._width // 2
        elif self._x > self._screen_width - self._width // 2:
            self._x = self._screen_width - self._width // 2
    
    def draw(self, screen):
        """Draw player as a basket/container shape"""
        # Shadow
        shadow_rect = pygame.Rect(
            self._x - self._width // 2 + 3,
            self._y - self._height // 2 + 3,
            self._width,
            self._height
        )
        pygame.draw.rect(screen, (0, 0, 0, 50), shadow_rect, border_radius=8)
        
        # Main body (outline)
        outline_rect = pygame.Rect(
            self._x - self._width // 2 - 2,
            self._y - self._height // 2 - 2,
            self._width + 4,
            self._height + 4
        )
        pygame.draw.rect(screen, self._outline_color, outline_rect, border_radius=10)
        
        # Main body
        main_rect = pygame.Rect(
            self._x - self._width // 2,
            self._y - self._height // 2,
            self._width,
            self._height
        )
        pygame.draw.rect(screen, self._color, main_rect, border_radius=8)
        
        # Basket pattern (vertical lines)
        for i in range(5):
            line_x = self._x - self._width // 2 + (i + 1) * (self._width // 6)
            pygame.draw.line(
                screen,
                self._outline_color,
                (line_x, self._y - self._height // 2 + 5),
                (line_x, self._y + self._height // 2 - 5),
                2
            )
        
        # Handle
        handle_start = (self._x - 20, self._y - self._height // 2)
        handle_top = (self._x, self._y - self._height // 2 - 15)
        handle_end = (self._x + 20, self._y - self._height // 2)
        pygame.draw.lines(screen, self._outline_color, False,
                         [handle_start, handle_top, handle_end], 3)
    
    def get_rect(self):
        """
        Get collision rectangle
        
        Returns:
            pygame.Rect: Collision box for the player
        """
        return pygame.Rect(
            self._x - self._width // 2,
            self._y - self._height // 2,
            self._width,
            self._height
        )
    
    # Properties for encapsulation
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height
