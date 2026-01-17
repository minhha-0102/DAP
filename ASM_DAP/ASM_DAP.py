import pyodbc

# =========================
# DATABASE CONNECTION
# =========================
def connect_db():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost\\SQLEXPRESS;"
        "DATABASE=product_dap;"
        "Trusted_Connection=yes;"
    )

# =========================
# VALIDATION
# =========================
def validate_product(name, quantity, price, size):
    if len(name) <= 1 or len(name) >= 33:
        print("❌ Name length must be greater than 1 and less than 33")
        return False
    if quantity <= 10:
        print("❌ Quantity must be greater than 10")
        return False
    if price <= 0 or price >= 1000:
        print("❌ Price must be greater than 0 and less than 1000")
        return False
    if size not in ['T', 'S', 'M', 'L', 'B', 'H']:
        print("❌ Size must be T, S, M, L, B or H")
        return False
    return True

# =========================
# ADD PRODUCT (4 POINTS)
# =========================
def add_product():
    name = input("Name: ")
    quantity = int(input("Quantity: "))
    price = float(input("Price: "))
    size = input("Size (T/S/M/L/B/H): ").upper()
    status = int(input("Status (1 = New, 0 = Old): "))
    date_import = input("Date import (YYYY-MM-DD): ")

    if not validate_product(name, quantity, price, size):
        return

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO products
        (name, quantity, price, size, status, date_import)
        VALUES (?, ?, ?, ?, ?, ?)
    """, name, quantity, price, size, status, date_import)

    conn.commit()
    conn.close()
    print("✔ Product added successfully")

# =========================
# VIEW PRODUCTS (4 POINTS)
# =========================
def view_products():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")

    print("\nID | Name | Quantity | Price | Size | Status | Date Import")
    for p in cursor.fetchall():
        print(f"{p.id} | {p.name} | {p.quantity} | {p.price} | "
              f"{p.size} | {'New' if p.status else 'Old'} | {p.date_import}")

    conn.close()

# =========================
# UPDATE PRODUCT (4 POINTS)
# =========================
def update_product():
    product_id = int(input("Enter product ID to update: "))

    name = input("New name: ")
    quantity = int(input("New quantity: "))
    price = float(input("New price: "))
    size = input("New size (T/S/M/L/B/H): ").upper()
    status = int(input("New status (1 = New, 0 = Old): "))

    if not validate_product(name, quantity, price, size):
        return

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE products
        SET name=?, quantity=?, price=?, size=?, status=?
        WHERE id=?
    """, name, quantity, price, size, status, product_id)

    conn.commit()
    conn.close()
    print("✔ Product updated successfully")

# =========================
# DELETE PRODUCT (3 POINTS)
# =========================
def delete_product():
    product_id = int(input("Enter product ID to delete: "))
    confirm = input("Are you sure? (y/n): ")

    if confirm.lower() != 'y':
        print("❌ Delete cancelled")
        return

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", product_id)
    conn.commit()
    conn.close()
    print("✔ Product deleted successfully")

# =========================
# MENU
# =========================
def main():
    while True:
        print("""
====== PRODUCT MANAGEMENT SYSTEM ======
1. Add product
2. View products
3. Update product
4. Delete product
0. Exit
======================================
""")
        choice = input("Choose an option: ")

        if choice == "1":
            add_product()
        elif choice == "2":
            view_products()
        elif choice == "3":
            update_product()
        elif choice == "4":
            delete_product()
        elif choice == "0":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
