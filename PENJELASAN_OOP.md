# 🎓 Penjelasan Konsep OOP di Game MBG RHYTHM

> Dokumentasi ini menjelaskan secara detail dan mudah dipahami konsep-konsep OOP yang diterapkan di game MBG RHYTHM. Cocok untuk mahasiswa Rekayasa Kecerdasan Artifisial yang sedang belajar OOP!

---

## 📂 Overview Struktur Game

Game MBG RHYTHM terdiri dari beberapa folder utama:

```
src/
├── main.py              # Program utama yang menjalankan game
├── core/                # File-file inti game
│   ├── item.py         # Sistem item makanan (good/bad)
│   ├── player.py       # Karakter pemain
│   ├── game.py         # Logic game utama
│   ├── background.py   # Background game
│   └── audio_manager.py# Sistem audio
├── screens/            # Sistem layar (menu, game, hasil)
│   ├── base.py        # Base class untuk semua screen
│   ├── main_menu.py   # Layar menu utama
│   ├── game_screen.py # Layar gameplay
│   └── high_score.py  # Layar hasil
├── ui/                # Komponen UI
│   └── button.py      # Tombol dengan animasi
└── utils/             # Fungsi bantuan
    └── load_image.py  # Helper untuk load gambar
```

---

## 🔥 5 Konsep OOP yang Digunakan

### 1️⃣ **Inheritance (Pewarisan)**
### 2️⃣ **Polymorphism (Polimorfisme)**
### 3️⃣ **Encapsulation (Enkapsulasi)**
### 4️⃣ **Composition (Komposisi)**
### 5️⃣ **Abstraction (Abstraksi)**

Mari kita bahas satu per satu di file mana saja konsep ini digunakan! 🚀

---

## 📝 Penjelasan Per File

### 1. **`core/item.py`** - Item Makanan yang Jatuh

**Fungsi File:** File ini mengatur semua item makanan yang jatuh di game (makanan segar dan busuk).

#### 🎯 Konsep OOP yang Digunakan:

#### **A. Inheritance (Pewarisan)** ⭐⭐⭐

Ada 3 class di file ini:
- `BaseItem` → Parent class (induk)
- `GoodItem` → Child class (anak) dari BaseItem
- `BadItem` → Child class (anak) dari BaseItem

**Penjelasan Gampangnya:**
Bayangin `BaseItem` itu kayak "cetakan dasar" untuk semua makanan. Nah, `GoodItem` dan `BadItem` itu "turunan" dari cetakan dasar ini. Mereka warisi semua sifat dari `BaseItem`, tapi bisa punya keunikan sendiri.

**Contoh Kode:**

```python
class BaseItem(ABC):
    """Parent class untuk semua item"""
    def __init__(self, x, y, radius=20):
        self._x = x
        self._y = y
        self._radius = radius
        self._speed = random.uniform(2.0, 4.0)
        self._is_caught = False

class GoodItem(BaseItem):
    """Makanan segar - WARISI dari BaseItem"""
    def __init__(self, x, y):
        super().__init__(x, y, radius=30)  # ← Panggil constructor parent!
        self._food_type = random.choice(self.FOOD_TYPES)
        self._name = self._food_type.capitalize()

class BadItem(BaseItem):
    """Makanan busuk - WARISI dari BaseItem"""
    def __init__(self, x, y):
        super().__init__(x, y, radius=30)  # ← Panggil constructor parent!
        self._food_type = random.choice(self.FOOD_TYPES)
```

**Bukti Inheritance:**
- `GoodItem` dan `BadItem` pakai `super().__init__()` untuk manggil constructor parent
- Mereka otomatis punya semua atribut dari `BaseItem` (`_x`, `_y`, `_speed`, dll)
- Mereka bisa pakai method dari `BaseItem` seperti `update()`, `check_collision()`, dll

---

#### **B. Polymorphism (Polimorfisme)** ⭐⭐⭐

**Penjelasan Gampangnya:**
Polymorphism itu artinya "satu nama method, banyak bentuk implementasi". Di game ini, `GoodItem` dan `BadItem` punya method yang **namanya sama**, tapi **kerjaannya beda**!

**Contoh Kode:**

