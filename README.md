# 🎮 MBG RHYTHM

Game arcade Python + Pygame bertema Nusantara dengan mekanik menangkap makanan yang jatuh.

## 📋 Fitur

### Gameplay
- **Timer 60 detik** - Tangkap sebanyak mungkin makanan dalam waktu terbatas
- **Sistem HP** - Mulai dengan 3 HP, berkurang jika menangkap makanan busuk
- **Scoring System** - Makanan segar +5 poin, makanan busuk -1 HP
- **Difficulty Progression** - Semakin lama bermain, item jatuh semakin cepat

### Visual Effects
- ✨ **Particle Effects** - Efek partikel saat menangkap item
- 💫 **Floating Score Text** - Teks +5 atau -1 muncul saat menangkap
- 🌈 **Gradient Background** - Latar belakang ungu-biru yang indah
- ⭐ **Star Rating** - Penilaian 1-3 bintang berdasarkan skor
- 🎯 **Smooth Animations** - Animasi halus di semua elemen

### Audio & Music 🎵
- 🎵 **Background Music** - Musik latar di menu dan gameplay (optional files)
- 🔊 **Sound Effects** - Sound ketika:
  - Tombol diklik (beep)
  - Tangkap makanan segar (rising tone)
  - Tangkap makanan busuk (falling tone)
  - Game over (descending tones)
  - Victory screen (fanfare)
- 🎚️ **Procedural Sounds** - Generated real-time tanpa perlu file audio
- 📁 **Optional Music Files** - Support MP3/OGG untuk custom music

### UI Modern
- Tombol dengan hover effect dan scale animation
- Menu utama dengan floating title
- Layar hasil dengan statistik lengkap
- Transisi antar layar yang smooth

## 🏗️ Struktur Folder

```
src/
├─ main.py              # Entry point utama
├─ assets/              # Asset
│  └─ images/           # Aset gambar
├─ core/               # Komponen inti game
│  ├─ game.py          # Logic game utama
│  ├─ player.py        # Karakter player
│  ├─ item.py          # Sistem item (good/bad)
│  ├─ background.py    # Rendering background
│  └─ audio_manager.py # Audio & music system
├─ ui/                 # Komponen UI
│  └─ button.py        # Button dengan animasi
├─ utils/              # Fungsi bantuan
│  └─ load_image.py    # Load gambar
└─ screens/            # Sistem screen
   ├─ base.py          # Base class untuk screen
   ├─ main_menu.py     # Menu utama
   ├─ game_screen.py   # Layar gameplay
   └─ high_score.py    # Layar hasil/high score
```

## 🎯 Prinsip OOP yang Diimplementasikan

### 1. **Inheritance (Pewarisan)**
```python
# BaseItem → GoodItem/BadItem
class BaseItem(ABC):
    # Parent class untuk semua item
    
class GoodItem(BaseItem):
    # Makanan segar, extends BaseItem
    
class BadItem(BaseItem):
    # Makanan busuk, extends BaseItem

# BaseScreen → MainMenu/GameScreen/HighScore
class BaseScreen(ABC):
    # Parent class untuk semua screen
```

### 2. **Polymorphism (Polimorfisme)**
```python
# Setiap item implements method yang sama dengan behavior berbeda
def draw(self, screen):
    # GoodItem: gambar makanan bagus
    # BadItem: gambar makanan basi

def get_effect(self):
    # GoodItem: return {'score': 5, 'hp': 0}
    # BadItem: return {'score': 0, 'hp': -1}
```

### 3. **Encapsulation (Enkapsulasi)**
```python
class Player:
    def __init__(self):
        self._x = x  # Private attribute
        self._y = y
        self._velocity_x = 0
    
    @property
    def x(self):
        return self._x  # Getter untuk akses read-only
```

### 4. **Composition (Komposisi)**
```python
class Game:
    def __init__(self):
        # Game mengandung Player, Items, Background
        self._player = Player(...)
        self._items = []
        self._background = Background(...)
```

### 5. **Exception Handling**
```python
try:
    item_rect = pygame.Rect(...)
    return item_rect.colliderect(player_rect)
except Exception as e:
    print(f"Collision detection error: {e}")
    return False
```

## 🎮 Cara Bermain

### Kontrol
- **← / A** - Gerak ke kiri
- **→ / D** - Gerak ke kanan
- **ESC** - Pause / kembali ke menu
- **R** - Restart (saat game over)

