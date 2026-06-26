#!/usr/bin/env python3
"""Excel Formatter — Free Lite Edition. Style your CSV for professional spreadsheets."""
import csv, sys

def format_csv(filepath):
    with open(filepath, newline='') as f:
        reader = csv.reader(f)
        headers = next(reader, [])
        rows = list(reader)
    
    out = filepath.replace('.csv', '_formatted.csv')
    with open(out, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        for row in rows:
            formatted = []
            for cell in row:
                # Auto-format numbers
                try:
                    num = float(cell.replace('$','').replace(',','').replace('%',''))
                    formatted.append(f"{num:,.2f}")
                except:
                    formatted.append(cell.strip())
            writer.writerow(formatted)
    
    print(f"Formatted: {out}")
    print(f"Rows: {len(rows)} | Columns: {len(headers)}")
    print(f"\nNeed advanced styling? Full Excel Formatter: https://payhip.com/DataCrafted")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 format_lite.py data.csv")
        sys.exit(0)
    format_csv(sys.argv[1])
