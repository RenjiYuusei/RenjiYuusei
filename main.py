from flask import Flask, request, render_template_string, abort
import os
import argparse

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Viewer</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f4f4f4;
        }
        h1 {
            color: #333;
        }
        form {
            margin-bottom: 20px;
        }
        input[type="text"] {
            width: 300px;
            padding: 5px;
        }
        button {
            padding: 5px 10px;
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        pre {
            background-color: #fff;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 10px;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        .error {
            color: red;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            margin-bottom: 5px;
        }
    </style>
</head>
<body>
    <h1>File Viewer</h1>
    <form method="post">
        <label for="filename">Enter file path:</label>
        <input type="text" id="filename" name="filename" value="{{ current_path }}" required>
        <button type="submit">View File</button>
    </form>
    {% if files %}
        <h2>Files in current directory:</h2>
        <ul>
        {% for file in files %}
            <li><a href="?filename={{ current_path }}/{{ file }}">{{ file }}</a></li>
        {% endfor %}
        </ul>
    {% endif %}
    {% if content %}
        <h2>File Content:</h2>
        <pre>{{ content }}</pre>
    {% endif %}
    {% if error %}
        <p class="error">{{ error }}</p>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def view_file():
    content = ''
    error = ''
    files = []
    current_path = os.getcwd()

    if request.method == 'POST':
        filename = request.form['filename']
    else:
        filename = request.args.get('filename', current_path)

    try:
        if os.path.isdir(filename):
            current_path = filename
            files = [f for f in os.listdir(current_path) if not f.startswith('.')]
        elif os.path.isfile(filename):
            with open(filename, 'r') as file:
                content = file.read()
            current_path = os.path.dirname(filename)
        else:
            error = "Path not found."
    except Exception as e:
        error = f"Error: {str(e)}"

    return render_template_string(HTML_TEMPLATE, content=content, error=error, files=files, current_path=current_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="File Viewer Web App")
    parser.add_argument('-p', '--port', type=int, default=5000, help="Port to run the server on")
    args = parser.parse_args()

    app.run(debug=True, port=args.port)