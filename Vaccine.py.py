from tkinter import *
from tkinter import ttk, messagebox
import os

# File to store user and patient data
USER_DATA_FILE = "users.txt"
PATIENT_DATA_FILE = "patients.txt"

# Function to save user credentials
def save_user(username, password):
    with open(USER_DATA_FILE, "a") as file:
        file.write(f"{username},{password}\n")

# Function to validate login credentials
def validate_login(username, password):
    try:
        with open(USER_DATA_FILE, "r") as file:
            for line in file:
                stored_user, stored_pass = line.strip().split(",")
                if stored_user == username and stored_pass == password:
                    return True
    except FileNotFoundError:
        return False
    return False

# Function to save patient details
def save_patient(name, contact, gender, vaccine, date, slot, city):
    with open(PATIENT_DATA_FILE, "a") as file:
        file.write(f"{name},{contact},{gender},{vaccine},{date},{slot},{city}\n")

# Function to get all patient details
def get_all_patients():
    try:
        with open(PATIENT_DATA_FILE, "r") as file:
            return [line.strip().split(",") for line in file.readlines()]
    except FileNotFoundError:
        return []

# Function to delete selected patient
def delete_patient(selected_item, tree):
    if not selected_item:
        messagebox.showerror("Error", "No patient selected!")
        return
    
    patients = get_all_patients()
    patient_data = tree.item(selected_item)["values"]

    if patient_data:
        updated_patients = [p for p in patients if p[:7] != patient_data]  # Remove selected patient
        with open(PATIENT_DATA_FILE, "w") as file:
            for p in updated_patients:
                file.write(",".join(p) + "\n")

        tree.delete(selected_item)
        messagebox.showinfo("Success", "Patient record deleted!")

# First Page: Main Menu
def main_menu():
    root = Tk()
    root.geometry('400x300')
    root.title("Vaccine Booking System")

    Label(root, text="Vaccine Booking", font=("bold", 18)).pack(pady=10)
    Button(root, text='Login', width=20, bg='brown', fg='white', command=lambda: [root.destroy(), login()]).pack(pady=5)
    Button(root, text='New User', width=20, bg='black', fg='white', command=lambda: [root.destroy(), register()]).pack(pady=5)
    Button(root, text='Exit', width=20, bg='red', fg='white', command=root.destroy).pack(pady=5)

    root.mainloop()

# Login Page
def login():
    login_window = Tk()
    login_window.geometry('400x300')
    login_window.title("Login Page")

    Label(login_window, text="User Login", font=("bold", 16)).pack(pady=10)
    Label(login_window, text="Username").pack()
    entry_username = Entry(login_window)
    entry_username.pack()

    Label(login_window, text="Password").pack()
    entry_password = Entry(login_window, show="*")
    entry_password.pack()

    def attempt_login():
        username = entry_username.get()
        password = entry_password.get()
        if validate_login(username, password):
            messagebox.showinfo("Login Success", "Welcome!")
            login_window.destroy()
            after_login()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    Button(login_window, text='Login', width=20, bg='brown', fg='white', command=attempt_login).pack(pady=10)
    login_window.mainloop()

# New User Registration
def register():
    register_window = Tk()
    register_window.geometry('400x300')
    register_window.title("Registration")

    Label(register_window, text="Register", font=("bold", 16)).pack(pady=10)
    Label(register_window, text="Username").pack()
    entry_username = Entry(register_window)
    entry_username.pack()

    Label(register_window, text="Password").pack()
    entry_password = Entry(register_window, show="*")
    entry_password.pack()

    def submit_registration():
        username = entry_username.get()
        password = entry_password.get()
        if username and password:
            save_user(username, password)
            messagebox.showinfo("Success", "Registration Successful!")
            register_window.destroy()
            main_menu()
        else:
            messagebox.showerror("Error", "All fields are required!")

    Button(register_window, text='Register', width=20, bg='black', fg='white', command=submit_registration).pack(pady=10)
    register_window.mainloop()

# After Login Page
def after_login():
    after_login_window = Tk()
    after_login_window.geometry('400x300')
    after_login_window.title("Dashboard")

    Label(after_login_window, text="Dashboard", font=("bold", 18)).pack(pady=10)
    Button(after_login_window, text='Patient Registration', width=20, bg='brown', fg='white', command=lambda: [after_login_window.destroy(), register_patient()]).pack(pady=5)
    Button(after_login_window, text='View Patients', width=20, bg='blue', fg='white', command=lambda: [after_login_window.destroy(), view_patients()]).pack(pady=5)
    Button(after_login_window, text='Exit', width=20, bg='red', fg='white', command=after_login_window.destroy).pack(pady=5)

    after_login_window.mainloop()

# Patient Registration
def register_patient():
    patient_window = Tk()
    patient_window.geometry('400x500')
    patient_window.title("Patient Registration")

    Label(patient_window, text="Patient Registration", font=("bold", 16)).pack(pady=10)
    Label(patient_window, text="Full Name").pack()
    entry_name = Entry(patient_window)
    entry_name.pack()

    Label(patient_window, text="Contact Number").pack()
    entry_contact = Entry(patient_window)
    entry_contact.pack()

    Label(patient_window, text="Gender").pack()
    gender_var = StringVar(value="Male")
    Radiobutton(patient_window, text="Male", variable=gender_var, value="Male").pack()
    Radiobutton(patient_window, text="Female", variable=gender_var, value="Female").pack()

    Label(patient_window, text="Vaccine Type").pack()
    vaccine_var = StringVar(value="Covaxin")
    vaccine_options = ttk.Combobox(patient_window, textvariable=vaccine_var, values=["Covaxin", "Covishield", "Sputnik V"])
    vaccine_options.pack()

    Label(patient_window, text="Date (DD/MM/YYYY)").pack()
    entry_date = Entry(patient_window)
    entry_date.pack()

    Label(patient_window, text="Slot (Morning/Afternoon)").pack()
    entry_slot = Entry(patient_window)
    entry_slot.pack()

    Label(patient_window, text="City").pack()
    entry_city = Entry(patient_window)
    entry_city.pack()

    def submit_patient():
        save_patient(entry_name.get(), entry_contact.get(), gender_var.get(), vaccine_var.get(), entry_date.get(), entry_slot.get(), entry_city.get())
        messagebox.showinfo("Success", "Patient Registered Successfully!")
        patient_window.destroy()
        after_login()

    Button(patient_window, text='Register', width=20, bg='brown', fg='white', command=submit_patient).pack(pady=10)
    patient_window.mainloop()

# View Patients with Delete Option
def view_patients():
    view_window = Tk()
    view_window.geometry('600x400')
    view_window.title("Registered Patients")

    Label(view_window, text="Registered Patients", font=("bold", 16)).pack(pady=10)

    tree = ttk.Treeview(view_window, columns=("Name", "Contact", "Gender", "Vaccine", "Date", "Slot", "City"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
    for patient in get_all_patients():
        tree.insert("", "end", values=patient)
    tree.pack()

    Button(view_window, text='Delete Selected', width=20, bg='red', fg='white', command=lambda: delete_patient(tree.selection(), tree)).pack(pady=5)
    Button(view_window, text='Back', width=20, bg='black', fg='white', command=lambda: [view_window.destroy(), after_login()]).pack(pady=10)

    view_window.mainloop()

# Start Program
main_menu()


