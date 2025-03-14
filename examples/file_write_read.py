import codecs
import pykm3_codec

pykm3_codec.register()

# Write game script to a file
with codecs.open("script.bin", "w", "pykm3") as f:
    f.write("PROF. OAK: Hello there!\nWelcome to the world of POKéMON!")

# Read game script from a file
with codecs.open("script.bin", "r", "pykm3") as f:
    content = f.read()


# Write game script to a file in japanese
with codecs.open("jap_script.bin", "w", "pykm3jap") as f:
    f.write("ユンゲラー　ハ　サイコキネシス　ヲ　ツカッタ！")

# Read game script from a file in japanese
with codecs.open("jap_script.bin", "r", "pykm3jap") as f:
    content = f.read()
