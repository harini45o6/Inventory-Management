from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, Response
import mysql.connector
from functools import wraps
from datetime import date, datetime

app = Flask(__name__)
app.secret_key = "shopstock_secret_key_change_in_prod"

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_HTTPONLY"] = True

import hashlib

def hash_password(password):
    """SHA-256 hash — matches the hashes stored by the DB seeder."""
    return hashlib.sha256(password.encode()).hexdigest()

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
        role = session.get("role", "admin")
        return redirect(url_for("billing") if role == "cashier" else url_for("dashboard"))

    error = None
    selected_role = "admin"

    if request.method == "POST":
        username      = request.form.get("username", "").strip()
        password      = request.form.get("password", "")
        selected_role = request.form.get("role", "admin")

        try:
            db = get_db()
            cursor = db.cursor(dictionary=True)
            cursor.execute(
                "SELECT id, username, password, role FROM users WHERE username = %s",
                (username,)
            )
            user = cursor.fetchone()
            db.close()

            # Accept SHA-256 hash (DB) or plaintext fallback (dev)
            pwd_hash = hash_password(password)
            if user and (user["password"] == pwd_hash or user["password"] == password):
                # Enforce the role tab matches the actual user role
                if user["role"] != selected_role:
                    error = f"This account is not a {selected_role}."
                else:
                    session["username"] = username
                    session["role"]     = user["role"]
                    session["user_id"]  = user["id"]
                    session.permanent   = False
                    if user["role"] == "cashier":
                        return redirect(url_for("billing"))
                    return redirect(url_for("dashboard"))
            else:
                error = "Invalid username or password."
        except Exception as e:
            error = f"Login error: {e}"

    return render_template("login.html", error=error, selected_role=selected_role)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

