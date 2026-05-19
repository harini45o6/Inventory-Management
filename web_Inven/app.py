from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, Response
import mysql.connector
from functools import wraps
from datetime import date, datetime

app = Flask(__name__)
app.secret_key = "shopstock_secret_key_change_in_prod"

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_HTTPONLY"] = True

VALID_USERS = {
    "admin": "admin123"
}

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Harini@2006",
    "database": "shopstock",
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

def log_activity(sku, name, action, qty_change, before, after, note):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            """INSERT INTO activity_log (sku, name, action, qty_change, stock_before, stock_after, note)
               VALUES (%s,%s,%s,%s,%s,%s,%s)""",
            (sku, name, action, int(qty_change), int(before), int(after), note)
        )
        db.commit()
        db.close()
        print(f"[LOG] {action} | {sku} | {before} -> {after}")
    except Exception as e:
        print(f"[LOG ERROR] {e}")

# ── AUTH ──────────────────────────────────────────────────────────────────────
@app.route("/", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect(url_for("dashboard"))

    error = None

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if VALID_USERS.get(username) == password:
            session["username"] = username
            session.permanent = False
            return redirect(url_for("dashboard"))

        error = "Invalid username or password."

    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ── DASHBOARD ─────────────────────────────────────────────────────────────────
@app.route("/dashboard")
@login_required
def dashboard():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS v FROM products")
    total_products = cursor.fetchone()["v"]

    cursor.execute("SELECT COALESCE(SUM(stock),0) AS v FROM products")
    total_units = int(cursor.fetchone()["v"])

    cursor.execute("SELECT COALESCE(SUM(price*stock),0) AS v FROM products")
    inventory_value = float(cursor.fetchone()["v"])

    cursor.execute("SELECT COUNT(*) AS v FROM products WHERE stock < 10")
    low_stock = cursor.fetchone()["v"]

    cursor.execute("SELECT COUNT(DISTINCT category) AS v FROM products")
    total_categories = cursor.fetchone()["v"]

    cursor.execute("""
        SELECT category,
               COUNT(*) AS product_count,
               SUM(stock) AS total_stock,
               ROUND(SUM(price*stock),2) AS total_value,
               ROUND(AVG(price),2) AS avg_price
        FROM products GROUP BY category ORDER BY total_value DESC
    """)
    categories = cursor.fetchall()

    cursor.execute("""
        SELECT sku, name, category, stock, price
        FROM products WHERE stock < 10 ORDER BY stock ASC LIMIT 8
    """)
    low_stock_items = cursor.fetchall()

    cursor.execute("""
        SELECT datetime, name, action, qty_change, stock_before, stock_after
        FROM activity_log ORDER BY id DESC LIMIT 2
    """)
    recent_activity = cursor.fetchall()

    cursor.execute("""
        SELECT name, sku, ROUND(price*stock,2) AS value, stock, price
        FROM products ORDER BY value DESC LIMIT 5
    """)
    top_products = cursor.fetchall()
    # In dashboard() route in app.py, add these queries before db.close():

    cursor.execute("""
        SELECT si.name, SUM(si.qty) AS total_qty, SUM(si.line_total) AS total_revenue
        FROM sale_items si
        JOIN sales s ON si.sale_id = s.id
        WHERE s.status = 'completed'
        GROUP BY si.name
        ORDER BY total_qty DESC
        LIMIT 8
    """)
    top_sold = cursor.fetchall()

    cursor.execute("""
    SELECT DATE(sale_date) AS day, COALESCE(SUM(total), 0) AS revenue
    FROM sales
    WHERE status = 'completed'
    GROUP BY DATE(sale_date)
    ORDER BY day DESC
    LIMIT 5
""")
    raw = cursor.fetchall()
    sales_last5 = list(reversed([
        {"day": str(r["day"]), "revenue": float(r["revenue"])}
    for r in raw
]))
    cursor.execute("""
    SELECT DATE(s.sale_date) AS day, COALESCE(SUM(s.total), 0) AS revenue
    FROM sales s
    WHERE s.status = 'completed'
    GROUP BY DATE(s.sale_date)
    ORDER BY day DESC
    LIMIT 7
""")
    raw_trend = cursor.fetchall()
    sales_trend = list(reversed([
    {"day": str(r["day"]), "revenue": float(r["revenue"])}
    for r in raw_trend
]))
    db.close()
    return render_template("dashboard.html",
        username=session["username"],
        total_products=total_products,
        total_units=total_units,
        inventory_value=inventory_value,
        low_stock=low_stock,
        total_categories=total_categories,
        categories=categories,
        low_stock_items=low_stock_items,
        recent_activity=recent_activity,
        top_products=top_products,
        top_sold=top_sold,
        sales_trend=sales_trend,
        sales_last5=sales_last5,
    )

# ── PRODUCTS ──────────────────────────────────────────────────────────────────
@app.route("/products")
@login_required
def products():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Products with supplier info
    cursor.execute("""
        SELECT
            p.sku,
            p.name,
            p.category,
            p.price,
            p.stock,
            s.supplier_name
        FROM products p
        LEFT JOIN suppliers s
        ON p.supplier_id = s.id
        ORDER BY p.sku
    """)
    items = cursor.fetchall()

    # Supplier dropdown data
    cursor.execute("""
        SELECT id, supplier_name
        FROM suppliers
        ORDER BY supplier_name
    """)
    suppliers = cursor.fetchall()

    db.close()

    return render_template(
        "products.html",
        items=items,
        suppliers=suppliers,
        username=session["username"]
    )

@app.route("/add_item", methods=["POST"])
@login_required
def add_item():
    sku      = request.form["sku"].strip()
    name     = request.form["name"].strip()
    category = request.form["category"].strip()
    price    = float(request.form["price"])
    stock    = int(request.form["stock"])
    supplier_id_raw = request.form.get("supplier_id", "").strip()

    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        # ── Resolve supplier_id ──────────────────────────────────────
        supplier_id = None

        if supplier_id_raw == "__new__":
            # Create the new supplier first
            new_name    = request.form.get("new_supplier_name", "").strip()
            new_contact = request.form.get("new_supplier_contact", "").strip()
            new_email   = request.form.get("new_supplier_email", "").strip()

            if new_name:
                cursor.execute("""
                    INSERT INTO suppliers (supplier_name, contact, email)
                    VALUES (%s, %s, %s)
                """, (new_name, new_contact, new_email))
                db.commit()
                supplier_id = cursor.lastrowid   # auto-generated id

        elif supplier_id_raw:
            supplier_id = int(supplier_id_raw)

        # ── Auto-generate SKU if empty ───────────────────────────────
        if not sku:
            cursor.execute("""
                SELECT sku FROM products
                ORDER BY CAST(SUBSTRING(sku, 4) AS UNSIGNED) DESC
                LIMIT 1
            """)
            last_item = cursor.fetchone()
            if last_item and last_item["sku"]:
                last_number = int(last_item["sku"].replace("PRD", ""))
                sku = f"PRD{last_number + 1:03d}"
            else:
                sku = "PRD001"

        # ── Insert product ───────────────────────────────────────────
        cursor.execute("""
            INSERT INTO products (sku, name, category, price, stock, supplier_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (sku, name, category, price, stock, supplier_id))

        # ── Update supplied_products count on supplier ───────────────
        if supplier_id:
            cursor.execute("""
                UPDATE suppliers
                SET supplied_products = (
                    SELECT COUNT(*) FROM products WHERE supplier_id = %s
                )
                WHERE id = %s
            """, (supplier_id, supplier_id))

        db.commit()
        db.close()

        log_activity(sku, name, "Add Item", stock, 0, stock,
                     f"New item added by {session['username']}")
        flash(f"'{name}' added successfully with SKU: {sku}", "success")

    except Exception as e:
        flash(f"Error: {e}", "error")

    return redirect(url_for("products"))

@app.route("/restock_in", methods=["POST"])
@login_required
def restock_in():
    sku = request.form["sku"]
    qty = int(request.form["qty"])
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT name, stock FROM products WHERE sku=%s", (sku,))
        row = cursor.fetchone()
        old = int(row["stock"]); new = old + qty
        cursor.execute("UPDATE products SET stock=%s WHERE sku=%s", (new, sku))
        db.commit(); db.close()
        log_activity(sku, row["name"], "Restock IN", qty, old, new,
                     f"Restocked by {session['username']}")
        flash(f"'{row['name']}' restocked: {old} -> {new} units.", "success")
    except Exception as e:
        flash(f"Error: {e}", "error")
    return redirect(url_for("products"))

@app.route("/restock_out", methods=["POST"])
@login_required
def restock_out():
    sku = request.form["sku"]
    qty = int(request.form["qty"])
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT name, stock FROM products WHERE sku=%s", (sku,))
        row = cursor.fetchone()
        old = int(row["stock"])
        if qty > old:
            flash("Cannot remove more than current stock.", "error")
            return redirect(url_for("products"))
        new = old - qty
        cursor.execute("UPDATE products SET stock=%s WHERE sku=%s", (new, sku))
        db.commit(); db.close()
        log_activity(sku, row["name"], "Restock OUT", -qty, old, new,
                     f"Stock removed by {session['username']}")
        flash(f"'{row['name']}' stock removed: {old} -> {new} units.", "success")
    except Exception as e:
        flash(f"Error: {e}", "error")
    return redirect(url_for("products"))

@app.route("/change_price", methods=["POST"])
@login_required
def change_price():
    sku       = request.form["sku"]
    new_price = float(request.form["new_price"])
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT name, price, stock FROM products WHERE sku=%s", (sku,))
        row = cursor.fetchone()
        old_price = float(row["price"])
        current_stock = int(row["stock"])
        cursor.execute("UPDATE products SET price=%s WHERE sku=%s", (new_price, sku))
        db.commit(); db.close()
        log_activity(sku, row["name"], "Price Change", 0, current_stock, current_stock,
                     f"Price changed by {session['username']}: {old_price:.2f} -> {new_price:.2f}")
        flash(f"'{row['name']}' price updated: {old_price:.2f} -> {new_price:.2f}", "success")
    except Exception as e:
        flash(f"Error: {e}", "error")
    return redirect(url_for("products"))

# ── EDIT PRODUCT ──────────────────────────────────────────────────────────────
@app.route("/edit_product", methods=["POST"])
@login_required
def edit_product():
    sku         = request.form["sku"].strip()
    new_name    = request.form["name"].strip()
    new_cat     = request.form["category"].strip()
    new_price   = float(request.form["price"])
    new_stock   = int(request.form["stock"])
    supplier_id = request.form.get("supplier_id", "").strip() or None
    if supplier_id:
        supplier_id = int(supplier_id)
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT name, stock, price FROM products WHERE sku=%s", (sku,))
        old = cursor.fetchone()
        cursor.execute("""
            UPDATE products
            SET name=%s, category=%s, price=%s, stock=%s, supplier_id=%s
            WHERE sku=%s
        """, (new_name, new_cat, new_price, new_stock, supplier_id, sku))
        # Update supplier product count if supplier changed
        if supplier_id:
            cursor.execute("""
                UPDATE suppliers SET supplied_products=(
                    SELECT COUNT(*) FROM products WHERE supplier_id=%s
                ) WHERE id=%s
            """, (supplier_id, supplier_id))
        db.commit(); db.close()
        if int(old["stock"]) != new_stock:
            log_activity(sku, new_name, "Manual Edit", new_stock - int(old["stock"]),
                         int(old["stock"]), new_stock,
                         f"Product edited by {session['username']}")
        flash(f"'{new_name}' updated successfully.", "success")
    except Exception as e:
        flash(f"Error: {e}", "error")
    return redirect(url_for("products"))

# ── DELETE PRODUCT ────────────────────────────────────────────────────────────
@app.route("/delete_product", methods=["POST"])
@login_required
def delete_product():
    sku = request.form["sku"].strip()
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT name, stock, supplier_id FROM products WHERE sku=%s", (sku,))
        row = cursor.fetchone()
        if not row:
            flash("Product not found.", "error")
            return redirect(url_for("products"))
        cursor.execute("DELETE FROM products WHERE sku=%s", (sku,))
        # Recalculate supplier count
        if row["supplier_id"]:
            cursor.execute("""
                UPDATE suppliers SET supplied_products=(
                    SELECT COUNT(*) FROM products WHERE supplier_id=%s
                ) WHERE id=%s
            """, (row["supplier_id"], row["supplier_id"]))
        db.commit(); db.close()
        log_activity(sku, row["name"], "Delete", 0, int(row["stock"]), 0,
                     f"Product deleted by {session['username']}")
        flash(f"Product '{row['name']}' ({sku}) deleted.", "success")
    except Exception as e:
        flash(f"Error: {e}", "error")
    return redirect(url_for("products"))

# ── EDIT SUPPLIER ─────────────────────────────────────────────────────────────
@app.route("/edit_supplier", methods=["POST"])
@login_required
def edit_supplier():
    supplier_id   = int(request.form["supplier_id"])
    supplier_name = request.form["supplier_name"].strip()
    contact       = request.form["contact"].strip()
    email         = request.form["email"].strip()
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            UPDATE suppliers SET supplier_name=%s, contact=%s, email=%s WHERE id=%s
        """, (supplier_name, contact, email, supplier_id))
        db.commit(); db.close()
        flash(f"Supplier '{supplier_name}' updated.", "success")
    except Exception as e:
        flash(f"Error: {e}", "error")
    return redirect(url_for("suppliers"))

# ── DELETE SUPPLIER ───────────────────────────────────────────────────────────
@app.route("/delete_supplier", methods=["POST"])
@login_required
def delete_supplier():
    supplier_id = int(request.form["supplier_id"])
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT supplier_name FROM suppliers WHERE id=%s", (supplier_id,))
        row = cursor.fetchone()
        if not row:
            flash("Supplier not found.", "error")
            return redirect(url_for("suppliers"))
        # Unlink products from this supplier (don't delete the products)
        cursor.execute("UPDATE products SET supplier_id=NULL WHERE supplier_id=%s", (supplier_id,))
        cursor.execute("DELETE FROM suppliers WHERE id=%s", (supplier_id,))
        db.commit(); db.close()
        flash(f"Supplier '{row['supplier_name']}' deleted. Linked products are now unassigned.", "success")
    except Exception as e:
        flash(f"Error: {e}", "error")
    return redirect(url_for("suppliers"))

# ── REFUND / DELETE SALE ──────────────────────────────────────────────────────
@app.route("/sales/<int:sale_id>/refund", methods=["POST"])
@login_required
def refund_sale(sale_id):
    """Mark sale as refunded and restore stock."""
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM sales WHERE id=%s", (sale_id,))
        sale = cursor.fetchone()
        if not sale:
            return jsonify({"error": "Sale not found"}), 404
        if sale["status"] == "refunded":
            return jsonify({"error": "Already refunded"}), 400
        # Restore stock for each item
        cursor.execute("SELECT * FROM sale_items WHERE sale_id=%s", (sale_id,))
        items = cursor.fetchall()
        for item in items:
            cursor.execute("SELECT stock FROM products WHERE sku=%s", (item["sku"],))
            prod = cursor.fetchone()
            if prod:
                old_stock = int(prod["stock"])
                new_stock = old_stock + int(item["qty"])
                cursor.execute("UPDATE products SET stock=%s WHERE sku=%s", (new_stock, item["sku"]))
                log_activity(item["sku"], item["name"], "Refund IN",
                             int(item["qty"]), old_stock, new_stock,
                             f"Refund of {sale['invoice_no']} by {session['username']}")
        cursor.execute("UPDATE sales SET status='refunded' WHERE id=%s", (sale_id,))
        db.commit(); db.close()
        return jsonify({"success": True, "invoice_no": sale["invoice_no"]})
    except Exception as e:
        try: db.rollback(); db.close()
        except: pass
        return jsonify({"error": str(e)}), 500

@app.route("/sales/<int:sale_id>/delete", methods=["POST"])
@login_required
def delete_sale(sale_id):
    """Permanently delete a sale record (only for refunded sales)."""
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT invoice_no, status FROM sales WHERE id=%s", (sale_id,))
        sale = cursor.fetchone()
        if not sale:
            return jsonify({"error": "Sale not found"}), 404
        if sale["status"] != "refunded":
            return jsonify({"error": "Only refunded sales can be deleted"}), 400
        cursor.execute("DELETE FROM sale_items WHERE sale_id=%s", (sale_id,))
        cursor.execute("DELETE FROM sales WHERE id=%s", (sale_id,))
        db.commit(); db.close()
        return jsonify({"success": True, "invoice_no": sale["invoice_no"]})
    except Exception as e:
        try: db.rollback(); db.close()
        except: pass
        return jsonify({"error": str(e)}), 500
# ── SUPPLIERS ────────────────────────────────────────────────────────────────
@app.route("/suppliers")
@login_required
def suppliers():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
    SELECT id, supplier_name, contact, email,
           CAST(COALESCE(supplied_products, 0) AS UNSIGNED) AS supplied_products,
           created_at
    FROM suppliers
    ORDER BY id DESC
""")

    supplier_list = cursor.fetchall()
    db.close()

    return render_template(
        "suppliers.html",
        suppliers=supplier_list,
        username=session["username"]
    )
@app.route("/add_supplier", methods=["POST"])
@login_required
def add_supplier():
    supplier_name = request.form["supplier_name"].strip()
    contact = request.form["contact"].strip()
    email = request.form["email"].strip()

    try:
        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO suppliers
            (supplier_name, contact, email)
            VALUES (%s, %s, %s)
        """, (
            supplier_name,
            contact,
            email
        ))

        db.commit()
        db.close()

        flash(f"Supplier '{supplier_name}' added successfully.", "success")

    except Exception as e:
        flash(f"Error: {e}", "error")

    return redirect(url_for("suppliers"))