### Aturan
1. Tangkap makanan segar untuk mendapat +5 poin
2. Hindari makanan busuk yang mengurangi -1 HP
3. Game berakhir jika HP = 0 atau waktu habis
4. Raih skor tertinggi dalam 60 detik!

### Star Rating
- ⭐ (1 bintang) - Skor 0-49
- ⭐⭐ (2 bintang) - Skor 50-99
- ⭐⭐⭐ (3 bintang) - Skor 100+

## 🚀 Instalasi & Menjalankan

### Persyaratan
- Python 3.7+
- Pygame

### Install Dependencies
```bash
pip install -r requirements.txt
# Atau manual:
pip install pygame numpy
```

### Jalankan Game
```bash
cd "GAME-MBG-PBO"
python src/main.py
```

## 📝 Penjelasan File

### Core Components

#### `main.py`
Entry point utama. Mengelola:
- Inisialisasi Pygame
- Screen manager (transisi antar layar)
- Game loop 60 FPS
- Exception handling global

#### `core/game.py`
Controller game logic utama:
- Timer 60 detik
- Sistem scoring & HP
- Spawning item dengan difficulty progression
- Collision detection
- Statistik permainan

#### `core/player.py`
Karakter player dengan:
- Movement kiri-kanan dengan boundary checking
- Visual berbentuk basket/keranjang
- Collision box untuk menangkap item

#### `core/item.py`
Sistem item dengan inheritance:
- **BaseItem**: Abstract class dengan falling behavior
- **GoodItem**: Makanan segar (hijau) +5 score
- **BadItem**: Makanan busuk (merah) -1 HP
- Polymorphic methods: `draw()`, `get_effect()`

#### `core/background.py`
Background dengan gradient ungu-biru modern

#### `core/audio_manager.py`
Sistem audio dengan:
- Procedural sound generation (numpy)
- Background music playback
- Sound effect management
- Singleton pattern untuk akses global

### UI Components

#### `ui/button.py`
Button modern dengan:
- Hover effect (scale animation)
- State management (normal/hover/pressed)
- Smooth transitions

### Screen System

#### `screens/base.py`
Abstract base class untuk semua screen dengan:
- Interface standard (handle_event, update, draw)
- Exception handling wrappers

#### `screens/main_menu.py`
Menu utama dengan:
- Floating title animation
- 3 button (Main, High Score, Keluar)
- Decorative rotating food items

#### `screens/game_screen.py`
Layar gameplay dengan:
- Real-time game rendering
- Particle effects saat catch
- Floating score text
- HUD (score, HP, timer)
- Game over overlay

#### `screens/high_score.py`
Layar hasil dengan:
- Animated star rating
- Statistik detail (score, catches, accuracy)
- Performance message

## 🎨 Makanan Nusantara

Item makanan segar menggunakan nama-nama makanan Indonesia:
- Nasi Goreng
- Rendang
- Sate
- Gado-Gado
- Bakso
- Soto
- Nasi Uduk
- Martabak

## 🔧 Kustomisasi

### Mengubah Difficulty
Edit di `core/game.py`:
```python
self._spawn_interval = 1000  # Ubah interval spawn (ms)
self._time_remaining = 60.0  # Ubah durasi game (detik)
```

### Mengubah Scoring
Edit di `core/item.py`:
```python
class GoodItem:
    def get_effect(self):
        return {'score': 5, 'hp': 0}  # Ubah nilai score
```

### Mengubah Warna
Edit di file masing-masing:
- Background: `core/background.py`
- Items: `core/item.py`
- Player: `core/player.py`

## 📊 Statistik Game

Setelah game selesai, ditampilkan:
- **Score Akhir** - Total poin yang didapat
- **Total Tangkapan** - Jumlah item yang berhasil ditangkap
- **Makanan Segar** - Item hijau yang ditangkap
- **Makanan Busuk** - Item merah yang ditangkap
- **Akurasi** - Persentase good catches
- **Waktu Bermain** - Durasi bermain

## 📜 License

Free to use for educational purposes.

## 🙏 Credits

**Image Assets Generated by:** [Gemini Nano Banana Pro](https://gemini.google.com)

Seluruh aset gambar dalam game ini di-generate menggunakan AI Gemini Nano Banana Pro.

---

**Selamat bermain! 🎮🍜**
