import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Read the anime data from CSV
anime_data = pd.read_csv("ranjith.csv")

# Create Tkinter window
root = tk.Tk()
root.title("Anime Analysis")

# Function to create a new window and display the plot
def display_plot(plot_function):
    # Create a new Tkinter window
    new_window = tk.Toplevel(root)
    new_window.title("Analysis Plot")

    # Create a figure and subplot for the plot
    fig = plt.Figure(figsize=(8, 6), dpi=100)
    ax = fig.add_subplot(111)

    # Call the provided plot function to generate the plot
    plot_function(ax)

    # Embed the figure in the new Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=new_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Function to perform genre analysis
def genre_analysis(ax):
    genre_counts = anime_data['Tags'].str.split(',').explode().value_counts()
    genre_counts.plot(kind='bar', ax=ax)
    ax.set_xlabel('Genre')
    ax.set_ylabel('Number of Anime')
    ax.set_title('Genre Analysis')

# Function to perform rating analysis
def rating_analysis(ax):
    anime_data['Rating'] = pd.to_numeric(anime_data['Rating'], errors='coerce')
    ax.hist(anime_data['Rating'].dropna(), bins=10, edgecolor='black')
    ax.set_xlabel('Rating')
    ax.set_ylabel('Frequency')
    ax.set_title('Rating Analysis')

# Function to perform studio performance analysis
def studio_performance(ax):
    studio_ratings = anime_data.groupby('Studio')['Rating'].mean().sort_values(ascending=False).head(10)
    studio_ratings.plot(kind='bar', ax=ax)
    ax.set_xlabel('Studio')
    ax.set_ylabel('Average Rating')
    ax.set_title('Top Studios by Average Rating')
    ax.set_xticklabels(studio_ratings.index, rotation=45)

# Function to perform seasonal analysis
def seasonal_analysis(ax):
    anime_data['Release_season'] = pd.Categorical(anime_data['Release_season'], categories=['Winter', 'Spring', 'Summer', 'Fall'], ordered=True)
    season_counts = anime_data['Release_season'].value_counts()
    season_counts.plot(kind='bar', ax=ax)
    ax.set_xlabel('Season')
    ax.set_ylabel('Number of Anime')
    ax.set_title('Seasonal Analysis')

# Function to perform duration analysis
def duration_analysis(ax):
    ax.hist(anime_data['Episodes'], bins=20, edgecolor='black')
    ax.set_xlabel('Number of Episodes')
    ax.set_ylabel('Frequency')
    ax.set_title('Duration Analysis')

# Create GUI elements
genre_button = ttk.Button(root, text="Genre Analysis", command=lambda: display_plot(genre_analysis))
genre_button.pack(pady=5)

rating_button = ttk.Button(root, text="Rating Analysis", command=lambda: display_plot(rating_analysis))
rating_button.pack(pady=5)

studio_button = ttk.Button(root, text="Studio Performance", command=lambda: display_plot(studio_performance))
studio_button.pack(pady=5)

seasonal_button = ttk.Button(root, text="Seasonal Analysis", command=lambda: display_plot(seasonal_analysis))
seasonal_button.pack(pady=5)

duration_button = ttk.Button(root, text="Duration Analysis", command=lambda: display_plot(duration_analysis))
duration_button.pack(pady=5)

# Run the Tkinter event loop
root.mainloop()
