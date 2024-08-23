from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Viewer</title>
</head>
<body>
    <h1>File Viewer</h1>
    <form method="post">
        <label for="filename">Enter file path:</label>
        <input type="text" id="filename" name="filename" required>
        <button type="submit">View File</button>
    </form>
    {% if content %}
        <h2>File Content:</h2>
        <pre>{{ content }}</pre>
    {% endif %}
    {% if error %}
        <p style="color: red;">{{ error }}</p>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def view_file():
    content = ''
    error = ''
    if request.method == 'POST':
        filename = request.form['filename']
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as file:
                    content = file.read()
            except Exception as e:
                error = f"Error reading file: {str(e)}"
        else:
            error = "File not found."
    return render_template_string(HTML_TEMPLATE, content=content, error=error)

if __name__ == '__main__':
 app.run(debug=True)