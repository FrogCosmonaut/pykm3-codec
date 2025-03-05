### Running the Benchmark

```bash
# Run benchmark with default settings (1000 iterations)
python benchmark.py

# Run with custom number of iterations
python benchmark.py --iterations 5000

# Save results to a specific file
python benchmark.py --output my_results.json

# Generate an HTML report
python benchmark.py --html
```

### Benchmark Results

The benchmark measures the performance of both Western and Japanese codecs for encoding and decoding operations. Results include:
- Mean execution time
- Median execution time
- Minimum execution time
- Maximum execution time
- Standard deviation

### GitHub Actions Integration

The benchmark automatically runs on GitHub Actions for each push to the main branch and for pull requests. You can also trigger it manually from the Actions tab.

To view the results:
1. Go to the Actions tab in the repository
2. Select the "Performance Benchmark" workflow run
3. Download the "benchmark-results" artifact
4. Open the HTML report to view the charts and detailed metrics