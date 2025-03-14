import pykm3_codec

# Register the codecs
# Western: pykm3 and pykm3codec
# Japanese: pykm3jap and pykm3japanese
pykm3_codec.register()

# Western text
text = "KADABRA used PSYCHIC!"
encoded = text.encode("pykm3")
decoded = encoded.decode("pykm3")
print(f"Original: {text}")
print(f"Encoded : {encoded.hex(' ')}")
print(f"Decoded : {decoded}")

# Japanese text
jp_text = "ユンゲラー　ハ　サイコキネシス　ヲ　ツカッタ！"
encoded = jp_text.encode("pykm3jap")
decoded = encoded.decode("pykm3jap")
print(f"Original: {jp_text}")
print(f"Encoded : {encoded.hex(' ')}")
print(f"Decoded : {decoded}")
