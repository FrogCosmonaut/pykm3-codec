import codecs
import os
import sys
import tempfile
import pytest

import pykm3_codec
from pykm3_codec import ByteConverter, JapanesePokeTextCodec, WesternPokeTextCodec

# Add the parent directory to the path
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))


class TestByteConverter:
    """Tests for the ByteConverter utility class."""

    def test_byte_converter_to_int(self):
        """Test conversion from bytes to int."""
        assert ByteConverter.to_int(b"\x01\x02")
        assert ByteConverter.to_int(b"\xff") == 255
        assert ByteConverter.to_int(b"\x00\x00") == 0
        assert ByteConverter.to_int(b"\xff\xff") == 65535
        assert ByteConverter.to_int(b"\xff\xff\xa9\x0d") == 229244927
        # test errors
        with pytest.raises(TypeError):
            ByteConverter.to_int("asd")
        with pytest.raises(TypeError):
            ByteConverter.to_int(0)

    def test_byte_converter_from_int(self):
        """Test conversion from int to bytes."""
        assert ByteConverter.from_int(513, 2) == b"\x01\x02"
        assert ByteConverter.from_int(255, 1) == b"\xff"
        assert ByteConverter.from_int(0, 2) == b"\x00\x00"
        assert ByteConverter.from_int(229244927, 4) == b"\xff\xff\xa9\x0d"
        # test padding
        assert ByteConverter.from_int(258496712, 6) == b"\xc8\x58\x68\x0f\x00\x00"
        assert ByteConverter.from_int(0, 8) == b"\x00\x00\x00\x00\x00\x00\x00\x00"
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
            with pytest.raises((TypeError, AttributeError, OverflowError, ValueError)):
                ByteConverter.from_int(value, bit_size)

    @pytest.mark.benchmark
    def test_byte_converter_to_int_benchmark(self, benchmark):
        """Benchmark conversion from bytes to int."""
        benchmark(ByteConverter.to_int, b"\xff\xff\xa9\x0d")

    @pytest.mark.benchmark
    def test_byte_converter_from_int_benchmark(self, benchmark):
        """Benchmark conversion from int to bytes."""
        benchmark(ByteConverter.from_int, 229244927, 4)


class TestWesternCodec:
    """Tests for the Western Pokémon text codec."""

    @pytest.fixture
    def codec(self):
        """Set up a codec instance for testing."""
        return WesternPokeTextCodec()

    def test_basic_encoding(self, codec):
        """Test basic encoding functionality."""
        assert codec.encode("HELLO")[:-1] == b"\xc2\xbf\xc6\xc6\xc9"
        assert codec.encode("hello")[:-1] == b"\xdc\xd9\xe0\xe0\xe3"

    def test_numbers_and_punctuation(self, codec):
        """Test encoding of numbers and punctuation."""
        assert codec.encode("123!?")[:-1] == b"\xa2\xa3\xa4\xab\xac"

    def test_special_characters(self, codec):
        """Test encoding of special Pokémon characters."""
        assert codec.encode("♂♀")[:-1] == b"\xb5\xb6"

    def test_accented_characters(self, codec):
        """Test encoding of accented characters."""
        assert codec.encode("éÉèÈ")[:-1] == b"\x1b\x06\x1a\x05"

    def test_line_breaks(self, codec):
        """Test handling of line breaks."""
        assert (
            codec.encode("Line1\nLine2")[:-1]
            == b"\xc6\xdd\xe2\xd9\xa2\xfe\xc6\xdd\xe2\xd9\xa3"
        )

    def test_basic_decoding(self, codec):
        """Test basic decoding functionality."""
        assert codec.decode(b"\xc2\xbf\xc6\xc6\xc9\xff") == "HELLO"
        assert codec.decode(b"\xdc\xd9\xe0\xe0\xe3\xff") == "hello"

    def test_decode_numbers_punctuation(self, codec):
        """Test decoding of numbers and punctuation."""
        assert codec.decode(b"\xa2\xa3\xa4\xab\xac\xff") == "123!?"

    def test_decode_special_characters(self, codec):
        """Test decoding of special Pokémon characters."""
        assert codec.decode(b"\xb5\xb6\xff") == "♂♀"

    def test_decode_with_line_breaks(self, codec):
        """Test decoding text with line breaks."""
        assert (
            codec.decode(b"\xc6\xdd\xe2\xd9\xa2\xfe\xc6\xdd\xe2\xd9\xa3\xff")
            == "Line1\nLine2"
        )

    @pytest.mark.benchmark
    def test_encode_benchmark_short(self, benchmark, codec):
        """Benchmark encoding of a short text."""
        benchmark(codec.encode, "HELLO")

    @pytest.mark.benchmark
    def test_encode_benchmark_medium(self, benchmark, codec):
        """Benchmark encoding of a medium-length text."""
        benchmark(codec.encode, "PIKACHU used THUNDERBOLT!")

    @pytest.mark.benchmark
    def test_encode_benchmark_long(self, benchmark, codec):
        """Benchmark encoding of a longer text."""
        benchmark(
            codec.encode,
            "PROF. OAK: Hello there! Welcome to the world of POKéMON! My name is OAK. People call me the POKéMON PROF.",
        )

    @pytest.mark.benchmark
    def test_decode_benchmark_short(self, benchmark, codec):
        """Benchmark decoding of a short text."""
        encoded = codec.encode("HELLO")
        benchmark(codec.decode, encoded)

    @pytest.mark.benchmark
    def test_decode_benchmark_medium(self, benchmark, codec):
        """Benchmark decoding of a medium-length text."""
        encoded = codec.encode("PIKACHU used THUNDERBOLT!")
        benchmark(codec.decode, encoded)

    @pytest.mark.benchmark
    def test_decode_benchmark_long(self, benchmark, codec):
        """Benchmark decoding of a longer text."""
        encoded = codec.encode(
            "PROF. OAK: Hello there! Welcome to the world of POKéMON! My name is OAK. People call me the POKéMON PROF."
        )
        benchmark(codec.decode, encoded)


