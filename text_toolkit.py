#!/usr/bin/env python3
"""
Digital Art Generator
A unique utility for creating ASCII art, digital patterns, and text-based visualizations
"""

import random
import math
import re
import string
import time
from typing import Counter, List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class Color:
    r: int
    g: int
    b: int

class DigitalArtGenerator:
    def __init__(self):
        self.ascii_chars = " .:-=+*#%@"
        self.dense_chars = "█▓▒░ "
        self.art_chars = "▀▁▂▃▄▅▆▇█"
        self.pattern_chars = "╔╗╚╝═║╠╣╦╩╬"
        
        # Color palettes for different moods
        self.palettes = {
            'neon': ['#FF0080', '#00FF80', '#8000FF', '#FF8000', '#0080FF'],
            'sunset': ['#FF6B6B', '#FFE66D', '#FF8E53', '#FF6B9D', '#C44569'],
            'ocean': ['#006994', '#00A8CC', '#7DD3FC', '#0EA5E9', '#0284C7'],
            'forest': ['#2D5016', '#4A7C59', '#6B8E23', '#8FBC8F', '#9ACD32'],
            'fire': ['#FF4500', '#FF6347', '#FF7F50', '#FFA500', '#FFD700']
        }
    
    def generate_mandelbrot(self, width: int = 60, height: int = 30, max_iter: int = 50) -> str:
        """Generate a Mandelbrot fractal in ASCII"""
        result = []
        for y in range(height):
            row = ""
            for x in range(width):
                # Map pixel coordinates to complex plane
                zx = (x - width/2) * 4.0 / width
                zy = (y - height/2) * 4.0 / height
                
                c = complex(zx, zy)
                z = 0
                iter_count = 0
                
                while abs(z) < 2 and iter_count < max_iter:
                    z = z*z + c
                    iter_count += 1
                
                # Map iteration count to ASCII character
                char_index = int((iter_count / max_iter) * (len(self.ascii_chars) - 1))
                row += self.ascii_chars[char_index]
            result.append(row)
        return '\n'.join(result)
    
    def generate_spiral(self, size: int = 20, char: str = '*') -> str:
        """Generate a spiral pattern"""
        matrix = [[' ' for _ in range(size)] for _ in range(size)]
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
        x, y = 0, 0
        direction = 0
        steps = 1
        step_count = 0
        
        for i in range(size * size):
            if 0 <= x < size and 0 <= y < size:
                matrix[x][y] = char
            
            x += directions[direction][0]
            y += directions[direction][1]
            step_count += 1
            
            if step_count == steps:
                step_count = 0
                direction = (direction + 1) % 4
                if direction % 2 == 0:  # Every two turns, increase steps
                    steps += 1
        
        return '\n'.join(''.join(row) for row in matrix)
    
    def generate_wave_pattern(self, width: int = 50, height: int = 20, frequency: float = 0.3) -> str:
        """Generate animated wave patterns"""
        result = []
        for y in range(height):
            row = ""
            for x in range(width):
                # Create wave using sine function
                wave = math.sin(x * frequency + time.time() * 2) * 5
                if abs(y - height//2 - wave) < 1:
                    row += "█"
                elif abs(y - height//2 - wave) < 2:
                    row += "▓"
                elif abs(y - height//2 - wave) < 3:
                    row += "▒"
                else:
                    row += " "
            result.append(row)
        return '\n'.join(result)
    
    def generate_random_landscape(self, width: int = 60, height: int = 20) -> str:
        """Generate a random ASCII landscape"""
        landscape_chars = " .,:;+*#%@"
        result = []
        
        # Generate height map using multiple sine waves
        height_map = []
        for x in range(width):
            height_val = (
                math.sin(x * 0.1) * 3 +
                math.sin(x * 0.05) * 5 +
                math.sin(x * 0.02) * 2 +
                random.uniform(-1, 1)
            )
            height_map.append(int(height_val + height//2))
        
        for y in range(height):
            row = ""
            for x in range(width):
                if y > height_map[x]:
                    row += " "  # Sky
                elif y == height_map[x]:
                    row += random.choice(["^", "▲", "⛰", "🏔"])  # Peaks
                elif y > height_map[x] - 2:
                    row += random.choice(["#", "█", "▓"])  # Mountain
                elif y > height_map[x] - 4:
                    row += random.choice([".", ":", ";"])  # Hills
                else:
                    row += random.choice(["~", "≈", "≈"])  # Water
            result.append(row)
        return '\n'.join(result)
    
    def generate_geometric_pattern(self, pattern_type: str = "diamond", size: int = 15) -> str:
        """Generate various geometric patterns"""
        matrix = [[' ' for _ in range(size)] for _ in range(size)]
        
        if pattern_type == "diamond":
            center = size // 2
            for i in range(size):
                for j in range(size):
                    if abs(i - center) + abs(j - center) <= center:
                        matrix[i][j] = "█"
        
        elif pattern_type == "circle":
            center = size // 2
            radius = center - 1
            for i in range(size):
                for j in range(size):
                    distance = math.sqrt((i - center)**2 + (j - center)**2)
                    if abs(distance - radius) < 1:
                        matrix[i][j] = "█"
        
        elif pattern_type == "checkerboard":
            for i in range(size):
                for j in range(size):
                    if (i + j) % 2 == 0:
                        matrix[i][j] = "█"
        
        elif pattern_type == "spiral_square":
            # Create a square spiral
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            x, y = 0, 0
            direction = 0
            steps = 1
            step_count = 0
            
            for i in range(size * size):
                if 0 <= x < size and 0 <= y < size:
                    matrix[x][y] = "█"
                
                x += directions[direction][0]
                y += directions[direction][1]
                step_count += 1
                
                if step_count == steps:
                    step_count = 0
                    direction = (direction + 1) % 4
                    if direction % 2 == 0:
                        steps += 1
        
        return '\n'.join(''.join(row) for row in matrix)
    
    def generate_text_art(self, text: str, font: str = "block") -> str:
        """Generate ASCII art from text"""
        fonts = {
            "block": {
                'A': [" ▄▀▀▄ ", "█   █", "█▀▀▀█", "█   █", "█   █"],
                'B': ["█▀▀▀▄ ", "█   █", "█▀▀▀▄ ", "█   █", "█▀▀▀▀ "],
                'C': [" ▄▀▀▀▄", "█     ", "█     ", "█     ", " ▀▀▀▀ "],
                'H': ["█   █", "█   █", "█▀▀▀█", "█   █", "█   █"],
                'E': ["█▀▀▀▀▀", "█     ", "█▀▀▀  ", "█     ", "█▀▀▀▀▀"],
                'L': ["█     ", "█     ", "█     ", "█     ", "█▀▀▀▀▀"],
                'O': [" ▄▀▀▄ ", "█   █", "█   █", "█   █", " ▀▀▀▀ "],
                ' ': ["     ", "     ", "     ", "     ", "     "]
            }
        }
        
        if font not in fonts:
            return text
        
        font_data = fonts[font]
        lines = [""] * 5
        
        for char in text.upper():
            if char in font_data:
                for i, line in enumerate(font_data[char]):
                    lines[i] += line + " "
            else:
                for i in range(5):
                    lines[i] += "      "
        
        return '\n'.join(lines)
    
    def generate_pixel_art(self, width: int = 20, height: int = 20, style: str = "random") -> str:
        """Generate pixel art patterns"""
        styles = {
            "random": lambda x, y: random.choice(["█", "▓", "▒", "░", " "]),
            "gradient": lambda x, y: self.dense_chars[int((x + y) / (width + height) * (len(self.dense_chars) - 1))],
            "checker": lambda x, y: "█" if (x + y) % 2 == 0 else " ",
            "circles": lambda x, y: "█" if math.sqrt((x - width//2)**2 + (y - height//2)**2) < min(width, height)//3 else " ",
            "waves": lambda x, y: "█" if math.sin(x * 0.5) * 3 + height//2 > y else " "
        }
        
        pattern_func = styles.get(style, styles["random"])
        result = []
        
        for y in range(height):
            row = ""
            for x in range(width):
                row += pattern_func(x, y)
            result.append(row)
        
        return '\n'.join(result)
    
    def generate_animation_frame(self, frame_num: int, total_frames: int = 20) -> str:
        """Generate a single frame of an animation"""
        width, height = 40, 15
        result = []
        
        for y in range(height):
            row = ""
            for x in range(width):
                # Create a rotating pattern
                angle = (frame_num * 2 * math.pi / total_frames) + (x + y) * 0.1
                wave = math.sin(angle) * 3
                
                if abs(y - height//2 - wave) < 1:
                    row += "█"
                elif abs(y - height//2 - wave) < 2:
                    row += "▓"
                elif abs(y - height//2 - wave) < 3:
                    row += "▒"
                else:
                    row += " "
            result.append(row)
        
        return '\n'.join(result)
    
    def create_digital_painting(self, width: int = 30, height: int = 20, style: str = "impressionist") -> str:
        """Create a digital painting using text characters"""
        styles = {
            "impressionist": self._impressionist_painting,
            "abstract": self._abstract_painting,
            "minimalist": self._minimalist_painting,
            "geometric": self._geometric_painting
        }
        
        painter = styles.get(style, self._impressionist_painting)
        return painter(width, height)
    
    def _impressionist_painting(self, width: int, height: int) -> str:
        """Create an impressionist-style digital painting"""
        chars = " .:;+=xX$&"
        result = []
        
        for y in range(height):
            row = ""
            for x in range(width):
                # Create brush strokes with noise
                noise = random.uniform(0, 1)
                brush_stroke = math.sin(x * 0.3) * math.cos(y * 0.2) + noise * 0.5
                char_index = int((brush_stroke + 1) * (len(chars) - 1) / 2)
                char_index = max(0, min(len(chars) - 1, char_index))
                row += chars[char_index]
            result.append(row)
        
        return '\n'.join(result)
    
    def _abstract_painting(self, width: int, height: int) -> str:
        """Create an abstract digital painting"""
        chars = " ░▒▓█"
        result = []
        
        for y in range(height):
            row = ""
            for x in range(width):
                # Random abstract patterns
                pattern = random.choice([
                    lambda: "█" if (x + y) % 3 == 0 else " ",
                    lambda: "▓" if math.sin(x * 0.5) > 0.5 else "░",
                    lambda: "▒" if random.random() > 0.7 else " "
                ])
                row += pattern()
            result.append(row)
        
        return '\n'.join(result)
    
    def _minimalist_painting(self, width: int, height: int) -> str:
        """Create a minimalist digital painting"""
        result = []
        
        for y in range(height):
            row = ""
            for x in range(width):
                # Simple geometric shapes
                if x == width//2 or y == height//2:
                    row += "█"
                elif abs(x - width//2) + abs(y - height//2) < 3:
                    row += "▓"
                else:
                    row += " "
            result.append(row)
        
        return '\n'.join(result)
    
    def _geometric_painting(self, width: int, height: int) -> str:
        """Create a geometric digital painting"""
        chars = " ░▒▓█"
        result = []
        
        for y in range(height):
            row = ""
            for x in range(width):
                # Geometric patterns
                if (x + y) % 4 == 0:
                    row += "█"
                elif (x - y) % 4 == 0:
                    row += "▓"
                elif (x + y) % 2 == 0:
                    row += "▒"
                else:
                    row += "░"
            result.append(row)
        
        return '\n'.join(result)
    
    def leet_speak_converter(self, text: str, intensity: float = 0.7) -> str:
        """Convert text to leet speak with customizable intensity"""
        result = text.lower()
        for char, replacement in self.leet_speak.items():
            if random.random() < intensity:
                result = result.replace(char, replacement)
        return result
    
    def text_shuffler(self, text: str, preserve_spaces: bool = True) -> str:
        """Shuffle characters while optionally preserving word boundaries"""
        if preserve_spaces:
            words = text.split()
            shuffled_words = []
            for word in words:
                chars = list(word)
                random.shuffle(chars)
                shuffled_words.append(''.join(chars))
            return ' '.join(shuffled_words)
        else:
            chars = list(text)
            random.shuffle(chars)
            return ''.join(chars)
    
    def reverse_words(self, text: str) -> str:
        """Reverse the order of words in text"""
        words = text.split()
        return ' '.join(reversed(words))
    
    def alternating_case(self, text: str, pattern: str = "random") -> str:
        """Convert text to alternating case patterns"""
        result = ""
        if pattern == "random":
            for char in text:
                result += char.upper() if random.choice([True, False]) else char.lower()
        elif pattern == "alternating":
            for i, char in enumerate(text):
                result += char.upper() if i % 2 == 0 else char.lower()
        elif pattern == "spongebob":
            for i, char in enumerate(text):
                if char.isalpha():
                    result += char.upper() if i % 2 == 0 else char.lower()
                else:
                    result += char
        return result
    
    def text_analyzer(self, text: str) -> Dict:
        """Analyze text characteristics"""
        words = re.findall(r'\b\w+\b', text.lower())
        chars = re.findall(r'[a-zA-Z]', text)
        
        analysis = {
            'word_count': len(words),
            'char_count': len(text),
            'letter_count': len(chars),
            'avg_word_length': sum(len(word) for word in words) / len(words) if words else 0,
            'most_common_words': Counter(words).most_common(5),
            'most_common_letters': Counter(chars).most_common(5),
            'unique_words': len(set(words)),
            'readability_score': self._calculate_readability(text)
        }
        return analysis
    
    def _calculate_readability(self, text: str) -> float:
        """Simple readability score based on average word length"""
        words = re.findall(r'\b\w+\b', text)
        if not words:
            return 0
        avg_word_length = sum(len(word) for word in words) / len(words)
        return max(0, 100 - (avg_word_length * 10))
    
    def text_generator(self, pattern: str, length: int = 50) -> str:
        """Generate text based on patterns"""
        generators = {
            'lorem': self._generate_lorem,
            'random_words': self._generate_random_words,
            'pattern_repeat': self._generate_pattern_repeat,
            'word_salad': self._generate_word_salad
        }
        
        generator = generators.get(pattern, self._generate_random_words)
        return generator(length)
    
    def _generate_lorem(self, length: int) -> str:
        """Generate lorem ipsum style text"""
        lorem_words = [
            'lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur',
            'adipiscing', 'elit', 'sed', 'do', 'eiusmod', 'tempor',
            'incididunt', 'ut', 'labore', 'et', 'dolore', 'magna',
            'aliqua', 'enim', 'ad', 'minim', 'veniam', 'quis'
        ]
        return ' '.join(random.choices(lorem_words, k=length))
    
    def _generate_random_words(self, length: int) -> str:
        """Generate random words"""
        words = []
        for _ in range(length):
            word_length = random.randint(3, 8)
            word = ''.join(random.choices(string.ascii_lowercase, k=word_length))
            words.append(word)
        return ' '.join(words)
    
    def _generate_pattern_repeat(self, length: int) -> str:
        """Generate text with repeating patterns"""
        patterns = ['ab', 'xyz', '123', 'qwerty', 'asdf']
        pattern = random.choice(patterns)
        result = []
        for i in range(length):
            result.append(pattern[i % len(pattern)])
        return ''.join(result)
    
    def _generate_word_salad(self, length: int) -> str:
        """Generate nonsensical word combinations"""
        prefixes = ['super', 'mega', 'ultra', 'hyper', 'neo']
        roots = ['word', 'text', 'data', 'info', 'content']
        suffixes = ['izer', 'ator', 'ifier', 'inator', 'er']
        
        words = []
        for _ in range(length):
            prefix = random.choice(prefixes) if random.random() < 0.3 else ''
            root = random.choice(roots)
            suffix = random.choice(suffixes) if random.random() < 0.4 else ''
            words.append(prefix + root + suffix)
        return ' '.join(words)
    
    def text_obfuscator(self, text: str, method: str = "unicode") -> str:
        """Obfuscate text using various methods"""
        if method == "unicode":
            return self._unicode_obfuscate(text)
        elif method == "rot13":
            return self._rot13(text)
        elif method == "binary":
            return self._binary_obfuscate(text)
        elif method == "hex":
            return self._hex_obfuscate(text)
        else:
            return text
    
    def _unicode_obfuscate(self, text: str) -> str:
        """Replace characters with similar unicode characters"""
        replacements = {
            'a': 'а', 'b': 'Ь', 'c': 'с', 'd': 'ԁ', 'e': 'е',
            'f': 'f', 'g': 'ɡ', 'h': 'һ', 'i': 'і', 'j': 'ј',
            'k': 'к', 'l': 'ⅼ', 'm': 'ⅿ', 'n': 'ո', 'o': 'о',
            'p': 'р', 'q': 'ԛ', 'r': 'г', 's': 'ѕ', 't': 'т',
            'u': 'ս', 'v': 'ѵ', 'w': 'ԝ', 'x': 'х', 'y': 'у', 'z': 'z'
        }
        result = text.lower()
        for original, replacement in replacements.items():
            result = result.replace(original, replacement)
        return result
    
    def _rot13(self, text: str) -> str:
        """ROT13 cipher"""
        result = ""
        for char in text:
            if char.isalpha():
                ascii_offset = 65 if char.isupper() else 97
                result += chr((ord(char) - ascii_offset + 13) % 26 + ascii_offset)
            else:
                result += char
        return result
    
    def _binary_obfuscate(self, text: str) -> str:
        """Convert text to binary representation"""
        binary_parts = []
        for char in text:
            binary_parts.append(format(ord(char), '08b'))
        return ' '.join(binary_parts)
    
    def _hex_obfuscate(self, text: str) -> str:
        """Convert text to hexadecimal representation"""
        return text.encode('utf-8').hex()
    
    def text_deobfuscator(self, obfuscated_text: str, method: str) -> str:
        """Deobfuscate text"""
        if method == "binary":
            binary_chars = obfuscated_text.split()
            return ''.join(chr(int(binary, 2)) for binary in binary_chars)
        elif method == "hex":
            return bytes.fromhex(obfuscated_text).decode('utf-8')
        elif method == "rot13":
            return self._rot13(obfuscated_text)  # ROT13 is its own inverse
        else:
            return obfuscated_text

def demo():
    """Demonstrate the Digital Art Generator capabilities"""
    art_gen = DigitalArtGenerator()
    
    print("🎨 DIGITAL ART GENERATOR DEMO 🎨")
    print("=" * 50)
    
    print("\n🌊 WAVE PATTERN:")
    print(art_gen.generate_wave_pattern(40, 10))
    
    print("\n🏔️ RANDOM LANDSCAPE:")
    print(art_gen.generate_random_landscape(50, 15))
    
    print("\n🌀 SPIRAL PATTERN:")
    print(art_gen.generate_spiral(15, '█'))
    
    print("\n💎 GEOMETRIC PATTERNS:")
    print("Diamond:")
    print(art_gen.generate_geometric_pattern("diamond", 12))
    print("\nCircle:")
    print(art_gen.generate_geometric_pattern("circle", 12))
    
    print("\n🎭 TEXT ART:")
    print(art_gen.generate_text_art("HELLO"))
    
    print("\n🎨 DIGITAL PAINTINGS:")
    print("Impressionist:")
    print(art_gen.create_digital_painting(25, 12, "impressionist"))
    print("\nAbstract:")
    print(art_gen.create_digital_painting(25, 12, "abstract"))
    print("\nMinimalist:")
    print(art_gen.create_digital_painting(25, 12, "minimalist"))
    
    print("\n🖼️ PIXEL ART:")
    print("Random Style:")
    print(art_gen.generate_pixel_art(20, 10, "random"))
    print("\nGradient Style:")
    print(art_gen.generate_pixel_art(20, 10, "gradient"))
    
    print("\n🎬 ANIMATION FRAME:")
    print(art_gen.generate_animation_frame(5, 20))
    
    print("\n🔢 MANDELBROT FRACTAL:")
    print(art_gen.generate_mandelbrot(40, 20))

def interactive_mode():
    """Interactive mode for creating custom art"""
    art_gen = DigitalArtGenerator()
    
    print("\n🎨 INTERACTIVE DIGITAL ART MODE 🎨")
    print("=" * 40)
    
    while True:
        print("\nChoose an art type:")
        print("1. Wave Pattern")
        print("2. Random Landscape") 
        print("3. Spiral")
        print("4. Geometric Pattern")
        print("5. Text Art")
        print("6. Digital Painting")
        print("7. Pixel Art")
        print("8. Animation Frame")
        print("9. Mandelbrot Fractal")
        print("0. Exit")
        
        choice = input("\nEnter your choice (0-9): ").strip()
        
        if choice == "0":
            print("Thanks for creating digital art! 🎨")
            break
        elif choice == "1":
            width = int(input("Width (default 40): ") or "40")
            height = int(input("Height (default 10): ") or "10")
            print(art_gen.generate_wave_pattern(width, height))
        elif choice == "2":
            width = int(input("Width (default 50): ") or "50")
            height = int(input("Height (default 15): ") or "15")
            print(art_gen.generate_random_landscape(width, height))
        elif choice == "3":
            size = int(input("Size (default 15): ") or "15")
            char = input("Character (default █): ") or "█"
            print(art_gen.generate_spiral(size, char))
        elif choice == "4":
            pattern = input("Pattern (diamond/circle/checkerboard/spiral_square): ") or "diamond"
            size = int(input("Size (default 12): ") or "12")
            print(art_gen.generate_geometric_pattern(pattern, size))
        elif choice == "5":
            text = input("Enter text: ")
            print(art_gen.generate_text_art(text))
        elif choice == "6":
            style = input("Style (impressionist/abstract/minimalist/geometric): ") or "impressionist"
            width = int(input("Width (default 25): ") or "25")
            height = int(input("Height (default 12): ") or "12")
            print(art_gen.create_digital_painting(width, height, style))
        elif choice == "7":
            style = input("Style (random/gradient/checker/circles/waves): ") or "random"
            width = int(input("Width (default 20): ") or "20")
            height = int(input("Height (default 10): ") or "10")
            print(art_gen.generate_pixel_art(width, height, style))
        elif choice == "8":
            frame = int(input("Frame number (0-19): ") or "5")
            print(art_gen.generate_animation_frame(frame))
        elif choice == "9":
            width = int(input("Width (default 40): ") or "40")
            height = int(input("Height (default 20): ") or "20")
            print(art_gen.generate_mandelbrot(width, height))
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    demo()
    print("\n" + "="*50)
    interactive_mode()
