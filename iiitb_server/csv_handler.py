import csv
import os

CSV_FILE = "database/data.csv"

def init_csv(csv_file=CSV_FILE):
    """Ensure the CSV file exists with a header."""
    if not os.path.exists(csv_file):
        with open(csv_file, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["timestamp", "description"])

def append_to_csv(timestamp, description, csv_file=CSV_FILE):
    """Append a row with the given timestamp and description to the CSV file."""
    try:
        with open(csv_file, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([timestamp, description])
    except Exception as e:
        raise Exception(f"Error writing to CSV: {e}")