# ── SUPPLIER PRODUCTS ─────────────────────────────────────────────────────────
@app.route("/supplier/<int:supplier_id>/products")
@login_required
def supplier_products(supplier_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Correct
    cursor.execute("SELECT id, supplier_name FROM suppliers WHERE id = %s", (supplier_id,))
    supplier = cursor.fetchone()

    if not supplier:
        return jsonify({"error": "Supplier not found"}), 404

    cursor.execute("""
        SELECT sku, name, category, price, stock
        FROM products
        WHERE supplier_id = %s
        ORDER BY name
    """, (supplier_id,))
    items = cursor.fetchall()
    db.close()

    return jsonify({
        "supplier": supplier,
        "products": [{
            "sku": r["sku"],
            "name": r["name"],
            "category": r["category"],
            "price": float(r["price"]),
            "stock": int(r["stock"])
        } for r in items]
    })


@app.route("/add_product_to_supplier", methods=["POST"])
@login_required
def add_product_to_supplier():
    supplier_id = request.form.get("supplier_id")
    sku         = request.form.get("sku", "").strip()
    name        = request.form.get("name", "").strip()
    category    = request.form.get("category", "").strip()
    price       = float(request.form.get("price", 0))
    stock       = int(request.form.get("stock", 0))

    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        # Auto-generate SKU if empty
        if not sku:
            cursor.execute("""
                SELECT sku FROM products
                ORDER BY CAST(SUBSTRING(sku, 4) AS UNSIGNED) DESC
                LIMIT 1
            """)
            last = cursor.fetchone()
            sku = f"PRD{(int(last['sku'].replace('PRD','')) + 1):03d}" if last else "PRD001"

        cursor.execute("""
            INSERT INTO products (sku, name, category, price, stock, supplier_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (sku, name, category, price, stock, supplier_id))

        # Update supplied_products count on supplier
        cursor.execute("""
            UPDATE suppliers
            SET supplied_products = (
                SELECT COUNT(*) FROM products WHERE supplier_id = %s
            )
            WHERE id = %s
        """, (supplier_id, supplier_id))

        db.commit()
        db.close()

        log_activity(sku, name, "Add Item", stock, 0, stock,
                     f"Added via supplier #{supplier_id} by {session['username']}")
        flash(f"'{name}' ({sku}) added to supplier successfully.", "success")

    except Exception as e:
        flash(f"Error: {e}", "error")

    return redirect(url_for("suppliers"))
# ── CUSTOMERS ─────────────────────────────────────────────────────────────────

@app.route("/customers")
@login_required
def customers():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            c.id,
            c.name,
            c.phone,
            c.email,
            c.created_at,
            COUNT(s.id)                      AS total_orders,
            COALESCE(SUM(s.total), 0)        AS total_spent,
            MAX(s.sale_date)                 AS last_visit
        FROM customers c
        LEFT JOIN sales s ON s.customer_id = c.id
        GROUP BY c.id
        ORDER BY c.id DESC
    """)
    customer_list = cursor.fetchall()
    db.close()
    return render_template(
        "customers.html",
        customers=customer_list,
        username=session["username"]
    )


@app.route("/customers/add", methods=["POST"])
@login_required
def add_customer():
    name  = request.form.get("name",  "").strip()
    phone = request.form.get("phone", "").strip()
    email = request.form.get("email", "").strip()
    if not name:
        flash("Customer name is required.", "error")
        return redirect(url_for("customers"))
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO customers (name, phone, email) VALUES (%s, %s, %s)",
            (name, phone or None, email or None)
        )
        db.commit()
        db.close()
        flash(f"Customer '{name}' added.", "success")
    except Exception as e:
        flash(f"Error: {e}", "error")
    return redirect(url_for("customers"))