def admin_required(f):
    """Restrict route to admin role only."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        if session.get("role") != "admin":
            flash("Admin access required.", "error")
            return redirect(url_for("cashier_dashboard"))
        return f(*args, **kwargs)
    return decorated

# ── CASHIER DASHBOARD ─────────────────────────────────────────────────────────
@app.route("/cashier")
@login_required
def cashier_dashboard():
    if session.get("role") == "admin":
        return redirect(url_for("dashboard"))

    db = get_db()
    cursor = db.cursor(dictionary=True)
    now = datetime.now()
    cashier_id = session.get("user_id")

    # Today's transaction count (this cashier only)
    cursor.execute("""
        SELECT COUNT(*) AS v FROM sales
        WHERE DATE(sale_date) = CURDATE() AND status = 'completed'
        AND cashier_id = %s
    """, (cashier_id,))
    today_count = cursor.fetchone()["v"]

    # Today's revenue (this cashier only)
    cursor.execute("""
        SELECT COALESCE(SUM(total), 0) AS v FROM sales
        WHERE DATE(sale_date) = CURDATE() AND status = 'completed'
        AND cashier_id = %s
    """, (cashier_id,))
    today_revenue = float(cursor.fetchone()["v"])

    # Items sold today (this cashier only)
    cursor.execute("""
        SELECT COALESCE(SUM(si.qty), 0) AS v
        FROM sale_items si
        JOIN sales s ON si.sale_id = s.id
        WHERE DATE(s.sale_date) = CURDATE() AND s.status = 'completed'
        AND s.cashier_id = %s
    """, (cashier_id,))
    today_items = int(cursor.fetchone()["v"])

    # Recent 8 sales (this cashier only)
    cursor.execute("""
        SELECT s.id, s.invoice_no, COALESCE(c.name, s.customer, '—') AS customer,
               s.total, s.sale_date, s.status,
               COALESCE(SUM(si.qty), 0) AS item_count
        FROM sales s
        LEFT JOIN customers c ON c.id = s.customer_id
        LEFT JOIN sale_items si ON si.sale_id = s.id
        WHERE s.cashier_id = %s
        GROUP BY s.id, s.invoice_no, c.name, s.customer, s.total, s.sale_date, s.status
        ORDER BY s.id DESC LIMIT 8
    """, (cashier_id,))
    recent_sales = cursor.fetchall()

    # Top products today by revenue (this cashier only)
    cursor.execute("""
        SELECT si.name, SUM(si.qty) AS qty, SUM(si.line_total) AS revenue
        FROM sale_items si
        JOIN sales s ON si.sale_id = s.id
        WHERE DATE(s.sale_date) = CURDATE() AND s.status = 'completed'
        AND s.cashier_id = %s
        GROUP BY si.name
        ORDER BY revenue DESC LIMIT 6
    """, (cashier_id,))
    top_today = cursor.fetchall()

    # Low stock items (cashier awareness — shared across all cashiers)
    cursor.execute("""
        SELECT sku, name, category, stock, price
        FROM products WHERE stock < 10 ORDER BY stock ASC LIMIT 6
    """)
    low_stock_items = cursor.fetchall()

    db.close()

    return render_template("cashier Dashboard.html",
        username=session["username"],
        now=now,
        today_count=today_count,
        today_revenue=today_revenue,
        today_items=today_items,
        recent_sales=recent_sales,
        top_today=top_today,
        low_stock_items=low_stock_items,
    )

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
        ORDER BY p.sku DESC
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

        # ── Auto-generate SKU ────────────────────────────────────────
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
    supplier_id = request.form.get("supplier_id", "").strip() or None
    if supplier_id:
        supplier_id = int(supplier_id)

    # Handle new supplier creation inside edit
    supplier_id_raw = request.form.get("supplier_id", "").strip()
    if supplier_id_raw == "__new_edit__":
        new_sup_name    = request.form.get("new_supplier_name", "").strip()
        new_sup_contact = request.form.get("new_supplier_contact", "").strip()
        new_sup_email   = request.form.get("new_supplier_email", "").strip()
        if new_sup_name:
            try:
                db2 = get_db()
                c2  = db2.cursor()
                c2.execute("INSERT INTO suppliers (supplier_name, contact, email) VALUES (%s,%s,%s)",
                           (new_sup_name, new_sup_contact, new_sup_email))
                db2.commit()
                supplier_id = c2.lastrowid
                db2.close()
            except Exception:
                pass

    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT name, stock, price FROM products WHERE sku=%s", (sku,))
        old = cursor.fetchone()
        cursor.execute("""
            UPDATE products
            SET name=%s, category=%s, supplier_id=%s
            WHERE sku=%s
        """, (new_name, new_cat, supplier_id, sku))
        # Update supplier product count if supplier changed
        if supplier_id:
            cursor.execute("""
                UPDATE suppliers SET supplied_products=(
                    SELECT COUNT(*) FROM products WHERE supplier_id=%s
                ) WHERE id=%s
            """, (supplier_id, supplier_id))
        db.commit(); db.close()
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
        WHERE name LIKE %s OR phone LIKE %s
        ORDER BY name ASC
        LIMIT 8
    """, (f"%{q}%", f"%{q}%"))
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
    cursor.execute("SELECT COUNT(*) AS v FROM sales WHERE DATE(sale_date) = CURDATE() AND status = 'completed'")
    today_count = cursor.fetchone()["v"]

    cursor.execute("SELECT COALESCE(SUM(total),0) AS v FROM sales WHERE DATE(sale_date) = CURDATE() AND status = 'completed'")
    today_revenue = float(cursor.fetchone()["v"])

    cursor.execute("SELECT COUNT(*) AS v FROM sales WHERE status = 'completed'")
    total_sales = cursor.fetchone()["v"]

    cursor.execute("SELECT COALESCE(SUM(total),0) AS v FROM sales WHERE status = 'completed'")
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
            INSERT INTO sales (invoice_no, customer, customer_id, total, note, status, cashier_id)
            VALUES (%s, %s, %s, %s, %s, 'completed', %s)
        """, (invoice_no, display_name, customer_id or None, total, note or None, session.get("user_id")))
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

# ── GET SINGLE PRODUCT ────────────────────────────────────────────────────────
@app.route("/get_product/<sku>")
@login_required
def get_product(sku):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.sku, p.name, p.category, p.price, p.stock,
               p.supplier_id, s.supplier_name
        FROM products p
        LEFT JOIN suppliers s ON p.supplier_id = s.id
        WHERE p.sku = %s
    """, (sku,))
    row = cursor.fetchone()
    db.close()
    if not row:
        return jsonify({"error": "Not found"}), 404
    return jsonify({
        "sku": row["sku"],
        "name": row["name"],
        "category": row["category"],
        "price": float(row["price"]),
        "stock": int(row["stock"]),
        "supplier_id": row["supplier_id"] or "",
        "supplier_name": row["supplier_name"] or ""
    })

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
    # Convert datetime objects to strings so the template can slice/display them safely
    for log in logs:
        if log.get("datetime") and hasattr(log["datetime"], "strftime"):
            log["datetime"] = log["datetime"].strftime("%Y-%m-%d %H:%M:%S")
        # Extract cashier name from note — notes end with "by <username>"
        note = log.get("note") or ""
        if " by " in note:
            log["cashier"] = note.split(" by ")[-1].strip()
        else:
            log["cashier"] = ""
    return render_template("activity_log.html", logs=logs, username=session["username"])

