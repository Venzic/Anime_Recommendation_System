from pymongo import MongoClient
import tkinter as tk
from tkinter import messagebox

# Dictionary to store the fields for each collection
collection_fields = {
    "Anime 40": ["Name", "Japanese_name", "Type", "Episodes", "Studio"],
    "Anime 401": ["Name", "Release_season", "Rating", "Release_year", "End_year"],
    "Anime402": ["Name", "Content_Warning", "Related_content"]
}

def create_new():
    # Hide result text
    result_text.pack_forget()

    # Show the appropriate frame for creating new documents
    frame1.pack()
    frame2.pack()
    frame3.pack()

def submit_new_data():
    # Get data from entry fields
    data1 = {}
    for field in collection_fields["Anime 40"]:
        data1[field] = entry_fields_collection1[field].get()

    data2 = {}
    for field in collection_fields["Anime 401"]:
        data2[field] = entry_fields_collection2[field].get()

    data3 = {}
    for field in collection_fields["Anime402"]:
        data3[field] = entry_fields_collection3[field].get()

    try:
        # Establish connection to MongoDB server
        client = MongoClient('mongodb://localhost:27017')

        # Access the database
        db = client['anime_db']

        # Access the collections
        collection1 = db['Anime 40']
        collection2 = db['Anime 401']
        collection3 = db['Anime402']

        # Insert new documents
        collection1.insert_one(data1)
        collection2.insert_one(data2)
        collection3.insert_one(data3)

        messagebox.showinfo("Success", "New documents added successfully.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    global result_text, frame1, frame2, frame3
    global entry_fields_collection1, entry_fields_collection2, entry_fields_collection3

    # Tkinter GUI
    root = tk.Tk()
    root.title("Create New Documents")

    # Button to create new documents
    create_button = tk.Button(root, text="Create New", command=create_new)
    create_button.pack(padx=5, pady=5)

    # Result text (hidden initially)
    result_text = tk.Text(root, height=10, width=40)
    result_text.pack_forget()

    # Frame for collection1 fields
    frame1 = tk.Frame(root)
    entry_fields_collection1 = {}
    for field in collection_fields["Anime 40"]:
        tk.Label(frame1, text=f"{field}:").pack()
        entry_fields_collection1[field] = tk.Entry(frame1)
        entry_fields_collection1[field].pack()

    # Frame for collection2 fields
    frame2 = tk.Frame(root)
    entry_fields_collection2 = {}
    for field in collection_fields["Anime 401"]:
        tk.Label(frame2, text=f"{field}:").pack()
        entry_fields_collection2[field] = tk.Entry(frame2)
        entry_fields_collection2[field].pack()

    # Frame for collection3 fields
    frame3 = tk.Frame(root)
    entry_fields_collection3 = {}
    for field in collection_fields["Anime402"]:
        tk.Label(frame3, text=f"{field}:").pack()
        entry_fields_collection3[field] = tk.Entry(frame3)
        entry_fields_collection3[field].pack()

    # Submit button for new data
    submit_button = tk.Button(root, text="Submit", command=submit_new_data)
    submit_button.pack(padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