@app.route("/customers/<int:customer_id>/sales")
@login_required
def customer_sales(customer_id):
    """Return all sales for a customer as JSON (used by modal)."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, name, phone, email FROM customers WHERE id = %s", (customer_id,))
    customer = cursor.fetchone()
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    cursor.execute("""
        SELECT s.id, s.invoice_no, s.total, s.sale_date, s.status,
               COALESCE(SUM(si.qty), 0) AS item_count
        FROM sales s
        LEFT JOIN sale_items si ON si.sale_id = s.id
        WHERE s.customer_id = %s
        GROUP BY s.id
        ORDER BY s.sale_date DESC
    """, (customer_id,))
    sales = cursor.fetchall()
    db.close()
    # Convert datetime to string for JSON
    for s in sales:
        if s["sale_date"]:
            s["sale_date"] = s["sale_date"].strftime("%d %b %Y, %I:%M %p")
    return jsonify({"customer": customer, "sales": sales})


@app.route("/search_customers")
@login_required
def search_customers():
    q = request.args.get("q", "").strip()
    if len(q) < 1:
        return jsonify([])
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, name, phone, email FROM customers
        WHERE name LIKE %s
        ORDER BY name ASC
        LIMIT 8
    """, (f"%{q}%",))
    results = cursor.fetchall()
    db.close()
    return jsonify(results)


