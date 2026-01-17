import pyodbc
from datetime import datetime

# =========================
# DATABASE CONNECTION
# =========================
def connect_db():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost\\SQLEXPRESS;"
        "DATABASE=medical_service;"
        "Trusted_Connection=yes;"
    )
    return conn


# =========================
# ADD 3 PATIENTS
# =========================
def add_patients():
    conn = connect_db()
    cursor = conn.cursor()

    for i in range(3):
        print(f"\nEnter patient {i+1}")
        full_name = input("Full name: ")
        dob = input("Date of birth (YYYY-MM-DD): ")
        gender = input("Gender: ")
        address = input("Address: ")
        phone = input("Phone number: ")
        email = input("Email: ")

        cursor.execute("""
            INSERT INTO patients
            (full_name, date_of_birth, gender, address, phone_number, email)
            VALUES (?, ?, ?, ?, ?, ?)
        """, full_name, dob, gender, address, phone, email)

    conn.commit()
    conn.close()
    print("✔ Successfully added 3 patients")


# =========================
# ADD 5 DOCTORS
# =========================
def add_doctors():
    conn = connect_db()
    cursor = conn.cursor()

    for i in range(5):
        print(f"\nEnter doctor {i+1}")
        full_name = input("Full name: ")
        specialization = input("Specialization: ")
        phone = input("Phone number: ")
        email = input("Email: ")
        experience = int(input("Years of experience: "))

        cursor.execute("""
            INSERT INTO doctors
            (full_name, specialization, phone_number, email, years_of_experience)
            VALUES (?, ?, ?, ?, ?)
        """, full_name, specialization, phone, email, experience)

    conn.commit()
    conn.close()
    print("✔ Successfully added 5 doctors")


# =========================
# ADD 3 APPOINTMENTS
# =========================
def add_appointments():
    conn = connect_db()
    cursor = conn.cursor()

    for i in range(3):
        print(f"\nEnter appointment {i+1}")
        patient_id = int(input("Patient ID: "))
        doctor_id = int(input("Doctor ID: "))
        appointment_date = input("Appointment date (YYYY-MM-DD HH:MM): ")
        reason = input("Reason: ")

        cursor.execute("""
            INSERT INTO appointments
            (patient_id, doctor_id, appointment_date, reason)
            VALUES (?, ?, ?, ?)
        """, patient_id, doctor_id, appointment_date, reason)

    conn.commit()
    conn.close()
    print("✔ Successfully added 3 appointments")


# =========================
# REPORT APPOINTMENTS
# =========================
def report_appointments():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            p.full_name AS patient_name,
            YEAR(p.date_of_birth) AS birth_year,
            p.gender,
            p.address,
            d.full_name AS doctor_name,
            a.reason,
            CAST(a.appointment_date AS DATE) AS appointment_date
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        JOIN doctors d ON a.doctor_id = d.doctor_id
    """)

    print("\n========= APPOINTMENT REPORT =========")
    print("No | Patient | Birth | Gender | Address | Doctor | Reason | Date")

    for i, row in enumerate(cursor.fetchall(), start=1):
        print(f"{i} | {row.patient_name} | {row.birth_year} | {row.gender} | "
              f"{row.address} | {row.doctor_name} | {row.reason} | {row.appointment_date}")

    conn.close()


# =========================
# GET TODAY APPOINTMENTS
# =========================
def today_appointments():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            p.address,
            p.full_name,
            YEAR(p.date_of_birth) AS birth_year,
            p.gender,
            d.full_name AS doctor_name,
            a.status,
            a.reason
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        JOIN doctors d ON a.doctor_id = d.doctor_id
        WHERE CAST(a.appointment_date AS DATE) = CAST(GETDATE() AS DATE)
    """)

    print("\n========= TODAY APPOINTMENTS =========")
    print("Address | Patient | Birth | Gender | Doctor | Status | Note")

    for row in cursor.fetchall():
        print(f"{row.address} | {row.full_name} | {row.birth_year} | "
              f"{row.gender} | {row.doctor_name} | {row.status} | {row.reason}")

    conn.close()


# =========================
# MAIN MENU
# =========================
def main():
    while True:
        print("""
========= MEDICAL SERVICE SYSTEM =========
1. Add 3 patients
2. Add 5 doctors
3. Add 3 appointments
4. Appointment report
5. Get today's appointments
0. Exit
========================================
""")
        choice = input("Choose an option: ")

        if choice == "1":
            add_patients()
        elif choice == "2":
            add_doctors()
        elif choice == "3":
            add_appointments()
        elif choice == "4":
            report_appointments()
        elif choice == "5":
            today_appointments()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("❌ Invalid choice, try again")


# =========================
# RUN PROGRAM
# =========================
if __name__ == "__main__":
    main()
