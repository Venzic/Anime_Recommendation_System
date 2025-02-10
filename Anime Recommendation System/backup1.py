import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import pandas as pd

# Load your anime dataset
anime_data = pd.read_csv(r'C:\\Users\\Venzic Barbosa\\Desktop\\BDA_Project\\a333.csv')
anime_data = anime_data.dropna(subset=['rating', 'members', 'genre'])
anime_data['members_percentage'] = (anime_data['members'] / anime_data['members'].max()) * 100
anime_data['features'] = anime_data.apply(lambda row: f'{row["rating"]} {row["members_percentage"]} {row["genre"]}', axis=1)

class RecommendationsWindow(tk.Toplevel):
    def __init__(self, master, recommendations):
        super().__init__(master)
        self.title("Anime Recommendations")
        background_image = Image.open("Dusk.jpg")
        background_photo = ImageTk.PhotoImage(background_image)
        self.background_label = tk.Label(self, image=background_photo)
        self.background_label.image = background_photo
        self.background_label.place(relwidth=1, relheight=1)
        self.tree = ttk.Treeview(self, columns=('Name', 'Rating', 'Members'), show='headings')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Rating', text='Rating')
        self.tree.heading('Members', text='Members')
        self.tree.pack()
        self.display_recommendations(recommendations)

    def display_recommendations(self, recommendations):
        for index, row in recommendations.iterrows():
            self.tree.insert('', 'end', values=(row['name'], row['rating'], row['members']))

class RetrieveByNameWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Retrieve by Name")
        self.geometry("300x150")
        
        tk.Label(self, text="Enter Anime Name:").pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()
        
        tk.Button(self, text="Retrieve", command=self.retrieve_data).pack()

    def retrieve_data(self):
        anime_name = self.name_entry.get()
        if anime_name:
            filtered_data = anime_data[anime_data['name'].str.contains(anime_name, case=False)]
            RecommendationsWindow(self.master, filtered_data[['name', 'rating', 'members']])
        else:
            messagebox.showerror("Error", "Please enter an anime name.")

class RetrieveByRatingWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Retrieve by Rating")
        self.geometry("300x150")
        self.choice = tk.StringVar(value="above")
        
        tk.Label(self, text="Select Condition:").pack()
        tk.Radiobutton(self, text="Above", variable=self.choice, value="above").pack()
        tk.Radiobutton(self, text="Below", variable=self.choice, value="below").pack()
        tk.Radiobutton(self, text="Equal", variable=self.choice, value="equal").pack()
        
        tk.Label(self, text="Enter Rating:").pack()
        self.rating_entry = tk.Entry(self)
        self.rating_entry.pack()
        
        tk.Button(self, text="Retrieve", command=self.retrieve_data).pack()

    def retrieve_data(self):
        choice = self.choice.get()
        try:
            rating = float(self.rating_entry.get())
            if choice == "above":
                filtered_data = anime_data[anime_data['rating'] > rating]
            elif choice == "below":
                filtered_data = anime_data[anime_data['rating'] < rating]
            elif choice == "equal":
                filtered_data = anime_data[anime_data['rating'] == rating]
            RecommendationsWindow(self.master, filtered_data[['name', 'rating', 'members']])
        except ValueError:
            messagebox.showerror("Error", "Invalid rating. Please enter a valid number.")

class RetrieveByTypeWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Retrieve by Type")
        self.geometry("300x150")
        
        tk.Label(self, text="Enter Anime Type:").pack()
        self.type_entry = tk.Entry(self)
        self.type_entry.pack()
        
        tk.Button(self, text="Retrieve", command=self.retrieve_data).pack()

    def retrieve_data(self):
        anime_type = self.type_entry.get()
        if anime_type:
            filtered_data = anime_data[anime_data['type'].str.contains(anime_type, case=False)]
            RecommendationsWindow(self.master, filtered_data[['name', 'rating', 'members']])
        else:
            messagebox.showerror("Error", "Please enter an anime type.")

class RetrieveBySeasonWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Retrieve by Season")
        self.geometry("300x150")

        tk.Label(self, text="Select Season:").pack()
        
        self.season_var = tk.StringVar(value="Summer")
        season_options = ["Summer", "Winter", "Spring"]
        self.season_menu = tk.OptionMenu(self, self.season_var, *season_options)
        self.season_menu.pack()

        tk.Button(self, text="Retrieve", command=self.retrieve_data).pack()

    def retrieve_data(self):
        anime_season = self.season_var.get().lower()
        if anime_season:
            filtered_data = anime_data[anime_data['season'].str.lower().str.contains(anime_season, case=False)]
            RecommendationsWindow(self.master, filtered_data[['name', 'rating', 'members']])
        else:
            messagebox.showerror("Error", "Please select a season.")

class PopularityOptionsWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Popularity Options")
        self.geometry("200x100")
        
        tk.Label(self, text="Select Popularity Option:").pack()
        
        tk.Button(self, text="Top 10", command=lambda: self.retrieve_popularity("top"), bg="yellow", border=5).pack()
        tk.Button(self, text="Last 10", command=lambda: self.retrieve_popularity("last"), bg="yellow", border=5).pack()

    def retrieve_popularity(self, option):
        n = 10
        if option == "top":
            sorted_data = anime_data.nlargest(n, 'members')
        elif option == "last":
            sorted_data = anime_data.nsmallest(n, 'members')
        RecommendationsWindow(self.master, sorted_data[['name', 'rating', 'members']])

class AnimeRecommendationApp:
    
    def __init__(self, master):
        self.master = master
        master.title("Anime Recommendation App")
        background_image = Image.open("Dusk.jpg")
        background_photo = ImageTk.PhotoImage(background_image)
        self.background_label = tk.Label(master, image=background_photo)
        self.background_label.image = background_photo
        self.background_label.place(relwidth=1, relheight=1)
        
        entry_frame = tk.Frame(master)
        entry_frame.pack()
        
        button_frame = tk.Frame(master)
        button_frame.pack()
        
        self.button_retrieve_by_name = tk.Button(button_frame, text="Retrieve by Name", command=self.retrieve_by_name, bg="yellow", border=5)
        self.button_retrieve_by_name.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.button_retrieve_by_rating = tk.Button(button_frame, text="Retrieve by Rating", command=self.retrieve_by_rating, bg="yellow", border=5)
        self.button_retrieve_by_rating.pack(side=tk.LEFT, padx=5, pady=5)

        self.button_retrieve_by_type = tk.Button(button_frame, text="Retrieve by Type", command=self.retrieve_by_type, bg="yellow", border=5)
        self.button_retrieve_by_type.pack(side=tk.LEFT, padx=5, pady=5)

        self.button_retrieve_by_season = tk.Button(button_frame, text="Retrieve by Season", command=self.retrieve_by_season, bg="yellow", border=5)
        self.button_retrieve_by_season.pack(side=tk.LEFT, padx=5, pady=5)

        self.button_sort_popularity = tk.Button(button_frame, text="Sort by Popularity", command=self.open_popularity_options, bg="yellow", border=5)
        self.button_sort_popularity.pack(side=tk.LEFT, padx=5, pady=5)

    def retrieve_by_name(self):
        RetrieveByNameWindow(self.master)

    def retrieve_by_rating(self):
        RetrieveByRatingWindow(self.master)
    
    def retrieve_by_type(self):
        RetrieveByTypeWindow(self.master)

    def retrieve_by_season(self):
        RetrieveBySeasonWindow(self.master)

    def open_popularity_options(self):
        PopularityOptionsWindow(self.master)

if __name__ == "__main__":
    root = tk.Tk()
    app = AnimeRecommendationApp(root)
    root.mainloop()
