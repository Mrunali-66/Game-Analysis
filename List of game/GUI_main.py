import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class GameAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Data Analysis")
        self.root.geometry("800x600")

        # Create sample data
        self.df = self.create_sample_data()

        # Create main frames
        self.create_frames()

        # Create widgets
        self.create_widgets()

    def create_sample_data(self):
        """Create sample game data"""
        data = {
            'game_title': ['The Witcher 3', 'Red Dead Redemption 2', 'God of War', 'Cyberpunk 2077',
                           'GTA V', 'Elden Ring', 'Horizon Zero Dawn', 'Spider-Man'],
            'genre': ['RPG', 'Action-Adventure', 'Action', 'RPG',
                      'Action-Adventure', 'RPG', 'Action-RPG', 'Action-Adventure'],
            'release_year': [2015, 2018, 2018, 2020, 2013, 2022, 2017, 2018],
            'rating': [9.8, 9.7, 9.5, 7.8, 9.6, 9.4, 9.2, 9.3],
            'sales_millions': [40.2, 50.5, 23.0, 18.2, 170.0, 20.5, 20.0, 33.2],
            'playtime_hours': [100, 80, 30, 60, 50, 70, 40, 25],
            'price': [39.99, 59.99, 49.99, 59.99, 29.99, 59.99, 49.99, 39.99]
        }
        return pd.DataFrame(data)

    def create_frames(self):
        """Create main frames for the GUI"""
        # Left frame for controls
        self.control_frame = ttk.Frame(self.root, padding="5")
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Right frame for display
        self.display_frame = ttk.Frame(self.root, padding="5")
        self.display_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def create_widgets(self):
        """Create all widgets for the GUI"""
        # Control Panel
        ttk.Label(self.control_frame, text="Analysis Options", font=('Helvetica', 12, 'bold')).pack(pady=5)

        # Analysis buttons
        ttk.Button(self.control_frame, text="View All Games",
                   command=self.show_all_games).pack(pady=5, fill=tk.X)
        ttk.Button(self.control_frame, text="Genre Analysis",
                   command=self.show_genre_analysis).pack(pady=5, fill=tk.X)
        ttk.Button(self.control_frame, text="Sales Chart",
                   command=self.show_sales_chart).pack(pady=5, fill=tk.X)
        ttk.Button(self.control_frame, text="Rating Distribution",
                   command=self.show_rating_distribution).pack(pady=5, fill=tk.X)

        # Filter frame
        filter_frame = ttk.LabelFrame(self.control_frame, text="Filters", padding="5")
        filter_frame.pack(pady=10, fill=tk.X)

        # Genre filter
        ttk.Label(filter_frame, text="Genre:").pack()
        self.genre_var = tk.StringVar()
        genres = ['All'] + list(self.df['genre'].unique())
        ttk.Combobox(filter_frame, textvariable=self.genre_var,
                     values=genres).pack(pady=5)

        # Year filter
        ttk.Label(filter_frame, text="Year:").pack()
        self.year_var = tk.StringVar()
        years = ['All'] + [str(year) for year in sorted(self.df['release_year'].unique())]
        ttk.Combobox(filter_frame, textvariable=self.year_var,
                     values=years).pack(pady=5)

        # Apply filter button
        ttk.Button(filter_frame, text="Apply Filters",
                   command=self.apply_filters).pack(pady=5)

        # Create Treeview for data display
        self.create_treeview()

    def create_treeview(self):
        """Create and configure the Treeview widget"""
        columns = ('Title', 'Genre', 'Year', 'Rating', 'Sales', 'Playtime', 'Price')
        self.tree = ttk.Treeview(self.display_frame, columns=columns, show='headings')

        # Configure columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.display_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Pack widgets
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def show_all_games(self):
        """Display all games in the Treeview"""
        self.clear_display()
        for _, row in self.df.iterrows():
            self.tree.insert('', tk.END, values=(
                row['game_title'], row['genre'], row['release_year'],
                f"{row['rating']:.1f}", f"{row['sales_millions']:.1f}M",
                f"{row['playtime_hours']}h", f"${row['price']:.2f}"
            ))

    def show_genre_analysis(self):
        """Show genre analysis stats"""
        self.clear_display()
        genre_stats = self.df.groupby('genre').agg({
            'game_title': 'count',
            'rating': 'mean',
            'sales_millions': 'sum'
        }).round(2)

        for genre, row in genre_stats.iterrows():
            self.tree.insert('', tk.END, values=(
                genre, 'Games: ' + str(int(row['game_title'])),
                'Avg Rating: ' + f"{row['rating']:.1f}",
                'Total Sales: ' + f"{row['sales_millions']:.1f}M",
                '', '', ''
            ))

    def show_sales_chart(self):
        """Display a bar chart of game sales"""
        self.clear_display()
        fig, ax = plt.subplots(figsize=(8, 6))
        self.df.plot(kind='bar', x='game_title', y='sales_millions', ax=ax)
        ax.set_title('Game Sales (Millions)')
        ax.set_xlabel('Games')
        ax.set_ylabel('Sales (M)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.display_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def show_rating_distribution(self):
        """Display a histogram of game ratings"""
        self.clear_display()
        fig, ax = plt.subplots(figsize=(8, 6))
        self.df['rating'].hist(ax=ax, bins=10)
        ax.set_title('Rating Distribution')
        ax.set_xlabel('Rating')
        ax.set_ylabel('Number of Games')
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.display_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def apply_filters(self):
        """Apply selected filters to the data display"""
        filtered_df = self.df.copy()

        if self.genre_var.get() != 'All':
            filtered_df = filtered_df[filtered_df['genre'] == self.genre_var.get()]

        if self.year_var.get() != 'All':
            filtered_df = filtered_df[filtered_df['release_year'] == int(self.year_var.get())]

        self.clear_display()
        for _, row in filtered_df.iterrows():
            self.tree.insert('', tk.END, values=(
                row['game_title'], row['genre'], row['release_year'],
                f"{row['rating']:.1f}", f"{row['sales_millions']:.1f}M",
                f"{row['playtime_hours']}h", f"${row['price']:.2f}"
            ))

    def clear_display(self):
        """Clear the display frame"""
        for widget in self.display_frame.winfo_children():
            widget.destroy()
        self.create_treeview()


if __name__ == "__main__":
    root = tk.Tk()
    app = GameAnalysisApp(root)
    root.mainloop()