# ── BILLING COUNTER (Cashier POS) ─────────────────────────────────────────────

@app.route("/billing")
@login_required
def billing():
    """Full-screen supermarket — cashier only."""
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # All products for the product grid
    cursor.execute("""
        SELECT sku, name, category, price, stock
        FROM products
        ORDER BY category, name
    """)
    products = cursor.fetchall()

    # Distinct categories for filter chips
    cursor.execute("SELECT DISTINCT category FROM products ORDER BY category")
    categories = [r["category"] for r in cursor.fetchall()]

    # Today's stats (this cashier only)
    cashier_id = session.get("user_id")
    cursor.execute("""
        SELECT COUNT(*) AS v FROM sales
        WHERE DATE(sale_date) = CURDATE() AND status = 'completed'
        AND cashier_id = %s
    """, (cashier_id,))
    today_count = cursor.fetchone()["v"]

    cursor.execute("""
        SELECT COALESCE(SUM(total), 0) AS v FROM sales
        WHERE DATE(sale_date) = CURDATE() AND status = 'completed'
        AND cashier_id = %s
    """, (cashier_id,))
    today_revenue = float(cursor.fetchone()["v"])

    cursor.execute("""
        SELECT COALESCE(SUM(si.qty), 0) AS v
        FROM sale_items si
        JOIN sales s ON si.sale_id = s.id
        WHERE DATE(s.sale_date) = CURDATE() AND s.status = 'completed'
        AND s.cashier_id = %s
    """, (cashier_id,))
    today_items = int(cursor.fetchone()["v"])

    # Next invoice number
    cursor.execute("""
        SELECT invoice_no FROM sales
        ORDER BY CAST(SUBSTRING(invoice_no, 4) AS UNSIGNED) DESC
        LIMIT 1
    """)
    last = cursor.fetchone()
    if last and last["invoice_no"]:
        num = int(last["invoice_no"].replace("INV", ""))
        next_invoice = f"INV{num + 1:03d}"
    else:
        next_invoice = "INV001"

    db.close()

    return render_template(
        "billing.html",
        products=products,
        categories=categories,
        today_count=today_count,
        today_revenue=today_revenue,
        today_items=today_items,
        next_invoice=next_invoice,
        username=session["username"],
    )


@app.route("/billing/next_invoice")
@login_required
def billing_next_invoice():
    """Return the next invoice number as JSON (called after sale to refresh UI)."""
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
        return jsonify({"invoice_no": f"INV{num + 1:03d}"})
    return jsonify({"invoice_no": "INV001"})