# ── SALES (updated) ───────────────────────────────────────────────────────────

def generate_invoice_no():
    """Auto-generate next invoice number e.g. INV001, INV002 …"""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT invoice_no FROM sales
        ORDER BY CAST(SUBSTRING(invoice_no, 4) AS UNSIGNED) DESC
        LIMIT 1
    """)
    last = cursor.fetchone()
    db.close()
    if last and last["invoice_no"]:
        num = int(last["invoice_no"].replace("INV", ""))
        return f"INV{num + 1:03d}"
    return "INV001"


@app.route("/sales")
@login_required
def sales():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    search    = request.args.get("search",    "").strip()
    date_from = request.args.get("date_from", "")
    date_to   = request.args.get("date_to",   "")
    status    = request.args.get("status",    "")

    query = """
        SELECT
            s.id,
            s.invoice_no,
            COALESCE(c.name, s.customer, '—') AS customer,
            c.phone                            AS customer_phone,
            s.customer_id,
            s.total,
            s.sale_date,
            s.status,
            s.note,
            COALESCE(SUM(si.qty), 0)           AS item_count
        FROM sales s
        LEFT JOIN customers c  ON c.id  = s.customer_id
        LEFT JOIN sale_items si ON si.sale_id = s.id
        WHERE 1=1
    """
    params = []

    if search:
        query += " AND (s.invoice_no LIKE %s OR c.name LIKE %s OR s.customer LIKE %s)"
        params += [f"%{search}%", f"%{search}%", f"%{search}%"]
    if date_from:
        query += " AND DATE(s.sale_date) >= %s"
        params.append(date_from)
    if date_to:
        query += " AND DATE(s.sale_date) <= %s"
        params.append(date_to)
    if status:
        query += " AND s.status = %s"
        params.append(status)

    query += """ GROUP BY s.id, s.invoice_no, c.name, s.customer, c.phone,
             s.customer_id, s.total, s.sale_date, s.status, s.note
             ORDER BY s.id DESC"""
    cursor.execute(query, params)
    sales_list = cursor.fetchall()

    # Summary cards
    cursor.execute("SELECT COUNT(*) AS v FROM sales WHERE DATE(sale_date) = CURDATE()")
    today_count = cursor.fetchone()["v"]

    cursor.execute("SELECT COALESCE(SUM(total),0) AS v FROM sales WHERE DATE(sale_date) = CURDATE()")
    today_revenue = float(cursor.fetchone()["v"])

    cursor.execute("SELECT COUNT(*) AS v FROM sales")
    total_sales = cursor.fetchone()["v"]

    cursor.execute("SELECT COALESCE(SUM(total),0) AS v FROM sales")
    total_revenue = float(cursor.fetchone()["v"])

    db.close()
    return render_template(
        "sales.html",
        sales_list=sales_list,
        today_count=today_count,
        today_revenue=today_revenue,
        total_sales=total_sales,
        total_revenue=total_revenue,
        search=search,
        date_from=date_from,
        date_to=date_to,
        status=status,
        username=session["username"],
    )


@app.route("/sales/add", methods=["POST"])
@login_required
def sales_add():
    data        = request.get_json()
    customer_id = data.get("customer_id")   # int or None
    # fallback plain name (walk-in typed without picking from list)
    customer_name = data.get("customer_name", "").strip()
    note          = data.get("note", "").strip()
    items         = data.get("items", [])

    if not items:
        return jsonify({"error": "No items in sale."}), 400

    try:
        db     = get_db()
        cursor = db.cursor(dictionary=True)

        # If a name was typed but no customer picked → create customer on the fly
        if not customer_id and customer_name:
            customer_phone = data.get("customer_phone", "").strip() or None
            customer_email = data.get("customer_email", "").strip() or None
            cursor.execute(
            "INSERT INTO customers (name, phone, email) VALUES (%s, %s, %s)",
            (customer_name, customer_phone, customer_email)
        )
        customer_id = cursor.lastrowid

        # Validate stock
        for item in items:
            cursor.execute(
                "SELECT stock, name FROM products WHERE sku = %s FOR UPDATE",
                (item["sku"],)
            )
            row = cursor.fetchone()
            if not row:
                db.close()
                return jsonify({"error": f"SKU {item['sku']} not found."}), 400
            if int(row["stock"]) < int(item["qty"]):
                db.close()
                return jsonify({
                    "error": f"Insufficient stock for '{row['name']}'. Available: {row['stock']}"
                }), 400

        invoice_no = generate_invoice_no()
        total = sum(float(i["unit_price"]) * int(i["qty"]) for i in items)

        # Resolve display name for legacy `customer` text column
        display_name = None
        if customer_id:
            cursor.execute("SELECT name FROM customers WHERE id = %s", (customer_id,))
            r = cursor.fetchone()
            if r:
                display_name = r["name"]
        elif customer_name:
            display_name = customer_name

        # Insert sale header
        cursor.execute("""
            INSERT INTO sales (invoice_no, customer, customer_id, total, note, status)
            VALUES (%s, %s, %s, %s, %s, 'completed')
        """, (invoice_no, display_name, customer_id or None, total, note or None))
        sale_id = cursor.lastrowid

        # Insert line items + decrement stock
        for item in items:
            qty        = int(item["qty"])
            unit_price = float(item["unit_price"])
            line_total = qty * unit_price

            cursor.execute("""
                INSERT INTO sale_items (sale_id, sku, name, qty, unit_price, line_total)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (sale_id, item["sku"], item["name"], qty, unit_price, line_total))

            cursor.execute("SELECT stock FROM products WHERE sku = %s", (item["sku"],))
            old_stock = int(cursor.fetchone()["stock"])
            new_stock = old_stock - qty
            cursor.execute(
                "UPDATE products SET stock = %s WHERE sku = %s",
                (new_stock, item["sku"])
            )
            log_activity(
                item["sku"], item["name"],
                "Sale OUT", -qty, old_stock, new_stock,
                f"Sale {invoice_no} by {session['username']}"
            )

        db.commit()
        # Fetch phone+email to send back for the info button
        c_phone = c_email = None
        if customer_id:
            cursor.execute("SELECT phone, email FROM customers WHERE id = %s", (customer_id,))
            crow = cursor.fetchone()
            if crow:
                c_phone = crow["phone"]
                c_email = crow["email"]

        
        db.close()

        return jsonify({
            "success":        True,
            "invoice_no":     invoice_no,
            "sale_id":        sale_id,
            "customer_id":    customer_id,
            "customer":       display_name or "—",
            "customer_phone": c_phone or "",
            "customer_email": c_email or "",
        })

    except Exception as e:
        try:
            db.rollback()
            db.close()
        except Exception:
            pass
        return jsonify({"error": str(e)}), 500


