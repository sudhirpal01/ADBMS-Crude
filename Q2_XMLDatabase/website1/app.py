from flask import Flask, render_template_string
import xml.etree.ElementTree as ET
from pathlib import Path

app = Flask(__name__)

BASE = Path(__file__).resolve().parent.parent
DB_PATH = BASE / "database.xml"

@app.route('/')
def home():
    if not DB_PATH.exists():
        return f"Database file not found: {DB_PATH}", 500

    tree = ET.parse(DB_PATH)
    root = tree.getroot()
    books = []
    for b in root.findall('book'):
        books.append({
            'id': b.find('id').text if b.find('id') is not None else '',
            'title': b.find('title').text if b.find('title') is not None else '',
            'price': b.find('price').text if b.find('price') is not None else ''
        })

    html = """
    <h2>📘 Website 1 - Book List</h2>
    <table border="1" cellpadding="6" cellspacing="0">
      <tr><th>ID</th><th>Title</th><th>Price (Rs)</th></tr>
      {% for book in books %}
        <tr>
          <td>{{book.id}}</td>
          <td>{{book.title}}</td>
          <td>{{book.price}}</td>
        </tr>
      {% endfor %}
    </table>
    <p><a href="http://127.0.0.1:5001/">Open Website 2 (admin)</a></p>
    """
    return render_template_string(html, books=books)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
