#!/usr/bin/env python3
"""Excel Auto-Formatter — Style any CSV for professional spreadsheets."""
import sys, csv, os

THEMES = {
    'dark': {'header_bg': '#1a1a2e', 'header_fg': '#ffffff', 'row_even': '#f8f9fa', 'row_odd': '#ffffff', 'border': '#e0e0e0'},
    'blue': {'header_bg': '#0a84ff', 'header_fg': '#ffffff', 'row_even': '#e8f4fd', 'row_odd': '#ffffff', 'border': '#cce4f7'},
    'green': {'header_bg': '#30d158', 'header_fg': '#ffffff', 'row_even': '#e8f8ed', 'row_odd': '#ffffff', 'border': '#c8e8d0'},
    'minimal': {'header_bg': '#f0f0f0', 'header_fg': '#333333', 'row_even': '#ffffff', 'row_odd': '#ffffff', 'border': '#e0e0e0'},
}

def format_csv(input_path, theme_name='dark', output_path=None):
    theme = THEMES.get(theme_name, THEMES['dark'])
    with open(input_path, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = list(reader)
    
    name = os.path.basename(input_path)
    html = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>""" + name + """</title>
<style>
body{font-family:-apple-system,system-ui,sans-serif;margin:20px}
table{border-collapse:collapse;width:100%}
th{background:""" + theme['header_bg'] + """;color:""" + theme['header_fg'] + """;padding:12px 16px;text-align:left;font-weight:600;font-size:13px;text-transform:uppercase}
td{padding:10px 16px;border-bottom:1px solid """ + theme['border'] + """;font-size:14px}
tr:nth-child(even) td{background:""" + theme['row_even'] + """}
tr:nth-child(odd) td{background:""" + theme['row_odd'] + """}
tr:hover td{background:#fff3cd}
.number{text-align:right;font-variant-numeric:tabular-nums}
</style></head><body>
<h2>""" + name + """</h2>
<table>
<tr>""" + "".join("<th>" + h + "</th>" for h in headers) + """</tr>
"""
    for row in rows:
        html += "<tr>" + "".join(
            '<td class="number">' + v + '</td>' if v.replace(",","").replace(".","").replace("-","").isdigit() else '<td>' + v + '</td>'
            for v in row
        ) + "</tr>\n"
    html += "</table></body></html>"
    
    out = output_path or input_path.replace('.csv', '_formatted.html')
    with open(out, 'w') as f:
        f.write(html)
    
    csv_out = input_path.replace('.csv', '_clean.csv')
    with open(csv_out, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in rows:
            writer.writerow([v.strip().replace('  ', ' ') for v in row])
    
    print(f"HTML: {out}")
    print(f"CSV: {csv_out}")
    return out

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Excel Auto-Formatter")
        print("  python3 format.py data.csv --theme dark|blue|green|minimal")
        sys.exit(0)
    theme = 'dark'
    if '--theme' in sys.argv:
        idx = sys.argv.index('--theme')
        theme = sys.argv[idx+1] if idx+1 < len(sys.argv) else 'dark'
    format_csv(sys.argv[1], theme)