@app.route("/billing/today_stats")
@login_required
def billing_today_stats():
    """Return today's summary stats as JSON for live refresh after a sale."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cashier_id = session.get("user_id")

    cursor.execute("""
        SELECT COUNT(*) AS v FROM sales
        WHERE DATE(sale_date) = CURDATE() AND status = 'completed'
        AND cashier_id = %s
    """, (cashier_id,))
    today_count = cursor.fetchone()["v"]

    cursor.execute("""
        SELECT COALESCE(SUM(total), 0) AS v FROM sales
        WHERE DATE(sale_date) = CURDATE() AND status = 'completed'
        AND cashier_id = %s
    """, (cashier_id,))
    today_revenue = float(cursor.fetchone()["v"])

    cursor.execute("""
        SELECT COALESCE(SUM(si.qty), 0) AS v
        FROM sale_items si
        JOIN sales s ON si.sale_id = s.id
        WHERE DATE(s.sale_date) = CURDATE() AND s.status = 'completed'
        AND s.cashier_id = %s
    """, (cashier_id,))
    today_items = int(cursor.fetchone()["v"])

    db.close()
    return jsonify({
        "today_count":   today_count,
        "today_revenue": today_revenue,
        "today_items":   today_items,
    })




# ── CASHIER: MY SALES ─────────────────────────────────────────────────────────
@app.route("/cashier/my-sales")
@login_required
def cashier_my_sales():
    if session.get("role") == "admin":
        return redirect(url_for("sales"))
    db = get_db()
    cursor = db.cursor(dictionary=True)

    date_filter = request.args.get("date", "today")
    cashier_id = session.get("user_id")

    if date_filter == "week":
        date_clause = "AND DATE(s.sale_date) >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)"
    elif date_filter == "month":
        date_clause = "AND MONTH(s.sale_date) = MONTH(CURDATE()) AND YEAR(s.sale_date) = YEAR(CURDATE())"
    else:
        date_filter = "today"
        date_clause = "AND DATE(s.sale_date) = CURDATE()"

    cursor.execute(f"""
        SELECT s.id, s.invoice_no,
               COALESCE(c.name, s.customer, '—') AS customer,
               c.phone AS customer_phone,
               s.total, s.sale_date, s.status, s.note,
               COALESCE(SUM(si.qty), 0) AS item_count
        FROM sales s
        LEFT JOIN customers c ON c.id = s.customer_id
        LEFT JOIN sale_items si ON si.sale_id = s.id
        WHERE s.cashier_id = {int(cashier_id)} {date_clause}
        GROUP BY s.id ORDER BY s.id DESC
    """)
    my_sales = cursor.fetchall()

    stats_date_clause = date_clause.replace("s.sale_date", "sale_date")
    cursor.execute(f"""
        SELECT COUNT(*) AS cnt, COALESCE(SUM(total),0) AS rev
        FROM sales WHERE status='completed' AND cashier_id = {int(cashier_id)} {stats_date_clause}
    """)
    stats = cursor.fetchone()

    db.close()
    return render_template("Cashier my sales.html",
        my_sales=my_sales,
        total_count=int(stats["cnt"]),
        total_revenue=float(stats["rev"]),
        date_filter=date_filter,
        username=session["username"],
    )


# ── CASHIER: CUSTOMERS ────────────────────────────────────────────────────────
@app.route("/cashier/customers")
@login_required
def cashier_customers():
    if session.get("role") == "admin":
        return redirect(url_for("customers"))
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cashier_id = session.get("user_id")
    # Show only customers who have had at least one sale with this cashier
    cursor.execute("""
        SELECT c.id, c.name, c.phone, c.email, c.created_at,
               COUNT(s.id) AS total_orders,
               COALESCE(SUM(s.total), 0) AS total_spent,
               MAX(s.sale_date) AS last_visit
        FROM customers c
        INNER JOIN sales s ON s.customer_id = c.id AND s.cashier_id = %s
        GROUP BY c.id ORDER BY c.id DESC
    """, (cashier_id,))
    customer_list = cursor.fetchall()
    # Convert datetime objects to strings for JSON safety
    for c in customer_list:
        if c.get("last_visit") and hasattr(c["last_visit"], "strftime"):
            c["last_visit"] = c["last_visit"].strftime("%Y-%m-%d %H:%M:%S")
        if c.get("created_at") and hasattr(c["created_at"], "strftime"):
            c["created_at"] = c["created_at"].strftime("%Y-%m-%d %H:%M:%S")
    db.close()
    return render_template("Cashier my customers.html",
        customers=customer_list,
        username=session["username"],
    )


# ── CASHIER: CUSTOMER SALES (JSON for modal) ──────────────────────────────────
@app.route("/cashier/customers/<int:customer_id>/sales")
@login_required
def cashier_customer_sales(customer_id):
    """Return all sales for a customer as JSON — used by the refund modal."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cashier_id = session.get("user_id")
    cursor.execute("""
        SELECT s.id, s.invoice_no, s.total, s.sale_date, s.status, s.note,
               COALESCE(SUM(si.qty), 0) AS item_count
        FROM sales s
        LEFT JOIN sale_items si ON si.sale_id = s.id
        WHERE s.customer_id = %s AND s.cashier_id = %s
        GROUP BY s.id
        ORDER BY s.id DESC
    """, (customer_id, cashier_id))
    sales = cursor.fetchall()
    db.close()
    result = []
    for s in sales:
        result.append({
            "id":         s["id"],
            "invoice_no": s["invoice_no"],
            "total":      float(s["total"]),
            "sale_date":  s["sale_date"].strftime("%d %b %Y, %I:%M %p") if s["sale_date"] else "—",
            "status":     s["status"],
            "note":       s["note"] or "",
            "item_count": int(s["item_count"]),
        })
    return jsonify(result)


