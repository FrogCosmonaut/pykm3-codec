import pykm3_codec

pykm3_codec.register()


class PokemonNameConverter:
    """Utility for converting Pokémon names between text and game encoding formats."""

    def __init__(self, language="western"):
        """Initialize with specified language codec."""
        self.encoding = "pykm3" if language.lower() == "western" else "pykm3jap"

    def encode_names(self, pokemon_names):
        """Convert a list of Pokémon names to their encoded format."""
        encoded_data = {}
        for name in pokemon_names:
            encoded = name.encode(self.encoding)
            encoded_data[name] = {
                "bytes": encoded,
                "hex": encoded.hex(" "),
                "length": len(encoded) - 1,
            }
        return encoded_data

    def decode_bytes(self, encoded_data):
        """Convert a dictionary of encoded data back to Pokémon names."""
        decoded_names = {}
        for name, data in encoded_data.items():
            decoded = data["bytes"].decode(self.encoding)
            decoded_names[name] = decoded
        return decoded_names


# Example usage
if __name__ == "__main__":
    # Western Pokémon names
    west_converter = PokemonNameConverter("western")
    west_pokemon = ["PIKACHU", "CHARIZARD", "MEWTWO", "EEVEE"]

    west_encoded = west_converter.encode_names(west_pokemon)

    print("Western Pokémon Names:")
    for name, data in west_encoded.items():
        print(f"{name}: {data['hex']} (Length: {data['length']} bytes)")

    # Japanese Pokémon names
    jap_converter = PokemonNameConverter("japanese")
    jap_pokemon = ["ピカチュウ", "リザードン", "ミュウツー", "イーブイ"]

    jap_encoded = jap_converter.encode_names(jap_pokemon)

    print("\nJapanese Pokémon Names:")
    for name, data in jap_encoded.items():
        print(f"{name}: {data['hex']} (Length: {data['length']} bytes)")

    # Verify decoding works correctly
    west_decoded = west_converter.decode_bytes(west_encoded)
    jap_decoded = jap_converter.decode_bytes(jap_encoded)

    print("\nDecoding verification:")
    print(f"Western: {west_decoded}")
    print(f"Japanese: {jap_decoded}")
