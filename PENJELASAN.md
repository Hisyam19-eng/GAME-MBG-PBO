# 📚 Penjelasan Detail Setiap File

## 🎯 Core Components

### 1. `core/background.py`
**Tujuan**: Rendering background gradient yang indah

**Fitur Utama**:
- Gradient vertikal dari ungu (Blue Violet) ke biru (Midnight Blue)
- Pre-rendering untuk performa optimal
- Encapsulation: Semua logic rendering tersembunyi dalam class

**Prinsip OOP**:
- ✅ **Encapsulation**: Attribute `_width`, `_height`, `_surface` adalah private
- ✅ **Property Getters**: Akses read-only melalui `@property`

**Method Penting**:
```python
_create_gradient()  # Private method untuk membuat gradient
draw(screen)        # Public method untuk render ke screen
```

---

### 2. `core/item.py`
**Tujuan**: Sistem item dengan inheritance hierarchy

**Class Hierarchy**:
```
BaseItem (Abstract)
    ├─ GoodItem (Makanan Segar)
    └─ BadItem (Makanan Busuk)
```

**Fitur Utama**:
- Falling physics dengan gravity
- Collision detection
- Different visual appearance per type
- Different effects saat tertangkap

**Prinsip OOP**:
- ✅ **Inheritance**: GoodItem & BadItem extends BaseItem
- ✅ **Polymorphism**: `draw()` dan `get_effect()` berbeda per subclass
- ✅ **Encapsulation**: Private attributes (`_x`, `_y`, `_speed`)
- ✅ **Abstraction**: BaseItem adalah abstract class
- ✅ **Exception Handling**: Try-catch di collision detection

**Method Penting**:
```python
# Abstract methods (harus di-override)
@abstractmethod
def draw(screen)        # Polymorphic - berbeda per subclass

@abstractmethod
def get_effect()        # Polymorphic - return berbeda per type

# Concrete methods (diwariskan)
update()                # Update posisi
check_collision()       # Cek tabrakan dengan player
catch()                 # Mark sebagai tertangkap
```

**GoodItem Details**:
- Warna: Hijau (34, 197, 94)
- Effect: +5 score, 0 HP
- Nama random dari makanan Nusantara
- Visual: Lingkaran hijau dengan highlight

**BadItem Details**:
- Warna: Merah (239, 68, 68)
- Effect: 0 score, -1 HP
- Visual: Lingkaran merah dengan tanda X

---

### 3. `core/player.py`
**Tujuan**: Karakter player yang bisa bergerak dan menangkap item

**Fitur Utama**:
- Smooth movement kiri-kanan
- Boundary checking (tidak keluar layar)
- Visual berbentuk basket/keranjang
- Collision rectangle untuk catching

**Prinsip OOP**:
- ✅ **Encapsulation**: Movement state dan position private
- ✅ **Composition**: Digunakan oleh Game class
- ✅ **Property Getters**: Read-only access ke posisi

**Method Penting**:
```python
move_left()     # Mulai bergerak kiri
move_right()    # Mulai bergerak kanan
stop()          # Berhenti
update()        # Update posisi dengan boundary check
draw(screen)    # Render visual player
get_rect()      # Return collision box
```

**Visual Design**:
- Warna amber/gold (251, 191, 36)
- Shadow effect untuk depth
- Basket pattern dengan garis vertikal
- Handle di atas basket

---

### 4. `core/game.py`
**Tujuan**: Main game controller dengan semua logic gameplay

**Fitur Utama**:
- Timer countdown 60 detik
- Score & HP management
- Item spawning dengan progressive difficulty
- Collision detection & processing
- Game over conditions
- Statistics tracking

**Prinsip OOP**:
- ✅ **Composition**: Contains Player, Items[], Background
- ✅ **Encapsulation**: Game state private
- ✅ **Exception Handling**: Safe item spawning & catching

**Game State**:
```python
_score          # Skor pemain
_hp             # Health points (mulai 3)
_time_remaining # Timer 60 detik
_items[]        # List item yang jatuh
_total_caught   # Statistik tangkapan
_good_caught    # Tangkapan baik
_bad_caught     # Tangkapan buruk
```

**Method Penting**:
```python
handle_input(keys)      # Process keyboard input
update()                # Update game state
_spawn_item()           # Spawn item baru (private)
_catch_item(item)       # Process tangkapan (private)
draw(screen)            # Render game
_draw_hud(screen)       # Render UI overlay (private)
get_results()           # Return statistik untuk high score
```

