import os

from dotenv import load_dotenv
import tkinter as tk
from PIL import Image, ImageTk

from module.sub import File_Management

load_dotenv()

class Sorter(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.NORMAL_IMAGE = os.getenv("NORMAL_IMAGE")
        self.NOT_NORMAL_IMAGE = os.getenv("NOT_NORMAL_IMAGE")
        
        self.title("이미지 분류기")
        self.geometry("1200x600")
        self.resizable(False, False)

        custom_font = ("Arial", 16)

        frame = tk.Frame(self)
        frame.pack(pady=10)

        self.path_input = tk.Entry(frame, width=30, font=custom_font)
        self.path_input.pack(side=tk.LEFT, padx=(0, 10))

        self.submit = tk.Button(frame, text="불러오기", command=self.set_image, width=10)
        self.submit.pack(side=tk.LEFT)

        # 클릭 이벤드
        self.image_path = []
        self.cur_idx = 0
        
        self.image_label = tk.Label(self)
        self.image_label.pack()

        self.bind("<Left>", self.show_previous_image)
        self.bind("<Right>", self.show_next_image)
    
    def set_image(self):
        path = self.path_input.get()
        file_m = File_Management()
        dir = file_m.get_Image(path=path)
        self.image_path = self.filter_image(dir)
        
        if self.image_path:
            self.cur_idx = 0
            self.load_image(self.cur_idx)
    
    def filter_image(self, paths: list[str]) -> list[str]:
        with open(self.NORMAL_IMAGE, 'r', encoding='utf8') as norml:
            normal_images = {line.strip() for line in norml}

        with open(self.NOT_NORMAL_IMAGE, 'r', encoding='utf8') as not_norml:
            not_normal_images = {line.strip() for line in not_norml}

        filtered_paths = [
            path for path in paths 
            if path not in normal_images and path not in not_normal_images
        ]

        return filtered_paths
    
    def load_image(self, index):
        if not self.image_path:
            return
        
        try:
            image_path = self.image_path[index]
            image = Image.open(image_path)
            
            
            desired_size = (800, 400)
            image.thumbnail(desired_size, Image.LANCZOS)
            
            self.tk_image = ImageTk.PhotoImage(image)
            
            self.image_label.config(image=self.tk_image)
            
            self.image_label.update_idletasks()
            self.image_label.configure(width=desired_size[0], height=desired_size[1])
        
        except Exception as e:
            print(f"Error loading image: {e}")
    
    def show_previous_image(self, event):
        if self.cur_idx > 0:
            self.cur_idx -= 1
            self.load_image(self.cur_idx)
    
    def show_next_image(self, event):
        if self.cur_idx < len(self.image_path) - 1:
            self.cur_idx += 1
            self.load_image(self.cur_idx)

if __name__ == "__main__":
    app = Sorter()
    app.mainloop()