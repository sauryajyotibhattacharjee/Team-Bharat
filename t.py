import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import webbrowser

class LoginApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login - Drone Delivery System")
        self.geometry("400x300")
        self.configure(bg='#2c3e50')
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.configure('TLabel', background='#2c3e50', foreground='#ecf0f1', font=('Helvetica', 12))
        style.configure('TEntry', font=('Helvetica', 12))
        style.configure('TButton', background='#2980b9', foreground='#ecf0f1', font=('Helvetica', 12, 'bold'))

        self.lbl_title = ttk.Label(self, text="Welcome to Drone Delivery System", font=('Helvetica', 16, 'bold'))
        self.lbl_title.pack(pady=20)

        self.lbl_username = ttk.Label(self, text="Username:")
        self.lbl_username.pack(pady=5)
        self.entry_username = ttk.Entry(self)
        self.entry_username.pack(pady=5)

        self.lbl_password = ttk.Label(self, text="Password:")
        self.lbl_password.pack(pady=5)
        self.entry_password = ttk.Entry(self, show='*')
        self.entry_password.pack(pady=5)

        self.btn_login = ttk.Button(self, text="Login", command=self.login)
        self.btn_login.pack(pady=20)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if self.authenticate(username, password):
            self.destroy()
            MainApp().start()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def authenticate(self, username, password):
        # Simulating authentication (replace with actual logic)
        return username == "admin" and password == "admin"

