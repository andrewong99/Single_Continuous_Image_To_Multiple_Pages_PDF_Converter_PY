import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from reportlab.pdfgen import canvas

# Increase the size limit for images to prevent DecompressionBombError
Image.MAX_IMAGE_PIXELS = None

class PDFCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to PDF Converter")
        
        # Set the window size (triple the default size)
        self.root.geometry("900x600")
        
        self.label = tk.Label(root, text="Select an Image to Convert to PDF", font=("Arial", 18))
        self.label.pack(pady=20)
        
        self.select_button = tk.Button(root, text="Select Image", command=self.select_image, font=("Arial", 14))
        self.select_button.pack(pady=10)
        
    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if file_path:
            self.save_as_pdf(file_path)
    
    def save_as_pdf(self, file_path):
        try:
            image = Image.open(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open image: {e}")
            return
        
        width, height = image.size
        slice_height = 2480
        
        num_slices = (height + slice_height - 1) // slice_height
        
        pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not pdf_path:
            return
        
        c = canvas.Canvas(pdf_path, pagesize=(width, slice_height))
        
        for i in range(num_slices):
            upper = i * slice_height
            lower = min((i + 1) * slice_height, height)
            bbox = (0, upper, width, lower)
            slice_img = image.crop(bbox)
            slice_path = f"{pdf_path[:-4]}_slice_{i}.png"
            slice_img.save(slice_path)
            
            c.drawImage(slice_path, 0, 0, width=width, height=slice_height)
            c.showPage()
            
            os.remove(slice_path)
        
        c.save()
        messagebox.showinfo("Success", f"PDF saved successfully as {pdf_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFCreatorApp(root)
    root.mainloop()
