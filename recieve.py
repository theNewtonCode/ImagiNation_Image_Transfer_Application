import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk
import socket
import os

class ImageReceiverGUI:

    def __init__(self, master):
        self.master = master
        master.title("Image Receiver")
        master.geometry('500x500')
        master.resizable(False, False)
        master.configure(bg="black")

        # Logo
        self.logo = tk.PhotoImage(file="logo.png")
        self.logo_label = tk.Label(master, image=self.logo, bg="black")
        self.logo_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Headline
        self.headline = tk.Label(master, text="Image Receiver", font=("Arial Bold", 20), fg="#ffffff", bg="black")
        self.headline.grid(row=1, column=0, columnspan=2, pady=15)

        # IP address input
        self.ip_label = tk.Label(master, text="Enter IMN Key:", font=("Arial", 12), fg="#ffffff", bg="black")
        self.ip_label.grid(row=2, column=0, padx=10)
        self.ip_entry = tk.Entry(master, font=("Arial", 12))
        self.ip_entry.grid(row=2, column=1, pady=8)

        # Browse for image saving folder
        self.folder_label = tk.Label(master, text="Choose save folder:", font=("Arial", 12), fg="#ffffff", bg="black")
        self.folder_label.grid(row=3, column=0, padx=10)
        self.folder_button = tk.Button(master, text="Browse...", font=("Arial", 12), command=self.choose_folder)
        self.folder_button.grid(row=3, column=1, pady=8)

        # Image name input
        self.name_label = tk.Label(master, text="Enter image name:", font=("Arial", 12), fg="#ffffff", bg="black")
        self.name_label.grid(row=4, column=0, padx=10)
        self.name_entry = tk.Entry(master, font=("Arial", 12))
        self.name_entry.grid(row=4, column=1, pady=8)

        self.progress_bar = ttk.Progressbar(master, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.progress_label = tk.Label(master, text='0% ', bg='black', fg='white', font=('Helvetica', 15))
        self.progress_bar.grid(row=5, columnspan=3, pady=10)
        self.progress_label.grid(row=5, column=1, padx=15, pady=10)

        # Receive button
        self.receive_button = tk.Button(master, text="Receive", font=("Arial", 14), bg="#7289da", fg="#ffffff", 
                                        command=self.receive_image, padx=10, pady=5, relief="groove", bd=0)
        self.receive_button.grid(row=6, column=0, padx=80, pady=20)

        # Close button
        self.close_button = tk.Button(master, text="Close", font=("Arial", 14), bg="#f04747", fg="#ffffff", 
                                      command=master.quit, padx=10, pady=5, relief="groove", bd=0)
        self.close_button.grid(row=6, column=1, padx=70, pady=20)

        # Set default folder for saving images
        # self.save_folder = os.path.join(os.path.expanduser("~"), "Pictures")

    def decV4(self, i4):
        eoctets = i4.split('70')
        eoctets.reverse()
        deoctets = [(int(encrypted_octet) - 10) % 256 for encrypted_octet in eoctets]
        dv4 = '.'.join(str(octet) for octet in deoctets)
        return dv4
    
    def choose_folder(self):
        self.save_folder = filedialog.askdirectory()

    def receive_image(self):
        # Get IP address and port number
        imn = self.ip_entry.get()
        ip_address = self.decV4(imn)
        port = 5000  # Change to any unused port number

        # Set up the sending and receiving sockets
        sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect to the sending socket
        sender_socket.connect((ip_address, port))

        # Receive the incoming image data
        image_data = b""
        progress_bar = ttk.Progressbar(self.master, orient="horizontal", length=300, mode="determinate")
        progress_bar.grid(row=5, column=0, columnspan=2, pady=10)
        progress_label = tk.Label(self.master, text="0%", font=("Arial", 12), fg="#ffffff", bg="black")
        progress_label.grid(row=5, column=1, padx=15, pady=10)

        while True:
            data = sender_socket.recv(1024 * 1024 * 5)
            if not data:
                break
            image_data += data
            received_size = len(image_data)
            progress_percent = received_size*100/received_size
            progress_bar["value"] = progress_percent
            progress_label.config(text=f"{progress_percent:.2f}% received")
            self.master.update()

        # Set the path to save the received image
        save_name = self.name_entry.get()
        save_path = os.path.join(self.save_folder, save_name)

        # Write the received image data to the specified file
        with open(save_path, 'wb') as file:
            file.write(image_data)

        # Close the connection and sockets
        sender_socket.close()
        receiver_socket.close()
        # Display message box on successful receive
        tk.messagebox.showinfo("Image Received", "Image received and saved successfully!")
        progress_percent = 0
        progress_bar["value"] = 0
        progress_label.config(text=f"{progress_percent}%")
        self.master.update()

root = tk.Tk()
app = ImageReceiverGUI(root)
root.mainloop()