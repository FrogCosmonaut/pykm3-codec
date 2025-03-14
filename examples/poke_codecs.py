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
