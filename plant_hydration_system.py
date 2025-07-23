import tkinter as tk
from tkinter import messagebox, scrolledtext
import time
import threading
import random

# Define a Plant class with name, moisture level, and watering threshold
class Plant:
    def __init__(self, name, watering_threshold):
        self.name = name
        self.soil_moisture_level = 50  # Initial level
        self.watering_threshold = watering_threshold

    def needs_water(self):
        return self.soil_moisture_level < self.watering_threshold

    def water(self):
        self.soil_moisture_level = 100

# Define the main watering system that manages all plants
class PlantHydrationSystem:
    def __init__(self, initial_water, interval, log_display):
        self.plants = []
        self.water_level = initial_water
        self.interval = interval
        self.log_display = log_display

    def add_plant(self, plant):
        self.plants.append(plant)

    def check_and_water(self):
        for plant in self.plants:
            if plant.needs_water():
                self.water_plant(plant)

    def water_plant(self, plant):
        if self.water_level >= plant.watering_threshold:
            plant.water()
            self.water_level -= plant.watering_threshold
            self.log_display.insert(tk.END, f"✅ {plant.name} was watered.\n")
        else:
            self.log_display.insert(tk.END, f"⚠️ Not enough water for {plant.name}.\n")

    def simulate_watering(self):
        for cycle in range(10):
            self.log_display.insert(tk.END, f"\n🌿 Cycle {cycle + 1} 🌿\n")
            self.check_and_water()
            refill = random.randint(0, 10)
            self.water_level += refill
            self.log_display.insert(tk.END, f"Water level updated: +{refill} → {self.water_level}\n")
            time.sleep(self.interval)
        self.log_display.insert(tk.END, "\n🌱 Hydration simulation completed.\n")


# GUI Application for the Plant Hydration System
class PlantHydrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Plant Hydration System")
        self.root.geometry("500x400")

        # Input: Plant Name
        tk.Label(root, text="Plant Name:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.plant_name_entry = tk.Entry(root)
        self.plant_name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Input: Watering Threshold
        tk.Label(root, text="Watering Threshold:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.watering_threshold_entry = tk.Entry(root)
        self.watering_threshold_entry.grid(row=1, column=1, padx=10, pady=5)

        # Buttons
        self.add_button = tk.Button(root, text="Add Plant", command=self.add_plant)
        self.add_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.simulate_button = tk.Button(root, text="Start Simulation", command=self.run_simulation)
        self.simulate_button.grid(row=3, column=0, columnspan=2, pady=5)

        # Output: Log area
        self.log_output = scrolledtext.ScrolledText(root, width=60, height=15)
        self.log_output.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Initialize system
        self.system = PlantHydrationSystem(initial_water=100, interval=1, log_display=self.log_output)

    def add_plant(self):
        name = self.plant_name_entry.get().strip()
        threshold = self.watering_threshold_entry.get().strip()

        if not name or not threshold:
            messagebox.showerror("Input Error", "Please enter both fields.")
            return

        try:
            threshold_value = int(threshold)
        except ValueError:
            messagebox.showerror("Input Error", "Watering threshold must be a number.")
            return

        new_plant = Plant(name, threshold_value)
        self.system.add_plant(new_plant)
        self.log_output.insert(tk.END, f"🌼 Added plant: {new_plant.name}\n")

        # Clear input fields
        self.plant_name_entry.delete(0, tk.END)
        self.watering_threshold_entry.delete(0, tk.END)

    def run_simulation(self):
        self.log_output.insert(tk.END, "\n🚿 Starting Plant Hydration Simulation...\n")
        simulation_thread = threading.Thread(target=self.system.simulate_watering)
        simulation_thread.start()


# Start the application
if __name__ == "__main__":
    root = tk.Tk()
    app = PlantHydrationApp(root)
    root.mainloop()