class TestJapaneseCodec:
    """Tests for the Japanese Pokémon text codec."""

    @pytest.fixture
    def codec(self):
        """Set up a codec instance for testing."""
        return JapanesePokeTextCodec()

    def test_hiragana(self, codec):
        """Test encoding and decoding of Hiragana characters."""
        hiragana = "あいうえお"
        encoded = codec.encode(hiragana)
        assert encoded[:-1] == b"\x01\x02\x03\x04\x05"
        assert codec.decode(encoded) == hiragana

    def test_katakana(self, codec):
        """Test encoding and decoding of Katakana characters."""
        katakana = "アイウエオ"
        encoded = codec.encode(katakana)
        assert encoded[:-1] == b"\x51\x52\x53\x54\x55"
        assert codec.decode(encoded) == katakana

    def test_mixed_japanese(self, codec):
        """Test encoding and decoding of mixed Japanese text."""
        mixed = "ポケモン　ゲットだぜ！"
        encoded = codec.encode(mixed)
        assert codec.decode(encoded) == mixed

    def test_japanese_punctuation(self, codec):
        """Test encoding and decoding of Japanese punctuation."""
        punctuation = "「こんにちは。」"
        encoded = codec.encode(punctuation)
        assert codec.decode(encoded) == punctuation

    @pytest.mark.benchmark
    def test_encode_benchmark_hiragana(self, benchmark, codec):
        """Benchmark encoding of Hiragana characters."""
        benchmark(codec.encode, "あいうえお")

    @pytest.mark.benchmark
    def test_encode_benchmark_katakana(self, benchmark, codec):
        """Benchmark encoding of Katakana characters."""
        benchmark(codec.encode, "アイウエオ")

    @pytest.mark.benchmark
    def test_encode_benchmark_mixed(self, benchmark, codec):
        """Benchmark encoding of mixed Japanese text."""
        benchmark(codec.encode, "ポケモン　ゲットだぜ！")

    @pytest.mark.benchmark
    def test_encode_benchmark_long(self, benchmark, codec):
        """Benchmark encoding of longer Japanese text."""
        benchmark(
            codec.encode,
            "オーキド　ハカセ：コンニチハ！\nポケットモンスターノ　セカイヘ　ヨウコソ！",
        )

    @pytest.mark.benchmark
    def test_decode_benchmark_hiragana(self, benchmark, codec):
        """Benchmark decoding of Hiragana characters."""
        encoded = codec.encode("あいうえお")
        benchmark(codec.decode, encoded)

    @pytest.mark.benchmark
    def test_decode_benchmark_katakana(self, benchmark, codec):
        """Benchmark decoding of Katakana characters."""
        encoded = codec.encode("アイウエオ")
        benchmark(codec.decode, encoded)

    @pytest.mark.benchmark
    def test_decode_benchmark_mixed(self, benchmark, codec):
        """Benchmark decoding of mixed Japanese text."""
        encoded = codec.encode("ポケモン　ゲットだぜ！")
        benchmark(codec.decode, encoded)

    @pytest.mark.benchmark
    def test_decode_benchmark_long(self, benchmark, codec):
        """Benchmark decoding of longer Japanese text."""
        encoded = codec.encode(
            "オーキド　ハカセ：コンニチハ！\nポケットモンスターノ　セカイヘ　ヨウコソ！"
        )
        benchmark(codec.decode, encoded)


