import pygame


class Background:
    """Renders a beautiful purple-to-blue gradient background"""
    
    def __init__(self, width, height):
        """
        Initialize background
        
        Args:
            width: Screen width
            height: Screen height
        """
        self._width = width
        self._height = height
        self._surface = pygame.Surface((width, height))
        self._create_gradient()
    
    def _create_gradient(self):
        """Create vertical gradient from purple to blue (encapsulated method)"""
        # Top color (purple)
        color_top = (138, 43, 226)  # Blue Violet
        # Bottom color (blue)
        color_bottom = (25, 25, 112)  # Midnight Blue
        
        for y in range(self._height):
            # Interpolate between colors
            ratio = y / self._height
            r = int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio)
            g = int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio)
            b = int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
            
            pygame.draw.line(self._surface, (r, g, b), (0, y), (self._width, y))
    
    def draw(self, screen):
        """Draw the background to screen"""
        screen.blit(self._surface, (0, 0))
    
    # Getters (encapsulation)
    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height
