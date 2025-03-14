import pykm3_codec

pykm3_codec.register()
west_codec = pykm3_codec.WesternPokeTextCodec()
jap_codec = pykm3_codec.JapanesePokeTextCodec()


def printh(data: bytes) -> None:
    print(data.hex(" "))


def prints(string: str) -> None:
    print(f'"{string}"')


def printe(expr) -> None:
    try:
        expr()
    except Exception as e:
        print(f"{type(e).__name__}: {e}")


err_text = "TEST すす"
west_bytes = b"\x49\x4a"

# Direct codec - Encode
print("\n", "-" * 10, "Direct codec - Encode", "-" * 10)
printe(lambda: west_codec.encode(err_text))
printh(west_codec.encode(err_text, errors="ignore"))
printh(west_codec.encode(err_text, errors="replace"))

# Direct codec - Decode
print("\n", "-" * 10, "Direct codec - Decode", "-" * 10)
printe(lambda: west_codec.decode(west_bytes))
prints(west_codec.decode(west_bytes, errors="ignore"))
prints(west_codec.decode(west_bytes, errors="replace"))


# Registered codec - Encode
print("\n", "-" * 10, "Registered codec - Encode", "-" * 10)
printe(lambda: err_text.encode("pykm3"))
printh(err_text.encode("pykm3", errors="ignore"))
printh(err_text.encode("pykm3", errors="replace"))

# Registered codec - Decode
print("\n", "-" * 10, "Registered codec - Decode", "-" * 10)
printe(lambda: west_bytes.decode("pykm3"))
prints(west_bytes.decode("pykm3", errors="ignore"))
prints(west_bytes.decode("pykm3", errors="replace"))


""" OUTPUT:

 ---------- Direct codec - Encode ----------
UnicodeEncodeError: 'pykm3' codec can't encode character '\u3059' in position 5: Invalid char: す
ce bf cd ce 00 ff
ce bf cd ce 00 00 00 ff

 ---------- Direct codec - Decode ----------
UnicodeDecodeError: 'pykm3' codec can't decode byte 0x49 in position 0: Invalid byte: 73
""
"??"

 ---------- Registered codec - Encode ----------
UnicodeEncodeError: 'pykm3' codec can't encode character '\u3059' in position 5: Invalid char: す
ce bf cd ce 00 ff
ce bf cd ce 00 00 00 ff

 ---------- Registered codec - Decode ----------
UnicodeDecodeError: 'pykm3' codec can't decode byte 0x49 in position 0: Invalid byte: 73
""
"??"

"""