@app.route("/sales/<int:sale_id>/invoice")
@login_required
def sales_invoice(sale_id):
    db     = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.*, COALESCE(c.name, s.customer) AS customer_display,
               c.phone AS customer_phone, c.email AS customer_email
        FROM sales s
        LEFT JOIN customers c ON c.id = s.customer_id
        WHERE s.id = %s
    """, (sale_id,))
    sale = cursor.fetchone()
    if not sale:
        flash("Sale not found.", "error")
        return redirect(url_for("sales"))
    cursor.execute("SELECT * FROM sale_items WHERE sale_id = %s", (sale_id,))
    items = cursor.fetchall()
    db.close()
    return render_template("invoice.html", sale=sale, items=items, username=session["username"])


# ── REPORTS ───────────────────────────────────────────────────────────────────

@app.route("/reports")
@login_required
def reports():
    db     = get_db()
    cursor = db.cursor(dictionary=True)
    tab    = request.args.get("tab", "daily")

    # ── Shared: all suppliers & categories for filter dropdowns ──────────────
    cursor.execute("SELECT id, supplier_name FROM suppliers ORDER BY supplier_name")
    all_suppliers = cursor.fetchall()

    cursor.execute("SELECT DISTINCT category FROM products ORDER BY category")
    all_categories = [r["category"] for r in cursor.fetchall()]

    # ════════════════════════════════════════════════════════════════════════
    # DAILY REPORT — default to most recent sale date in DB
    # ════════════════════════════════════════════════════════════════════════
    cursor.execute("SELECT DATE(sale_date) AS d FROM sales ORDER BY sale_date DESC LIMIT 1")
    last_sale    = cursor.fetchone()
    default_date = last_sale["d"].strftime("%Y-%m-%d") if last_sale else date.today().strftime("%Y-%m-%d")
    daily_date   = request.args.get("daily_date", default_date)

    cursor.execute("""
        SELECT COUNT(*) AS total_sales, COALESCE(SUM(total), 0) AS revenue
        FROM sales
        WHERE DATE(sale_date) = %s AND status = 'completed'
    """, (daily_date,))
    d_summary = cursor.fetchone()

    cursor.execute("""
        SELECT COALESCE(SUM(si.qty), 0) AS items_sold
        FROM sale_items si
        JOIN sales s ON si.sale_id = s.id
        WHERE DATE(s.sale_date) = %s AND s.status = 'completed'
    """, (daily_date,))
    d_items = cursor.fetchone()

    total_sales = d_summary["total_sales"]
    revenue     = float(d_summary["revenue"])
    items_sold  = int(d_items["items_sold"])
    avg_order   = revenue / total_sales if total_sales else 0.0

    cursor.execute("""
        SELECT s.id, s.invoice_no, s.customer, s.total, s.sale_date, s.status,
               COUNT(si.id) AS item_count
        FROM sales s
        LEFT JOIN sale_items si ON si.sale_id = s.id
        WHERE DATE(s.sale_date) = %s
        GROUP BY s.id
        ORDER BY s.sale_date DESC
    """, (daily_date,))
    transactions = cursor.fetchall()

    cursor.execute("""
        SELECT si.sku, si.name,
               SUM(si.qty)        AS qty,
               SUM(si.line_total) AS revenue
        FROM sale_items si
        JOIN sales s ON si.sale_id = s.id
        WHERE DATE(s.sale_date) = %s AND s.status = 'completed'
        GROUP BY si.sku, si.name
        ORDER BY revenue DESC
        LIMIT 5
    """, (daily_date,))
    daily_top = cursor.fetchall()

    daily = {
        "total_sales":  total_sales,
        "revenue":      revenue,
        "items_sold":   items_sold,
        "avg_order":    avg_order,
        "transactions": transactions,
        "top_products": daily_top,
    }

    # ════════════════════════════════════════════════════════════════════════
    # MONTHLY REPORT — default to most recent sale month in DB
    # ════════════════════════════════════════════════════════════════════════
    
 
    cursor.execute("SELECT DATE_FORMAT(sale_date, '%%Y-%%m') AS m FROM sales ORDER BY sale_date DESC LIMIT 1")
    last_month    = cursor.fetchone()
    default_month = last_month["m"] if last_month else date.today().strftime("%Y-%m")
    monthly_month = request.args.get("monthly_month", default_month)  # ← only here, once

    cursor.execute("""
        SELECT COUNT(*) AS total_sales, COALESCE(SUM(total), 0) AS revenue
        FROM sales
        WHERE DATE_FORMAT(sale_date, '%%Y-%%m') = %s AND status = 'completed'
    """, (monthly_month,))
    m_summary = cursor.fetchone()

    cursor.execute("""
        SELECT COALESCE(SUM(si.qty), 0) AS items_sold
        FROM sale_items si JOIN sales s ON si.sale_id = s.id
        WHERE DATE_FORMAT(s.sale_date, '%%Y-%%m') = %s AND s.status = 'completed'
    """, (monthly_month,))
    m_items = cursor.fetchone()

    cursor.execute("""
        SELECT COUNT(DISTINCT DATE(sale_date)) AS active_days
        FROM sales
        WHERE DATE_FORMAT(sale_date, '%%Y-%%m') = %s AND status = 'completed'
    """, (monthly_month,))
    m_days = cursor.fetchone()

    cursor.execute("""
        SELECT DATE(s.sale_date) AS sale_day,
           COUNT(DISTINCT s.id) AS sales_count,
           COALESCE(SUM(si.qty), 0) AS items_sold,
           COALESCE(SUM(s.total), 0) AS revenue
        FROM sales s
        LEFT JOIN sale_items si ON si.sale_id = s.id
        WHERE DATE_FORMAT(s.sale_date, '%%Y-%%m') = %s AND s.status = 'completed'
        GROUP BY DATE(s.sale_date)
        ORDER BY sale_day DESC
    """, (monthly_month,))
    daily_breakdown = cursor.fetchall()

    cursor.execute("""
        SELECT si.sku, si.name, p.category,
           SUM(si.qty) AS qty, SUM(si.line_total) AS revenue
        FROM sale_items si
        JOIN sales s ON si.sale_id = s.id
        LEFT JOIN products p ON p.sku = si.sku
        WHERE DATE_FORMAT(s.sale_date, '%%Y-%%m') = %s AND s.status = 'completed'
        GROUP BY si.sku, si.name, p.category
        ORDER BY revenue DESC LIMIT 10
    """, (monthly_month,))
    monthly_top = cursor.fetchall()

    monthly = {
        "total_sales":     int(m_summary["total_sales"]),
        "revenue":         float(m_summary["revenue"]),
        "items_sold":      int(m_items["items_sold"]),
        "active_days":     int(m_days["active_days"]),
        "daily_breakdown": daily_breakdown,
        "top_products":    monthly_top,
    }

    # ════════════════════════════════════════════════════════════════════════
    # PURCHASE REPORT
    # ════════════════════════════════════════════════════════════════════════
    pur_from     = request.args.get("pur_from", "")
    pur_to       = request.args.get("pur_to",   "")
    pur_supplier = request.args.get("pur_supplier", "")

    prod_query  = """
        SELECT p.sku, p.name, p.category, p.price, p.stock,
               ROUND(p.price * p.stock, 2) AS stock_value,
               s.supplier_name
        FROM products p
        LEFT JOIN suppliers s ON p.supplier_id = s.id
        WHERE 1=1
    """
    prod_params = []
    if pur_supplier:
        prod_query += " AND p.supplier_id = %s"
        prod_params.append(pur_supplier)
    prod_query += " ORDER BY s.supplier_name, p.name"
    cursor.execute(prod_query, prod_params)
    purchase_products = cursor.fetchall()

    cursor.execute("""
        SELECT COUNT(*)                        AS total_products,
               COUNT(DISTINCT supplier_id)     AS total_suppliers,
               COALESCE(SUM(price * stock), 0) AS inventory_value,
               SUM(CASE WHEN stock < 10 THEN 1 ELSE 0 END) AS low_stock_count
        FROM products
    """)
    p_stats = cursor.fetchone()

    cursor.execute("""
        SELECT
            COALESCE(s.supplier_name, 'No Supplier')      AS supplier_name,
            COUNT(p.sku)                                   AS product_count,
            COALESCE(SUM(p.stock), 0)                     AS total_stock,
            ROUND(COALESCE(SUM(p.price * p.stock), 0), 2) AS stock_value
        FROM products p
        LEFT JOIN suppliers s ON p.supplier_id = s.id
        GROUP BY s.supplier_name
        ORDER BY stock_value DESC
    """)
    supplier_summary = cursor.fetchall()

    purchase = {
        "total_products":   int(p_stats["total_products"]),
        "total_suppliers":  int(p_stats["total_suppliers"]),
        "inventory_value":  float(p_stats["inventory_value"]),
        "low_stock_count":  int(p_stats["low_stock_count"]),
        "products":         purchase_products,
        "supplier_summary": supplier_summary,
    }

    # ════════════════════════════════════════════════════════════════════════
    # STOCK REPORT
    # ════════════════════════════════════════════════════════════════════════
    stock_filter   = request.args.get("stock_filter",   "all")
    stock_category = request.args.get("stock_category", "")

    stock_query  = """
        SELECT p.sku, p.name, p.category, p.price, p.stock,
               ROUND(p.price * p.stock, 2) AS stock_value,
               s.supplier_name
        FROM products p
        LEFT JOIN suppliers s ON p.supplier_id = s.id
        WHERE 1=1
    """
    stock_params = []

    if stock_filter == "low":
        stock_query += " AND p.stock > 0 AND p.stock < 10"
    elif stock_filter == "critical":
        stock_query += " AND p.stock > 0 AND p.stock < 5"
    elif stock_filter == "out":
        stock_query += " AND p.stock = 0"

    if stock_category:
        stock_query += " AND p.category = %s"
        stock_params.append(stock_category)

    stock_query += " ORDER BY p.stock ASC, p.name"
    cursor.execute(stock_query, stock_params)
    stock_items = cursor.fetchall()

    cursor.execute("""
        SELECT
            COUNT(*)                                                    AS total_skus,
            COALESCE(SUM(stock), 0)                                    AS total_units,
            SUM(CASE WHEN stock < 10 AND stock > 0 THEN 1 ELSE 0 END) AS low_count,
            SUM(CASE WHEN stock = 0 THEN 1 ELSE 0 END)                AS out_count
        FROM products
    """)
    s_stats = cursor.fetchone()

    stock_summary = {
        "total_skus":  int(s_stats["total_skus"]),
        "total_units": int(s_stats["total_units"]),
        "low_count":   int(s_stats["low_count"]),
        "out_count":   int(s_stats["out_count"]),
    }

    cursor.execute("""
        SELECT category,
               COUNT(*)                               AS sku_count,
               COALESCE(SUM(stock), 0)               AS total_units,
               ROUND(COALESCE(SUM(price*stock),0),2)  AS stock_value
        FROM products
        GROUP BY category
        ORDER BY stock_value DESC
    """)
    raw_cat   = cursor.fetchall()
    total_val = sum(float(c["stock_value"]) for c in raw_cat) or 1
    stock_by_category = [{
        "category":    c["category"],
        "sku_count":   c["sku_count"],
        "total_units": c["total_units"],
        "stock_value": float(c["stock_value"]),
        "share_pct":   round(float(c["stock_value"]) / total_val * 100, 1),
    } for c in raw_cat]

    db.close()

    return render_template(
        "reports.html",
        username=session["username"],
        tab=tab,
        daily_date=daily_date,
        daily=daily,
        monthly_month=monthly_month,
        monthly=monthly,
        pur_from=pur_from,
        pur_to=pur_to,
        pur_supplier=pur_supplier,
        all_suppliers=all_suppliers,
        purchase=purchase,
        stock_filter=stock_filter,
        stock_category=stock_category,
        all_categories=all_categories,
        stock_items=stock_items,
        stock_summary=stock_summary,
        stock_by_category=stock_by_category,
    )

# ── PRODUCT SEARCH API ────────────────────────────────────────────────────────
@app.route("/search_products")
@login_required
def search_products():
    q = request.args.get("q", "").strip()
    if len(q) < 2:
        return jsonify([])
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        """SELECT sku, name, category, price, stock
           FROM products
           WHERE name LIKE %s OR sku LIKE %s
           ORDER BY name LIMIT 10""",
        (f"%{q}%", f"%{q}%")
    )
    results = cursor.fetchall()
    db.close()
    return jsonify([{
        "sku": r["sku"], "name": r["name"],
        "category": r["category"],
        "price": float(r["price"]),
        "stock": int(r["stock"])
    } for r in results])
# ── CATEGORIES API ────────────────────────────────────────────────────────────
@app.route("/get_categories")
@login_required
def get_categories():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT DISTINCT category FROM products ORDER BY category")
    cats = [row["category"] for row in cursor.fetchall()]
    db.close()
    return jsonify(cats)

# ── ACTIVITY LOG ──────────────────────────────────────────────────────────────
@app.route("/activity_log")
@login_required
def activity_log():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, datetime, sku, name, action, qty_change, "
        "stock_before, stock_after, note FROM activity_log ORDER BY id DESC"
    )
    logs = cursor.fetchall()
    db.close()
    return render_template("activity_log.html", logs=logs, username=session["username"])

if __name__ == "__main__":
    app.run(debug=True)