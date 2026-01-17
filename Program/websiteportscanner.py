from flask import Flask, request, render_template_string
import socket
app = Flask(__name__)
page = '''<!DOCTYPE html>
<html>
<head>
<title>Port Scanner</title>
<style>
body { font-family: Arial; background: white; color: black; padding: 40px }
input, button { padding: 8px; margin: 5px }
table { border-collapse: collapse; margin-top: 20px }
td, th { border: 1px solid black; padding: 6px }
</style>
</head>
<body>
<h1>Web Port Scanner</h1>
<p>Scan only hosts you own or have permission to test.</p>
<form method="post">
<input type="text" name="host" placeholder="Target host" required>
<input type="number" name="start" placeholder="Start port" required>
<input type="number" name="end" placeholder="End port" required>
<button type="submit">Scan</button>
</form>
{% if results %}
<table>
<tr><th>Port</th><th>Status</th></tr>
{% for port, status in results %}
<tr><td>{{ port }}</td><td>{{ status }}</td></tr>
{% endfor %}
</table>
{% endif %}
</body>
</html>'''

def scan(host, start, end):
    output = []
    for port in range(start, end + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        try:
            s.connect((host, port))
            output.append((port, "Open"))
        except:
            output.append((port, "Closed"))
        s.close()
    return output

@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    if request.method == "POST":
        host = request.form.get("host")
        start = int(request.form.get("start"))
        end = int(request.form.get("end"))
        results = scan(host, start, end)
    return render_template_string(page, results=results)

app.run()
