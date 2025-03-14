import timeit as ti
from typing import Union, List
import pykm3_codec
from pykm3_codec import WesternPokeTextCodec, JapanesePokeTextCodec

pykm3_codec.register()
west_codec = WesternPokeTextCodec()
jap_codec = JapanesePokeTextCodec()


def test_encode_with_codec(
    codec: Union[WesternPokeTextCodec, JapanesePokeTextCodec], text: str
) -> None:
    codec.encode(text)


def test_encode_with_register(text: str, codec: str) -> None:
    text.encode(codec)


def run_benchmark(func: callable, iterations: int, runs: int = 3) -> float:
    """Run a benchmark multiple times and return the best time"""
    times = []
    for _ in range(runs):
        times.append(ti.timeit(func, number=iterations))
        print(".", end="", flush=True)
    return min(times)


def format_time(seconds: float, iterations: int) -> str:
    ns_per_op = (seconds / iterations) * 1_000_000_000
    if ns_per_op < 1000:
        return f"{ns_per_op:.2f} ns/op"
    else:
        return f"{ns_per_op/1000:.2f} μs/op"


def print_table(headers: List[str], rows: List[List[str]]) -> None:
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    row_template = "│ " + " │ ".join(["{:<" + str(w) + "}" for w in col_widths]) + " │"
    divider = "─┼─".join(["─" * w for w in col_widths])

    print("┌─" + divider.replace("┼", "┬") + "─┐")
    print(row_template.format(*headers))
    print("├─" + divider + "─┤")
    for row in rows:
        print(row_template.format(*row))
    print("└─" + divider.replace("┼", "┴") + "─┘")


west_text = "Hello trainer!"
jap_text = "こんにちは．トレーナー！"

iterations = [5, 50, 500, 5_000, 50_000, 500_000, 1_000_000]
max_width = len(f"{max(iterations):,}")

results = []

for i in iterations:
    print(f"Running {i:<{max_width},} iterations", end=" ", flush=True)

    wc_time = run_benchmark(lambda: test_encode_with_codec(west_codec, west_text), i)
    wr_time = run_benchmark(lambda: test_encode_with_register(west_text, "pykm3"), i)
    jc_time = run_benchmark(lambda: test_encode_with_codec(jap_codec, jap_text), i)
    jr_time = run_benchmark(lambda: test_encode_with_register(jap_text, "pykm3jap"), i)

    results.append(
        [
            f"{i:,}",
            format_time(wc_time, i),
            format_time(wr_time, i),
            f"{wr_time/wc_time:.2f}x",
            format_time(jc_time, i),
            format_time(jr_time, i),
            f"{jr_time/jc_time:.2f}x",
        ]
    )

    print(" ✔️")

width = 95
title = "😜  RESULTS  🥵"
print("\n" + "╔" + "═" * (width - 2) + "╗")
print("║" + title.center(width - 4) + "║")
print("╚" + "═" * (width - 2) + "╝")

headers = [
    "Iterations",
    "West Direct",
    "West Register",
    "Speedup",
    "Jap Direct",
    "Jap Register",
    "Speedup",
]

print_table(headers, results)
