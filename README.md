# PyKM3 Codec

A Python codec for encoding and decoding text in Pokémon Generation III games (Ruby, Sapphire, Emerald, FireRed, LeafGreen).

## Features

- Full support for Western and Japanese character sets
- Implementation as a standard Python codec
- Automatic encoding detection

## Installation

```bash
pip install pykm3-codec
```

## Usage

### Basic Usage - Automatic language detection
```python
import codecs
import pykm3_codec

# Western text
text = "PIKACHU used THUNDERBOLT!"
encoded = text.encode('pykm3')
decoded = encoded.decode('pykm3')
print(f"Original: {text}")
print(f"Encoded (hex): {encoded.hex(' ')}")
print(f"Decoded: {decoded}")

# Japanese text - automatic detection
jp_text = "ピカチュウの　１０まんボルト！"
encoded = jp_text.encode('pykm3')
decoded = encoded.decode('pykm3')
print(f"Original: {jp_text}")
print(f"Encoded (hex): {encoded.hex(' ')}")
print(f"Decoded: {decoded}")
```

**⚠ WARNING**
For decoding to japanese is recommended to use directly the "pykm3jap" codec,
in most cases the automatic detection works but it can fail in some edge cases,
specially when encoding short words/bytearrays.
```python
# Automatic language detection won't work
# because all byte values are also in the western dictionary
encoded = b"\x0B\x08\x27" # さくら (sakura 🌸)
decoded = encoded.decode('pykm3') # Output: 'ÎËú'
decoded = encoded.decode('pykm3jap') # Output: 'さくら'

# This works because byte 4A is not in the western dictionary
encoded = b"\x0B\x08\x27\xE2\x4A" # さくらんぼ (sakuranbo 🍒)
decoded = encoded.decode('pykm3') # Output: 'さくらｎぼ'
```
For example: in bytes to japanese: "A2 A3 A4 A5" == "１２３４" _(fullwidth numbers)_
in bytes to western: "A2 A3 A4 A5" == "1234"
and "1234" != "１２３４"

### Using the Codec Directly

```python
from pykm3_codec import WesternPokeTextCodec, JapanesePokeTextCodec

# Western text
western_codec = WesternPokeTextCodec()
text = "Hello, Trainer!"
encoded = western_codec.encode(text)
decoded = western_codec.decode(encoded)

# Japanese text
japanese_codec = JapanesePokeTextCodec()
jp_text = "こんにちは、トレーナー！"
encoded = japanese_codec.encode(jp_text)
decoded = japanese_codec.decode(encoded)
```

### Reading/Writing Files

```python
import pykm3_codec
import codecs

# Write game script to a file
with codecs.open('script.bin', 'w', 'pykm3') as f:
    f.write("PROF. OAK: Hello there!\nWelcome to the world of POKéMON!")

# Read game script from a file
with codecs.open('script.bin', 'r', 'pykm3') as f:
    content = f.read()
    print(content)
```

## Character Support

### Western Characters

- Basic Latin alphabet (uppercase and lowercase)
- Numbers (0-9)
- Common punctuation
- Special characters (♂, ♀, etc.)
- Accented characters (é, ü, etc.)

### Japanese Characters

- Hiragana
- Katakana
- Full-width numbers and punctuation
- Full-width Latin alphabet

## License

GNU GENERAL PUBLIC LICENSE Version 3

## Acknowledgements

This codec was inspired by the documentation and research on Gen III Pokémon text format by various ROM hacking communities.
Specially bulbapedia: https://bulbapedia.bulbagarden.net/wiki/Character_encoding_(Generation_III)