**Difficulty Progression**:
- Mulai spawn interval: 1000ms (1 detik)
- Berkurang 10ms setiap spawn
- Minimum: 500ms
- Item jatuh lebih cepat seiring waktu

**Game Over Conditions**:
1. HP <= 0 (terlalu banyak tangkap makanan busuk)
2. Time remaining <= 0 (waktu habis)

---

## 🎨 UI Components

### 5. `ui/button.py`
**Tujuan**: Modern button dengan smooth animations

**Fitur Utama**:
- Hover detection dengan scale animation
- State management (normal/hover/pressed)
- Color changes per state
- Shadow effect untuk depth
- Smooth transitions

**Prinsip OOP**:
- ✅ **Encapsulation**: Internal state private
- ✅ **Property Setter**: Text dapat diubah

**Button States**:
```python
Normal  → Indigo (99, 102, 241)
Hover   → Light Indigo (129, 140, 248) + scale 1.05
Pressed → Dark Indigo (67, 56, 202)
```

**Method Penting**:
```python
update(mouse_pos, mouse_pressed)  # Update state
draw(screen)                      # Render button
is_clicked(mouse_pos, clicked)    # Detect click
```

**Animation**:
- Target scale 1.05 saat hover
- Smooth interpolation dengan factor 0.2
- Instant response tapi smooth motion

---

## 🖼️ Screen System

### 6. `screens/base.py`
**Tujuan**: Abstract base class untuk semua screen

**Fitur Utama**:
- Standard interface untuk semua screen
- Exception handling wrappers
- Screen transition support

**Prinsip OOP**:
- ✅ **Abstraction**: Abstract methods harus di-implement
- ✅ **Inheritance**: Semua screen extends ini
- ✅ **Exception Handling**: Safe wrappers untuk semua method

**Abstract Methods**:
```python
@abstractmethod
def handle_event(event)  # Process events

@abstractmethod
def update()             # Update state

@abstractmethod
def draw(screen)         # Render screen
```

**Safe Wrappers**:
```python
safe_handle_event()  # Try-catch wrapper
safe_update()        # Try-catch wrapper
safe_draw()          # Try-catch wrapper
```

**Screen Transition**:
```python
set_next_screen(name)  # Set screen tujuan
get_next_screen()      # Get & clear next screen
```

---

### 7. `screens/main_menu.py`
**Tujuan**: Menu utama dengan animations

**Fitur Utama**:
- Floating title animation (sin wave)
- 3 buttons interaktif
- Decorative rotating food items
- Background gradient

**Prinsip OOP**:
- ✅ **Inheritance**: Extends BaseScreen
- ✅ **Composition**: Contains Background & Buttons

**Buttons**:
1. **MAIN** → Start game (transition ke GAME screen)
2. **HIGH SCORE** → View high scores (placeholder)
3. **KELUAR** → Quit game (post QUIT event)

**Animations**:
```python
Title: sin(time) * 10         # Vertical floating
Food items: Rotate in circle   # Decorative
```

**Visual Elements**:
- Title "NUSANTARA" dengan shadow
- Subtitle "Food Catcher"
- 6 rotating food icons (alternating green/red)
- Instructions di bawah

---

### 8. `screens/game_screen.py`
**Tujuan**: Active gameplay screen dengan effects

**Fitur Utama**:
- Real-time gameplay rendering
- Particle system saat catch
- Floating score text (+5, -1)
- Game over overlay dengan stats
- Restart & pause functionality

**Prinsip OOP**:
- ✅ **Inheritance**: Extends BaseScreen
- ✅ **Composition**: Contains Game, Particles[], FloatingTexts[]
- ✅ **Exception Handling**: Safe effect creation

**Sub-Classes**:

#### **Particle**
- Life: 30 frames
- Physics: velocity + gravity
- Visual: Fading circle
- Color: Matches item type

#### **FloatingText**
- Life: 60 frames
- Movement: Float upward
- Visual: Fading text
- Content: "+5" atau "-1"

**Effect Creation**:
```python
Good catch → Green particles + "+5" text
Bad catch  → Red particles + "-1" text
```

**Game Over Screen**:
- Semi-transparent black overlay
- "GAME OVER" title
- Statistics:
  - Final score
  - Catches (good/total)
  - Accuracy percentage
- Star rating (1-3)
- Instructions (R=restart, ESC=menu)

**Controls**:
- ESC: Pause/return to menu
- R: Restart (saat game over)
- Arrow keys / A,D: Movement

---

