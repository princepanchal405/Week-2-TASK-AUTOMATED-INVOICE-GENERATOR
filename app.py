from flask import Flask, render_template, request, send_file
import sqlite3
import os
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

app = Flask(__name__)

# Create invoices folder if not exists
if not os.path.exists('invoices'):
    os.makedirs('invoices')

# Database table creation with automatic 'filename' column check
def create_table():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    # Create table if not exists (initial structure without filename)
    cur.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            customer_email TEXT,
            item TEXT,
            quantity INTEGER,
            price REAL,
            total REAL,
            date TEXT
        )
    ''')
    # Check if 'filename' column exists
    cur.execute("PRAGMA table_info(invoices)")
    columns = [col[1] for col in cur.fetchall()]
    if 'filename' not in columns:
        cur.execute("ALTER TABLE invoices ADD COLUMN filename TEXT")
    conn.commit()
    conn.close()

create_table()

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Professional PDF generation
def generate_pdf(data, filename):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Company Header
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 50, "MY COMPANY NAME")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 70, "Email: info@company.com | Phone: 123-456-7890")

    # Invoice Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(220, height - 120, "INVOICE")

    # Customer Info
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 160, "Bill To:")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 180, f"Name: {data['customer_name']}")
    c.drawString(50, height - 200, f"Email: {data['customer_email']}")
    c.drawString(50, height - 220, f"Date: {data['date']}")

    # Invoice Table
    table_data = [
        ["Item", "Quantity", "Unit Price", "Total"],
        [data['item'], str(data['quantity']), f"${data['price']:.2f}", f"${data['total']:.2f}"]
    ]

    table = Table(table_data, colWidths=[200, 80, 80, 80])
    style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('ALIGN', (1,1), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
    ])
    table.setStyle(style)
    table.wrapOn(c, width, height)
    table.drawOn(c, 50, height - 320)

    # Total Amount
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 370, f"Total Amount: ${data['total']:.2f}")

    # Footer
    c.setFont("Helvetica-Oblique", 12)
    c.drawString(50, height - 420, "Thank you for your business!")

    c.save()

# Create invoice
@app.route('/create_invoice', methods=['POST'])
def create_invoice():
    customer_name = request.form['customer_name']
    customer_email = request.form['customer_email']
    item = request.form['item']
    quantity = int(request.form['quantity'])
    price = float(request.form['price'])
    total = quantity * price
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    filename = f"invoices/invoice_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"

    # Save to database
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO invoices (customer_name, customer_email, item, quantity, price, total, date, filename)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (customer_name, customer_email, item, quantity, price, total, date, filename))
    conn.commit()
    conn.close()

    # Generate PDF
    generate_pdf({
        'customer_name': customer_name,
        'customer_email': customer_email,
        'item': item,
        'quantity': quantity,
        'price': price,
        'total': total,
        'date': date
    }, filename)

    return send_file(filename, as_attachment=True)

# History page
@app.route('/history')
def history():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM invoices ORDER BY id DESC")
    invoices = cur.fetchall()
    conn.close()
    return render_template('history.html', invoices=invoices)

# PDF download route
@app.route('/download/<filename>')
def download_file(filename):
    path = os.path.join('invoices', filename)
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
