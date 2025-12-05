# 🎮 Walkthrough: Nusantara Food Catcher

## 🚀 Quick Start

### Step 1: Instalasi
```bash
# Install dependencies
pip install -r requirements.txt
```

### Step 2: Jalankan Game
```bash
# Dari direktori root
cd "d:/BELAJAR_PYTHON/GAME CAK"
python src/main.py
```

---

## 📖 Tutorial Bermain

### Scene 1: Main Menu

Saat game dimulai, kamu akan melihat:
- **Title "NUSANTARA"** yang floating naik-turun
- **Subtitle "Food Catcher"**
- **3 Tombol**:
  - **MAIN** - Mulai permainan
  - **HIGH SCORE** - Lihat skor tertinggi (coming soon)
  - **KELUAR** - Keluar dari game
- **6 item makanan** yang berputar di sekitar title
- **Instructions** di bawah: "Use ← → or A D to move"

**Aksi**: Klik tombol **MAIN** untuk mulai bermain

---

### Scene 2: Gameplay

**Objective**: Tangkap sebanyak mungkin makanan segar dalam 60 detik!

#### HUD (Heads-Up Display):
- **Kiri atas**:
  - `Score: X` - Skor kamu saat ini
  - `HP: X` - Health points (mulai dari 3)
- **Kanan atas**:
  - `Time: Xs` - Waktu tersisa (countdown dari 60)

#### Controls:
- **← / A** - Gerak ke kiri
- **→ / D** - Gerak ke kanan
- **ESC** - Pause/kembali ke menu

#### Item yang Jatuh:

1. **Makanan Segar (Hijau)** 🟢
   - Lingkaran hijau dengan highlight putih
   - Nama random: Nasi Goreng, Rendang, Sate, dll
   - **Effect**: +5 score
   - **Visual**: Partikel hijau + teks "+5" muncul

2. **Makanan Busuk (Merah)** 🔴
   - Lingkaran merah dengan tanda X putih
   - **Effect**: -1 HP
   - **Visual**: Partikel merah + teks "-1" muncul

#### Gameplay Tips:
- 🎯 Fokus pada makanan hijau
- ⚠️ Hindari makanan merah
- 🏃 Jangan terlalu fokus satu sisi - item spawn random
- ⏱️ Perhatikan timer - jangan panik di detik terakhir
- ❤️ Jaga HP - kalau HP = 0, game over!

#### Difficulty Progression:
Semakin lama bermain, item jatuh semakin cepat dan semakin sering!

#### Game Over Conditions:
1. ⏰ **Waktu habis** - Timer mencapai 0
2. 💔 **HP habis** - Terlalu banyak tangkap makanan busuk

---

### Scene 3: Game Over Screen

Saat game berakhir, overlay hitam transparan muncul dengan:

#### Display:
- **"GAME OVER"** di tengah (warna gold)
- **Score: X** - Skor akhir kamu
- **Caught: X/Y** - Item hijau / total tangkapan
- **Accuracy: X%** - Persentase tangkapan baik
- **Star Rating** ⭐ - Bintang berdasarkan performa:
  - ⭐ (1 bintang) - Score 0-49
  - ⭐⭐ (2 bintang) - Score 50-99
  - ⭐⭐⭐ (3 bintang) - Score 100+

#### Controls:
- **R** - Restart game (main lagi)
- **ESC** - Kembali ke main menu

---

### Scene 4: High Score Screen (Optional)

Jika kamu mencapai skor tinggi, kamu akan melihat:

#### Display:
- **"HASIL PERMAINAN"** title
- **Animated Stars** - Muncul satu per satu dengan glow effect
- **Detailed Statistics**:
  - Score Akhir
  - Total Tangkapan
  - Makanan Segar (good catches)
  - Makanan Busuk (bad catches)
  - Akurasi (percentage)
  - Waktu Bermain (seconds)
- **Rating Message**:
  - 0 stars: "Ayo coba lagi!"
  - 1 star: "Lumayan!"
  - 2 stars: "Bagus sekali!"
  - 3 stars: "Sempurna!"
- **MENU button** - Kembali ke main menu

#### Controls:
- **Click MENU** - Kembali ke main menu
- **ESC** atau **ENTER** - Shortcut ke main menu

---

## 🎯 Strategi Mendapat High Score

### Bronze Strategy (Score 20-49) ⭐
- Fokus menangkap item hijau saja
- Hindari semua item merah
- Stay alive untuk 60 detik penuh

