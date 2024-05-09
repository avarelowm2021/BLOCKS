import tkinter as tk
from tkinter import messagebox
import sqlite3

class DatabaseApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Simple Database App")
        self.master.configure(bg="black")

        self.label = tk.Label(master, text="Entrez une donnée :", fg="white", bg="black")
        self.label.grid(row=0, column=0, padx=10, pady=10)

        self.data_entry = tk.Entry(master)
        self.data_entry.grid(row=0, column=1, padx=10, pady=10)
        self.data_entry.bind("<KeyRelease>", self.start_timer)

        self.listbox_frame = tk.Frame(master, bg="black")
        self.listbox_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        self.listbox = tk.Listbox(self.listbox_frame, bg="black", fg="white", width=50, height=10)
        self.listbox.grid(row=0, column=0, padx=10, pady=10)
        self.listbox.bind('<<ListboxSelect>>', self.display_selected_data)

        self.details_label = tk.Label(master, text="Détails :", fg="white", bg="black")
        self.details_label.grid(row=2, column=0, padx=10, pady=10)

        self.details_text = tk.Text(master, height=5, width=50, bg="black", fg="white")
        self.details_text.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

        # Créer la base de données et la table si elles n'existent pas
        self.create_database()

        # Variable pour stocker l'ID du timer
        self.timer_id = None

    def create_database(self):
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS data
                               (id INTEGER PRIMARY KEY, value TEXT)''')
        self.conn.commit()

    def add_data(self, data):
        if data:
            if not self.check_duplicate(data):
                self.cursor.execute("INSERT INTO data (value) VALUES (?)", (data,))
                self.conn.commit()
                self.display_data()
            else:
                messagebox.showerror("Erreur", "Donnée invalide ou déjà inscrite", icon='error')

    def check_duplicate(self, data):
        self.cursor.execute("SELECT * FROM data WHERE value=?", (data,))
        row = self.cursor.fetchone()
        return row is not None

    def display_data(self):
        self.listbox.delete(0, tk.END)
        self.cursor.execute("SELECT * FROM data")
        rows = self.cursor.fetchall()
        for row in rows:
            self.listbox.insert(tk.END, row[1])
            print(row[1])  # Afficher les données dans la console

    def display_selected_data(self, event):
        index = self.listbox.curselection()[0]
        data = self.listbox.get(index)
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(tk.END, f"Data: {data}")

    def start_timer(self, event):
        if self.timer_id:
            self.master.after_cancel(self.timer_id)
        self.timer_id = self.master.after(2000, self.add_data_from_entry)  # Appeler add_data_from_entry après 2 secondes

    def add_data_from_entry(self):
        data = self.data_entry.get()
        self.add_data(data)
        self.clear_data_entry()

    def clear_data_entry(self):
        self.data_entry.delete(0, tk.END)

def main():
    root = tk.Tk()
    root.configure(bg="black")
    app = DatabaseApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
