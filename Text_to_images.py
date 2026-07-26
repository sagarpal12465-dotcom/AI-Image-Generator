import tkinter as tk
from tkinter import messagebox, filedialog
import urllib.request
import io
from PIL import Image, ImageTk


current_image_bytes = None

def generate_and_display():
    global current_image_bytes
    prompt = prompt_entry.get().strip()
    if not prompt:
        messagebox.showwarning("Warning", "Please enter a description first!")
        return
    
    status_label.config(text="Generating image... Please wait...", fg="#f9e2af")
    root.update()
    
    try:
        formatted_prompt = prompt.replace(" ", "%20")
        image_url = f"https://image.pollinations.ai/p/{formatted_prompt}?model=flux&width=512&height=512"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        request = urllib.request.Request(image_url, headers=headers)
        
        with urllib.request.urlopen(request) as response:
            current_image_bytes = response.read()
            
     
        img_open = Image.open(io.BytesIO(current_image_bytes))
        img_resized = img_open.resize((350, 350), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img_resized)
        
        image_display_label.config(image=img_tk, text="", width=350, height=350)
        image_display_label.image = img_tk
        
        status_label.config(text="Success! Click 'Save Image As' below to save.", fg="#a6e3a1")
        save_btn.config(state=tk.NORMAL) 
        
    except Exception as e:
        status_label.config(text="Failed!", fg="#f38ba8")
        messagebox.showerror("Error", f"Failed to generate image:\n{e}")

def save_image_as():
    if not current_image_bytes:
        messagebox.showwarning("Warning", "No image available to save!")
        return
        
    file_path = filedialog.asksaveasfilename(
        defaultextension=".jpg",
        filetypes=[("JPEG Image", "*.jpg"), ("PNG Image", "*.png"), ("All Files", "*.*")],
        title="Save Image As"
    )
    
    if file_path:
        try:
            with open(file_path, "wb") as f:
                f.write(current_image_bytes)
            messagebox.showinfo("Saved!", f"Image successfully saved at:\n{file_path}")
            status_label.config(text="Image saved successfully!", fg="#a6e3a1")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file:\n{e}")

# UI Design (Tkinter)
root = tk.Tk()
root.title("AI Image Generator")
root.geometry("450x700")
root.configure(bg="#1e1e2e")
root.resizable(False, False)

# Header Title
title_label = tk.Label(root, text="✨ AI Image Generator ✨", font=("Arial", 18, "bold"), fg="#cdd6f4", bg="#1e1e2e")
title_label.pack(pady=15)

# Instruction
instruction_label = tk.Label(root, text="Write the description of your imagination in English:", font=("Arial", 10), fg="#a6adc8", bg="#1e1e2e")
instruction_label.pack(pady=5)

# Input Box
prompt_entry = tk.Entry(root, font=("Arial", 12), width=35, bg="#313244", fg="#cdd6f4", insertbackground="white", justify="center")
prompt_entry.pack(pady=10)
prompt_entry.insert(0, "Ladakh view")

# Generate Button
generate_btn = tk.Button(root, text="Create an image 🎨", font=("Arial", 11, "bold"), bg="#89b4fa", fg="#11111b", command=generate_and_display, cursor="hand2")
generate_btn.pack(pady=8)

# Status Label
status_label = tk.Label(root, text="Your photo will be displayed below", font=("Arial", 9, "italic"), fg="#a6adc8", bg="#1e1e2e")
status_label.pack(pady=4)

# Canvas Display Area
image_display_label = tk.Label(root, text="[ Photo Canvas ]", font=("Arial", 12), fg="#585b70", bg="#313244", width=35, height=17)
image_display_label.pack(pady=10)

# Save Button
save_btn = tk.Button(root, text="💾 Save Image As...", font=("Arial", 10, "bold"), bg="#a6e3a1", fg="#11111b", command=save_image_as, cursor="hand2", state=tk.DISABLED)
save_btn.pack(pady=10)

root.mainloop()