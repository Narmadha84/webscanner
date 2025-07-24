from xhtml2pdf import pisa
from datetime import datetime

def generate_html_report(results, output_html="report.html"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html_content = f"""<!DOCTYPE html>
<html>
<head><title>Scan Report</title>
<style>
body {{font-family: Arial; padding:20px;}}
h1 {{color:#333;}}
pre {{background:#f4f4f4; padding:15px; border:1px solid #ccc;}}
</style></head>
<body>
<h1>Web Vulnerability Scan Report</h1>
<p><strong>Date:</strong> {now}</p>
<h2>Results:</h2><pre>{results}</pre>
</body></html>"""

    with open(output_html, "w") as f:
        f.write(html_content)
    print(f"[+] HTML report saved: {output_html}")
    return html_content

def convert_html_to_pdf(html_content, pdf_file="report.pdf"):
    try:
        with open(pdf_file, "wb") as f:
            pisa.CreatePDF(html_content, dest=f)
        print(f"[+] PDF report saved: {pdf_file}")
    except Exception as e:
        print(f"[!] PDF generation failed: {e}")