```python
# Di BaseItem (parent)
@abstractmethod
def get_effect(self):
    """Method abstrak - harus di-implement oleh child"""
    pass

# Di GoodItem (child 1)
def get_effect(self):
    """Makanan segar kasih +5 score"""
    return {'score': 5, 'hp': 0, 'name': self._name}

# Di BadItem (child 2)
def get_effect(self):
    """Makanan busuk kurangi -1 HP"""
    return {'score': 0, 'hp': -1, 'name': 'Busuk!'}
```

**Kenapa Ini Polymorphism?**
- Semua item punya method `get_effect()` (nama sama)
- Tapi hasilnya beda:
  - `GoodItem.get_effect()` → tambah score
  - `BadItem.get_effect()` → kurangi HP
- Waktu game manggil `item.get_effect()`, Python otomatis tau harus panggil versi mana!

**Contoh Polymorphism Lainnya:**

```python
# Method draw() juga polymorphic!

# Di GoodItem
def draw(self, screen):
    """Gambar makanan segar (pakai sprite hijau)"""
    if self._image:
        screen.blit(self._image, ...)
    else:
        pygame.draw.circle(screen, (34, 197, 94), ...)  # Hijau

# Di BadItem
def draw(self, screen):
    """Gambar makanan busuk (pakai sprite merah + X)"""
    if self._image:
        screen.blit(self._image, ...)
    else:
        pygame.draw.circle(screen, (239, 68, 68), ...)  # Merah
        # Gambar tanda X
        pygame.draw.line(screen, (255, 255, 255), ...)
```

---

#### **C. Encapsulation (Enkapsulasi)** ⭐⭐⭐

**Penjelasan Gampangnya:**
Encapsulation itu "sembunyikan data penting di dalam class, kasih akses lewat method/property". Ini buat keamanan dan kontrol data.

**Bukti di Kode:**

```python
class BaseItem(ABC):
    def __init__(self, x, y, radius=20):
        # Atribut PRIVATE (pakai underscore _)
        self._x = x          # ← Private, gak bisa diakses langsung
        self._y = y          # ← Private
        self._is_caught = False  # ← Private
    
    # Akses data lewat PROPERTY (getter)
    @property
    def x(self):
        return self._x  # ← Hanya bisa dibaca, gak bisa diubah dari luar!
    
    @property
    def y(self):
        return self._y
    
    @property
    def is_caught(self):
        return self._is_caught
    
    # Ubah data lewat METHOD
    def catch(self):
        """Method untuk mengubah _is_caught"""
        self._is_caught = True
```

**Kenapa Ini Penting?**
- Data sensitif kayak `_x`, `_y` dilindungi
- Kode luar cuma bisa **baca** lewat property (`item.x`), tapi gak bisa langsung ubah (`item.x = 100` → error!)
- Kalau mau ubah data, harus lewat method yang sudah disediakan (`item.catch()`)

---

#### **D. Abstraction (Abstraksi)** ⭐⭐

**Penjelasan Gampangnya:**
Abstraction itu bikin "template class" yang gak bisa langsung dipake, tapi **wajib** di-inherit dan di-implement oleh child class.

**Bukti di Kode:**

```python
from abc import ABC, abstractmethod

class BaseItem(ABC):  # ← Inherit dari ABC (Abstract Base Class)
    
    @abstractmethod
    def draw(self, screen):
        """Method abstrak - WAJIB di-implement oleh child!"""
        pass
    
    @abstractmethod
    def get_effect(self):
        """Method abstrak - WAJIB di-implement oleh child!"""
        pass
```

**Kenapa Pakai Abstract?**
- `BaseItem` itu cuma "kontrak" / "template"
- Kamu **GAK BISA** bikin object langsung: `item = BaseItem(10, 20)` → ERROR!
- Child class (`GoodItem`, `BadItem`) **WAJIB** implement `draw()` dan `get_effect()`
- Ini memastikan semua item pasti punya method-method penting

---

### 2. **`screens/base.py`** - Template untuk Semua Layar

**Fungsi File:** File ini adalah "cetakan dasar" untuk semua layar di game (menu, gameplay, hasil).

#### 🎯 Konsep OOP yang Digunakan:

