import codecs
import os
import sys
import tempfile
import unittest

import pykm3_codec
from pykm3_codec import ByteConverter, JapanesePokeTextCodec, WesternPokeTextCodec

# Add the parent directory to the path
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))


class TestByteConverter(unittest.TestCase):
    """Tests for the ByteConverter utility class."""

    def test_to_int(self):
        """Test conversion from bytes to int."""
        self.assertEqual(ByteConverter.to_int(b"\x01\x02"), 513)
        self.assertEqual(ByteConverter.to_int(b"\xff"), 255)
        self.assertEqual(ByteConverter.to_int(b"\x00\x00"), 0)
        self.assertEqual(ByteConverter.to_int(b"\xff\xff"), 65535)
        self.assertEqual(ByteConverter.to_int(b"\xff\xff\xa9\x0d"), 229244927)
        # test errors
        with self.assertRaises(TypeError):
            ByteConverter.to_int("asd")
        with self.assertRaises(TypeError):
            ByteConverter.to_int(0)

    def test_from_int(self):
        """Test conversion from int to bytes."""
        self.assertEqual(ByteConverter.from_int(513, 2), b"\x01\x02")
        self.assertEqual(ByteConverter.from_int(255, 1), b"\xff")
        self.assertEqual(ByteConverter.from_int(0, 2), b"\x00\x00")
        self.assertEqual(ByteConverter.from_int(229244927, 4), b"\xff\xff\xa9\x0d")
        # test padding
        self.assertEqual(
            ByteConverter.from_int(258496712, 6), b"\xc8\x58\x68\x0f\x00\x00"
        )
        self.assertEqual(
            ByteConverter.from_int(0, 8), b"\x00\x00\x00\x00\x00\x00\x00\x00"
        )
        # test errors
        invalid_inputs = [
            ("asd", 1),
            ("asd", "0"),
            (255, "-1"),
            ("0", 1),
            (-1, 1),
            (1, -1),
            (1, 0),
            ([0, 1], 1 + 3),
        ]
        for value, bit_size in invalid_inputs:
            with self.assertRaises(
                (TypeError, AttributeError, OverflowError, ValueError)
            ):
                ByteConverter.from_int(value, bit_size)


class TestWesternCodec(unittest.TestCase):
    """Tests for the Western Pokémon text codec."""

    def setUp(self):
        """Set up a codec instance for testing."""
        self.codec = WesternPokeTextCodec()

    def test_basic_encoding(self):
        """Test basic encoding functionality."""
        self.assertEqual(self.codec.encode("HELLO")[:-1], b"\xc2\xbf\xc6\xc6\xc9")
        self.assertEqual(self.codec.encode("hello")[:-1], b"\xdc\xd9\xe0\xe0\xe3")

    def test_numbers_and_punctuation(self):
        """Test encoding of numbers and punctuation."""
        self.assertEqual(self.codec.encode("123!?")[:-1], b"\xa2\xa3\xa4\xab\xac")

    def test_special_characters(self):
        """Test encoding of special Pokémon characters."""
        self.assertEqual(self.codec.encode("♂♀")[:-1], b"\xb5\xb6")

    def test_accented_characters(self):
        """Test encoding of accented characters."""
        self.assertEqual(self.codec.encode("éÉèÈ")[:-1], b"\x1b\x06\x1a\x05")

    def test_line_breaks(self):
        """Test handling of line breaks."""
        self.assertEqual(
            self.codec.encode("Line1\nLine2")[:-1],
            b"\xc6\xdd\xe2\xd9\xa2\xfe\xc6\xdd\xe2\xd9\xa3",
        )

    def test_basic_decoding(self):
        """Test basic decoding functionality."""
        self.assertEqual(self.codec.decode(b"\xc2\xbf\xc6\xc6\xc9\xff"), "HELLO")
        self.assertEqual(self.codec.decode(b"\xdc\xd9\xe0\xe0\xe3\xff"), "hello")

    def test_decode_numbers_punctuation(self):
        """Test decoding of numbers and punctuation."""
        self.assertEqual(self.codec.decode(b"\xa2\xa3\xa4\xab\xac\xff"), "123!?")

    def test_decode_special_characters(self):
        """Test decoding of special Pokémon characters."""
        self.assertEqual(self.codec.decode(b"\xb5\xb6\xff"), "♂♀")

    def test_decode_with_line_breaks(self):
        """Test decoding text with line breaks."""
        self.assertEqual(
            self.codec.decode(b"\xc6\xdd\xe2\xd9\xa2\xfe\xc6\xdd\xe2\xd9\xa3\xff"),
            "Line1\nLine2",
        )


