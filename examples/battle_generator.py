import random

import pykm3_codec

pykm3_codec.register()


class BattleMessageFormatter:
    """Utility for formatting and encoding Pokémon battle messages."""

    # Templates for various battle messages
    TEMPLATES = {
        "attack": ["{pokemon} used {move}!", "{trainer}'s {pokemon} used {move}!"],
        "critical": ["A critical hit!", "It's super effective!"],
        "miss": ["{pokemon}'s attack missed!", "But it failed!"],
        "status": ["{pokemon} was {status}!", "{trainer}'s {pokemon} was {status}!"],
        "faint": ["{pokemon} fainted!", "{trainer}'s {pokemon} fainted!"],
        "exp": [
            "{pokemon} gained {exp} EXP. Points!",
            "{trainer}'s {pokemon} grew to LV. {level}!",
        ],
    }

    # Status conditions
    STATUS_CONDITIONS = [
        "paralyzed",
        "poisoned",
        "badly poisoned",
        "burned",
        "frozen",
        "put to sleep",
    ]

    def __init__(self, language="western"):
        """Initialize with the appropriate codec."""
        self.encoding = "pykm3" if language.lower() == "western" else "pykm3jap"

    def format_message(self, message_type, **kwargs):
        """Format a battle message using templates and parameters."""
        if message_type not in self.TEMPLATES:
            raise ValueError(f"Unknown message type: {message_type}")

        # Handle special cases
        if message_type == "status" and "status" not in kwargs:
            kwargs["status"] = random.choice(self.STATUS_CONDITIONS)

        # Select a template that can be satisfied with the provided kwargs
        # For templates that may need a trainer, select appropriate template based on whether trainer is provided
        templates = self.TEMPLATES[message_type]
        if "trainer" not in kwargs:
            # Filter templates that don't require a trainer parameter
            valid_templates = [t for t in templates if "{trainer}" not in t]
            if not valid_templates:
                raise ValueError(
                    f"No valid template found for {message_type} without 'trainer' parameter"
                )
            template = random.choice(valid_templates)
        else:
            template = random.choice(templates)

        # Format the message
        try:
            formatted = template.format(**kwargs)
            return formatted
        except KeyError as e:
            raise ValueError(f"Missing parameter {e} for template: {template}")

    def encode_message(self, message):
        """Encode a battle message using the appropriate codec."""
        encoded = message.encode(self.encoding)
        return {
            "message": message,
            "encoded": encoded,
            "hex": encoded.hex(" "),
            "length": len(encoded) - 1,  # Subtract 1 for terminator
        }

    def generate_battle_sequence(
        self,
        player_pokemon,
        enemy_pokemon,
        enemy_trainer=None,
        player_move=None,
        enemy_move=None,
    ):
        """Generate a sequence of battle messages."""
        sequence = []

        # If moves not provided, use placeholders
        if not player_move:
            player_move = "TACKLE"
        if not enemy_move:
            enemy_move = "TACKLE"

        # Player attack
        attack_msg = self.format_message(
            "attack", pokemon=player_pokemon, move=player_move
        )
        sequence.append(self.encode_message(attack_msg))

        # Critical hit (50% chance)
        if random.random() > 0.5:
            crit_msg = self.format_message("critical")
            sequence.append(self.encode_message(crit_msg))

        # Enemy attack
        attack_kwargs = {"pokemon": enemy_pokemon, "move": enemy_move}
        if enemy_trainer:
            attack_kwargs["trainer"] = enemy_trainer
        else:
            attack_kwargs["pokemon"] = f"Wild {enemy_pokemon}"

        enemy_attack_msg = self.format_message("attack", **attack_kwargs)
        sequence.append(self.encode_message(enemy_attack_msg))

        # Miss (30% chance)
        if random.random() > 0.7:
            miss_msg = self.format_message("miss", pokemon=enemy_pokemon)
            sequence.append(self.encode_message(miss_msg))

        # Status effect (40% chance)
        if random.random() > 0.6:
            status_kwargs = {"pokemon": enemy_pokemon}
            if enemy_trainer:
                status_kwargs["trainer"] = enemy_trainer
            else:
                status_kwargs["pokemon"] = f"Wild {enemy_pokemon}"

            status_msg = self.format_message("status", **status_kwargs)
            sequence.append(self.encode_message(status_msg))

        # Faint message (20% chance)
        if random.random() > 0.8:
            faint_kwargs = {"pokemon": enemy_pokemon}
            if enemy_trainer:
                faint_kwargs["trainer"] = enemy_trainer
            else:
                faint_kwargs["pokemon"] = f"Wild {enemy_pokemon}"

            faint_msg = self.format_message("faint", **faint_kwargs)
            sequence.append(self.encode_message(faint_msg))

            # Experience points
            exp = random.randint(50, 150)
            exp_msg = self.format_message(
                "exp", pokemon=player_pokemon, exp=exp, level=random.randint(5, 35)
            )
            sequence.append(self.encode_message(exp_msg))

        return sequence


# Example usage
if __name__ == "__main__":
    formatter = BattleMessageFormatter()

    sequence = formatter.generate_battle_sequence(
        player_pokemon="PIKACHU",
        enemy_pokemon="GEODUDE",
        enemy_trainer="BROCK",
        player_move="THUNDERBOLT",
        enemy_move="ROCK THROW",
    )

    print("Battle Sequence:")
    print("-" * 50)

    for i, message in enumerate(sequence):
        print(f"{i+1}. {message['message']}")
        print(f"   Hex: {message['hex']}")
        print(f"   Length: {message['length']} bytes")
        print()

    print("Wild Battle Example:")
    print("-" * 50)

    wild_sequence = formatter.generate_battle_sequence(
        player_pokemon="PIKACHU",
        enemy_pokemon="RATTATA",
        player_move="THUNDERSHOCK",
        enemy_move="TACKLE",
    )

    for i, message in enumerate(wild_sequence):
        print(f"{i+1}. {message['message']}")
        print(f"   Hex: {message['hex']}")
        print()

    print("Individual Message Examples:")
    print("-" * 50)

    attack_msg = formatter.format_message(
        "attack", pokemon="CHARIZARD", move="FLAMETHROWER"
    )
    print(f"Attack: {attack_msg}")
    print(f"Encoded: {formatter.encode_message(attack_msg)['hex']}\n")

    crit_msg = formatter.format_message("critical")
    print(f"Critical: {crit_msg}")
    print(f"Encoded: {formatter.encode_message(crit_msg)['hex']}\n")

    status_msg = formatter.format_message(
        "status", pokemon="BULBASAUR", status="poisoned"
    )
    print(f"Status: {status_msg}")
    print(f"Encoded: {formatter.encode_message(status_msg)['hex']}")