#### **A. Abstraction (Abstraksi)** ⭐⭐⭐

**Penjelasan:**
`BaseScreen` adalah abstract class yang jadi template untuk semua screen.

**Contoh Kode:**

```python
from abc import ABC, abstractmethod

class BaseScreen(ABC):
    """Abstract base class untuk semua screen"""
    
    @abstractmethod
    def handle_event(self, event):
        """Setiap screen WAJIB punya cara handle event!"""
        pass
    
    @abstractmethod
    def update(self):
        """Setiap screen WAJIB punya cara update state!"""
        pass
    
    @abstractmethod
    def draw(self, screen):
        """Setiap screen WAJIB punya cara draw!"""
        pass
```

**Kenapa Penting?**
- Semua screen (`MainMenu`, `GameScreen`, `HighScore`) pasti punya 3 method ini
- Bikin kode konsisten dan mudah di-maintain
- Main loop tinggal panggil `screen.update()` dan `screen.draw()` tanpa peduli screen apa yang aktif

---

#### **B. Encapsulation (Enkapsulasi)** ⭐⭐

**Contoh Kode:**

```python
class BaseScreen(ABC):
    def __init__(self, screen_width, screen_height):
        self._width = screen_width      # ← Private
        self._height = screen_height    # ← Private
        self._next_screen = None        # ← Private
    
    # Akses lewat property
    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height
    
    # Method untuk kontrol state
    def set_next_screen(self, screen_name):
        """Set screen mana yang mau dituju"""
        self._next_screen = screen_name
    
    def get_next_screen(self):
        """Ambil dan hapus next screen"""
        next_screen = self._next_screen
        self._next_screen = None  # Reset
        return next_screen
```

---

#### **C. Exception Handling** ⭐

**Penjelasan:**
`BaseScreen` punya method "wrapper" yang aman dari error.

**Contoh Kode:**

```python
def safe_handle_event(self, event):
    """Handle event dengan proteksi error"""
    try:
        self.handle_event(event)  # Panggil method child
    except Exception as e:
        print(f"Error handling event in {self.__class__.__name__}: {e}")

def safe_update(self):
    """Update dengan proteksi error"""
    try:
        self.update()
    except Exception as e:
        print(f"Error updating {self.__class__.__name__}: {e}")

def safe_draw(self, screen):
    """Draw dengan proteksi error"""
    try:
        self.draw(screen)
    except Exception as e:
        print(f"Error drawing {self.__class__.__name__}: {e}")
```

**Kenapa Penting?**
- Kalau ada bug di satu screen, game gak langsung crash
- Error langsung ke-print di console buat debugging
- Game tetap bisa jalan meskipun ada error kecil

---

### 3. **`core/player.py`** - Karakter Pemain

**Fungsi File:** File ini mengatur karakter pemain yang bisa bergerak kiri-kanan dan menangkap item.

#### 🎯 Konsep OOP yang Digunakan:

#### **A. Encapsulation (Enkapsulasi)** ⭐⭐⭐

**Contoh Kode:**

```python
class Player:
    def __init__(self, x, y, screen_width):
        # Semua atribut PRIVATE
        self._x = x
        self._y = y
        self._screen_width = screen_width
        self._width = 150
        self._height = 150
        self._speed = 6
        self._velocity_x = 0      # Kecepatan saat ini
        self._max_speed = 8
        self._current_state = 'idle'  # State: 'idle', 'left', 'right'
    
    # Method PUBLIC untuk kontrol
    def move_left(self):
        """Gerak ke kiri"""
        self._velocity_x = -self._speed
        self._current_state = 'left'
    
    def move_right(self):
        """Gerak ke kanan"""
        self._velocity_x = self._speed
        self._current_state = 'right'
    
    def stop(self):
        """Berhenti"""
        self._velocity_x = 0
        self._current_state = 'idle'
    
    # Property untuk akses read-only
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
```

**Kenapa Ini Encapsulation?**
- Atribut seperti `_velocity_x`, `_current_state` disembunyikan (private)
- Kode luar gak bisa langsung ubah: `player._velocity_x = 999` → TIDAK DISARANKAN!
- Kode luar harus pakai method: `player.move_left()`, `player.stop()`
- Ini bikin kontrol lebih aman dan terstruktur

