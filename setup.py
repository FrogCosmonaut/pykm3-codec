from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pykm3-codec",
    version="0.1.0",
    author="Juan Franco",
    author_email="pykm3-codec@juanfg.es",
    description="Pokémon Generation III Text Codec",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FrogCosmonaut/pykm3-codec",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Games/Entertainment",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    keywords="pokemon, codec, game, text, encoding, decoding, rom, hack",
)