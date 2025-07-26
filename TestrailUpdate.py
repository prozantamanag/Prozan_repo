import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import requests
import threading

class TestRailUpdaterGUI:
    def __init__(self, master):
        self.master = master
        master.title("TestRail CSV Results Updater")

        # TestRail Fields
        tk.Label(master, text="TestRail URL:").grid(row=0, column=0, sticky="e")
        self.url_entry = tk.Entry(master, width=40)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(master, text="Username:").grid(row=1, column=0, sticky="e")
        self.user_entry = tk.Entry(master, width=40)
        self.user_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(master, text="API Key/Password:").grid(row=2, column=0, sticky="e")
        self.pass_entry = tk.Entry(master, width=40, show="*")
        self.pass_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(master, text="Test Run ID:").grid(row=3, column=0, sticky="e")
        self.run_entry = tk.Entry(master, width=40)
        self.run_entry.grid(row=3, column=1, padx=5, pady=5)

        # CSV File Selector
        tk.Label(master, text="CSV File:").grid(row=4, column=0, sticky="e")
        self.csv_path = tk.StringVar()
        tk.Entry(master, textvariable=self.csv_path, width=30).grid(row=4, column=1, sticky="w", padx=5, pady=5)
        tk.Button(master, text="Browse", command=self.browse_csv).grid(row=4, column=2, padx=5, pady=5)

        # Update Button
        self.update_btn = tk.Button(master, text="Update TestRail", command=self.start_update)
        self.update_btn.grid(row=5, column=1, pady=10)

        # Status
        self.status_text = tk.StringVar()
        self.status_label = tk.Label(master, textvariable=self.status_text, fg="blue")
        self.status_label.grid(row=6, column=0, columnspan=3, pady=5)

    def browse_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.csv_path.set(file_path)

    def start_update(self):
        # Run the update in a separate thread to avoid freezing the GUI
        t = threading.Thread(target=self.update_testrail)
        t.start()

    def update_testrail(self):
        url = self.url_entry.get().strip()
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()
        run_id = self.run_entry.get().strip()
        csv_file = self.csv_path.get().strip()

        if not all([url, username, password, run_id, csv_file]):
            self.set_status("Please fill in all fields.", error=True)
            return

        self.set_status("Updating TestRail... Please wait.", error=False)
        try:
            with open(csv_file, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    case_id = row.get('case_id')
                    status_id = row.get('status_id')
                    comment = row.get('comment', '')
                    if not (case_id and status_id):
                        continue
                    api_url = f"{url}/index.php?/api/v2/add_result_for_case/{run_id}/{case_id}"
                    auth = (username, password)
                    payload = {
                        "status_id": int(status_id),
                        "comment": comment
                    }
                    resp = requests.post(api_url, json=payload, auth=auth)
                    if resp.status_code == 200:
                        self.set_status(f"Updated case {case_id}", error=False)
                    else:
                        self.set_status(f"Failed to update case {case_id}: {resp.text}", error=True)
            self.set_status("All updates complete!", error=False)
            messagebox.showinfo("Success", "TestRail update completed.")
        except Exception as e:
            self.set_status(f"Error: {str(e)}", error=True)
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

    def set_status(self, message, error=False):
        self.status_text.set(message)
        self.status_label.config(fg="red" if error else "blue")

if __name__ == "__main__":
    root = tk.Tk()
    gui = TestRailUpdaterGUI(root)
    root.mainloop()