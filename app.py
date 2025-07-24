from flask import Flask, request, render_template, send_file
from scanner import scan_website

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    message_type = ''
    results = ''

    if request.method == 'POST':
        url = request.form['url'].strip()
        if not url.startswith('http'):
            message = "❌ Please enter a valid URL with http:// or https://"
            message_type = "error"
        else:
            try:
                results = scan_website(url)
                message = "✅ Scan completed successfully!"
                message_type = "success"
            except Exception as e:
                message = f"❌ Error during scanning: {str(e)}"
                message_type = "error"

    return render_template('index.html',
                           message=message,
                           message_type=message_type,
                           results=results)

@app.route('/download/<filetype>')
def download(filetype):
    if filetype == "html":
        return send_file("report.html", as_attachment=True)
    elif filetype == "pdf":
        return send_file("report.pdf", as_attachment=True)
    else:
        return "❌ Invalid file type."

if __name__ == '__main__':
    app.run(debug=True)