class TestJapaneseCodec(unittest.TestCase):
    """Tests for the Japanese Pokémon text codec."""

    def setUp(self):
        """Set up a codec instance for testing."""
        self.codec = JapanesePokeTextCodec()

    def test_hiragana(self):
        """Test encoding and decoding of Hiragana characters."""
        hiragana = "あいうえお"
        encoded = self.codec.encode(hiragana)
        self.assertEqual(encoded[:-1], b"\x01\x02\x03\x04\x05")
        self.assertEqual(self.codec.decode(encoded), hiragana)

    def test_katakana(self):
        """Test encoding and decoding of Katakana characters."""
        katakana = "アイウエオ"
        encoded = self.codec.encode(katakana)
        self.assertEqual(encoded[:-1], b"\x51\x52\x53\x54\x55")
        self.assertEqual(self.codec.decode(encoded), katakana)

    def test_mixed_japanese(self):
        """Test encoding and decoding of mixed Japanese text."""
        mixed = "ポケモン　ゲットだぜ！"
        encoded = self.codec.encode(mixed)
        self.assertEqual(self.codec.decode(encoded), mixed)

    def test_japanese_punctuation(self):
        """Test encoding and decoding of Japanese punctuation."""
        punctuation = "「こんにちは。」"
        encoded = self.codec.encode(punctuation)
        self.assertEqual(self.codec.decode(encoded), punctuation)


