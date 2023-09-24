import tkinter as tk
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.ttk as ttk

def go(probability):
    if random.random() <= probability:
        return "Success"
    else:
        return "Failure"

# Initialize scatterplot_data at the beginning
scatterplot_data = []

def run(population, max_links, probability):
    pop2 = population
    for links in range(1, max_links + 1):
        avg_resends = 0  # Initialize the average resends for each set of trials
        for _ in range(population):
            total_trials = 0
            good_trials = 0

            while good_trials < links:
                result = go(probability)
                total_trials += 1

                if result == "Success":
                    good_trials += 1
                else:
                    good_trials = 0
            
            avg_resends += total_trials
        
        avg_resends /= population  # Calculate the average resends for this set of trials
        
        result_label.config(text=f"With a sample size of {pop2} packets, on average, it took {avg_resends:.2f} resends to get 1 packet across {links} nodes.")
        
        # Add the data point to the scatterplot
        scatterplot_data.append((links, avg_resends))
    
    # After the loop, update the scatterplot
    update_scatterplot()

def reset_data():
    # Clear the scatterplot_data list to remove all drawn dots
    scatterplot_data.clear()
    
    # Clear the scatterplot and update result labels
    update_scatterplot()
    result_label.config(text="")

def update_scatterplot():
    # Clear the previous plot
    scatterplot_ax.clear()
    
    if scatterplot_data:  # Check if there are data points to plot
        # Extract x and y values from the scatterplot_data
        x, y = zip(*scatterplot_data)
        
        # Create the scatterplot
        scatterplot_ax.scatter(x, y, marker='o', color='blue')
    
    scatterplot_ax.set_xlabel('Nodes')
    scatterplot_ax.set_ylabel('Average Resends')
    
    # Draw the updated scatterplot on the canvas
    scatterplot_canvas.draw()

def on_scatter_click(event):
    # Convert the click coordinates to data coordinates
    x_data, y_data = scatterplot_ax.transData.inverted().transform([event.x, event.y])
    
    # Find the closest point in the scatterplot to the clicked point
    if scatterplot_data:
        min_distance = float('inf')
        closest_point = None
        for x, y in scatterplot_data:
            distance = ((x_data - x)**2 + (y_data - y)**2)**0.5
            if distance < min_distance:
                min_distance = distance
                closest_point = (x, y)
        
        if closest_point:
            x, y = closest_point
            clicked_point_info = f"Node: {int(x)}, Avg Resends: {y:.2f}"
            result_label.config(text=clicked_point_info)

def run_button_click():
    pop = int(population_entry.get())
    max_links = int(links_entry.get())
    prob = float(probability_entry.get())
    run(pop, max_links, prob)

# Create the main window
root = tk.Tk()
root.title("Packet Transmission Simulation")

# Set the initial window size (width x height)
root.geometry("800x900") 
root.minsize(640, 750)

# Labels and Text Boxes
population_label = tk.Label(root, text="Packet Sample Size:", font=("Helvetica", 12))
population_label.pack()

population_entry = tk.Entry(root, justify="center")
population_entry.pack()

links_label = tk.Label(root, text="Maximum Number of Nodes:", font=("Helvetica", 12))
links_label.pack()

links_entry = tk.Entry(root, justify="center")
links_entry.pack()

probability_label = tk.Label(root, text="Probability of Success (e.g., 0.1 for 10%):", font=("Helvetica", 12))
probability_label.pack()

probability_entry = tk.Entry(root, justify="center")
probability_entry.pack()

result_label = tk.Label(root, text="")
result_label.pack()

# Run Button
run_button = tk.Button(root, text="Run Simulation", command=run_button_click, pady=8, bg="#66AD56", fg="white")
run_button.pack()

# Reset Data Button
reset_button = tk.Button(root, text="Reset Data", command=reset_data)
reset_button.pack()

# Scatterplot
scatterplot_fig, scatterplot_ax = plt.subplots()
scatterplot_ax.set_xlabel('Nodes')
scatterplot_ax.set_ylabel('Average Resends')

scatterplot_frame = ttk.Frame(root)
scatterplot_frame.pack(padx=10, pady=10, fill="both", expand=True)

scatterplot_canvas = FigureCanvasTkAgg(scatterplot_fig, master=scatterplot_frame)
scatterplot_canvas_widget = scatterplot_canvas.get_tk_widget()
scatterplot_canvas_widget.pack(fill="both", expand=True)

# Connect the click event handler to the scatterplot
scatterplot_canvas_widget.bind('<ButtonPress-1>', on_scatter_click)

# Start the Tkinter main event loop
root.mainloop()