---

#### **B. State Management** ⭐⭐

**Penjelasan:**
Player punya berbagai "state" (keadaan) yang dikelola dengan baik.

**Contoh Kode:**

```python
class Player:
    def __init__(self, x, y, screen_width):
        # State management
        self._current_state = 'idle'  # State sprite
        self._is_bad_state = False     # Apakah lagi kena bad item?
        self._bad_state_timer = 0.0    # Timer bad state
        self._bad_state_duration = 1.0  # Durasi bad state
        
        # Load sprites untuk setiap state
        self._load_sprites()
    
    def trigger_bad_state(self):
        """Aktifkan bad state (kena makanan busuk)"""
        self._is_bad_state = True
        self._bad_state_timer = self._bad_state_duration
    
    def update(self, delta_time=1/60):
        """Update player (termasuk timer bad state)"""
        self._x += self._velocity_x
        
        # Update bad state timer
        if self._is_bad_state:
            self._bad_state_timer -= delta_time
            if self._bad_state_timer <= 0:
                self._is_bad_state = False  # Kembali normal
    
    def draw(self, screen):
        """Draw sprite sesuai state"""
        sprite_prefix = 'bad' if self._is_bad_state else 'normal'
        sprite_key = f'{sprite_prefix}-{self._current_state}'
        current_sprite = self._sprites.get(sprite_key)
        screen.blit(current_sprite, ...)
```

---

### 4. **`core/game.py`** - Logic Game Utama

**Fungsi File:** File ini adalah "otak" game, ngatur semua logic: scoring, HP, timer, spawning item, collision detection.

#### 🎯 Konsep OOP yang Digunakan:

#### **A. Composition (Komposisi)** ⭐⭐⭐

**Penjelasan Gampangnya:**
Composition itu "class yang mengandung object dari class lain". `Game` itu kayak "wadah" yang isinya `Player`, `Items`, dan `Background`.

**Contoh Kode:**

```python
class Game:
    def __init__(self, screen_width, screen_height):
        self._width = screen_width
        self._height = screen_height
        
        # COMPOSITION: Game "punya" object-object ini
        self._background = Background(screen_width, screen_height)  # ← Object Background
        self._player = Player(screen_width // 2, screen_height - 80, screen_width)  # ← Object Player
        self._items = []  # ← List of Item objects
```

**Kenapa Ini Composition?**
- `Game` **HAS-A** (punya) `Background` → komposisi
- `Game` **HAS-A** (punya) `Player` → komposisi
- `Game` **HAS-A** (punya) list of `Items` → komposisi
- Kalau `Game` dihapus, semua object di dalamnya juga ikut terhapus

**Beda dengan Inheritance:**
- Inheritance → **IS-A** (adalah)
  - Contoh: `GoodItem` **IS-A** `BaseItem`
- Composition → **HAS-A** (punya)
  - Contoh: `Game` **HAS-A** `Player`

---

#### **B. Encapsulation (Enkapsulasi)** ⭐⭐⭐

**Contoh Kode:**

```python
class Game:
    def __init__(self, screen_width, screen_height):
        # State game PRIVATE
        self._score = 0
        self._hp = 3
        self._max_hp = 3
        self._time_remaining = 60.0
        self._is_game_over = False
        
        # Statistics PRIVATE
        self._total_caught = 0
        self._good_caught = 0
        self._bad_caught = 0
    
    # Method PRIVATE (encapsulated logic)
    def _spawn_item(self):
        """Spawn item baru (private method)"""
        x = random.randint(50, self._width - 50)
        y = -30
        
        if random.random() < 0.7:
            item = GoodItem(x, y)
        else:
            item = BadItem(x, y)
        
        self._items.append(item)
    
    def _catch_item(self, item):
        """Process tangkapan item (private method)"""
        item.catch()
        effect = item.get_effect()
        
        self._score += effect['score']
        self._hp += effect['hp']
        
        # Update statistics
        self._total_caught += 1
        if effect['score'] > 0:
            self._good_caught += 1
        else:
            self._bad_caught += 1
    
    # Property untuk akses read-only
    @property
    def score(self):
        return self._score
    
    @property
    def hp(self):
        return self._hp
    
    @property
    def is_game_over(self):
        return self._is_game_over
```

