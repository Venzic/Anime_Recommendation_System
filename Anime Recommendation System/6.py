from pymongo import MongoClient
import tkinter as tk
from tkinter import messagebox
import subprocess

def display_retrieved_data(data, collection_name):
    # Display the collection name
    result_text.insert(tk.END, f"\nCollection: {collection_name}\n", "collection")

    # Format and display the retrieved data
    for doc in data:
        formatted_data = ""
        for key, value in doc.items():
            formatted_data += f"{key}: {value}\n"
            # Apply tag to attribute
            result_text.insert(tk.END, key + ": ", "attribute")
            result_text.insert(tk.END, str(value) + "\n")
        formatted_data += "\n"  # Add a newline between documents

def retrieve_data_by_name():
    name_to_retrieve = name_entry.get()

    if name_to_retrieve.strip() == "":
        messagebox.showerror("Error", "Please enter a name.")
        return

    try:
        # Establish connection to MongoDB server
        client = MongoClient('mongodb://localhost:27017')

        # Access the database
        db = client['anime_db']

        # Access the collections
        collection1 = db['Anime 40']
        collection2 = db['Anime 401']
        collection3 = db['Anime402']

        # Retrieve one document from each collection
        result1 = collection1.find_one({'Name': name_to_retrieve})
        result2 = collection2.find_one({'Name': name_to_retrieve})
        result3 = collection3.find_one({'Name': name_to_retrieve})

        # Display the retrieved data for each collection
        if result1:
            display_retrieved_data([result1], "Anime 40")
        if result2:
            display_retrieved_data([result2], "Anime 401")
        if result3:
            display_retrieved_data([result3], "Anime402")

        # If no data found in any collection, show a message box
        if not (result1 or result2 or result3):
            messagebox.showinfo("Info", "No data found for the given name.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def delete_data_by_name():
    name_to_delete = name_entry.get()

    if name_to_delete.strip() == "":
        messagebox.showerror("Error", "Please enter a name.")
        return

    try:
        # Establish connection to MongoDB server
        client = MongoClient('mongodb://localhost:27017')

        # Access the database
        db = client['anime_db']

        # Access the collections
        collection1 = db['Anime 40']
        collection2 = db['Anime 401']
        collection3 = db['Anime402']

        # Delete documents by name across collections
        collection1.delete_many({'Name': name_to_delete})
        collection2.delete_many({'Name': name_to_delete})
        collection3.delete_many({'Name': name_to_delete})

        messagebox.showinfo("Success", f"Data with name '{name_to_delete}' deleted successfully.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def clear_text():
    result_text.delete('1.0', tk.END)

def run_script():
    subprocess.run(["python", "3.py"])

def create_new():
    subprocess.run(["python", "5.py"])

def main():
    global name_entry, result_text

    # Tkinter GUI
    root = tk.Tk()
    root.title("Retrieve and Delete Data by Name")

    # Label and entry for name input
    name_label = tk.Label(root, text="Enter Name:")
    name_label.grid(row=0, column=0, padx=5, pady=5,)
    name_entry = tk.Entry(root)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    # Button to retrieve data
    retrieve_button = tk.Button(root, text="Retrieve", command=retrieve_data_by_name)
    retrieve_button.grid(row=1, column=0, padx=5, pady=5)

    # Button to delete data
    delete_button = tk.Button(root, text="Delete", command=delete_data_by_name)
    delete_button.grid(row=1, column=1, padx=5, pady=5)

    # Button to clear text
    clear_button = tk.Button(root, text="Clear", command=clear_text)
    clear_button.grid(row=1, column=2, padx=5, pady=5)

    # Button to run script
    run_button = tk.Button(root, text="Update", command=run_script)
    run_button.grid(row=1, column=3, padx=5, pady=5)

    # Button to create new
    create_button = tk.Button(root, text="Create New", command=create_new)
    create_button.grid(row=1, column=4, padx=5, pady=5)

    # Create a text widget to display the retrieved data
    result_text = tk.Text(root, height=40, width=160)  # Adjust height and width as needed
    result_text.grid(row=2, columnspan=5, padx=5, pady=5)

    # Configure tags for attribute and collection name colors
    result_text.tag_configure("attribute", foreground="blue")
    result_text.tag_configure("collection", foreground="red")

    root.mainloop()

if __name__ == "__main__":
    main()
