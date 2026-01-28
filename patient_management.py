import logging

# ---------- LOGGING SETUP ----------
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

patients = []
DATA_FILE = "patients.txt"

# ---------- VALIDATION ----------

def is_valid_patient_id(pid):
    return pid.startswith("P") and pid[1:].isdigit()

def is_duplicate_id(pid):
    for p in patients:
        if p["id"] == pid:
            return True
    return False

# ---------- FILE HANDLING ----------

def load_from_file():
    try:
        with open(DATA_FILE, "r") as file:
            for line in file:
                data = line.strip().split(",")

                if len(data) != 5:
                    logging.warning("Skipping corrupted line in file")
                    continue

                pid, name, age, disease, doctor = data

                if not is_valid_patient_id(pid):
                    logging.warning(f"Invalid patient ID found: {pid}")
                    continue

                patients.append({
                    "id": pid,
                    "name": name,
                    "age": age,
                    "disease": disease,
                    "doctor": doctor
                })

        logging.info("Patient data loaded successfully")

    except FileNotFoundError:
        logging.info("patients.txt not found. Starting with empty records")

def append_patient_to_file(patient):
    with open(DATA_FILE, "a") as file:
        file.write(
            f"{patient['id']},{patient['name']},{patient['age']},"
            f"{patient['disease']},{patient['doctor']}\n"
        )

def rewrite_file():
    with open(DATA_FILE, "w") as file:
        for p in patients:
            file.write(
                f"{p['id']},{p['name']},{p['age']},"
                f"{p['disease']},{p['doctor']}\n"
            )

# ---------- DISPLAY ----------

def display_header():
    print("\nID     Name       Age   Disease       Doctor")
    print("-----------------------------------------------")

def display_patient(p):
    print(f"{p['id']:<6} {p['name']:<10} {p['age']:<5} {p['disease']:<12} {p['doctor']}")

# ---------- CORE FEATURES ----------

def add_patient():
    pid = input("Enter Patient ID: ")

    if not is_valid_patient_id(pid):
        print("Invalid Patient ID format. Use format like P101.")
        logging.error(f"Invalid Patient ID entered: {pid}")
        return

    if is_duplicate_id(pid):
        print("Patient ID already exists.")
        logging.error(f"Duplicate Patient ID attempted: {pid}")
        return

    name = input("Enter Name: ")
    age = input("Enter Age: ")
    disease = input("Enter Disease: ")
    doctor = input("Enter Doctor Name: ")

    patient = {
        "id": pid,
        "name": name,
        "age": age,
        "disease": disease,
        "doctor": doctor
    }

    patients.append(patient)
    append_patient_to_file(patient)

    logging.info(f"Patient added successfully: {pid}")
    print("Patient added and saved successfully")

def search_by_name():
    key = input("Enter patient name to search: ").lower()
    found = False

    display_header()
    for p in patients:
        if key in p["name"].lower():
            display_patient(p)
            found = True

    if not found:
        print("Patient not found")

def search_by_id():
    key = input("Enter Patient ID to search: ").lower()
    found = False

    display_header()
    for p in patients:
        if key in p["id"].lower():
            display_patient(p)
            found = True

    if not found:
        print("Patient not found")

def search_by_doctor():
    key = input("Enter Doctor Name: ").lower()
    found = False

    display_header()
    for p in patients:
        if key in p["doctor"].lower():
            display_patient(p)
            found = True

    if not found:
        print("No patients found for this doctor")

def update_patient_by_id():
    pid = input("Enter Patient ID to update: ")

    for p in patients:
        if p["id"] == pid:
            print("Leave blank to keep existing value")

            new_name = input(f"Enter Name [{p['name']}]: ")
            new_age = input(f"Enter Age [{p['age']}]: ")
            new_disease = input(f"Enter Disease [{p['disease']}]: ")
            new_doctor = input(f"Enter Doctor [{p['doctor']}]: ")

            if new_name.strip():
                p["name"] = new_name
            if new_age.strip():
                p["age"] = new_age
            if new_disease.strip():
                p["disease"] = new_disease
            if new_doctor.strip():
                p["doctor"] = new_doctor

            rewrite_file()
            logging.info(f"Patient record updated: {pid}")
            print("Patient record updated successfully")
            return

    logging.warning(f"Update attempted for non-existing ID: {pid}")
    print("Patient ID not found")

def delete_patient_by_id():
    pid = input("Enter Patient ID to delete: ")

    for p in patients:
        if p["id"] == pid:
            patients.remove(p)
            rewrite_file()

            logging.info(f"Patient record deleted: {pid}")
            print("Patient record deleted successfully")
            return

    logging.warning(f"Delete attempted for non-existing ID: {pid}")
    print("Patient ID not found")

# ---------- PROGRAM START ----------

load_from_file()

while True:
    print("\n===== Hospital Management System =====")
    print("1. Add Patient")
    print("2. Search Patient by Name")
    print("3. Search Patient by ID")
    print("4. Update Patient by ID")
    print("5. Delete Patient by ID")
    print("6. View Patients by Doctor")
    print("7. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        add_patient()
    elif choice == "2":
        search_by_name()
    elif choice == "3":
        search_by_id()
    elif choice == "4":
        update_patient_by_id()
    elif choice == "5":
        delete_patient_by_id()
    elif choice == "6":
        search_by_doctor()
    elif choice == "7":
        print("Exiting system...")
        break
    else:
        print("Invalid choice")