@app.route("/cashier/sales/<int:sale_id>/items")
@login_required
def cashier_sale_items(sale_id):
    """Return line items for a specific sale — used by the refund detail view."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT si.sku, si.name, si.qty, si.unit_price, si.line_total
        FROM sale_items si
        WHERE si.sale_id = %s
        ORDER BY si.id
    """, (sale_id,))
    items = cursor.fetchall()
    db.close()
    return jsonify([{
        "sku":        r["sku"],
        "name":       r["name"],
        "qty":        int(r["qty"]),
        "unit_price": float(r["unit_price"]),
        "line_total": float(r["line_total"]),
    } for r in items])


def ensure_finance_settings(db_conn):
    """Auto-create finance_settings table and seed initial capital if missing."""
    try:
        c = db_conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS finance_settings (
                id            INT AUTO_INCREMENT PRIMARY KEY,
                setting_key   VARCHAR(100) NOT NULL UNIQUE,
                setting_value DECIMAL(15,2) NOT NULL DEFAULT 0.00,
                updated_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
                              ON UPDATE CURRENT_TIMESTAMP
            )
        """)
        c.execute("""
            INSERT IGNORE INTO finance_settings (setting_key, setting_value)
            VALUES ('initial_capital', 0.00)
        """)
        db_conn.commit()
        c.close()
    except Exception as e:
        print(f"[FINANCE SETTINGS] {e}")


def get_initial_capital(db_conn):
    """Return the stored initial capital float."""
    try:
        ensure_finance_settings(db_conn)
        c = db_conn.cursor(dictionary=True)
        c.execute(
            "SELECT setting_value FROM finance_settings WHERE setting_key='initial_capital'"
        )
        row = c.fetchone()
        c.close()
        return float(row["setting_value"]) if row else 0.0
    except Exception:
        return 0.0


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 3 — Add these two routes to app.py
# (paste them after the existing /reports route)
# ═══════════════════════════════════════════════════════════════════════════════

@app.route("/finance")
@admin_required
def finance():
    """Admin Finance overview — P&L, capital tracking, credit payables."""
    db     = get_db()
    cursor = db.cursor(dictionary=True)

    # ── Period filter ────────────────────────────────────────────────────────
    period = request.args.get("period", "month")
    period_labels = {
        "today": "Today",
        "week":  "This Week",
        "month": "This Month",
        "all":   "All Time",
    }
    period_label = period_labels.get(period, "This Month")

    if period == "today":
        date_clause  = "DATE(s.sale_date) = CURDATE()"
        date_clause2 = "DATE(sale_date) = CURDATE()"
    elif period == "week":
        date_clause  = "DATE(s.sale_date) >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)"
        date_clause2 = "DATE(sale_date) >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)"
    elif period == "all":
        date_clause  = "1=1"
        date_clause2 = "1=1"
    else:  # month
        period = "month"
        date_clause  = "MONTH(s.sale_date)=MONTH(CURDATE()) AND YEAR(s.sale_date)=YEAR(CURDATE())"
        date_clause2 = "MONTH(sale_date)=MONTH(CURDATE()) AND YEAR(sale_date)=YEAR(CURDATE())"

    # ── Revenue & sales count ────────────────────────────────────────────────
    cursor.execute(f"""
        SELECT
            COUNT(*) AS total_sales,
            COALESCE(SUM(s.total), 0) AS total_revenue
        FROM sales s
        WHERE s.status = 'completed' AND {date_clause}
    """)
    rev_row       = cursor.fetchone()
    total_sales   = int(rev_row["total_sales"])
    total_revenue = float(rev_row["total_revenue"])

    # ── Refunds in period ────────────────────────────────────────────────────
    cursor.execute(f"""
        SELECT COALESCE(SUM(s.total), 0) AS v
        FROM sales s
        WHERE s.status = 'refunded' AND {date_clause}
    """)
    refund_total = float(cursor.fetchone()["v"])

    # ── COGS — estimate as 90% of retail price × qty sold ───────────────────
    # Uses sale_items joined with products to get cost at time of sale
    cursor.execute(f"""
        SELECT COALESCE(SUM(si.line_total * 0.9), 0) AS cogs
        FROM sale_items si
        JOIN sales s ON si.sale_id = s.id
        WHERE s.status = 'completed' AND {date_clause}
    """)
    total_cogs = float(cursor.fetchone()["cogs"])
    gross_profit = total_revenue - total_cogs

    # ── Supplier credit payables (ALL TIME — obligations don't filter) ───────
    cursor.execute("""
        SELECT
            COALESCE(SUM(total_amount), 0)               AS total_billed,
            COALESCE(SUM(amount_paid),  0)               AS total_paid,
            COALESCE(SUM(total_amount - amount_paid), 0) AS total_due,
            SUM(CASE WHEN status != 'paid' THEN 1 ELSE 0 END) AS pending_invoices
        FROM supplier_purchases
    """)
    credit_row            = cursor.fetchone()
    credit_total_billed   = float(credit_row["total_billed"])
    total_paid_suppliers  = float(credit_row["total_paid"])
    total_pending         = float(credit_row["total_due"])
    pending_invoices      = int(credit_row["pending_invoices"])

    # ── Inventory value ──────────────────────────────────────────────────────
    cursor.execute("""
        SELECT
            COALESCE(SUM(price * stock), 0) AS inv_value,
            COUNT(*) AS total_products
        FROM products
    """)
    inv_row         = cursor.fetchone()
    inventory_value = float(inv_row["inv_value"])
    total_products  = int(inv_row["total_products"])

    # ── Credit by supplier ───────────────────────────────────────────────────
    cursor.execute("""
        SELECT
            s.supplier_name,
            COALESCE(SUM(sp.total_amount), 0)               AS total_billed,
            COALESCE(SUM(sp.amount_paid),  0)               AS total_paid,
            COALESCE(SUM(sp.total_amount - sp.amount_paid), 0) AS total_due,
            SUM(CASE WHEN sp.due_date < CURDATE()
                     AND sp.status != 'paid' THEN 1 ELSE 0 END) AS overdue_count
        FROM suppliers s
        LEFT JOIN supplier_purchases sp ON sp.supplier_id = s.id
        GROUP BY s.id, s.supplier_name
        HAVING total_billed > 0
        ORDER BY total_due DESC
    """)
    credit_by_supplier = cursor.fetchall()
    for row in credit_by_supplier:
        row["total_billed"] = float(row["total_billed"])
        row["total_paid"]   = float(row["total_paid"])
        row["total_due"]    = float(row["total_due"])

    # ── Open invoices detail ─────────────────────────────────────────────────
    cursor.execute("""
        SELECT
            sp.id, sp.invoice_ref, sp.total_amount, sp.amount_paid,
            (sp.total_amount - sp.amount_paid) AS balance,
            sp.purchase_date, sp.due_date, sp.status, sp.note,
            s.supplier_name
        FROM supplier_purchases sp
        JOIN suppliers s ON s.id = sp.supplier_id
        WHERE sp.status != 'paid'
        ORDER BY sp.due_date ASC, sp.purchase_date DESC
    """)
    open_invoices = cursor.fetchall()
    for inv in open_invoices:
        inv["total_amount"] = float(inv["total_amount"])
        inv["amount_paid"]  = float(inv["amount_paid"])
        inv["balance"]      = float(inv["balance"])
        due = inv.get("due_date")
        if due:
            from datetime import date as _date
            inv["is_overdue"] = (due < _date.today())
            inv["due_date"]   = due.strftime("%d %b %Y")
        else:
            inv["is_overdue"] = False
            inv["due_date"]   = None

    # ── Monthly revenue trend (last 6 months) ────────────────────────────────
    cursor.execute("""
        SELECT
            DATE_FORMAT(sale_date, '%b %Y') AS month,
            DATE_FORMAT(sale_date, '%Y-%m') AS sort_key,
            COUNT(*) AS sales,
            COALESCE(SUM(total), 0) AS revenue
        FROM sales
        WHERE status = 'completed'
        GROUP BY DATE_FORMAT(sale_date, '%Y-%m')
        ORDER BY sort_key DESC
        LIMIT 6
    """)
    monthly_trend = list(reversed([
        {"month": r["month"], "sales": int(r["sales"]), "revenue": float(r["revenue"])}
        for r in cursor.fetchall()
    ]))

    # ── Initial capital ──────────────────────────────────────────────────────
    initial_capital = get_initial_capital(db)

    cursor.close()
    db.close()

    fin = {
        "total_sales":            total_sales,
        "total_revenue":          total_revenue,
        "refund_total":           refund_total,
        "total_cogs":             total_cogs,
        "gross_profit":           gross_profit,
        "credit_total_billed":    credit_total_billed,
        "total_paid_to_suppliers":total_paid_suppliers,
        "total_pending":          total_pending,
        "pending_invoices":       pending_invoices,
        "inventory_value":        inventory_value,
        "total_products":         total_products,
    }

    return render_template(
        "finance.html",
        fin=fin,
        period=period,
        period_label=period_label,
        initial_capital=initial_capital,
        credit_by_supplier=credit_by_supplier,
        open_invoices=open_invoices,
        monthly_trend=monthly_trend,
        username=session["username"],
    )


@app.route("/finance/set_capital", methods=["POST"])
@admin_required
def finance_set_capital():
    """Update the stored initial capital."""
    capital = float(request.form.get("capital", 0) or 0)
    try:
        db = get_db()
        ensure_finance_settings(db)
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO finance_settings (setting_key, setting_value)
            VALUES ('initial_capital', %s)
            ON DUPLICATE KEY UPDATE setting_value = %s
        """, (capital, capital))
        db.commit()
        cursor.close()
        db.close()
        flash(f"Initial capital updated to ₹{capital:,.2f}", "success")
    except Exception as e:
        flash(f"Error: {e}", "error")
    return redirect(url_for("finance"))

if __name__ == "__main__":
    app.run(debug=True)