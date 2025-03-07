from .character_maps import CharacterMap, JapaneseCharacterMap, WesternCharacterMap


class PokeTextCodec:
    """Base class for Pokémon text codecs."""

    def __init__(self, char_map: CharacterMap):
        """
        Initialize the codec with a character map.

        Args:
            char_map: The character map to use
        """
        self.char_map = char_map

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
        result = bytearray()

        for i, char in enumerate(text):
            if char == "\n":
                result.append(self.char_map.LINE_BREAK)
            elif char in self.char_map.char_to_byte:
                result.append(self.char_map.char_to_byte[char])
            else:
                # Handle unknown chars according to the errors parameter
                if errors == "strict":
                    raise UnicodeEncodeError(
                        "pykm3", text, i, i + 1, f"Invalid char: {char}"
                    )
                elif errors == "replace":
                    result.append(self.char_map.char_to_byte.get(" ", 0x00))
                elif errors == "ignore":
                    pass  # Skip this char
                else:
                    # Default fallback
                    result.append(self.char_map.char_to_byte.get(" ", 0x00))

        # Add terminator
        result.append(self.char_map.TERMINATOR)
        return bytes(result)

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
        result = []
        i = 0

        while i < len(data):
            byte = data[i]

            if byte == self.char_map.TERMINATOR:
                break  # Stop at terminator
            elif byte == self.char_map.LINE_BREAK:
                result.append("\n")
            elif byte in self.char_map.byte_to_char:
                result.append(self.char_map.byte_to_char[byte])
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

            i += 1

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
