import os
import json
import time
import statistics
import argparse
from typing import Dict, List, Any
import pykm3_codec

def generate_test_data() -> Dict[str, List[str]]:
    """Generate test data for benchmarking."""
    return {
        "western": [
            "HELLO WORLD!" * 10,
            "The quick brown fox jumps over the lazy dog." * 5,
            "PIKACHU used THUNDERBOLT! It's super effective!" * 8,
            "POKéMON FireRed and LeafGreen are remakes of the original games." * 3,
            "PROF. OAK: Welcome to the world of POKéMON!" * 12
        ],
        "japanese": [
            "こんにちは、せかい！" * 10,  # Hello, world!
            "ピカチュウの　１０まんボルト！　ばつぐんだ！" * 8,  # Pikachu's 10 million volts! It's super effective!
            "ポケットモンスター　ファイアレッド・リーフグリーン" * 5,  # Pocket Monsters FireRed/LeafGreen
            "オーキド：　ポケモンの　せかいへ　ようこそ！" * 12,  # Prof. Oak: Welcome to the world of Pokémon!
            "ふしぎな　いきもの　ポケモンの　せかい" * 7  # The world of the mysterious creatures Pokémon
        ]
    }

def run_benchmark(iterations: int = 1000) -> Dict[str, Dict[str, Any]]:
    """
    Run benchmark tests for both Western and Japanese codecs.
    
    Args:
        iterations: Number of iterations for each test
        
    Returns:
        Dictionary with benchmark results
    """
    test_data = generate_test_data()
    results = {
        "western": {"encode": [], "decode": []},
        "japanese": {"encode": [], "decode": []}
    }
    
    western_codec = pykm3_codec.WesternPokeTextCodec()
    japanese_codec = pykm3_codec.JapanesePokeTextCodec()
    
    # WESTERN
    print("Benchmarking Western codec...")
    for text in test_data["western"]:
        # encoding
        start = time.perf_counter()
        for _ in range(iterations):
            encoded = western_codec.encode(text)
        end = time.perf_counter()
        results["western"]["encode"].append((end - start) / iterations)
        
        # decoding
        start = time.perf_counter()
        for _ in range(iterations):
            western_codec.decode(encoded)
        end = time.perf_counter()
        results["western"]["decode"].append((end - start) / iterations)
    
    # JAPANESE
    print("Benchmarking Japanese codec...")
    for text in test_data["japanese"]:
        # encoding
        start = time.perf_counter()
        for _ in range(iterations):
            encoded = japanese_codec.encode(text)
        end = time.perf_counter()
        results["japanese"]["encode"].append((end - start) / iterations)
        
        # decoding
        start = time.perf_counter()
        for _ in range(iterations):
            japanese_codec.decode(encoded)
        end = time.perf_counter()
        results["japanese"]["decode"].append((end - start) / iterations)
    
    return results

def calculate_stats(results: Dict[str, Dict[str, List[float]]]) -> Dict[str, Dict[str, Dict[str, float]]]:
    """Calculate statistics from benchmark results."""
    stats = {
        "western": {"encode": {}, "decode": {}},
        "japanese": {"encode": {}, "decode": {}}
    }
    
    for codec in ["western", "japanese"]:
        for operation in ["encode", "decode"]:
            times = results[codec][operation]
            stats[codec][operation] = {
                "mean": statistics.mean(times) * 1000, # to ms
                "median": statistics.median(times) * 1000,
                "min": min(times) * 1000,
                "max": max(times) * 1000,
                "stdev": statistics.stdev(times) * 1000 if len(times) > 1 else 0
            }
    
    return stats

def print_results(stats: Dict[str, Dict[str, Dict[str, float]]]) -> None:
    """Print benchmark results in a formatted table."""
    print("\n=== BENCHMARK RESULTS (times in milliseconds) ===\n")
    print(f"{'Codec':<10} | {'Operation':<10} | {'Mean':>10} | {'Median':>10} | {'Min':>10} | {'Max':>10} | {'StdDev':>10}")
    print("-" * 80)
    
    for codec in ["western", "japanese"]:
        for operation in ["encode", "decode"]:
            s = stats[codec][operation]
            print(f"{codec:<10} | {operation:<10} | {s['mean']:>10.6f} | {s['median']:>10.6f} | "
                  f"{s['min']:>10.6f} | {s['max']:>10.6f} | {s['stdev']:>10.6f}")
    
    print("\n")

def main():
    """Main function to run the benchmark."""
    parser = argparse.ArgumentParser(description="Benchmark for pykm3_codec")
    parser.add_argument("-i", "--iterations", type=int, default=5000)
    parser.add_argument("-o", "--output", type=str, default="benchmark/reports/benchmark_results.json")
    parser.add_argument("--html", action="store_true", default=True)
    args = parser.parse_args()
    
    print(f"Running benchmark with {args.iterations} iterations per test...")
    results = run_benchmark(args.iterations)
    stats = calculate_stats(results)
    print_results(stats)
    
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(args.output, "w") as f:
        json.dump(stats, f, indent=2)
    print(f"Results saved to {args.output}")
    
    if args.html:
        try:
            import benchmark_report
            benchmark_report.generate_html_report(stats)
            print("HTML report generated")
        except ImportError:
            print("Could not import benchmark_report.py. Make sure it exists in the current directory.")

if __name__ == "__main__":
    main()