**Kenapa Pakai Private Method (`_spawn_item`, `_catch_item`)?**
- Method ini cuma dipakai internal di class `Game`
- Kode luar gak perlu (dan gak boleh) panggil method ini
- Bikin kode lebih rapi dan gampang di-maintain

---

#### **C. Dependency Injection** ⭐

**Penjelasan:**
Class `Game` butuh object lain, tapi gak bikin sendiri (inject dari luar).

**Contoh Kode:**

```python
class Game:
    def __init__(self, screen_width, screen_height):
        # Game BIKIN object sendiri (tidak direkomendasikan untuk testing)
        self._player = Player(screen_width // 2, screen_height - 80, screen_width)
        self._background = Background(screen_width, screen_height)
```

> **Note:** Di game ini masih create object sendiri. Kalau mau lebih bagus, bisa pakai dependency injection:

```python
class Game:
    def __init__(self, screen_width, screen_height, player=None, background=None):
        # Inject dari luar (lebih flexible untuk testing)
        self._player = player or Player(screen_width // 2, screen_height - 80, screen_width)
        self._background = background or Background(screen_width, screen_height)
```

---

### 5. **`ui/button.py`** - Tombol dengan Animasi

**Fungsi File:** File ini bikin komponen tombol yang interaktif dengan efek hover dan animasi.

#### 🎯 Konsep OOP yang Digunakan:

#### **A. Encapsulation (Enkapsulasi)** ⭐⭐⭐

**Contoh Kode:**

```python
class Button:
    def __init__(self, x, y, width, height, text, font_size=32, audio_manager=None, image_name=None):
        # Atribut PRIVATE
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._text = text
        self._font = pygame.font.Font(None, font_size)
        
        # State internal
        self._is_hovered = False
        self._is_pressed = False
        
        # Animation state
        self._scale = 1.0
        self._target_scale = 1.0
    
    # Method PUBLIC untuk interaksi
    def update(self, mouse_pos, mouse_pressed):
        """Update button state"""
        button_rect = self._get_rect()
        self._is_hovered = button_rect.collidepoint(mouse_pos)
        
        if self._is_hovered:
            self._target_scale = 1.05  # Zoom sedikit
        else:
            self._target_scale = 1.0
        
        # Smooth animation
        self._scale += (self._target_scale - self._scale) * 0.2
    
    def is_clicked(self, mouse_pos, mouse_clicked):
        """Check apakah button diklik"""
        button_rect = self._get_rect()
        clicked = button_rect.collidepoint(mouse_pos) and mouse_clicked
        
        if clicked and self._audio_manager:
            self._audio_manager.play_sound('click')
        
        return clicked
    
    # Private helper method
    def _get_rect(self):
        """Get button rectangle (private method)"""
        return pygame.Rect(
            self._x - self._width // 2,
            self._y - self._height // 2,
            self._width,
            self._height
        )
    
    # Property dengan getter dan setter
    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value):
        self._text = value
```

**Kenapa Ini Encapsulation?**
- Semua state internal (`_is_hovered`, `_scale`, dll) disembunyikan
- Kode luar cuma butuh tau 2 method: `update()` dan `is_clicked()`
- Internal logic animasi disembunyikan di dalam class

---

### 6. **`main.py`** - Program Utama

**Fungsi File:** File ini adalah "entry point" game, yang jalanin main loop dan atur transisi antar screen.

#### 🎯 Konsep OOP yang Digunakan:

#### **A. Composition (Komposisi)** ⭐⭐

**Penjelasan:**
Main loop punya "screen manager" yang isinya berbagai screen objects.

**Contoh Kode:**

```python
def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Create screen dictionary (composition)
    screens = {
        'main_menu': MainMenu(SCREEN_WIDTH, SCREEN_HEIGHT),
        'game': GameScreen(SCREEN_WIDTH, SCREEN_HEIGHT),
        'high_score': HighScore(SCREEN_WIDTH, SCREEN_HEIGHT)
    }
    
    current_screen_name = 'main_menu'
    
    # Main loop
    while running:
        current_screen = screens[current_screen_name]
        
        # Handle events
        for event in pygame.event.get():
            current_screen.safe_handle_event(event)
        
        # Update
        current_screen.safe_update()
        
        # Draw
        current_screen.safe_draw(screen)
        
        # Check screen transition
        next_screen = current_screen.get_next_screen()
        if next_screen:
            current_screen_name = next_screen
```

