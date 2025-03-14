from pykm3_codec import ByteConverter as pk_byte

pk_byte.to_int(b"\xff")  # Output: 255
pk_byte.from_int(513, 2)  # Output: b"\x01\x02"
