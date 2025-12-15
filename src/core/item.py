"""
Item classes with inheritance and polymorphism
Demonstrates: Inheritance, Polymorphism, Encapsulation, Exception Handling
"""
import pygame
import random
from abc import ABC, abstractmethod
from utils.load_image import get_assets_path, load_image_fit


class BaseItem(ABC):
    """
    Abstract base class for falling items
    Inheritance: Parent class for GoodItem and BadItem
    Encapsulation: Private attributes with property accessors
    """
    
    def __init__(self, x, y, radius=20):
        """
        Initialize base item
        
        Args:
            x: Initial x position
            y: Initial y position
            radius: Item size
        """
        self._x = x
        self._y = y
        self._radius = radius
        self._speed = random.uniform(2.0, 4.0)
        self._is_caught = False
    
    def update(self):
        """Update item position (polymorphic method)"""
        if not self._is_caught:
            self._y += self._speed
    
    @abstractmethod
    def draw(self, screen):
        """Draw the item (abstract method - must be implemented by children)"""
        pass
    
    @abstractmethod
    def get_effect(self):
        """
        Get the effect of catching this item
        Returns: dict with 'score' and 'hp' changes
        (Polymorphism: each child implements differently)
        """
        pass
    
    def check_collision(self, player_rect):
        """
        Check collision with player
        
        Args:
            player_rect: pygame.Rect of the player
            
        Returns:
            bool: True if collision detected
        """
        try:
            item_rect = pygame.Rect(
                self._x - self._radius,
                self._y - self._radius,
                self._radius * 2,
                self._radius * 2
            )
            return item_rect.colliderect(player_rect)
        except Exception as e:
            # Exception handling
            print(f"Collision detection error: {e}")
            return False
    
    def catch(self):
        """Mark item as caught"""
        self._is_caught = True
    
    # Properties for encapsulation
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @property
    def is_caught(self):
        return self._is_caught
    
    @property
    def is_off_screen(self):
        """Check if item has fallen off screen"""
        return self._y > 700  # Assuming screen height around 600-700


class GoodItem(BaseItem):
    """
    Good food item (fresh) - adds score
    Inheritance: Extends BaseItem
    Polymorphism: Implements abstract methods with specific behavior
    """
    
    # Class variable for available food types
    FOOD_TYPES = ['banana', 'carrot', 'chicken', 'fish', 'milk', 'rice', 'vegetable']
    
    def __init__(self, x, y):
        super().__init__(x, y, radius=30)
        self._food_type = random.choice(self.FOOD_TYPES)
        self._name = self._food_type.capitalize()
        self._color = (34, 197, 94)  # Green (fallback)
        self._outline_color = (22, 163, 74)
        
        # Load food image
        self._load_image()
    
    def _load_image(self):
        """Load food sprite image"""
        try:
            image_path = get_assets_path('images', 'foods', f'{self._food_type}.png')
            image, width, height = load_image_fit(
                image_path, 
                self._radius * 2, 
                self._radius * 2, 
                convert_alpha=True
            )
            self._image = image
            self._image_width = width
            self._image_height = height
        except Exception as e:
            print(f"Error loading good food image '{self._food_type}.png': {e}")
            self._image = None
    
    def draw(self, screen):
        """Draw good item using sprite image (polymorphic implementation)"""
        if self._image:
            # Draw sprite image
            image_rect = self._image.get_rect(center=(int(self._x), int(self._y)))
            screen.blit(self._image, image_rect)
        else:
            # Fallback to colored circle if image not loaded
            pygame.draw.circle(screen, self._outline_color, 
                             (int(self._x), int(self._y)), self._radius + 2)
            pygame.draw.circle(screen, self._color, 
                             (int(self._x), int(self._y)), self._radius)
            pygame.draw.circle(screen, (187, 247, 208), 
                             (int(self._x - 5), int(self._y - 5)), 6)
    
    def get_effect(self):
        """Good item adds 5 score (polymorphic implementation)"""
        return {'score': 5, 'hp': 0, 'name': self._name}
    
    @property
    def name(self):
        return self._name


class BadItem(BaseItem):
    """
    Bad food item (rotten) - reduces HP
    Inheritance: Extends BaseItem
    Polymorphism: Implements abstract methods differently than GoodItem
    """
    
    # Class variable for available bad food types
    FOOD_TYPES = ['banana', 'carrot', 'chicken', 'fish', 'milk', 'rice', 'vegetable']
    
    def __init__(self, x, y):
        super().__init__(x, y, radius=30)
        self._food_type = random.choice(self.FOOD_TYPES)
        self._color = (239, 68, 68)  # Red (fallback)
        self._outline_color = (220, 38, 38)
        
        # Load bad food image
        self._load_image()
    
    def _load_image(self):
        """Load bad food sprite image"""
        try:
            image_path = get_assets_path('images', 'foods', f'{self._food_type}-bad.png')
            image, width, height = load_image_fit(
                image_path, 
                self._radius * 2, 
                self._radius * 2, 
                convert_alpha=True
            )
            self._image = image
            self._image_width = width
            self._image_height = height
        except Exception as e:
            print(f"Error loading bad food image '{self._food_type}-bad.png': {e}")
            self._image = None
    
    def draw(self, screen):
        """Draw bad item using sprite image (polymorphic implementation)"""
        if self._image:
            # Draw sprite image
            image_rect = self._image.get_rect(center=(int(self._x), int(self._y)))
            screen.blit(self._image, image_rect)
        else:
            # Fallback to colored circle with X mark if image not loaded
            pygame.draw.circle(screen, self._outline_color, 
                             (int(self._x), int(self._y)), self._radius + 2)
            pygame.draw.circle(screen, self._color, 
                             (int(self._x), int(self._y)), self._radius)
            pygame.draw.line(screen, (255, 255, 255),
                            (self._x - 8, self._y - 8),
                            (self._x + 8, self._y + 8), 3)
            pygame.draw.line(screen, (255, 255, 255),
                            (self._x + 8, self._y - 8),
                            (self._x - 8, self._y + 8), 3)
    
    def get_effect(self):
        """Bad item reduces 1 HP (polymorphic implementation)"""
        return {'score': 0, 'hp': -1, 'name': 'Busuk!'}
