from flask import Flask, render_template_string, request, redirect, url_for
import xml.etree.ElementTree as ET
from pathlib import Path

app = Flask(__name__)
BASE = Path(__file__).resolve().parent.parent
DB_PATH = BASE / "database.xml"

# helper to load XML root
def load_root():
    if not DB_PATH.exists():
        # create empty structure if missing
        root = ET.Element('books')
        tree = ET.ElementTree(root)
        tree.write(DB_PATH, encoding='utf-8', xml_declaration=True)
    tree = ET.parse(DB_PATH)
    return tree, tree.getroot()

@app.route('/')
def index():
    tree, root = load_root()
    books = []
    for b in root.findall('book'):
        books.append({
            'id': b.find('id').text if b.find('id') is not None else '',
            'title': b.find('title').text if b.find('title') is not None else '',
            'price': b.find('price').text if b.find('price') is not None else ''
        })
    html = """
    <h2>Website 2 - Admin</h2>
    <p><a href="http://127.0.0.1:5000/">Open Website 1 (view)</a></p>
    <h3>Add Book</h3>
    <form method="post" action="{{ url_for('add') }}">
      ID: <input name="id" required> &nbsp;
      Title: <input name="title" required> &nbsp;
      Price: <input name="price" required>
      <button type="submit">Add</button>
    </form>

    <h3>Update Book (by ID)</h3>
    <form method="post" action="{{ url_for('update') }}">
      ID: <input name="id" required> &nbsp;
      New Title: <input name="title"> &nbsp;
      New Price: <input name="price">
      <button type="submit">Update</button>
    </form>

    <h3>Delete Book (by ID)</h3>
    <form method="post" action="{{ url_for('delete') }}">
      ID: <input name="id" required>
      <button type="submit">Delete</button>
    </form>

    <h3>Current Books</h3>
    <table border="1" cellpadding="6" cellspacing="0">
      <tr><th>ID</th><th>Title</th><th>Price</th></tr>
      {% for b in books %}
        <tr><td>{{b.id}}</td><td>{{b.title}}</td><td>{{b.price}}</td></tr>
      {% endfor %}
    </table>
    """
    return render_template_string(html, books=books)

@app.route('/add', methods=['POST'])
def add():
    book_id = request.form.get('id').strip()
    title = request.form.get('title').strip()
    price = request.form.get('price').strip()

    tree, root = load_root()

    # check duplicate id
    for b in root.findall('book'):
        if b.find('id') is not None and b.find('id').text == book_id:
            return f"Book with ID {book_id} already exists. Use update instead.", 400

    new = ET.Element('book')
    id_el = ET.SubElement(new, 'id'); id_el.text = book_id
    title_el = ET.SubElement(new, 'title'); title_el.text = title
    price_el = ET.SubElement(new, 'price'); price_el.text = price
    root.append(new)
    tree.write(DB_PATH, encoding='utf-8', xml_declaration=True)
    return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update():
    book_id = request.form.get('id').strip()
    new_title = request.form.get('title')
    new_price = request.form.get('price')

    tree, root = load_root()
    found = False
    for b in root.findall('book'):
        id_el = b.find('id')
        if id_el is not None and id_el.text == book_id:
            found = True
            if new_title and new_title.strip():
                if b.find('title') is None:
                    ET.SubElement(b, 'title').text = new_title.strip()
                else:
                    b.find('title').text = new_title.strip()
            if new_price and new_price.strip():
                if b.find('price') is None:
                    ET.SubElement(b, 'price').text = new_price.strip()
                else:
                    b.find('price').text = new_price.strip()
            break

    if not found:
        return f"No book with ID {book_id} found.", 404

    tree.write(DB_PATH, encoding='utf-8', xml_declaration=True)
    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete():
    book_id = request.form.get('id').strip()
    tree, root = load_root()
    removed = False
    for b in root.findall('book'):
        id_el = b.find('id')
        if id_el is not None and id_el.text == book_id:
            root.remove(b)
            removed = True
            break

    if not removed:
        return f"No book with ID {book_id} found.", 404

    tree.write(DB_PATH, encoding='utf-8', xml_declaration=True)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
