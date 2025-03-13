from .character_maps import CharacterMap, JapaneseCharacterMap, WesternCharacterMap


class PokeTextCodec:
    """Base class for Pokémon text codecs."""

    __slots__ = (
        "_terminator",
        "_line_break",
        "_char_to_byte",
        "_byte_to_char",
        "_space_byte",
    )

    def __init__(self, char_map: CharacterMap):
        """
        Initialize the codec with a character map.

        Args:
            char_map: The character map to use
        """
        # Cache frequently accessed values
        self._terminator = char_map.TERMINATOR
        self._line_break = char_map.LINE_BREAK
        self._char_to_byte = char_map.char_to_byte
        self._byte_to_char = char_map.byte_to_char
        self._space_byte = char_map.char_to_byte.get(" ", 0x00)

    def encode(self, text: str, errors: str = "replace") -> bytes:
        """
        Encode a string into Pokémon text format.

        Args:
            text (str): The string to encode.
            errors (str, optional): Error handling strategy.
                - 'strict': Raises an error on invalid characters.
                - 'replace': Replaces invalid characters with a space.
                - 'ignore': Skips invalid characters.
                Defaults to 'replace'.

        Returns:
            bytes: The encoded Pokémon text as a byte sequence.
        """
        # Fast path for empty string
        if not text:
            return bytes([self._terminator])

        # Pre-allocate result with estimated size
        result = bytearray(len(text) + 1)  # +1 for terminator
        pos = 0

        # Direct access to dictionaries is faster
        char_to_byte = self._char_to_byte
        line_break = self._line_break
        space_byte = self._space_byte

        for i, char in enumerate(text):
            if char in char_to_byte:
                result[pos] = char_to_byte[char]
                pos += 1
            elif char == "\n":
                result[pos] = line_break
                pos += 1
            else:
                # Handle unknown chars according to the errors parameter
                if errors == "strict":
                    raise UnicodeEncodeError(
                        "pykm3", text, i, i + 1, f"Invalid char: {char}"
                    )
                elif errors == "replace":
                    result[pos] = space_byte
                    pos += 1
                elif errors == "ignore":
                    pass  # Skip this char
                else:
                    # Default fallback
                    result[pos] = space_byte
                    pos += 1

        # Add terminator
        result[pos] = self._terminator
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
        result_append = result.append  # Local reference for faster method lookup

        # Cache lookups
        terminator = self._terminator
        line_break = self._line_break
        byte_to_char = self._byte_to_char

        for i, byte in enumerate(data):
            if byte in byte_to_char:
                result_append(byte_to_char[byte])
            elif byte == terminator:
                break  # Stop at terminator
            elif byte == line_break:
                result_append("\n")
            else:
                # Handle unknown bytes according to the errors parameter
                if errors == "strict":
                    raise UnicodeDecodeError(
                        "pykm3", data, i, i + 1, f"Invalid byte: {byte}"
                    )
                elif errors == "replace":
                    result_append("?")
                elif errors == "ignore":
                    pass  # Skip this byte
                else:
                    # Default fallback
                    result_append("?")

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
