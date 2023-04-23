import socket
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk


def get_local_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

def encV4(i4):
    octets = i4.split('.')
    octets.reverse()
    enoctets = [(int(octet) + 10) % 256 for octet in octets]
    en4 = '70'.join(str(octet) for octet in enoctets)
    return en4

class ImageSender:
    def __init__(self, master):
        self.master = master
        master.title('Image Sender')
        master.geometry("500x450")
        master.configure(bg='black')
        master.resizable(False, False)

        self.file_path = tk.StringVar()

        # Load logo image
        logo_image = tk.PhotoImage(file="logo.png")

        # Create widgets
        self.logo_label = tk.Label(master, image=logo_image, bg='black')
        self.logo_label.image = logo_image  # keep reference to image to avoid garbage collection
        self.headline_label = tk.Label(master, text='Image Sender', bg='black', fg='#ffffff', font=('Helvetica', 20, 'bold'))
        self.V4label = tk.Label(master, text=f'Secret IMN Key: {encV4(get_local_ip())}', bg='black', fg='#ffffff', font=('Helvetica', 10))
        self.file_label = tk.Label(master, text='Select Image:', bg='black', fg='#ffffff', font=('Helvetica', 12))
        self.file_entry = tk.Entry(master, textvariable=self.file_path, width=30, font=('Helvetica', 12))
        self.file_button = tk.Button(master, text='Browse', command=self.browse_file, bg='white', fg='black', font=('Helvetica', 12, 'bold'))
        self.send_button = tk.Button(master, text='Send', command=self.send_image, bg='#7289da', fg='#ffffff', font=('Helvetica', 15, 'bold'))
        self.quit_button = tk.Button(master, text='Quit', command=master.quit, bg='#f04747', fg='#ffffff', font=('Helvetica', 15, 'bold'))

        # Create progress bar
        # Progress bar
        
        self.progress_bar = ttk.Progressbar(master, orient=tk.HORIZONTAL, length=340, mode='determinate')
        self.progress_label = tk.Label(master, text='0%', bg='black', fg='white', font=('Helvetica', 15))

        # Lay out widgets
        self.logo_label.grid(row=0, column=0, columnspan=3, pady=10)
        self.headline_label.grid(row=1, column=0, columnspan=3, pady=10)
        self.V4label.grid(row=2, column=0, columnspan=3, pady=10)
        self.file_label.grid(row=3, column=0, padx=10, pady=10, sticky=tk.E)
        self.file_entry.grid(row=3, column=1, padx=5, pady=10)
        self.file_button.grid(row=3, column=2, padx=10, pady=10)
        self.progress_bar.grid(row=4, columnspan=3, pady=10)
        self.progress_label.grid(row=4, column=2, pady=10)
        self.send_button.grid(row=5, column=1,ipadx=50, pady=10)
        self.quit_button.grid(row=6, column=1, ipadx=50, pady=10)

        # Configure grid
        master.columnconfigure(0, weight=1)
        master.columnconfigure(1, weight=1)
        master.columnconfigure(2, weight=1)
        master.rowconfigure(0, weight=1)
        master.rowconfigure(1, weight=1)
        master.rowconfigure(2, weight=1)
        master.rowconfigure(3, weight=1)
        master.rowconfigure(4, weight=1)
        master.rowconfigure(5, weight=1)
        # Run the mainloop

    def browse_file(self):
        # Open file dialog to select image file
        file_path = filedialog.askopenfilename(initialdir='/', title='Select Image', filetypes=[('Image Files', '*.jpg *.jpeg *.png *.bmp')])

        if file_path:
            # Update file path entry with selected file
            self.file_path.set(file_path)
    def send_image(self):
        # Get the IP address and port number
        ip_address = get_local_ip()
        port = 5000

        # Ask user to confirm sending the image
        # confirm = messagebox.askyesno('Confirm', f'Are you sure you want to send the image to {ip_address}?')

        try:
            # Set up the sending socket
            receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect to the receiver socket
            receiver_socket.bind((ip_address, port))

            # Listen for incoming connections
            receiver_socket.listen(1)
            connection, sender_address = receiver_socket.accept()
            # Get the size of the image
            image_path = self.file_path.get()
            image_size = os.path.getsize(image_path)

            # Open the image file and read the contents
            with open(image_path, 'rb') as file:
                # Send the image data in chunks of 5 MB
                chunk_size = 1024*1024*5
                num_chunks = image_size // chunk_size + 1
                for i in range(num_chunks):
                    chunk = file.read(chunk_size)
                    connection.sendall(chunk)

                    # Update progress bar
                    progress = (i + 1) / num_chunks * 100
                    self.progress_bar['value'] = progress
                    self.progress_label.config(text=f'{int(progress)}% Sent')
                    self.master.update()

            # Close the connection and sockets
            receiver_socket.close()

            # Show message box indicating success
            messagebox.showinfo('Success', 'Image sent successfully!')
            progress = 0
            self.progress_bar['value'] = progress
            self.progress_label.config(text=f'{int(progress)}%')
            self.master.update()
        except Exception as e:
            # Show error message if there was an error sending the image
            messagebox.showerror('Error', f'Error sending image: {str(e)}')
        # else:
        #     # Do nothing if user does not confirm sending the image
        #     pass


root = tk.Tk()
app = ImageSender(root)
root.mainloop()