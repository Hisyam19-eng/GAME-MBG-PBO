"""
Item classes with inheritance and polymorphism
Demonstrates: Inheritance, Polymorphism, Encapsulation, Exception Handling
"""
import pygame
import random
from abc import ABC, abstractmethod


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
    
    # Class variable for item names (Indonesian foods)
    FOOD_NAMES = [
        "Nasi Goreng", "Rendang", "Sate", "Gado-Gado",
        "Bakso", "Soto", "Nasi Uduk", "Martabak"
    ]
    
    def __init__(self, x, y):
        super().__init__(x, y, radius=22)
        self._name = random.choice(self.FOOD_NAMES)
        self._color = (34, 197, 94)  # Green
        self._outline_color = (22, 163, 74)
    
    def draw(self, screen):
        """Draw good item as green circle (polymorphic implementation)"""
        # Outer glow
        pygame.draw.circle(screen, self._outline_color, 
                         (int(self._x), int(self._y)), self._radius + 2)
        # Main circle
        pygame.draw.circle(screen, self._color, 
                         (int(self._x), int(self._y)), self._radius)
        # Highlight
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
    
    def __init__(self, x, y):
        super().__init__(x, y, radius=20)
        self._color = (239, 68, 68)  # Red
        self._outline_color = (220, 38, 38)
    
    def draw(self, screen):
        """Draw bad item as red circle with X mark (polymorphic implementation)"""
        # Outer glow
        pygame.draw.circle(screen, self._outline_color, 
                         (int(self._x), int(self._y)), self._radius + 2)
        # Main circle
        pygame.draw.circle(screen, self._color, 
                         (int(self._x), int(self._y)), self._radius)
        # X mark
        pygame.draw.line(screen, (255, 255, 255),
                        (self._x - 8, self._y - 8),
                        (self._x + 8, self._y + 8), 3)
        pygame.draw.line(screen, (255, 255, 255),
                        (self._x + 8, self._y - 8),
                        (self._x - 8, self._y + 8), 3)
    
    def get_effect(self):
        """Bad item reduces 1 HP (polymorphic implementation)"""
        return {'score': 0, 'hp': -1, 'name': 'Busuk!'}
