import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports

class DialControl(tk.Tk):
    def __init__(self):
        """
        Initialize the main window and its widgets.
        """
        super().__init__()

        self.title("Dial Control")

        # === SERIAL PORT SELECTION ===
        self.port_var = tk.StringVar()
        self.port_combo = ttk.Combobox(self, textvariable=self.port_var, width=30)
        self.port_combo.grid(row=0, column=0, padx=5, pady=10)

        # Refresh button to update list of serial ports
        self.refresh_button = ttk.Button(self, text="Refresh", command=self.populate_ports)
        self.refresh_button.grid(row=0, column=1, padx=5, pady=10)

        # Connect/Disconnect button to handle serial communication
        self.connection_button = ttk.Button(self, text="Connect", width=10, command=self.toggle_connection)
        self.connection_button.grid(row=0, column=2, padx=5, pady=10)

        # Standby toggle switch moved to top
        self.standby_var = tk.BooleanVar()
        self.standby_chk = ttk.Checkbutton(self, text="Standby", variable=self.standby_var, command=self.toggle_standby)
        self.standby_chk.grid(row=0, column=3, padx=5, pady=10)


        # Populate the ports on initialization
        self.populate_ports()

        # === DIAL CONTROLS ===
        self.sliders = {}
        self.entries = {}
        self.create_control("Speedometer", 1, 0, 360, "°")
        self.create_control("Tachometer", 2, 0, 360, "°")
        self.create_control("Dynamometer", 3, 0, 360, "°")
        self.create_control("Chargeometer", 4, 0, 360, "°")
        self.create_control("Thermometer", 5, 0, 360, "°")

    # Function to update the list of available serial ports
    def populate_ports(self):
        """
        Populate the combobox with available serial ports.
        """
        self.port_combo['values'] = [port.device for port in serial.tools.list_ports.comports()]

    # Function to handle connecting and disconnecting from the selected serial port
    def toggle_connection(self):
        """
        Establish or close the serial connection based on current state.
        """
        if hasattr(self, 'ser') and self.ser.is_open:
            self.ser.close()
            self.connection_button.config(text="Connect")
        else:
            try:
                self.ser = serial.Serial(self.port_var.get(), 9600)
                self.connection_button.config(text="Disconnect")
                self.send_all_current_values()
            except Exception as e:
                print(f"Error: {e}")

    # Function to create controls for a dial: a label, a slider, and an entry for manual input
    def create_control(self, name, row_num, min_val, max_val, unit):
        """
        Create slider and entry for a given dial name and position.

        :param name: Name of the dial (e.g. "Speedometer").
        :param row_num: Row number for the positioning of the dial in the UI.
        :param min_val: Minimum value for the dial.
        :param max_val: Maximum value for the dial.
        :param unit: Unit for the dial's measurement (e.g. "°").
        """
        # Name of the dial
        label = ttk.Label(self, text=name, anchor='e', width=15)
        label.grid(row=row_num, column=0, pady=10, sticky='e')

        # Entry field for manual degree input
        entry_var = tk.StringVar(value=str(min_val))
        entry = ttk.Entry(self, textvariable=entry_var, validate="key", width=3)
        entry.grid(row=row_num, column=2, pady=10, padx=(0,5))
        entry.bind("<Return>", lambda e, name=name, min_val=min_val, max_val=max_val: self.entry_update(name, min_val, max_val))

        # Degree symbol
        degree_label = ttk.Label(self, text=unit)
        degree_label.grid(row=row_num, column=2, pady=10, padx=(110,0), sticky='w')

        # Slider for adjusting degree visually
        slider = ttk.Scale(self, from_=min_val, to=max_val, orient="horizontal", length=250, command=lambda v, name=name, e_var=entry_var, min_val=min_val, max_val=max_val: self.slider_update(v, name, e_var, min_val, max_val))
        slider.grid(row=row_num, column=1, pady=10, padx=10)

        # Display min and max values beside the slider
        min_label = ttk.Label(self, text=str(min_val), font=("Arial", 10, "bold"))
        min_label.grid(row=row_num, column=1, padx=(0,245), sticky='w')

        max_label = ttk.Label(self, text=str(max_val), font=("Arial", 10, "bold"))
        max_label.grid(row=row_num, column=1, padx=(270,0), sticky='e')


        # Validation command for Entry to only allow numbers
        vcmd = (self.register(self.validate_entry), '%P')
        entry.config(validatecommand=vcmd)

        self.sliders[name] = slider
        self.entries[name] = entry_var

    # Function to update slider and send serial data based on manual input
    def entry_update(self, name, min_val, max_val):
        """
        Update the value of the corresponding slider and send it over serial.

        :param name: Name of the dial.
        :param min_val: Minimum value for the dial.
        :param max_val: Maximum value for the dial.
        """
        entry_value = self.entries[name].get()
        try:
            value = int(entry_value) % (max_val - min_val) + min_val
            self.entries[name].set(f"{value}")
            self.sliders[name].set(value)
            self.send_angle(value, name)
        except ValueError:
            pass

    # Function to update the entry field based on slider movement and send the serial data
    def slider_update(self, value, name, entry_var, min_val, max_val):
        """
        Update the text entry with the value of the slider and send it over serial.

        :param value: Current value of the slider.
        :param name: Name of the dial.
        :param entry_var: StringVar associated with the text entry.
        :param min_val: Minimum value for the dial.
        :param max_val: Maximum value for the dial.
        """
        angle = int(float(value))
        angle = angle % (max_val - min_val + 1) + min_val
        entry_var.set(f"{angle}")
        self.send_angle(angle, name)

    def send_angle(self, angle, name):
        """
        Send angle value over serial connection.

        :param angle: Angle value.
        :param name: Name of the dial.
        """
        if hasattr(self, 'ser') and self.ser.is_open:
            message = f"{name}:{angle}\n"
            self.ser.write(message.encode())

    def toggle_standby(self):
        """
        Toggle standby mode and send the corresponding command over serial.
        """
        if hasattr(self, 'ser') and self.ser.is_open:
            if self.standby_var.get():
                self.ser.write(b"STBY:1\n")
            else:
                self.ser.write(b"STBY:0\n")

    def send_all_current_values(self):
        """
        Send the current values of all sliders and the standby mode over serial.
        """
        for name, slider in self.sliders.items():
            self.send_angle(int(slider.get()), name)
        self.toggle_standby()

    def validate_entry(self, value):
        """
        Validate the text entry to ensure it only contains numbers.

        :param value: Current content of the text entry.
        :return: Boolean indicating whether the entry is valid.
        """
        if value == "":
            return True
        try:
            int(value)
            return True
        except ValueError:
            return False

if __name__ == "__main__":
    app = DialControl()
    app.mainloop()