class TestCodecRegistration(unittest.TestCase):
    """Tests for codec registration and usage through the standard interface."""

    def setUp(self):
        """Register the codec for testing."""
        pykm3_codec.register()

    def test_encode_decode_western(self):
        """Test encoding and decoding Western text through the registered codec."""
        text = "PIKACHU used THUNDERBOLT!"
        encoded = text.encode("pykm3")
        decoded = encoded.decode("pykm3")
        self.assertEqual(decoded, text)

    def test_encode_decode_japanese(self):
        """Test encoding and decoding Japanese text through the registered codec."""
        text = "ピカチュウの　１０まんボルト！"
        encoded = text.encode("pykm3jap")
        decoded = encoded.decode("pykm3jap")
        self.assertEqual(decoded, "ピカチュウの　１０まんボルト！")

    def test_stream_io_western(self):
        """Test reading and writing using stream IO."""
        text = "PROF. OAK: Hello there!\nWelcome to the world of POKéMON!"

        with tempfile.NamedTemporaryFile(delete=False) as f:
            filename = f.name

        try:
            with codecs.open(filename, "w", "pykm3") as f:
                f.write(text)

            with codecs.open(filename, "r", "pykm3") as f:
                content = f.read()

            self.assertEqual(content, text)
        finally:
            if os.path.exists(filename):
                os.remove(filename)

    def test_stream_io_japanese(self):
        """Test reading and writing using stream IO."""
        text = (
            "オーキド　ハカセ：コンニチハ！\nポケットモンスターノ　セカイヘ　ヨウコソ！"
        )

        with tempfile.NamedTemporaryFile(delete=False) as f:
            filename = f.name

        try:
            with codecs.open(filename, "w", "pykm3jap") as f:
                f.write(text)

            with codecs.open(filename, "r", "pykm3jap") as f:
                content = f.read()

            self.assertEqual(content, text)
        finally:
            if os.path.exists(filename):
                os.remove(filename)


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases and error handling."""

    WESTERN_CHARACTERS = (
        "ÀÁÂÇÈÉÊËÌÎÏÒÓÔŒÙÚÛÑßàáçèéêëìîïòóôœùúûñºª&+Lv=;▯¿¡PKMNÍ%()âí↑↓←→*****"
        + "**ᵉ<>0123456789!?.-･‥“”‘'♂♀$,×/ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghij"
        + "klmnopqrstuvwxyz►:ÄÖÜäöü"
    )
    JAPANESE_CHARACTERS = (
        "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろ"
        + "わをんぁぃぅぇぉゃゅょがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽっアイウエオカキクケ"
        + "コサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンァィゥェォャュョガ"
        + "ギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポッ０１２３４５６７８９！？。ー・‥『』「」♂♀円"
        + "．×／ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ►：ÄÖÜäöü"
    )

    def setUp(self):
        """Set up codec instances for testing."""
        self.western_codec = WesternPokeTextCodec()
        self.japanese_codec = JapanesePokeTextCodec()

    def test_empty_string(self):
        """Test encoding and decoding an empty string."""
        self.assertEqual(self.western_codec.decode(self.western_codec.encode("")), "")
        self.assertEqual(self.japanese_codec.decode(self.japanese_codec.encode("")), "")

    def test_unsupported_characters(self):
        """Test handling of unsupported characters."""
        text_with_unsupported = "Hello 😊 World ⚡ PikáChU!"  # Emoji is unsupported
        encoded = self.western_codec.encode(text_with_unsupported)
        decoded = self.western_codec.decode(encoded)
        self.assertEqual(decoded, "Hello   World   PikáChU!")

    def test_unsupported_characters_error_scheme(self):
        """Test handling of unsupported characters with error scheme."""
        text_with_unsupported = "Hello 😊 World ⚡ PikáChU!"  # Emoji is unsupported
        encoded = text_with_unsupported.encode("pykm3", errors="replace")
        decoded = encoded.decode("pykm3", errors="replace")
        self.assertEqual(decoded, "Hello   World   PikáChU!")

    def test_incomplete_data(self):
        """Test decoding of incomplete data (no terminator)."""
        self.assertEqual(self.western_codec.decode(b"\xc2\xbf\xc6\xc6\xc9"), "HELLO")

    def test_all_western_characters_substrings(self):
        """Test encoding creating all possible substrings of all western characters."""
        test_string = self.WESTERN_CHARACTERS

        for i in range(len(test_string)):
            for z in range(i + 1, len(test_string) + 1):
                substring = test_string[i:z]
                encoded = substring.encode("pykm3")
                decoded = encoded.decode("pykm3")

                self.assertEqual(
                    decoded,
                    substring,
                    f"Failed with substring: '{substring}' at indices {i}:{z}",
                )

    def test_all_japanese_characters_substrings(self):
        """Test encoding creating all possible substrings of all japanese characters."""
        test_string = self.JAPANESE_CHARACTERS

        for i in range(len(test_string)):
            for z in range(i + 1, len(test_string) + 1):
                substring = test_string[i:z]
                encoded = substring.encode("pykm3jap")
                decoded = encoded.decode("pykm3jap")

                self.assertEqual(
                    decoded,
                    substring,
                    f"Failed with substring: '{substring}' at indices {i}:{z}",
                )

    def test_combined_characters(self):
        """Test encoding and decoding of combined characters, this should raise an Exception."""
        test_string = "となにぬね is not Pikachu! - ゅょがぎぐげござ"
        with self.assertRaises(UnicodeEncodeError):
            test_string.encode("pykm3")

    def test_brainfuck_characters(self):
        """Test encoding and decoding of strange characters, this should raise an Exception."""
        test_string = (
            "ꙮ ၌ ꧁ ꧂ ፍ ߷ ᚕ ᨏ ᥦ Ⴚ ꓄ ꕥ ꘎ ꩜ ꫞ ꯍℵ ⅏ ⊰ ⋋ ⌬ ⏧ ⑁ ⛮ ✿ ❁ ❧ ⠺ ⣿ ⭔ ⮷ ⺫ ⽏ ⿀"
        )
        with self.assertRaises(UnicodeEncodeError):
            test_string.encode("pykm3")


if __name__ == "__main__":
    unittest.main()
