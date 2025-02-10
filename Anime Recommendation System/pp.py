import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from pymongo import MongoClient
from tkinter import ttk---------------------------------------------------------------------------------------------
import matplotlib.pyplot as plt
import subprocess

class LoginWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Login")
        self.geometry("300x150")
        self.background_image = Image.open("Dusk.jpg")  # Change "login_background.jpg" to your image path
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(self, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)
        
        self.username_label = tk.Label(self, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()
        
        self.password_label = tk.Label(self, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()
        
        self.login_button = tk.Button(self, text="Login", command=self.login)
        self.login_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Perform authentication (e.g., check against a database or hardcoded credentials)
        if username == "r" and password == "r":
            self.destroy()  # Close the login window
            root.deiconify()  # Show the main application window
            app = AnimeRecommendationApp(root)  # Create instance of AnimeRecommendationApp
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")


# Load your anime dataset
anime_data = pd.read_csv(r'C:\Users\Venzic Barbosa\Desktop\BDA_Project\anime.csv')
anime_data = anime_data.dropna(subset=['rating', 'members', 'genre'])
anime_data['members_percentage'] = (anime_data['members'] / anime_data['members'].max()) * 100
anime_data['features'] = anime_data.apply(lambda row: f'{row["rating"]} {row["members_percentage"]} {row["genre"]}', axis=1)
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(anime_data['features'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

def get_personalized_recommendations(watched_anime, cosine_sim=cosine_sim, anime_data=anime_data):
    watched_idx = anime_data[anime_data['name'] == watched_anime].index
    if not watched_idx.empty:
        watched_idx = watched_idx[0]
        sim_scores = list(enumerate(cosine_sim[watched_idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        anime_indices = [i[0] for i in sim_scores[1:11]]
        watched_rating = anime_data.loc[watched_idx, 'rating']
        filtered_recommendations = anime_data.iloc[anime_indices]
        filtered_recommendations = filtered_recommendations[
            (filtered_recommendations['rating'] >= watched_rating - 1) &
            (filtered_recommendations['rating'] <= watched_rating + 1)
        ]
        return filtered_recommendations[['name', 'rating', 'members', 'members_percentage']]
    else:
        return pd.DataFrame(columns=['name', 'rating', 'members', 'members_percentage'])

class RecommendationsWindow(tk.Toplevel):
    def __init__(self, master, recommendations):
        super().__init__(master)
        self.title("Anime Recommendations")
        background_image = Image.open("Dusk.jpg")
        background_photo = ImageTk.PhotoImage(background_image)
        self.background_label = tk.Label(self, image=background_photo)
        self.background_label.image = background_photo
        self.background_label.place(relwidth=1, relheight=1)
        self.tree = ttk.Treeview(self, columns=('Name', 'Rating', 'Members', 'Members Percentage'), show='headings')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Rating', text='Rating')
        self.tree.heading('Members', text='Members')
        self.tree.heading('Members Percentage', text='Members Percentage')
        self.tree.pack()
        self.display_recommendations(recommendations)

    def display_recommendations(self, recommendations):
        for index, row in recommendations.iterrows():
            self.tree.insert('', 'end', values=(row['name'], row['rating'], row['members'], row['members_percentage']))



class TopAnimeOfYearWindow(tk.Toplevel):
    def __init__(self, master, top_anime):
        
        # Sort the DataFrame by 'members_percentage' in ascending order
        top_anime_sorted = top_anime.sort_values(by='members_percentage')
        
        # Prepare data for plotting
        anime_names = top_anime_sorted['name']
        members_percentage = top_anime_sorted['members_percentage']
        
        # Create bar chart
        plt.figure(figsize=(10, 6))
        plt.barh(anime_names, members_percentage, color='skyblue')
        plt.xlabel('Members Percentage')
        plt.title('Top Anime of the Year')
        
        # Display bar chart
        plt.tight_layout()
        plt.show()


class AnimeRecommendationApp:
    
    def __init__(self, master):
        self.master = master
        master.title("Anime Recommendation App")
        background_image = Image.open("Dusk.jpg")
        background_photo = ImageTk.PhotoImage(background_image)
        self.background_label = tk.Label(master, image=background_photo)
        self.background_label.image = background_photo
        self.background_label.place(relwidth=1, relheight=1)
        self.client, self.collection = self.connect_to_mongodb()
        entry_frame = tk.Frame(master)
        entry_frame.pack()
        self.anime_title_label = tk.Label(entry_frame, text="Enter Watched Anime:")
        self.anime_title_label.grid(row=0, column=0, padx=5, pady=5)
        self.anime_title_entry = tk.Entry(entry_frame)
        self.anime_title_entry.grid(row=0, column=1, padx=5, pady=5)
        button_frame = tk.Frame(master)
        button_frame.pack()
        self.button_anime_recommendation = tk.Button(button_frame, text="Anime Recommendation", command=self.show_recommendations, border=5)
        self.button_anime_recommendation.pack(side=tk.LEFT, padx=5, pady=5)
        self.button_anime_of_the_year = tk.Button(button_frame, text="Anime of the Year::prediction", command=self.show_top_anime_of_the_year,  border=5)
        self.button_anime_of_the_year.pack(side=tk.LEFT, padx=5, pady=5)
        self.button_execute_script = tk.Button(button_frame, text="Multiple collection", command=self.execute_script, border=5)
        self.button_execute_script.pack(side=tk.LEFT, padx=5, pady=5)
        self.button_analysis = tk.Button(button_frame, text="Analysis", command=self.open_analysis_script, border=5)
        self.button_analysis.pack(side=tk.LEFT, padx=5, pady=5)
        self.button_retrieve_backup = tk.Button(button_frame, text="Retrieve", command=self.retrieve_backup,  border=5)
        self.button_retrieve_backup.pack(side=tk.LEFT, padx=5, pady=5)
        mongo_frame = tk.Frame(master)
        mongo_frame.pack()
        self.label_anime_id = tk.Label(mongo_frame, text="Anime ID:")
        self.label_anime_id.grid(row=0, column=0, padx=5, pady=5)
        self.entry_anime_id = tk.Entry(mongo_frame)
        self.entry_anime_id.grid(row=0, column=1, padx=5, pady=5)
        self.label_new_anime_id = tk.Label(mongo_frame, text="New Anime ID:")
        self.label_new_anime_id.grid(row=1, column=0, padx=5, pady=5)
        self.entry_new_anime_id = tk.Entry(mongo_frame)
        self.entry_new_anime_id.grid(row=1, column=1, padx=5, pady=5)

        self.label_new_name = tk.Label(mongo_frame, text="New Name:")
        self.label_new_name.grid(row=1, column=2, padx=5, pady=5)
        self.entry_new_name = tk.Entry(mongo_frame)
        self.entry_new_name.grid(row=1, column=3, padx=5, pady=5)
        self.label_new_genre = tk.Label(mongo_frame, text="New Genre:")
        self.label_new_genre.grid(row=2, column=0, padx=5, pady=5)
        self.entry_new_genre = tk.Entry(mongo_frame)
        self.entry_new_genre.grid(row=2, column=1, padx=5, pady=5)
        self.label_new_type = tk.Label(mongo_frame, text="New Type:")
        self.label_new_type.grid(row=2, column=2, padx=5, pady=5)
        self.entry_new_type = tk.Entry(mongo_frame)
        self.entry_new_type.grid(row=2, column=3, padx=5, pady=5)
        self.label_new_episodes = tk.Label(mongo_frame, text="New Episodes:")
        self.label_new_episodes.grid(row=3, column=0, padx=5, pady=5)
        self.entry_new_episodes = tk.Entry(mongo_frame)
        self.entry_new_episodes.grid(row=3, column=1, padx=5, pady=5)
        self.label_new_rating = tk.Label(mongo_frame, text="New Rating:")
        self.label_new_rating.grid(row=3, column=2, padx=5, pady=5)
        self.entry_new_rating = tk.Entry(mongo_frame)
        self.entry_new_rating.grid(row=3, column=3, padx=5, pady=5)
        self.label_new_members = tk.Label(mongo_frame, text="New Members:")
        self.label_new_members.grid(row=4, column=0, padx=5, pady=5)
        self.entry_new_members = tk.Entry(mongo_frame)
        self.entry_new_members.grid(row=4, column=1, padx=5, pady=5)
        
        self.button_update_by_id = tk.Button(mongo_frame, text="Update by ID", command=self.update_data_by_id,  border=5)
        self.button_update_by_id.grid(row=5, column=0, padx=5, pady=5)
        self.button_delete_by_id = tk.Button(mongo_frame, text="Delete by ID", command=self.delete_data_by_id,  border=5)
        self.button_delete_by_id.grid(row=5, column=1, padx=5, pady=5)
        self.button_create_new_anime = tk.Button(mongo_frame, text="Create New Anime", command=self.create_new_anime,  border=5)
        self.button_create_new_anime.grid(row=5, column=2, padx=5, pady=5)
        self.button_retrieve_by_id = tk.Button(mongo_frame, text="Retrieve by ID", command=self.retrieve_data_by_id,  border=5)
        self.button_retrieve_by_id.grid(row=5, column=3, padx=5, pady=5)
        self.display_text = tk.Text(master, height=10, width=50)
        self.display_text.pack()

    def connect_to_mongodb(self):
        client = MongoClient('mongodb://localhost:27017/')
        db = client['anime_db']
        collection = db['anime_collection']
        return client, collection

    def close_mongodb_connection(self):
        self.client.close()

    def clear_display_text(self):
        self.display_text.delete(1.0, tk.END)

    def display_message(self, message):
        self.clear_display_text()
        self.display_text.insert(tk.END, message)
    def retrieve_data_by_id(self):
        anime_id = self.entry_anime_id.get()
        if anime_id:
            result = self.collection.find_one({'anime_id': int(anime_id)})
            if result:
                self.display_message(f"Retrieved anime data for ID {anime_id}:\n{result}\n")
            else:
                self.display_message(f"No data found for ID {anime_id}")
        else:
            self.display_message("Please enter an anime ID")

    
    def update_data_by_id(self):
        anime_id = self.entry_anime_id.get()
        new_name = self.entry_new_name.get()
        new_genre = self.entry_new_genre.get()
        new_type = self.entry_new_type.get()
        new_episodes = self.entry_new_episodes.get()
        new_rating = self.entry_new_rating.get()
        new_members = self.entry_new_members.get()

        if anime_id:
            result = self.collection.update_one(
                {'anime_id': int(anime_id)},
                {'$set': {'name': new_name, 'genre': new_genre, 'type': new_type, 'episodes': new_episodes,
                          'rating': new_rating, 'members': new_members}}
            )
            if result.modified_count > 0:
                self.display_message(f"Updated anime data for ID {anime_id}\n")
            else:
                self.display_message(f"No data found for ID {anime_id}")
        else:
            self.display_message("Please enter an anime ID")

    def delete_data_by_id(self):
        anime_id = self.entry_anime_id.get()
        if anime_id:
            result = self.collection.delete_one({'anime_id': int(anime_id)})
            if result.deleted_count > 0:
                self.display_message(f"Deleted anime data for ID {anime_id}\n")
            else:
                self.display_message(f"No data found for ID {anime_id}")
        else:
            self.display_message("Please enter an anime ID")

    def create_new_anime(self):
        anime_id = self.entry_new_anime_id.get()
        name = self.entry_new_name.get()
        genre = self.entry_new_genre.get()
        anime_type = self.entry_new_type.get()
        episodes = self.entry_new_episodes.get()
        rating = self.entry_new_rating.get()
        members = self.entry_new_members.get()

        print(f"Received data: Anime ID: {anime_id}, Name: {name}, Genre: {genre}, Type: {anime_type}, Episodes: {episodes}, Rating: {rating}, Members: {members}")

        if anime_id and name and genre and anime_type and episodes and rating and members:
            anime_entry = {
                'anime_id': int(anime_id),
                'name': name,
                'genre': genre,
                'type': anime_type,
                'episodes': int(episodes),
                'rating': float(rating),
                'members': int(members)
        }
            print("Inserting anime entry:", anime_entry)
            result = self.collection.insert_one(anime_entry)
            if result.inserted_id:
                self.display_message(f"Created new anime entry with ID {anime_id}\n")
            else:
                self.display_message(f"Failed to create new anime entry\n")
        else:
                self.display_message("Please fill in all the fields for creating a new anime entry")

    

    def show_recommendations(self):
        watched_anime = self.anime_title_entry.get()
        recommendations = get_personalized_recommendations(watched_anime)
        RecommendationsWindow(self.master, recommendations)

    def show_top_anime_of_the_year(self):
        top_anime_of_the_year = anime_data.sort_values(by='members_percentage', ascending=False).head(10)
        TopAnimeOfYearWindow(self.master, top_anime_of_the_year)

    def execute_script(self):
        script_path = "6.py"  # Update with the path to your script
        subprocess.Popen(["python", script_path])
    
    def open_analysis_script(self):
        script_path = "analysis.py"  # Update with the path to your analysis script
        subprocess.Popen(["python", script_path])
    
    def retrieve_backup(self):
        script_path = "backup1.py"  # Update with the path to your backup script
        subprocess.Popen(["python", script_path])

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main window for now
    login_window = LoginWindow(root)
    root.mainloop()
