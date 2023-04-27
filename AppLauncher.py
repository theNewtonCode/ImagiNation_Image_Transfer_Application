import subprocess
import tkinter as tk
from PIL import ImageTk, Image

# Create the main window
root = tk.Tk()
root.geometry("600x400")
root.title("ImagiNation")
root.configure(bg='black')
root.resizable(False, False)

def launch_app1():
        # open app1 using subprocess
    subprocess.Popen(["python", "new_multiple.py"])
        
def launch_app2():
        # open app2 using subprocessKO
    subprocess.Popen(["python", "recieve.py"])
# Add logo image
img = ImageTk.PhotoImage(Image.open("logo.png"))
logo_label = tk.Label(root, image=img, bg='black')
logo_label.pack(pady=10)

# Add headline
headline_label = tk.Label(root, text="Begin your Give n Take", font=("Courier", 16), fg="white", bg='black')
headline_label.pack(pady=10)

# Create a frame for the buttons
button_frame = tk.Frame(root, bg='black')
button_frame.pack(pady=10)

# Add the first app button
app1_button = tk.Button(button_frame, text="Send IMG", font=("Helvetica", 16), bg='#7289da', fg='white', padx=20, pady=10, bd=0, relief="solid", command=launch_app1)
app1_button.pack(side=tk.LEFT, padx=10)

# Add the second app button
app2_button = tk.Button(button_frame, text="Receive IMG", font=("Helvetica", 16), bg='#7289da', fg='white', padx=20, pady=10, bd=0, relief="solid", command=launch_app2)
app2_button.pack(side=tk.LEFT, padx=10)

# Add the quit button
quit_button = tk.Button(root, text="Quit", font=("Helvetica", 16), bg='#f04747', fg='white', padx=20, pady=10, bd=0, relief="solid", command=root.quit)
quit_button.pack(pady=10)

footer_label = tk.Label(root, text="Proudly created by Abhyuday & Aaryaman", font=("Prestige Elite Std", 12), fg="#b0bbc5", bg='black')
footer_label.pack(pady=10)
# Run the main loop
root.mainloop()
