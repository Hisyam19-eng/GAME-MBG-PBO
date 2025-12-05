"""
Main game logic controller
Demonstrates: Composition, Encapsulation, Exception Handling
"""
import pygame
import random
from core.player import Player
from core.item import GoodItem, BadItem
from core.background import Background


class Game:
    """
    Main game controller
    Composition: Contains Player, Items, Background
    Encapsulation: Private game state management
    """
    
    def __init__(self, screen_width, screen_height):
        """
        Initialize game
        
        Args:
            screen_width: Width of game screen
            screen_height: Height of game screen
        """
        self._width = screen_width
        self._height = screen_height
        
        # Composition: Game contains these objects
        self._background = Background(screen_width, screen_height)
        self._player = Player(screen_width // 2, screen_height - 80, screen_width)
        self._items = []
        
        # Game state (encapsulated)
        self._score = 0
        self._hp = 3
        self._max_hp = 3
        self._time_remaining = 60.0  # 60 seconds
        self._spawn_timer = 0
        self._spawn_interval = 1000  # milliseconds
        self._last_time = pygame.time.get_ticks()
        
        # Statistics
        self._total_caught = 0
        self._good_caught = 0
        self._bad_caught = 0
        self._total_spawned = 0
        
        # Game state flags
        self._is_game_over = False
        self._game_over_reason = ""
    
    def handle_input(self, keys):
        """
        Handle keyboard input
        
        Args:
            keys: pygame key state
        """
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self._player.move_left()
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self._player.move_right()
        else:
            self._player.stop()
    
    def update(self):
        """Update game state"""
        if self._is_game_over:
            return
        
        # Update timer
        current_time = pygame.time.get_ticks()
        delta_time = (current_time - self._last_time) / 1000.0  # seconds
        self._last_time = current_time
        
        self._time_remaining -= delta_time
        if self._time_remaining <= 0:
            self._time_remaining = 0
            self._is_game_over = True
            self._game_over_reason = "Time's up!"
            return
        
        # Check HP
        if self._hp <= 0:
            self._hp = 0
            self._is_game_over = True
            self._game_over_reason = "HP habis!"
            return
        
        # Update player
        self._player.update()
        
        # Spawn items
        self._spawn_timer += delta_time * 1000
        if self._spawn_timer >= self._spawn_interval:
            self._spawn_item()
            self._spawn_timer = 0
            # Gradually increase difficulty
            if self._spawn_interval > 500:
                self._spawn_interval -= 10
        
        # Update items
        player_rect = self._player.get_rect()
        for item in self._items[:]:
            item.update()
            
            # Check collision
            if not item.is_caught and item.check_collision(player_rect):
                self._catch_item(item)
            
            # Remove off-screen items
            if item.is_off_screen or item.is_caught:
                self._items.remove(item)
    
    def _spawn_item(self):
        """Spawn a new item (encapsulated method)"""
        try:
            x = random.randint(50, self._width - 50)
            y = -30
            
            # 70% chance for good item, 30% for bad
            if random.random() < 0.7:
                item = GoodItem(x, y)
            else:
                item = BadItem(x, y)
            
            self._items.append(item)
            self._total_spawned += 1
        except Exception as e:
            print(f"Error spawning item: {e}")
    
    def _catch_item(self, item):
        """
        Process catching an item (encapsulated method)
        
        Args:
            item: The caught item
        """
        try:
            item.catch()
            effect = item.get_effect()
            
            self._score += effect['score']
            self._hp += effect['hp']
            
            # Cap HP at max
            if self._hp > self._max_hp:
                self._hp = self._max_hp
            
            # Update statistics
            self._total_caught += 1
            if effect['score'] > 0:
                self._good_caught += 1
            else:
                self._bad_caught += 1
        except Exception as e:
            print(f"Error catching item: {e}")
    
    def draw(self, screen):
        """Draw game elements"""
        self._background.draw(screen)
        
        # Draw items
        for item in self._items:
            item.draw(screen)
        
        # Draw player
        self._player.draw(screen)
        
        # Draw HUD
        self._draw_hud(screen)
    
    def _draw_hud(self, screen):
        """Draw heads-up display (encapsulated method)"""
        font = pygame.font.Font(None, 48)
        small_font = pygame.font.Font(None, 36)
        
        # Score
        score_text = font.render(f"Score: {self._score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))
        
        # HP
        hp_color = (34, 197, 94) if self._hp > 1 else (239, 68, 68)
        hp_text = font.render(f"HP: {self._hp}", True, hp_color)
        screen.blit(hp_text, (20, 70))
        
        # Timer
        time_color = (255, 255, 255) if self._time_remaining > 10 else (239, 68, 68)
        time_text = small_font.render(f"Time: {int(self._time_remaining)}s", True, time_color)
        screen.blit(time_text, (self._width - 150, 30))
    
    def get_results(self):
        """
        Get game results for high score screen
        
        Returns:
            dict: Game statistics
        """
        accuracy = (self._good_caught / self._total_caught * 100) if self._total_caught > 0 else 0
        
        return {
            'score': self._score,
            'total_caught': self._total_caught,
            'good_caught': self._good_caught,
            'bad_caught': self._bad_caught,
            'accuracy': accuracy,
            'time_played': 60.0 - self._time_remaining
        }
    
    # Properties for encapsulation
    @property
    def is_game_over(self):
        return self._is_game_over
    
    @property
    def score(self):
        return self._score
    
    @property
    def hp(self):
        return self._hp
    
    @property
    def time_remaining(self):
        return self._time_remaining
