"""
Base screen class for all game screens
Demonstrates: Inheritance (abstract base class), Exception Handling
"""
from abc import ABC, abstractmethod
import pygame
from utils.load_image import load_background_image


class BaseScreen(ABC):
    """
    Abstract base class for all screens
    Inheritance: All screen classes extend this
    Exception Handling: Wrapper methods with try-catch
    """
    
    def __init__(self, screen_width, screen_height):
        """
        Initialize base screen
        
        Args:
            screen_width: Width of the screen
            screen_height: Height of the screen
        """
        self._width = screen_width
        self._height = screen_height
        self._next_screen = None
        self._transition_alpha = 0
    
    @abstractmethod
    def handle_event(self, event):
        """
        Handle pygame events (abstract method)
        
        Args:
            event: pygame event
        """
        pass
    
    @abstractmethod
    def update(self):
        """Update screen state (abstract method)"""
        pass
    
    @abstractmethod
    def draw(self, screen):
        """
        Draw screen content (abstract method)
        
        Args:
            screen: pygame surface to draw on
        """
        pass
    
    def safe_handle_event(self, event):
        """
        Safely handle event with exception handling
        
        Args:
            event: pygame event
        """
        try:
            self.handle_event(event)
        except Exception as e:
            print(f"Error handling event in {self.__class__.__name__}: {e}")
    
    def safe_update(self):
        """Safely update with exception handling"""
        try:
            self.update()
        except Exception as e:
            print(f"Error updating {self.__class__.__name__}: {e}")
    
    def safe_draw(self, screen):
        """
        Safely draw with exception handling
        
        Args:
            screen: pygame surface
        """
        try:
            self.draw(screen)
        except Exception as e:
            print(f"Error drawing {self.__class__.__name__}: {e}")
    
    def set_next_screen(self, screen_name):
        """
        Set the next screen to transition to
        
        Args:
            screen_name: Name of the next screen
        """
        self._next_screen = screen_name
    
    def get_next_screen(self):
        """
        Get and clear the next screen
        
        Returns:
            str or None: Next screen name
        """
        next_screen = self._next_screen
        self._next_screen = None
        return next_screen
    
    # Properties
    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height
    
    def _load_background(self, image_name, fallback_color=(50, 50, 100)):
        """
        Load and scale background image using utility function
        
        Args:
            image_name: Name of the image file in assets/images/backgrounds/
            fallback_color: RGB tuple for fallback color if image fails to load
        
        Returns:
            pygame.Surface: The loaded and scaled background surface
        """
        return load_background_image(image_name, self._width, self._height, fallback_color)
