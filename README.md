Automated Invoice Generator

A Flask-based web application to generate professional PDF invoices instantly. Users can input customer information and product details to create downloadable invoices. All invoices are stored in a SQLite database, and a history page allows users to view and download previous invoices.

Features

Create professional PDF invoices with customer info, table of items, totals, and footer.

Automatically save all invoices in SQLite database.

Download invoices as PDF files.

Invoice history page to view all previously generated invoices.

Responsive and user-friendly UI with Bootstrap-like styling.

Sticky footer and clean layout.

Supports single item per invoice, easily extendable for multiple items.

Technologies

Python 3

Flask (Web Framework)

SQLite (Database)

ReportLab (PDF Generation)

HTML/CSS (Responsive Design)

Usage

Clone the repository:

git clone <your-repo-url>


Install dependencies:

pip install flask reportlab


Run the app:

python app.py


Open http://127.0.0.1:5000/ in your browser to start generating invoices.
