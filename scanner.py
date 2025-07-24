import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from report_generator import generate_html_report, convert_html_to_pdf

# ---------------------------------------
# XSS Scanner
# ---------------------------------------
def scan_xss(url):
    print(f"[+] Scanning for XSS: {url}")
    payload = "<script>alert('XSS')</script>"
    try:
        res = requests.get(url)
        soup = bs(res.text, "html.parser")
        forms = soup.find_all("form")

        for i, form in enumerate(forms):
            action = form.get("action")
            method = form.get("method", "get").lower()
            target = urljoin(url, action)
            data = {}

            for input_tag in form.find_all("input"):
                name = input_tag.get("name")
                if name:
                    data[name] = payload if input_tag.get("type") != "submit" else "test"

            if method == "post":
                r = requests.post(target, data=data)
            else:
                r = requests.get(target, params=data)

            if payload in r.text:
                with open("scan_report.txt", "a") as f:
                    f.write(f"[XSS] Found at: {target}\nPayload: {payload}\n\n")
                print(f"[!!!] XSS vulnerability detected in form #{i+1}")
    except Exception as e:
        print(f"[XSS Error] {e}")

# ---------------------------------------
# SQL Injection Scanner
# ---------------------------------------
def scan_sqli(url):
    print(f"[+] Scanning for SQL Injection: {url}")
    payloads = [
        "' OR 1=1 --",
        "' OR '1'='1",
        "'; DROP TABLE users; --",
        "' UNION SELECT NULL --",
        "' OR 1=1#"
    ]

    try:
        res = requests.get(url)
        soup = bs(res.text, "html.parser")
        forms = soup.find_all("form")

        for i, form in enumerate(forms):
            action = form.get("action")
            method = form.get("method", "get").lower()
            target = urljoin(url, action)
            inputs = form.find_all("input")

            for payload in payloads:
                data = {}
                for input_tag in inputs:
                    name = input_tag.get("name")
                    if name:
                        data[name] = payload if input_tag.get("type") != "submit" else "test"

                if method == "post":
                    r = requests.post(target, data=data)
                else:
                    r = requests.get(target, params=data)

                if any(err in r.text.lower() for err in ["sql", "mysql", "syntax", "error", "warning"]):
                    with open("scan_report.txt", "a") as f:
                        f.write(f"[SQLi] Found at: {target}\nPayload: {payload}\n\n")
                    print(f"[!!!] SQL Injection detected with payload: {payload}")
    except Exception as e:
        print(f"[SQLi Error] {e}")

# ---------------------------------------
# CSRF Scanner
# ---------------------------------------
def scan_csrf(url):
    print(f"[+] Scanning for missing CSRF tokens: {url}")
    try:
        res = requests.get(url)
        soup = bs(res.text, "html.parser")
        forms = soup.find_all("form")

        for i, form in enumerate(forms):
            inputs = form.find_all("input")
            has_csrf = False

            for inp in inputs:
                name = inp.get("name", "").lower()
                if "csrf" in name or "token" in name:
                    has_csrf = True
                    break

            if not has_csrf:
                with open("scan_report.txt", "a") as f:
                    f.write(f"[CSRF] Missing token in form #{i+1} at {url}\n\n")
                print(f"[!!!] Form #{i+1} may be vulnerable to CSRF (no token found)")
    except Exception as e:
        print(f"[CSRF Error] {e}")

# ---------------------------------------
# Full Website Scanner + Report Generator
# ---------------------------------------
def scan_website(url):
    # Clear previous report
    open("scan_report.txt", "w").close()

    scan_xss(url)
    scan_sqli(url)
    scan_csrf(url)

    # Read results
    with open("scan_report.txt", "r") as f:
        results = f.read()

    # Generate reports
    html = generate_html_report(results)
    convert_html_to_pdf(html)

    return results
