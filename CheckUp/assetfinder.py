import argparse
import subprocess

parser = argparse.ArgumentParser(description='Scan a list of domains with assetfinder')
parser.add_argument("-i", "--input", required=True, type=str, help='Input file containing list of domains')
parser.add_argument("-o", "--output", required=True, type=str, help='Output file for assetfinder results')

args = parser.parse_args()

file_input = args.input
file_output = args.output

with open(file_input, 'r') as f:
    domains = f.read().splitlines()

results = set()
for domain in domains:
    cmd = f'assetfinder {domain}'
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if proc.stdout:
        print(proc.stdout)
        results.update(proc.stdout.splitlines())

with open(file_output, 'w') as f:
    f.write('\n'.join(results))
