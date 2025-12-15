"""
Player class with movement and catching mechanics
Demonstrates: Encapsulation, Composition
"""
import pygame
from utils.load_image import get_assets_path, load_image_fit


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
        self._width = 150
        self._height = 150
        self._speed = 6
        self._velocity_x = 0
        self._max_speed = 8
        
        # Load sprite images
        self._load_sprites()
        
        # Sprite state
        self._current_state = 'idle'  # 'idle', 'left', 'right'
        self._is_bad_state = False
        self._bad_state_timer = 0.0
        self._bad_state_duration = 1.0  # 1 second
    
    def _load_sprites(self):
        """Load all character sprites"""
        self._sprites = {}
        sprite_names = ['idle', 'left', 'right']
        
        for sprite_name in sprite_names:
            # Load normal sprite
            try:
                normal_path = get_assets_path('images', 'characters', f'normal-{sprite_name}.png')
                normal_sprite, _, _ = load_image_fit(normal_path, self._width, self._height, convert_alpha=True)
                self._sprites[f'normal-{sprite_name}'] = normal_sprite
            except Exception as e:
                print(f"Error loading normal-{sprite_name}.png: {e}")
                self._sprites[f'normal-{sprite_name}'] = self._create_fallback_sprite()
            
            # Load bad sprite
            try:
                bad_path = get_assets_path('images', 'characters', f'bad-{sprite_name}.png')
                bad_sprite, _, _ = load_image_fit(bad_path, self._width, self._height, convert_alpha=True)
                self._sprites[f'bad-{sprite_name}'] = bad_sprite
            except Exception as e:
                print(f"Error loading bad-{sprite_name}.png: {e}")
                self._sprites[f'bad-{sprite_name}'] = self._create_fallback_sprite((239, 68, 68))
    
    def _create_fallback_sprite(self, color=(251, 191, 36)):
        """Create a fallback sprite if image loading fails"""
        surface = pygame.Surface((self._width, self._height), pygame.SRCALPHA)
        pygame.draw.rect(surface, color, (0, 0, self._width, self._height), border_radius=8)
        return surface
    
    def move_left(self):
        """Start moving left"""
        self._velocity_x = -self._speed
        self._current_state = 'left'
    
    def move_right(self):
        """Start moving right"""
        self._velocity_x = self._speed
        self._current_state = 'right'
    
    def stop(self):
        """Stop horizontal movement"""
        self._velocity_x = 0
        self._current_state = 'idle'
    
    def trigger_bad_state(self):
        """Trigger bad state when hit by BadItem"""
        self._is_bad_state = True
        self._bad_state_timer = self._bad_state_duration
    
    def update(self, delta_time=1/60):
        """
        Update player position with boundary checking
        
        Args:
            delta_time: Time elapsed since last update (default 1/60 for 60 FPS)
        """
        self._x += self._velocity_x
        
        # Boundary checking (encapsulated logic)
        if self._x < self._width // 2:
            self._x = self._width // 2
        elif self._x > self._screen_width - self._width // 2:
            self._x = self._screen_width - self._width // 2
        
        # Update bad state timer
        if self._is_bad_state:
            self._bad_state_timer -= delta_time
            if self._bad_state_timer <= 0:
                self._is_bad_state = False
                self._bad_state_timer = 0
    
    def draw(self, screen):
        """Draw player sprite based on current state"""
        # Determine sprite key based on state
        sprite_prefix = 'bad' if self._is_bad_state else 'normal'
        sprite_key = f'{sprite_prefix}-{self._current_state}'
        
        # Get current sprite
        current_sprite = self._sprites.get(sprite_key)
        
        if current_sprite:
            # Draw sprite centered at player position
            sprite_rect = current_sprite.get_rect(center=(int(self._x), int(self._y)))
            screen.blit(current_sprite, sprite_rect)
        else:
            # Fallback drawing if sprite not found
            fallback_rect = pygame.Rect(
                self._x - self._width // 2,
                self._y - self._height // 2,
                self._width,
                self._height
            )
            color = (239, 68, 68) if self._is_bad_state else (251, 191, 36)
            pygame.draw.rect(screen, color, fallback_rect, border_radius=8)
    
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