---

## 🎯 Ringkasan: Konsep OOP di Setiap File

| File | Inheritance | Polymorphism | Encapsulation | Composition | Abstraction |
|------|-------------|--------------|---------------|-------------|-------------|
| **`core/item.py`** | ✅✅✅ | ✅✅✅ | ✅✅✅ | ❌ | ✅✅ |
| **`screens/base.py`** | ✅ | ❌ | ✅✅ | ❌ | ✅✅✅ |
| **`core/player.py`** | ❌ | ❌ | ✅✅✅ | ❌ | ❌ |
| **`core/game.py`** | ❌ | ❌ | ✅✅✅ | ✅✅✅ | ❌ |
| **`ui/button.py`** | ❌ | ❌ | ✅✅✅ | ❌ | ❌ |
| **`main.py`** | ❌ | ❌ | ❌ | ✅✅ | ❌ |

**Keterangan:**
- ✅✅✅ = Banyak dipakai
- ✅✅ = Cukup banyak
- ✅ = Sedikit
- ❌ = Tidak dipakai

---

## 💡 Tips Memahami OOP di Game Ini

### 1. **Mulai dari `core/item.py`**
File ini paling lengkap konsep OOP-nya! Ada:
- Inheritance (`BaseItem` → `GoodItem`/`BadItem`)
- Polymorphism (`get_effect()`, `draw()`)
- Encapsulation (private attributes + properties)
- Abstraction (abstract methods)

### 2. **Lihat Hierarchy Class**
```
BaseItem (Abstract)
├── GoodItem (Concrete)
└── BadItem (Concrete)

BaseScreen (Abstract)
├── MainMenu (Concrete)
├── GameScreen (Concrete)
└── HighScore (Concrete)
```

### 3. **Perhatikan Relasi Antar Class**
```
Game (Controller)
├── HAS-A Player (composition)
├── HAS-A Background (composition)
└── HAS-A List[Items] (composition)
    ├── GoodItem (IS-A BaseItem) ← inheritance
    └── BadItem (IS-A BaseItem) ← inheritance
```

---

## 🔥 Konsep OOP Paling Keren di Game Ini

### 🥇 **Polymorphism di `item.py`**

Ini yang paling bagus! Lihat kode ini di `game.py`:

```python
def _catch_item(self, item):
    """Tangkap item - gak peduli GoodItem atau BadItem!"""
    item.catch()
    effect = item.get_effect()  # ← Polymorphism!
    
    self._score += effect['score']
    self._hp += effect['hp']
```

**Kenapa Keren?**
- Method `_catch_item` gak perlu tau apakah `item` itu `GoodItem` atau `BadItem`
- Tinggal panggil `item.get_effect()`, Python otomatis tau mau jalanin method yang mana!
- Kalau mau tambah jenis item baru (misal `SuperGoodItem`), tinggal inherit dari `BaseItem`, gak perlu ubah kode di `game.py`!

---

## 📚 Kesimpulan

Game MBG RHYTHM ini adalah contoh yang **SANGAT BAGUS** untuk belajar OOP karena:

1. ✅ **Inheritance yang Jelas** - `BaseItem` jadi parent untuk `GoodItem` dan `BadItem`
2. ✅ **Polymorphism yang Powerful** - Method `get_effect()` dan `draw()` punya banyak implementasi
3. ✅ **Encapsulation yang Ketat** - Semua atribut private, akses lewat property/method
4. ✅ **Composition yang Rapi** - `Game` mengandung `Player`, `Items`, `Background`
5. ✅ **Abstraction yang Benar** - `BaseItem` dan `BaseScreen` adalah abstract class murni

---

**Selamat belajar OOP! 🎮🚀**

Kalau ada yang masih bingung, coba baca file `core/item.py` dulu karena di situ paling lengkap konsep OOP-nya!
