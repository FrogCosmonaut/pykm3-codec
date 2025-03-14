# PyKM3 Codec

A Python codec for encoding and decoding text in Pokémon Generation III games (Ruby, Sapphire, Emerald, FireRed, LeafGreen).

## Features

- Full support for Western and Japanese character sets
- Implementation as a standard Python codec, easy to use
- Byte to int, int to byte, little endian converter util
- LRU Cache for fast batch encoding/decoding

## Installation

```bash
pip install pykm3-codec
```

## Usage

### Basic Usage - Registered codec

```python
import pykm3_codec

# Register the codecs
# Western: pykm3 and pykm3codec
# Japanese: pykm3jap and pykm3japanese
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

western_codec = WesternPokeTextCodec()
japanese_codec = JapanesePokeTextCodec()

# Western text
text = "Hello, trainer!"
encoded = western_codec.encode(text)  # Output: b'\xc2\xd9\xe0\xe0\xe3\xb8\x00\xe8\xe6\xd5\xdd\xe2\xd9\xe6\xab\xff'
decoded = western_codec.decode(encoded)  # Output: Hello, trainer!

# Japanese text
jp_text = "こんにちは．トレーナー！"
encoded = japanese_codec.encode(jp_text)  # Output: b'\n.\x16\x11\x1a\xb8dz\xaee\xae\xab\xff'
decoded = japanese_codec.decode(encoded)  # Output: こんにちは．トレーナー！
```

### Reading/Writing Files

```python
import codecs
import pykm3_codec

pykm3_codec.register()

# Write game script to a file
with codecs.open('script.bin', 'w', 'pykm3') as f:
    f.write("PROF. OAK: Hello there!\nWelcome to the world of POKéMON!")

# Read game script from a file
with codecs.open('script.bin', 'r', 'pykm3') as f:
    content = f.read()
```

### Byte-int converter
###### This is just a helper of int.from_bytes() and int.to_bytes() type methods, with LRU cache and Little Endian predefined (PK-GEN3 save standard)
```python
from pykm3_codec import ByteConverter as pk_byte

pk_byte.to_int(b"\xff")   # Output: 255
pk_byte.from_int(513, 2)  # Output: b"\x01\x02"
```

### Error handling
- strict: Raises UnicodeDecodeError / UnicodeEncodeError
- ignore: Skip the char/byte
- replace: Replaces the invalid chars with spaces and invalid bytes with 0x00.

```python
from pykm3_codec import WesternPokeTextCodec

west_codec = WesternPokeTextCodec()

test = "TEST すす"
test_bytes = b"\x49\x4a"

# Encode
west_codec.encode(test)  # UnicodeEncodeError: Invalid char: す
print(west_codec.encode(test, errors="ignore"))   # Output: b'\xce\xbf\xcd\xce\x00\xff'
print(west_codec.encode(test, errors="replace"))  # Output: b'\xce\xbf\xcd\xce\x00\x00\x00\xff'

# Decode
west_codec.decode(test_bytes)  # UnicodeDecodeError: Invalid byte: 73
print(west_codec.decode(test_bytes, errors="ignore"))   # Output  "  "
print(west_codec.decode(test_bytes, errors="replace"))  # Output  "??"
```
> ℹ: Error handling also works with registered "pykm3" and "pykm3jap" codecs.  
`str.encode("pykm3", errors="ignore")`

### Notes
The register method is slower than WesternPokeTextCodec and JapanesePokeTextCodec, direct class usage is ~x2.4 times faster according to benchmarks. For bigger projects maybe is simpler to register the codec once and use it as string.encode/decode("pykm3") along the project instead of passing the codec class to modules. 👽🤷

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