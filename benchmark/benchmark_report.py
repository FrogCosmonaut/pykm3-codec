import json
import os
import argparse
from datetime import datetime
from typing import Dict

def generate_html_report(stats: Dict[str, Dict[str, Dict[str, float]]], 
                         output_file: str = "benchmark/reports/benchmark_report.html") -> None:
    """
    Generate an HTML report from benchmark statistics.
    
    Args:
        stats: Benchmark statistics
        output_file: Output HTML file path
    """
    # Generate HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>pykm3_codec Benchmark Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                line-height: 1.6;
            }}
            h1, h2 {{
                color: #333;
            }}
            .container {{
                max-width: 1000px;
                margin: 0 auto;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }}
            th, td {{
                padding: 8px;
                text-align: right;
                border: 1px solid #ddd;
            }}
            th {{
                background-color: #f2f2f2;
                font-weight: bold;
            }}
            tr:hover {{
                background-color: #f5f5f5;
            }}
            .header-row {{
                background-color: #e9e9e9;
            }}
            .chart-container {{
                width: 100%;
                height: 400px;
                margin: 20px 0;
            }}
        </style>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body>
        <div class="container">
            <h1>pykm3_codec Benchmark Report</h1>
            <p>Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            
            <h2>Results (times in milliseconds)</h2>
            <table>
                <tr class="header-row">
                    <th>Codec</th>
                    <th>Operation</th>
                    <th>Mean</th>
                    <th>Median</th>
                    <th>Min</th>
                    <th>Max</th>
                    <th>StdDev</th>
                </tr>
    """
    
    for codec in ["western", "japanese"]:
        for operation in ["encode", "decode"]:
            s = stats[codec][operation]
            html_content += f"""
                <tr>
                    <td>{codec}</td>
                    <td>{operation}</td>
                    <td>{s['mean']:.6f}</td>
                    <td>{s['median']:.6f}</td>
                    <td>{s['min']:.6f}</td>
                    <td>{s['max']:.6f}</td>
                    <td>{s['stdev']:.6f}</td>
                </tr>
            """
    
    html_content += """
            </table>
            
            <h2>Performance Comparison</h2>
            <div class="chart-container">
                <canvas id="performanceChart"></canvas>
            </div>

            <script>
                // Chart.js implementation
                const ctx = document.getElementById('performanceChart').getContext('2d');
                const performanceChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: ['Western Encode', 'Western Decode', 'Japanese Encode', 'Japanese Decode'],
                        datasets: [{
                            label: 'Mean Time (ms)',
                            data: [
    """
    
    # Add data points for the chart
    data_points = [
        stats['western']['encode']['mean'],
        stats['western']['decode']['mean'],
        stats['japanese']['encode']['mean'],
        stats['japanese']['decode']['mean']
    ]
    html_content += ", ".join([f"{dp:.6f}" for dp in data_points])
    
    html_content += """
                            ],
                            backgroundColor: [
                                'rgba(75, 192, 192, 0.5)',
                                'rgba(75, 192, 192, 0.8)',
                                'rgba(153, 102, 255, 0.5)',
                                'rgba(153, 102, 255, 0.8)'
                            ],
                            borderColor: [
                                'rgba(75, 192, 192, 1)',
                                'rgba(75, 192, 192, 1)',
                                'rgba(153, 102, 255, 1)',
                                'rgba(153, 102, 255, 1)'
                            ],
                            borderWidth: 1
                        }]
                    },
                    options: {
                        scales: {
                            y: {
                                beginAtZero: true,
                                title: {
                                    display: true,
                                    text: 'Milliseconds (lower is better)'
                                }
                            }
                        },
                        plugins: {
                            title: {
                                display: true,
                                text: 'Codec Performance Comparison'
                            }
                        }
                    }
                });
            </script>
        </div>
    </body>
    </html>
    """
    
    # Write to file
    with open(output_file, "w") as f:
        f.write(html_content)
    
    print(f"HTML report generated: {output_file}")

def main():
    """Main function to generate the HTML report."""
    parser = argparse.ArgumentParser(description="Generate HTML report from benchmark results")
    parser.add_argument("-i", "--input", type=str, default="benchmark/reports/benchmark_results.json")
    parser.add_argument("-o", "--output", type=str, default="benchmark/reports/benchmark_report.html")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file {args.input} not found")
        return
    
    with open(args.input, "r") as f:
        stats = json.load(f)
    
    generate_html_report(stats, args.output)

if __name__ == "__main__":
    main()