### Silver Strategy (Score 50-99) ⭐⭐
- Gerak agresif untuk catch lebih banyak
- Track multiple items sekaligus
- Quick reflexes untuk hindari merah

### Gold Strategy (Score 100+) ⭐⭐⭐
- Master movement - predict spawn locations
- Perfect timing on catches
- Zero bad catches (100% accuracy)
- Utilize full 60 seconds
- Quick side-to-side movement

### Pro Tips:
1. **Positioning**: Stay di tengah saat idle
2. **Prediction**: Watch item spawn patterns
3. **Priority**: Lebih baik miss item hijau daripada tangkap item merah
4. **Rhythm**: Develop rhythm dengan spawn intervals
5. **Endgame**: Di detik terakhir, fokus survival

---

## 🐛 Troubleshooting

### Game tidak berjalan?
```bash
# Cek Python version
python --version  # Harus 3.7+

# Install/update Pygame
pip install --upgrade pygame
```

### Game lag/slow?
- Tutup aplikasi lain yang berat
- Cek FPS masih 60 (di code: self._fps = 60)
- Update graphics drivers

### Error "module not found"?
```bash
# Pastikan di direktori yang benar
cd "d:/BELAJAR_PYTHON/GAME CAK"

# Install dependencies
pip install -r requirements.txt
```

### Kontrol tidak respond?
- Pastikan window game ter-focus (klik window)
- Test keyboard di aplikasi lain
- Restart game

---

## 🎓 Learning Exercises

### Beginner Challenges:
1. 🎯 Mainkan sampai dapat 1 bintang
2. 🏃 Survive full 60 detik
3. 📈 Beat skor sebelumnya

### Intermediate Challenges:
1. ⭐⭐ Dapat 2 bintang (score 50+)
2. 🎯 Accuracy 80%+
3. 💯 Score 100+ (3 bintang)

### Expert Challenges:
1. 🏆 Perfect game (100% accuracy)
2. 🚀 Score 150+
3. 🎮 Zero HP loss

---

## 🔧 Customization Guide

### Mengubah Difficulty

**File**: `src/core/game.py`

```python
# Lebih mudah
self._spawn_interval = 1500  # Spawn lebih jarang
self._time_remaining = 90.0  # Waktu lebih lama

# Lebih sulit
self._spawn_interval = 600   # Spawn lebih sering
self._time_remaining = 45.0  # Waktu lebih sedikit
```

### Mengubah Scoring

**File**: `src/core/item.py`

```python
class GoodItem:
    def get_effect(self):
        return {'score': 10, 'hp': 0}  # +10 instead of +5

class BadItem:
    def get_effect(self):
        return {'score': 0, 'hp': -2}  # -2 HP instead of -1
```

### Mengubah Player Speed

**File**: `src/core/player.py`

```python
def __init__(self, x, y, screen_width):
    self._speed = 8  # Default: 6
```

### Mengubah Star Rating Threshold

**File**: `src/screens/high_score.py`

```python
def _calculate_stars(self):
    score = self._results['score']
    if score >= 150:  # Was 100
        return 3
    elif score >= 75:  # Was 50
        return 2
    elif score >= 30:  # Was 20
        return 1
    return 0
```

---

## 📊 Example Play Session

```
[0:00] Game Start
       - HP: 3
       - Score: 0
       
[0:05] Caught 3 green items
       - HP: 3
       - Score: 15
       
[0:15] Caught 1 red item by mistake
       - HP: 2 (-1)
       - Score: 15
       
[0:30] Caught 8 more green items
       - HP: 2
       - Score: 55
       
[0:45] Still going strong
       - HP: 2
       - Score: 85
       
[0:58] Last second catches!
       - HP: 2
       - Score: 105
       
[1:00] Time's Up!
       - Final Score: 105
       - Rating: ⭐⭐⭐
       - Message: "Sempurna!"
```

---

## 🎉 Achievements Ideas

Buat challenge sendiri:
- 🥇 **First Victory**: Survive 60 seconds
- 🎯 **Sharpshooter**: 90% accuracy
- 💯 **Century Club**: Score 100+
- 🏆 **Triple Crown**: Get 3 stars
- 🚫 **Untouchable**: No HP loss
- 🎮 **Speed Demon**: 20+ catches
- 🌟 **Flawless**: 100% accuracy

---

Selamat bermain dan semoga berhasil! 🎮✨
