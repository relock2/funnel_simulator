"""Simple Funnel Simulator

This program provides a simple simulation of candidates passing through a
5-stage recruiting funnel. Users can select the number of simulations, the
number of starting candidates, and the expected conversion rate for each
stage. The program then visualizes the distribution of simulated billed
employees for each funnel.
"""

# Notice the blank line above. Code should continue on this line.


import tkinter as tk  # Import the tkinter module for GUI
from tkinter import ttk  # Import themed tkinter for styling
from ttkthemes import ThemedTk  # Import themed tkinter for styling
import numpy as np  # Import numpy for numerical computations
import matplotlib.pyplot as plt  # Import matplotlib for plotting
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Import for embedding matplotlib plots in tkinter
from scipy.stats import percentileofscore  # Import for calculating percentiles

def submit_values():
    # Function to handle button click event, runs simulations and displays histograms
    num_simulations = int(simulation_count_entry.get())  # Get the number of simulations from entry field
    all_results = []  # Initialize an empty list to store results of all simulations
    for i, practice in enumerate(practices):  # Iterate over each practice
        applicants = int(applicant_entries[i].get())  # Get the number of applicants for the current practice
        conv_rates = [float(entry.get()) / 100 for entry in conv_rate_entries[i]]  # Get conversion rates for each stage
        results = []  # Initialize an empty list to store results of current practice simulations
        for _ in range(num_simulations):  # Perform simulations for the current practice
            results.append(run_simulation(applicants, conv_rates))  # Run simulation and append result
        all_results.append(results)  # Append results of current practice to the list of all results
        # Calculate statistics for the current practice results
        avg_value = np.mean(results)
        median_value = np.median(results)
        lower_bound = np.percentile(results, 2.5)
        upper_bound = np.percentile(results, 97.5)
        # Print statistics to console
        print(f"{practice}: {applicants} applicants, Conversion rates: {conv_rates}")
        print(f"Average: {avg_value}, 2.5%: {lower_bound}, 97.5%: {upper_bound}")
        # Create histogram for the current practice results
        fig = plt.figure(figsize=(6, 4))
        plt.hist(results, bins=20, alpha=0.5, color=colors[i])  # Plot histogram
        plt.axvline(lower_bound, color='r', linestyle='dashed', linewidth=1)  # Add lower bound line
        plt.axvline(upper_bound, color='r', linestyle='dashed', linewidth=1)  # Add upper bound line
        plt.axvline(median_value, color='black', linestyle='solid', linewidth=1)  # Add median line
        plt.title(practice)  # Set title
        plt.text(0.1, 0.9, f"Median: {median_value}", transform=plt.gca().transAxes)  # Add median text

        canvas = FigureCanvasTkAgg(fig, master=mainframe)  # Embed the plot in a tkinter canvas
        canvas.draw()  # Draw the canvas
        canvas.get_tk_widget().grid(column=0, row=len(practices) + 4 + i, columnspan=len(stages) + 2)  # Place the canvas on the tkinter frame

def run_simulation(applicants, conv_rates):
    # Function to run a single simulation
    candidates = applicants
    for rate in conv_rates:  # Iterate over conversion rates for each stage
        candidates = np.random.binomial(candidates, rate)  # Apply conversion rate to candidates
    return candidates  # Return the final number of candidates

# Create a list of practices
practices = ["Office A", "Office B"]

# Colors for histograms
colors = ["blue", "orange"]

# Default values for the number of candidates and conversion rates
default_applicants = [50546, 46630]
default_conv_rates = [
    [57.2, 53.6, 71.7, 71.6, 49.0],
    [29.8, 19.5, 100, 91.6, 66.0]
]

stages = ["Interview", "Conditional Offer", "Offer Accepted", "Hired", "Billed"]

root = ThemedTk(theme="arc")  # Create themed tkinter window
root.title("Recruitment Simulation")  # Set window title

mainframe = ttk.Frame(root, padding="10 10 10 10")  # Create a main frame for widgets
mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))  # Place main frame in the window

ttk.Label(mainframe, text="Number of simulations:").grid(column=0, row=0, sticky=(tk.W))  # Create label for number of simulations entry field
simulation_count_entry = ttk.Entry(mainframe, width=10)  # Create entry field for number of simulations
simulation_count_entry.grid(column=1, row=0, sticky=(tk.W, tk.E))  # Place entry field in the main frame
simulation_count_entry.insert(0, "10000")  # Set default value for number of simulations

applicant_entries = []  # Initialize list to store entry fields for number of applicants
conv_rate_entries = []  # Initialize list to store entry fields for conversion rates

for i, stage in enumerate(stages):  # Iterate over stages
    ttk.Label(mainframe, text=f"{stage} (%):").grid(column=i+2, row=0, sticky=(tk.W, tk.E), padx=5)  # Create label for each stage

for i, practice in enumerate(practices):  # Iterate over practices
    ttk.Label(mainframe, text=practice).grid(column=0, row=i+1, sticky=(tk.W))  # Create label for each practice

    applicant_entry = ttk.Entry(mainframe, width=10)  # Create entry field for number of applicants
    applicant_entry.grid(column=1, row=i+1, sticky=(tk.W, tk.E))  # Place entry field in the main frame
    applicant_entry.insert(0, default_applicants[i])  # Set default value for number of applicants
    applicant_entries.append(applicant_entry)  # Append entry field to the list of applicant entries

    practice_conv_rate_entries = []  # Initialize list to store entry fields for conversion rates for each practice
    for j, rate in enumerate(default_conv_rates[i]):  # Iterate over conversion rates for each practice
        conv_rate_entry = ttk.Entry(mainframe, width=6)  # Create entry field for conversion rate
        conv_rate_entry.grid(column=j+2, row=i+1, sticky=(tk.W, tk.E), padx=5)  # Place entry field in the main frame
        conv_rate_entry.insert(0, rate)  # Set default value for conversion rate
        practice_conv_rate_entries.append(conv_rate_entry)  # Append entry field to the list of conversion rate entries for the current practice
        conv_rate_entries.append(practice_conv_rate_entries)  # Append entry field to the list of all conversion rate entries

ttk.Button(mainframe, text="Run simulation", command=submit_values).grid(column=0, row=len(practices)+1, columnspan=len(stages) + 2)  # Create button to run simulation
root.mainloop()  # Start the tkinter event loop
