from pymongo import MongoClient
import tkinter as tk
from tkinter import messagebox

class UpdateWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Update Data")
        
        self.anime_label = tk.Label(self.master, text="Enter Anime:")
        self.anime_label.grid(row=0, column=0, padx=5, pady=5)
        self.anime_entry = tk.Entry(self.master)
        self.anime_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.collection_label = tk.Label(self.master, text="Select Collection:")
        self.collection_label.grid(row=1, column=0, padx=5, pady=5)
        self.collection_var = tk.StringVar()
        self.collection_var.set("anime 40")
        self.collection_radio1 = tk.Radiobutton(self.master, text="Anime 40", variable=self.collection_var, value="anime40")
        self.collection_radio1.grid(row=1, column=1, padx=5, pady=5)
        self.collection_radio2 = tk.Radiobutton(self.master, text="Anime 401", variable=self.collection_var, value="anime401")
        self.collection_radio2.grid(row=1, column=2, padx=5, pady=5)
        self.collection_radio3 = tk.Radiobutton(self.master, text="Anime402", variable=self.collection_var, value="anime402")
        self.collection_radio3.grid(row=1, column=3, padx=5, pady=5)
        
        self.submit_button = tk.Button(self.master, text="Submit", command=self.retrieve_data)
        self.submit_button.grid(row=2, columnspan=4, padx=5, pady=5)
        
    def retrieve_data(self):
        anime_name = self.anime_entry.get()
        collection_name = self.collection_var.get()
        
        if anime_name.strip() == "":
            messagebox.showerror("Error", "Please enter an anime name.")
            return

        try:
            client = MongoClient('mongodb://localhost:27017')
            db = client['anime_db']
            collection = db[collection_name]
            
            result = collection.find_one({'Name': anime_name})
            if result:
                self.open_edit_window(result, collection)
            else:
                messagebox.showinfo("Info", "No data found for the given anime name.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def open_edit_window(self, data, collection):
        self.edit_window = tk.Toplevel(self.master)
        self.edit_window.title("Edit Data")

        self.result_text = tk.Text(self.edit_window, height=20, width=100)
        self.result_text.grid(row=0, columnspan=2, padx=5, pady=5)
        self.result_text.tag_configure("attribute", foreground="blue")
        
        for key, value in data.items():
            self.result_text.insert(tk.END, f"{key}: {value}\n", "attribute")
        
        self.save_button = tk.Button(self.edit_window, text="Save", command=lambda: self.save_data(collection))
        self.save_button.grid(row=1, column=0, padx=5, pady=5)
        
        self.cancel_button = tk.Button(self.edit_window, text="Cancel", command=self.edit_window.destroy)
        self.cancel_button.grid(row=1, column=1, padx=5, pady=5)
        
    def save_data(self, collection):
        updated_data = {}
        for line in self.result_text.get('1.0', tk.END).split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)  # Split only at the first occurrence of ':'
                updated_data[key.strip()] = value.strip()
    
        anime_name = updated_data.get('Name', None)
        if not anime_name:
            messagebox.showerror("Error", "Anime name not found in updated data.")
            return

        try:
            updated_data.pop('_id', None)  # Exclude _id field from update
            collection.update_one({'Name': anime_name}, {'$set': updated_data})
            messagebox.showinfo("Success", "Data updated successfully.")
            self.edit_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    root = tk.Tk()
    root.title("Update Data")
    update_window = UpdateWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