class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Drone-Based Organ Delivery System")
        self.root.geometry("1200x800")
        self.root.configure(bg='#34495e')

        self.create_widgets()

    def create_widgets(self):
        # Add Logo
        logo_frame = ttk.Frame(self.root)
        logo_frame.pack(pady=10)

        try:
            image = Image.open("drone5.png")  # Make sure you have a logo image
            cropped_image = image.crop((100, 100, 400, 300))  # Crop the image to desired area
            photo = ImageTk.PhotoImage(cropped_image)
            label = ttk.Label(logo_frame, image=photo)
            label.image = photo
            label.pack()
        except FileNotFoundError:
            label = ttk.Label(logo_frame, text="Logo Image Not Found")
            label.pack()

        # Tabs
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(expand=True, fill=tk.BOTH)

        # Dashboard Tab
        self.dashboard_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.dashboard_tab, text='Dashboard')

        # Hospitals Tab
        self.hospitals_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.hospitals_tab, text='Hospitals')
        self.create_hospitals_table()

        # Chat Tab
        self.chat_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.chat_tab, text='Chat')
        self.create_chat_interface()

        # Company Info Tab
        self.company_info_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.company_info_tab, text='Company Info')
        self.create_company_info()

        # Initialize drone simulation
        self.init_drone_simulation()

    def start(self):
        self.root.mainloop()

    def create_hospitals_table(self):
        cols = ('Hospital Name', 'Blood Units', 'Organ Units')
        self.hospital_table = ttk.Treeview(self.hospitals_tab, columns=cols, show='headings')

        for col in cols:
            self.hospital_table.heading(col, text=col)

        self.hospital_table.pack(fill=tk.BOTH, expand=True)

        # Example data with websites and types of organs
        self.hospitals_data = [
            ('Hospital A', 10, 2, 'https://hospitalA.com', 'A+, B+', 'Heart, Kidney'),
            ('Hospital B', 5, 3, 'https://hospitalB.com', 'O-, AB+', 'Liver, Lung'),
            ('Hospital C', 8, 1, 'https://hospitalC.com', 'A-, B-', 'Heart, Pancreas'),
            ('Hospital D', 7, 5, 'https://hospitalD.com', 'B+, AB-', 'Kidney, Liver'),
            ('Hospital E', 9, 4, 'https://hospitalE.com', 'O+, A+', 'Lung, Pancreas'),
        ]

        for hospital in self.hospitals_data:
            self.hospital_table.insert('', tk.END, values=hospital[:3])

        self.hospital_table.bind('<Double-1>', self.on_hospital_click)

    def on_hospital_click(self, event):
        item = self.hospital_table.selection()[0]
        hospital_name = self.hospital_table.item(item, "values")[0]
        for hospital in self.hospitals_data:
            if hospital[0] == hospital_name:
                webbrowser.open(hospital[3])
                messagebox.showinfo("Organ Availability", f"Available organs at {hospital_name}: {hospital[5]}")
                break

    def create_chat_interface(self):
        self.chat_frame = ttk.Frame(self.chat_tab)
        self.chat_frame.pack(expand=True, fill=tk.BOTH)

        self.chat_log = tk.Text(self.chat_frame, state='disabled', height=15)
        self.chat_log.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.chat_entry = ttk.Entry(self.chat_frame)
        self.chat_entry.pack(fill=tk.X, padx=10, pady=5)

        self.send_button = ttk.Button(self.chat_frame, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

    def send_message(self):
        message = self.chat_entry.get()
        if message:
            self.chat_entry.delete(0, tk.END)
            self.chat_log.config(state='normal')
            self.chat_log.insert(tk.END, f"You: {message}\n")
            self.chat_log.config(state='disabled')
            self.chat_log.see(tk.END)

    def create_company_info(self):
        info_frame = ttk.Frame(self.company_info_tab)
        info_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        company_info = """
        Welcome to the Drone-Based Organ Delivery System.

        Our company specializes in the rapid and safe delivery of organs using state-of-the-art drone technology.

        Services:
        - Fast organ transport
        - Real-time tracking
        - Temperature-controlled compartments

        For more details, visit our website:
        """
        ttk.Label(info_frame, text=company_info, font=('Helvetica', 14), wraplength=700, justify=tk.LEFT).pack(pady=10)
        
        website_link = ttk.Label(info_frame, text="Drone Delivery System Website", font=('Helvetica', 14, 'underline'), foreground="blue", cursor="hand2")
        website_link.pack(pady=10)
        website_link.bind("<Button-1>", lambda e: webbrowser.open("http://yourwebsite.com"))

    def init_drone_simulation(self):
        self.simulation_frame = ttk.Frame(self.dashboard_tab)
        self.simulation_frame.pack(expand=True, fill=tk.BOTH)

        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.simulation_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.location = [0, 0]
        self.destination = [100, 100]
        self.temperature = 4  # Initial temperature in Celsius
        self.temperature_range = [2, 8]  # Safe temperature range for organ transport

        # Labels to display temperature and location
        self.temp_label = ttk.Label(self.dashboard_tab, text=f"Temperature: {self.temperature:.2f}°C", font=('Helvetica', 14))
        self.temp_label.pack(pady=10)

        self.location_label = ttk.Label(self.dashboard_tab, text=f"Location: {self.location[0]:.2f}, {self.location[1]:.2f}", font=('Helvetica', 14))
        self.location_label.pack(pady=10)

        self.ani = animation.FuncAnimation(self.fig, self.update_plots, interval=100, blit=False)

    def move_drone(self):
        direction = np.array(self.destination) - np.array(self.location)
        step = direction / np.linalg.norm(direction)
        self.location = np.array(self.location) + step

    def adjust_temperature(self):
        if self.temperature < self.temperature_range[0]:
            self.temperature += 0.1  # Heat up
        elif self.temperature > self.temperature_range[1]:
            self.temperature -= 0.1  # Cool down
        else:
            self.temperature += random.uniform(-0.05, 0.05)  # Minor fluctuation

    def update_plots(self, i):
        self.move_drone()
        self.adjust_temperature()

        self.ax1.clear()
        self.ax2.clear()

        self.ax1.plot(self.destination[0], self.destination[1], 'ro', label='Destination')
        self.ax1.plot(self.location[0], self.location[1], 'bo', label='Drone')
        self.ax1.set_xlim(0, 120)
        self.ax1.set_ylim(0, 120)
        self.ax1.set_title('Drone Movement')
        self.ax1.legend()

        self.ax2.plot(0, self.temperature, 'bo')
        self.ax2.axhline(y=self.temperature_range[0], color='r', linestyle='--')
        self.ax2.axhline(y=self.temperature_range[1], color='r', linestyle='--')
        self.ax2.set_xlim(-1, 1)
        self.ax2.set_ylim(0, 10)
        self.ax2.set_title('Temperature Control')
        self.ax2.text(-0.5, self.temperature + 0.5, f'{self.temperature:.2f}°C')

        self.canvas.draw()

        # Update the labels with the latest temperature and location
        self.temp_label.config(text=f"Temperature: {self.temperature:.2f}°C")
        self.location_label.config(text=f"Location: {self.location[0]:.2f}, {self.location[1]:.2f}")

if __name__ == "__main__":
    login_app = LoginApp()
    login_app.mainloop()
