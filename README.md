# PyKM3 Codec

A Python codec for encoding and decoding text in Pokémon Generation III games (Ruby, Sapphire, Emerald, FireRed, LeafGreen).

## Features

- Full support for Western and Japanese character sets
- Implementation as a standard Python codec
- Automatic encoding detection
- Comprehensive test suite

## Installation

```bash
pip install pykm3-codec
```

## Usage

### Basic Usage

```python
import codecs
import pykm3_codec

# Register the codec
codecs.register(pykm3_codec.pykm3_search_function)

# Western text
text = "PIKACHU used THUNDERBOLT!"
encoded = text.encode('pykm3')
decoded = encoded.decode('pykm3')
print(f"Original: {text}")
print(f"Encoded (hex): {encoded.hex(' ')}")
print(f"Decoded: {decoded}")

# Japanese text (use @jp: prefix)
jp_text = "@jp:ピカチュウの　１０まんボルト！"
encoded = jp_text.encode('pykm3')
decoded = encoded.decode('pykm3')
print(f"Original: {jp_text}")
print(f"Encoded (hex): {encoded.hex(' ')}")
print(f"Decoded: {decoded}")
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
import codecs
codecs.register(pykm3_codec.pykm3_search_function)

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

## Development

### Running Tests

```bash
python -m unittest test_pykm3_codec.py
```

## License

GNU GENERAL PUBLIC LICENSE

## Acknowledgements

This codec was inspired by the documentation and research on Gen III Pokémon text format by various ROM hacking communities.
