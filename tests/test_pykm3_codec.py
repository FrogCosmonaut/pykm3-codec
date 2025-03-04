import unittest
import codecs
import os
import sys

# Add the parent directory to the path
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import pykm3_codec
from pykm3_codec import (
    WesternPokeTextCodec,
    JapanesePokeTextCodec,
    ByteConverter
)


class TestByteConverter(unittest.TestCase):
    """Tests for the ByteConverter utility class."""

    def test_to_int(self):
        """Test conversion from bytes to int."""
        self.assertEqual(ByteConverter.to_int(b'\x01\x02'), 513)
        self.assertEqual(ByteConverter.to_int(b'\xFF'), 255)
        self.assertEqual(ByteConverter.to_int(b'\x00\x00'), 0)

    def test_from_int(self):
        """Test conversion from int to bytes."""
        self.assertEqual(ByteConverter.from_int(513, 2), b'\x01\x02')
        self.assertEqual(ByteConverter.from_int(255, 1), b'\xFF')
        self.assertEqual(ByteConverter.from_int(0, 2), b'\x00\x00')


class TestWesternCodec(unittest.TestCase):
    """Tests for the Western Pokémon text codec."""

    def setUp(self):
        """Set up a codec instance for testing."""
        self.codec = WesternPokeTextCodec()

    def test_basic_encoding(self):
        """Test basic encoding functionality."""
        # Test basic ASCII text
        self.assertEqual(
            self.codec.encode("HELLO")[:-1],  # Exclude terminator
            b'\xC2\xBF\xC6\xC6\xC9'
        )
        # Test lowercase
        self.assertEqual(
            self.codec.encode("hello")[:-1],
            b'\xDC\xD9\xE0\xE0\xE3'
        )

    def test_numbers_and_punctuation(self):
        """Test encoding of numbers and punctuation."""
        self.assertEqual(
            self.codec.encode("123!?")[:-1],
            b'\xA2\xA3\xA4\xAB\xAC'
        )

    def test_special_characters(self):
        """Test encoding of special Pokémon characters."""
        self.assertEqual(
            self.codec.encode("♂♀")[:-1],
            b'\xB5\xB6'
        )

    def test_accented_characters(self):
        """Test encoding of accented characters."""
        self.assertEqual(
            self.codec.encode("éÉèÈ")[:-1],
            b'\x1B\x06\x1A\x05'
        )

    def test_line_breaks(self):
        """Test handling of line breaks."""
        self.assertEqual(
            self.codec.encode("Line1\nLine2")[:-1],
            b'\xC6\xDD\xE2\xD9\xA2\xFE\xC6\xDD\xE2\xD9\xA3'
        )

    def test_basic_decoding(self):
        """Test basic decoding functionality."""
        self.assertEqual(
            self.codec.decode(b'\xC2\xBF\xC6\xC6\xC9\xFF'),
            "HELLO"
        )
        self.assertEqual(
            self.codec.decode(b'\xDC\xD9\xE0\xE0\xE3\xFF'),
            "hello"
        )

    def test_decode_numbers_punctuation(self):
        """Test decoding of numbers and punctuation."""
        self.assertEqual(
            self.codec.decode(b'\xA2\xA3\xA4\xAB\xAC\xFF'),
            "123!?"
        )

    def test_decode_special_characters(self):
        """Test decoding of special Pokémon characters."""
        self.assertEqual(
            self.codec.decode(b'\xB5\xB6\xFF'),
            "♂♀"
        )

    def test_decode_with_line_breaks(self):
        """Test decoding text with line breaks."""
        self.assertEqual(
            self.codec.decode(b'\xC6\xDD\xE2\xD9\xA2\xFE\xC6\xDD\xE2\xD9\xA3\xFF'),
            "Line1\nLine2"
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
        # Check encoding (excluding terminator)
        self.assertEqual(encoded[:-1], b'\x01\x02\x03\x04\x05')
        # Check round-trip
        self.assertEqual(self.codec.decode(encoded), hiragana)

    def test_katakana(self):
        """Test encoding and decoding of Katakana characters."""
        katakana = "アイウエオ"
        encoded = self.codec.encode(katakana)
        # Check encoding (excluding terminator)
        self.assertEqual(encoded[:-1], b'\x51\x52\x53\x54\x55')
        # Check round-trip
        self.assertEqual(self.codec.decode(encoded), katakana)

    def test_mixed_japanese(self):
        """Test encoding and decoding of mixed Japanese text."""
        mixed = "ポケモン　ゲットだぜ！"
        encoded = self.codec.encode(mixed)
        # Check round-trip
        self.assertEqual(self.codec.decode(encoded), mixed)

    def test_japanese_punctuation(self):
        """Test encoding and decoding of Japanese punctuation."""
        punctuation = "「こんにちは。」"
        encoded = self.codec.encode(punctuation)
        # Check round-trip
        self.assertEqual(self.codec.decode(encoded), punctuation)


class TestCodecRegistration(unittest.TestCase):
    """Tests for codec registration and usage through the standard interface."""

    def setUp(self):
        """Register the codec for testing."""
        codecs.register(pykm3_codec.pykm3_search_function)

    def test_encode_decode_western(self):
        """Test encoding and decoding Western text through the registered codec."""
        text = "PIKACHU used THUNDERBOLT!"
        encoded = text.encode('pykm3')
        decoded = encoded.decode('pykm3')
        self.assertEqual(decoded, text)

    def test_encode_decode_japanese(self):
        """Test encoding and decoding Japanese text through the registered codec."""
        text = "@jp:ピカチュウの　１０まんボルト！"
        encoded = text.encode('pykm3')
        decoded = encoded.decode('pykm3')
        # The prefix should be stripped during encoding and not present in the decoded result
        self.assertEqual(decoded, "ピカチュウの　１０まんボルト！")

    def test_stream_io(self):
        """Test reading and writing using stream IO."""
        text = "PROF. OAK: Hello there!\nWelcome to the world of POKéMON!"
        
        # Create a temporary file
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False) as f:
            filename = f.name
        
        try:
            # Write to the file
            with codecs.open(filename, 'w', 'pykm3') as f:
                f.write(text)
            
            # Read from the file
            with codecs.open(filename, 'r', 'pykm3') as f:
                content = f.read()
            
            self.assertEqual(content, text)
        finally:
            # Clean up
            if os.path.exists(filename):
                os.remove(filename)


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases and error handling."""

    def setUp(self):
        """Set up codec instances for testing."""
        self.western_codec = WesternPokeTextCodec()
        self.japanese_codec = JapanesePokeTextCodec()
        codecs.register(pykm3_codec.pykm3_search_function)

    def test_empty_string(self):
        """Test encoding and decoding an empty string."""
        self.assertEqual(self.western_codec.decode(self.western_codec.encode("")), "")
        self.assertEqual(self.japanese_codec.decode(self.japanese_codec.encode("")), "")

    def test_unsupported_characters(self):
        """Test handling of unsupported characters."""
        # Western codec should replace unsupported characters with spaces
        text_with_unsupported = "Hello 😊 World"  # Emoji is unsupported
        encoded = self.western_codec.encode(text_with_unsupported)
        decoded = self.western_codec.decode(encoded)
        # The emoji should be replaced with a space
        self.assertEqual(decoded, "Hello   World")

    def test_incomplete_data(self):
        """Test decoding of incomplete data (no terminator)."""
        # Data without terminator should still be decoded
        self.assertEqual(
            self.western_codec.decode(b'\xC2\xBF\xC6\xC6\xC9'),
            "HELLO"
        )

    def test_auto_detection(self):
        """Test automatic detection of encoding type."""
        # Encode text with both codecs
        western_text = "PIKACHU"
        japanese_text = "ピカチュウ"
        
        western_encoded = western_text.encode('pykm3')
        japanese_encoded = ("@jp:" + japanese_text).encode('pykm3')
        
        # Decode without specifying the codec
        self.assertEqual(western_encoded.decode('pykm3'), western_text)
        self.assertEqual(japanese_encoded.decode('pykm3'), japanese_text)


if __name__ == '__main__':
    unittest.main()