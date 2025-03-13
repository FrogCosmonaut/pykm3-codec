# PyKM3 Codec

A Python codec for encoding and decoding text in Pokémon Generation III games (Ruby, Sapphire, Emerald, FireRed, LeafGreen).

## Features

- Full support for Western and Japanese character sets
- Implementation as a standard Python codec

## Installation

```bash
pip install pykm3-codec
```

## Usage

### Basic Usage - Registered codec
```python
import pykm3_codec

# Register the codecs
pykm3_codec.register()

# Western text
text = "KADABRA used PSYCHIC!"
encoded = text.encode('pykm3')
decoded = encoded.decode('pykm3')
print(f"Original: {text}")
print(f"Encoded : {encoded.hex(' ')}")
print(f"Decoded : {decoded}")

# Japanese text
jp_text = "ユンゲラー　ハ　サイコキネシス　ヲ　ツカッタ！"
encoded = jp_text.encode('pykm3jap')
decoded = encoded.decode('pykm3jap')
print(f"Original: {jp_text}")
print(f"Encoded : {encoded.hex(' ')}")
print(f"Decoded : {decoded}")
```

Output:
```
Original: KADABRA used PSYCHIC!
Encoded : c5 bb be bb bc cc bb 00 e9 e7 d9 d8 00 ca cd d3 bd c2 c3 bd ab ff
Decoded : KADABRA used PSYCHIC!
Original: ユンゲラー　ハ　サイコキネシス　ヲ　ツカッタ！
Encoded : 75 7e 8a 77 ae 00 6a 00 5b 52 5a 57 68 5c 5d 00 7d 00 62 56 a0 60 ab ff
Decoded : ユンゲラー　ハ　サイコキネシス　ヲ　ツカッタ！
```

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