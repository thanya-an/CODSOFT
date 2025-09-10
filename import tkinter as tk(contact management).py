import tkinter as tk
from tkinter import messagebox, simpledialog


phonebook = {}

def save_entry():
    """Store a new person into the phonebook"""
    person = full_name.get().strip()
    number = phone_no.get().strip()
    mail = email_id.get().strip()
    place = addr.get().strip()

    if person and number:
        phonebook[person] = {"phone": number, "email": mail, "address": place}
        refresh_list()
        reset_inputs()
        status_label.config(text=f"✔ Contact '{person}' saved!")
    else:
        messagebox.showwarning("Missing Data", "Please provide both name and phone.")

def refresh_list():
    """Update listbox display with current contacts"""
    records.delete(0, tk.END)
    for person, info in phonebook.items():
        records.insert(tk.END, f"{person} ({info['phone']})")

def reset_inputs():
    """Clear all entry fields"""
    full_name.delete(0, tk.END)
    phone_no.delete(0, tk.END)
    email_id.delete(0, tk.END)
    addr.delete(0, tk.END)

def show_details():
    """Show details of the chosen person"""
    selected = records.curselection()
    if selected:
        person = list(phonebook.keys())[selected[0]]
        info = phonebook[person]
        messagebox.showinfo("Details", 
                            f"👤 {person}\n📞 {info['phone']}\n📧 {info['email']}\n🏠 {info['address']}")
    else:
        status_label.config(text="⚠ Select a contact first.")

def remove_entry():
    """Remove a chosen person from phonebook"""
    selected = records.curselection()
    if selected:
        person = list(phonebook.keys())[selected[0]]
        if messagebox.askyesno("Confirm", f"Delete '{person}' permanently?"):
            del phonebook[person]
            refresh_list()
            status_label.config(text=f"❌ Contact '{person}' removed.")
    else:
        status_label.config(text="⚠ No contact selected.")

def search_entry():
    """Look for a person by name or phone"""
    keyword = simpledialog.askstring("Search", "Enter name or number:")
    if keyword:
        results = [f"{p} ({i['phone']})" for p, i in phonebook.items()
                   if keyword.lower() in p.lower() or keyword in i["phone"]]
        records.delete(0, tk.END)
        if results:
            for item in results:
                records.insert(tk.END, item)
        else:
            messagebox.showinfo("No Match", "No contact found.")

def edit_entry():
    """Modify existing contact info"""
    selected = records.curselection()
    if selected:
        person = list(phonebook.keys())[selected[0]]
        info = phonebook[person]

        new_person = simpledialog.askstring("Edit Name", "Update name:", initialvalue=person)
        new_num = simpledialog.askstring("Edit Phone", "Update phone:", initialvalue=info["phone"])
        new_mail = simpledialog.askstring("Edit Email", "Update email:", initialvalue=info["email"])
        new_place = simpledialog.askstring("Edit Address", "Update address:", initialvalue=info["address"])

        if new_person and new_num:
            if new_person != person:
                del phonebook[person]
            phonebook[new_person] = {"phone": new_num, "email": new_mail, "address": new_place}
            refresh_list()
            status_label.config(text=f"✏ Contact '{new_person}' updated.")
        else:
            messagebox.showwarning("Error", "Name and Phone cannot be empty.")
    else:
        status_label.config(text="⚠ Select a contact first.")


app = tk.Tk()
app.title("My Phonebook")
app.geometry("560x560")
app.configure(bg="#1E272E")

# Heading
header = tk.Label(app, text="Contact Manager", font=("Calibri", 20, "bold"),
                  fg="white", bg="#0A3D62", pady=10)
header.pack(fill="x")

# Input Section
frame = tk.Frame(app, bg="#2C3A47", bd=5, relief="ridge")
frame.pack(pady=10)

tk.Label(frame, text="Full Name:", fg="white", bg="#2C3A47").grid(row=0, column=0, sticky="w", padx=5, pady=5)
full_name = tk.Entry(frame, width=28)
full_name.grid(row=0, column=1, padx=5)

tk.Label(frame, text="Phone No:", fg="white", bg="#2C3A47").grid(row=1, column=0, sticky="w", padx=5, pady=5)
phone_no = tk.Entry(frame, width=28)
phone_no.grid(row=1, column=1, padx=5)

tk.Label(frame, text="Email ID:", fg="white", bg="#2C3A47").grid(row=2, column=0, sticky="w", padx=5, pady=5)
email_id = tk.Entry(frame, width=28)
email_id.grid(row=2, column=1, padx=5)

tk.Label(frame, text="Address:", fg="white", bg="#2C3A47").grid(row=3, column=0, sticky="w", padx=5, pady=5)
addr = tk.Entry(frame, width=28)
addr.grid(row=3, column=1, padx=5)

# Buttons
tk.Button(app, text=" Save", command=save_entry, bg="#27AE60", fg="white", width=12).pack(pady=5)

records = tk.Listbox(app, width=50, height=12, font=("Consolas", 11))
records.pack(pady=10)

btns = tk.Frame(app, bg="#1E272E")
btns.pack()

tk.Button(btns, text=" Search", command=search_entry, bg="#8E44AD", fg="white", width=10).grid(row=0, column=0, padx=5)
tk.Button(btns, text=" View", command=show_details, bg="#2980B9", fg="white", width=10).grid(row=0, column=1, padx=5)
tk.Button(btns, text="Edit", command=edit_entry, bg="#F39C12", fg="white", width=10).grid(row=0, column=2, padx=5)
tk.Button(btns, text=" Delete", command=remove_entry, bg="#C0392B", fg="white", width=10).grid(row=0, column=3, padx=5)

# Status bar
status_label = tk.Label(app, text="Welcome to Phonebook!", fg="white", bg="#0A3D62", anchor="w")
status_label.pack(fill="x", side="bottom")

app.mainloop()
