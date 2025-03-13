from .character_maps import CharacterMap, JapaneseCharacterMap, WesternCharacterMap

from functools import lru_cache


class PokeTextCodec:
    """Base class for Pokémon text codecs."""

    __slots__ = ("_char_to_byte", "_byte_to_char")

    BYTE_SPACE = 0x00
    BYTE_TERMINATOR = 0xFF

    def __init__(self, char_map: CharacterMap):
        """
        Initialize the codec with a character map.

        Args:
            char_map: The character map to use
        """
        self.encode = lru_cache(maxsize=128)(self.encode)
        self.decode = lru_cache(maxsize=128)(self.decode)

        self._char_to_byte = char_map.char_to_byte
        self._byte_to_char = char_map.byte_to_char

    def encode(self, text: str, errors: str = "strict") -> bytes:
        """
        Encode a string into Pokémon text format.

        Args:
            text (str): The string to encode.
            errors (str, optional): Error handling strategy.
                - 'strict': Raises an error on invalid characters.
                - 'replace': Replaces invalid characters with a space.
                - 'ignore': Skips invalid characters.
                Defaults to 'strict'.

        Returns:
            bytes: The encoded Pokémon text as a byte sequence.
        """
        # Fast path for empty string
        if not text:
            return bytes([self.BYTE_TERMINATOR])

        # Pre-allocate result with estimated size
        result = bytearray(len(text) + 1)  # +1 for terminator
        pos = 0

        # Direct access to dictionaries is faster
        char_to_byte = self._char_to_byte

        for i, char in enumerate(text):
            if char in char_to_byte:
                result[pos] = char_to_byte[char]
                pos += 1
            else:
                # Handle unknown chars according to the errors parameter
                if errors == "strict":
                    raise UnicodeEncodeError(
                        "pykm3", text, i, i + 1, f"Invalid char: {char}"
                    )
                elif errors == "replace":
                    result[pos] = self.BYTE_SPACE
                    pos += 1
                elif errors == "ignore":
                    pass  # Skip this char
                else:
                    # Default fallback
                    result[pos] = self.BYTE_SPACE
                    pos += 1

        # Add terminator
        result[pos] = self.BYTE_TERMINATOR
        pos += 1

        # Trim the bytearray to actual size used
        return bytes(result[:pos])

    def decode(self, data: bytes, errors: str = "strict") -> str:
        """
        Decode a Pokémon text format byte sequence back into a string.

        Args:
            data (bytes): The encoded byte sequence.
            errors (str, optional): Error handling strategy.
                - 'strict': Raises an error on invalid bytes.
                - 'replace': Replaces invalid bytes with '?'.
                - 'ignore': Skips invalid bytes.
                Defaults to 'strict'.

        Returns:
            str: The decoded string.
        """
        # Fast path for empty data
        if not data:
            return ""

        # Pre-allocate result buffer
        result = []

        # Cache lookups
        byte_to_char = self._byte_to_char

        for i, byte in enumerate(data):
            if byte in byte_to_char:
                result.append(byte_to_char[byte])
            elif byte == self.BYTE_TERMINATOR:
                break  # Stop at terminator
            else:
                # Handle unknown bytes according to the errors parameter
                if errors == "strict":
                    raise UnicodeDecodeError(
                        "pykm3", data, i, i + 1, f"Invalid byte: {byte}"
                    )
                elif errors == "replace":
                    result.append("?")
                elif errors == "ignore":
                    pass  # Skip this byte
                else:
                    # Default fallback
                    result.append("?")

        return "".join(result)


class WesternPokeTextCodec(PokeTextCodec):
    """Codec for Western Pokémon text."""

    def __init__(self):
        """Initialize with Western character map."""
        super().__init__(WesternCharacterMap())


class JapanesePokeTextCodec(PokeTextCodec):
    """Codec for Japanese Pokémon text."""

    def __init__(self):
        """Initialize with Japanese character map."""
        super().__init__(JapaneseCharacterMap())