class TestCodecRegistration:
    """Tests for codec registration and usage through the standard interface."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Register the codec for testing."""
        pykm3_codec.register()

    def test_encode_decode_western(self):
        """Test encoding and decoding Western text through the registered codec."""
        text = "PIKACHU used THUNDERBOLT!"
        encoded = text.encode("pykm3")
        decoded = encoded.decode("pykm3")
        assert decoded == text

    def test_encode_decode_japanese(self):
        """Test encoding and decoding Japanese text through the registered codec."""
        text = "ピカチュウの　１０まんボルト！"
        encoded = text.encode("pykm3jap")
        decoded = encoded.decode("pykm3jap")
        assert decoded == "ピカチュウの　１０まんボルト！"

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

            assert content == text
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

            assert content == text
        finally:
            if os.path.exists(filename):
                os.remove(filename)

    @pytest.mark.benchmark
    def test_benchmark_western_encode_decode(self, benchmark):
        """Benchmark end-to-end encoding and decoding of Western text."""
        text = "PIKACHU used THUNDERBOLT!"

        def encode_decode():
            encoded = text.encode("pykm3")
            return encoded.decode("pykm3")

        benchmark(encode_decode)

    @pytest.mark.benchmark
    def test_benchmark_japanese_encode_decode(self, benchmark):
        """Benchmark end-to-end encoding and decoding of Japanese text."""
        text = "ピカチュウの　１０まんボルト！"

        def encode_decode():
            encoded = text.encode("pykm3jap")
            return encoded.decode("pykm3jap")

        benchmark(encode_decode)

    @pytest.mark.benchmark
    def test_benchmark_western_file_io(self, benchmark):
        """Benchmark reading and writing Western text using file IO."""
        text = "PROF. OAK: Hello there!\nWelcome to the world of POKéMON!"

        def file_io():
            with tempfile.NamedTemporaryFile(delete=False) as f:
                filename = f.name

            try:
                with codecs.open(filename, "w", "pykm3") as f:
                    f.write(text)

                with codecs.open(filename, "r", "pykm3") as f:
                    content = f.read()

                return content
            finally:
                if os.path.exists(filename):
                    os.remove(filename)

        result = benchmark(file_io)
        assert result == text

    @pytest.mark.benchmark
    def test_benchmark_japanese_file_io(self, benchmark):
        """Benchmark reading and writing Japanese text using file IO."""
        text = (
            "オーキド　ハカセ：コンニチハ！\nポケットモンスターノ　セカイヘ　ヨウコソ！"
        )

        def file_io():
            with tempfile.NamedTemporaryFile(delete=False) as f:
                filename = f.name

            try:
                with codecs.open(filename, "w", "pykm3jap") as f:
                    f.write(text)

                with codecs.open(filename, "r", "pykm3jap") as f:
                    content = f.read()

                return content
            finally:
                if os.path.exists(filename):
                    os.remove(filename)

        result = benchmark(file_io)
        assert result == text


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    WESTERN_CHARACTERS = (
        "ÀÁÂÇÈÉÊËÌÎÏÒÓÔŒÙÚÛÑßàáçèéêëìîïòóôœùúûñºª&+Lv=;▯¿¡PKMNÍ%()âí↑↓←→*****"
        + "**ᵉ<>0123456789!?.-･‥"
        "''♂♀$,×/ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghij" + "klmnopqrstuvwxyz►:ÄÖÜäöü"
    )
    JAPANESE_CHARACTERS = (
        "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろ"
        + "わをんぁぃぅぇぉゃゅょがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽっアイウエオカキクケ"
        + "コサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンァィゥェォャュョガ"
        + "ギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポッ０１２３４５６７８９！？。ー・‥『』「」♂♀円"
        + "．×／ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ►：ÄÖÜäöü"
    )

    WESTERN_SAMPLE = "ÀÁÂÇÈÉÊËÌÎÏÒÓÔŒÙÚÛÑßàáçèéêëìîïòóôœùúûñºª&+Lv="
    JAPANESE_SAMPLE = (
        "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめも"
    )

    @pytest.fixture
    def western_codec(self):
        """Set up western codec instance for testing."""
        return WesternPokeTextCodec()

    @pytest.fixture
    def japanese_codec(self):
        """Set up japanese codec instance for testing."""
        return JapanesePokeTextCodec()

    def test_empty_string(self, western_codec, japanese_codec):
        """Test encoding and decoding an empty string."""
        assert western_codec.decode(western_codec.encode("")) == ""
        assert japanese_codec.decode(japanese_codec.encode("")) == ""

    def test_unsupported_characters(self, western_codec):
        """Test handling of unsupported characters."""
        text_with_unsupported = "Hello 😊 World ⚡ PikáChU!"  # Emoji is unsupported
        with pytest.raises(UnicodeEncodeError):
            western_codec.encode(text_with_unsupported)

    def test_unsupported_characters_error_scheme(self):
        """Test handling of unsupported characters with error scheme."""
        text_with_unsupported = "Hello 😊 World ⚡ PikáChU!"  # Emoji is unsupported
        encoded = text_with_unsupported.encode("pykm3", errors="replace")
        decoded = encoded.decode("pykm3", errors="replace")
        assert decoded == "Hello   World   PikáChU!"

    def test_incomplete_data(self, western_codec):
        """Test decoding of incomplete data (no terminator)."""
        assert western_codec.decode(b"\xc2\xbf\xc6\xc6\xc9") == "HELLO"

    def test_all_western_characters_substrings(self):
        """Test encoding creating all possible substrings of all western characters."""
        test_string = self.WESTERN_CHARACTERS

        for i in range(len(test_string)):
            for z in range(i + 1, len(test_string) + 1):
                substring = test_string[i:z]
                encoded = substring.encode("pykm3")
                decoded = encoded.decode("pykm3")

                assert (
                    decoded == substring
                ), f"Failed with substring: '{substring}' at indices {i}:{z}"

    def test_all_japanese_characters_substrings(self):
        """Test encoding creating all possible substrings of all japanese characters."""
        test_string = self.JAPANESE_CHARACTERS

        for i in range(len(test_string)):
            for z in range(i + 1, len(test_string) + 1):
                substring = test_string[i:z]
                encoded = substring.encode("pykm3jap")
                decoded = encoded.decode("pykm3jap")

                assert (
                    decoded == substring
                ), f"Failed with substring: '{substring}' at indices {i}:{z}"

    def test_combined_characters(self):
        """Test encoding and decoding of combined characters, this should raise an Exception."""
        test_string = "となにぬね is not Pikachu! - ゅょがぎぐげござ"
        with pytest.raises(UnicodeEncodeError):
            test_string.encode("pykm3")

    def test_brainfuck_characters(self):
        """Test encoding and decoding of strange characters, this should raise an Exception."""
        test_string = (
            "ꙮ ၌ ꧁ ꧂ ፍ ߷ ᚕ ᨏ ᥦ Ⴚ ꓄ ꕥ ꘎ ꩜ ꫞ ꯍℵ ⅏ ⊰ ⋋ ⌬ ⏧ ⑁ ⛮ ✿ ❁ ❧ ⠺ ⣿ ⭔ ⮷ ⺫ ⽏ ⿀"
        )
        with pytest.raises(UnicodeEncodeError):
            test_string.encode("pykm3")

    @pytest.mark.benchmark
    def test_benchmark_western_all_chars(self, benchmark, western_codec):
        """Benchmark encoding and decoding of a sample of Western characters."""

        def encode_decode():
            encoded = western_codec.encode(self.WESTERN_SAMPLE)
            return western_codec.decode(encoded)

        result = benchmark(encode_decode)
        assert result == self.WESTERN_SAMPLE

    @pytest.mark.benchmark
    def test_benchmark_japanese_all_chars(self, benchmark, japanese_codec):
        """Benchmark encoding and decoding of a sample of Japanese characters."""

        def encode_decode():
            encoded = japanese_codec.encode(self.JAPANESE_SAMPLE)
            return japanese_codec.decode(encoded)

        result = benchmark(encode_decode)
        assert result == self.JAPANESE_SAMPLE


if __name__ == "__main__":
    print("To run all tests:")
    print("  pytest test_pykm3.py -v")
    print("\nTo run only benchmarks:")
    print("  pytest test_pykm3.py -v -m benchmark")