### 9. `screens/high_score.py`
**Tujuan**: Results screen dengan star rating

**Fitur Utama**:
- Animated star appearance
- Star rating 0-3 based on score
- Detailed statistics
- Performance message
- Back to menu button

**Prinsip OOP**:
- ✅ **Inheritance**: Extends BaseScreen
- ✅ **Composition**: Contains Background & Button

**Star Rating Logic**:
```python
Score >= 100 → ⭐⭐⭐ (3 stars)
Score >= 50  → ⭐⭐ (2 stars)
Score >= 20  → ⭐ (1 star)
Score < 20   → (0 stars)
```

**Animations**:
- Stars scale from 0 to 1.0
- Smooth scale interpolation
- Glow effect on active stars
- Sequential appearance

**Statistics Displayed**:
1. Score Akhir
2. Total Tangkapan
3. Makanan Segar (good items)
4. Makanan Busuk (bad items)
5. Akurasi (%)
6. Waktu Bermain (seconds)

**Rating Messages**:
- 0 stars: "Ayo coba lagi!"
- 1 star: "Lumayan!"
- 2 stars: "Bagus sekali!"
- 3 stars: "Sempurna!"

**Visual Effects**:
- Star shape dengan 5 points
- Glow effect menggunakan alpha blending
- Color: Gold (251, 191, 36)
- Inactive stars: Gray (100, 100, 100)

---

## 🚀 Main Entry Point

### 10. `main.py`
**Tujuan**: Entry point dengan screen manager

**Fitur Utama**:
- Pygame initialization
- Screen management system
- 60 FPS game loop
- Global exception handling
- Clean resource cleanup

**Prinsip OOP**:
- ✅ **Composition**: GameManager contains screens
- ✅ **Exception Handling**: Comprehensive error recovery

**GameManager Class**:

**Screen Management**:
```python
_screens = {
    'MAIN_MENU': MainMenu instance,
    'GAME': GameScreen instance,
    'HIGH_SCORE': HighScore instance (dynamic)
}
```

**Screen Transitions**:
- MAIN_MENU → GAME: Create fresh GameScreen
- GAME → HIGH_SCORE: Pass game results
- HIGH_SCORE → MAIN_MENU: Return to menu
- Any screen → MAIN_MENU: Fallback on error

**Main Loop**:
```python
while running:
    1. Handle events → Pass to current screen
    2. Update → Current screen update + check transition
    3. Draw → Render current screen
    4. Flip display
    5. Maintain 60 FPS
```

**Exception Handling**:
- Init errors → Exit gracefully
- Screen switch errors → Fallback to main menu
- Loop errors → Continue running
- Cleanup errors → Print and exit

**Cleanup**:
- pygame.quit()
- Close all resources
- sys.exit()

---

## 🔗 Interaction Flow

### Game Flow:
```
Start
  ↓
Main Menu
  ↓ (Click MAIN)
Game Screen
  ↓ (Game Over)
High Score Screen
  ↓ (Click MENU)
Main Menu
```

### Event Flow:
```
User Input
  ↓
pygame.event
  ↓
current_screen.handle_event()
  ↓
Screen-specific logic
  ↓
set_next_screen() if needed
```

### Update Flow:
```
GameManager.run()
  ↓
current_screen.update()
  ↓
Game logic / animations
  ↓
Check transitions
  ↓
Switch screen if needed
```

---

## 📊 Class Diagram

```
BaseScreen (Abstract)
    ├─ MainMenu
    ├─ GameScreen
    └─ HighScore

BaseItem (Abstract)
    ├─ GoodItem
    └─ BadItem

Game (Composition)
    ├─ Player
    ├─ Background
    └─ Items[]

GameScreen (Composition)
    ├─ Game
    ├─ Particles[]
    └─ FloatingTexts[]

GameManager (Composition)
    └─ Screens{}
```

---

## 🎓 Learning Points

### Dari game ini kamu belajar:

1. **OOP Fundamentals**:
   - Class inheritance & abstraction
   - Polymorphism dalam action
   - Encapsulation patterns
   - Composition over inheritance

2. **Game Development**:
   - Game loop architecture
   - State management
   - Collision detection
   - Particle systems
   - Screen transitions

3. **Python Skills**:
   - ABC (Abstract Base Class)
   - Properties & decorators
   - Exception handling
   - List comprehensions
   - Math operations

4. **Pygame Specifics**:
   - Event handling
   - Surface rendering
   - FPS management
   - Input processing
   - Visual effects

---

Selamat belajar! 🎓
