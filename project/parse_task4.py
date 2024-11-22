import csv
import sys

# Ensure NB_WORKERS is passed as an argument
if len(sys.argv) != 2:
    print("Usage: python parse_task4.py <NB_WORKERS>")
    sys.exit(1)

# Get NB_WORKERS from command-line arguments
nb_workers = sys.argv[1]

input_file = 'output.txt'
output_file = 'output.csv'

metrics = [
    'task-clock', 'cycles', 'instructions', 'branches', 
    'branch-misses', 'L1-dcache-loads', 'L1-dcache-load-misses', 'stalled-cycles-frontend'
]

def parse_line(line):
    parts = line.split('#')
    if len(parts) == 2:
        metric_part, _ = parts
        metric_parts = metric_part.split()
        value = metric_parts[0].replace('.', '').replace(',', '.')
        unit = metric_parts[1]
        metric = ' '.join(metric_parts[2:])
        return value, metric, unit
    return None

with open(input_file, 'r') as infile:
    lines = infile.readlines()

data_lines = [line for line in lines if any(metric in line for metric in metrics) and "stalled cycles" not in line]

csv_headers = ['NB_WORKERS']
csv_data = [nb_workers]

for line in data_lines:
    parsed_data = parse_line(line)
    if parsed_data:
        value, metric, unit = parsed_data
        csv_headers.append(f"{metric} ({unit})")
        csv_data.append(value) 

with open(output_file, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(csv_headers)
    csvwriter.writerow(csv_data)

print(f"Data has been written to {output_file}")
