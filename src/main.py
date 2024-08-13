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

        # 클릭 이벤트 설정
        self.image_path = []
        self.cur_idx = 0
        
        self.image_label = tk.Label(self)
        self.image_label.pack()

        self.bind("<Left>", self.show_previous_image)
        self.bind("<Right>", self.show_next_image)
        self.bind("<a>", self.nomal_image)
        self.bind("<s>", self.not_nomal_image)
        
        self.tk_image = None
        
    def set_image(self):
        path = self.path_input.get()
        file_m = File_Management()
        dir = file_m.get_Image(path=path)
        self.image_path = self.filter_image(paths=dir)
        
        if self.image_path:
            self.cur_idx = 0
            self.load_image(self.cur_idx)
        else:
            self.clear_image()
    
    def filter_image(self, paths: list[str]) -> list[str]:
        with open(self.NORMAL_IMAGE, 'r', encoding='utf8') as norml:
            normal_images = {os.path.abspath(line.strip().lower()) for line in norml}

        with open(self.NOT_NORMAL_IMAGE, 'r', encoding='utf8') as not_norml:
            not_normal_images = {os.path.abspath(line.strip().lower()) for line in not_norml}

        filtered_paths = [
            os.path.abspath(path.lower()) for path in paths 
            if os.path.abspath(path.lower()) not in normal_images and os.path.abspath(path.lower()) not in not_normal_images
        ]

        return filtered_paths
    
    def load_image(self, index):
        if not self.image_path or index < 0 or index >= len(self.image_path):
            self.clear_image()
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
    
    def nomal_image(self, event):
        if self.image_path:
            path = self.image_path[self.cur_idx]
            file_m = File_Management()
            file_m.set_Nomal_Image(path=path)
            self.image_path.pop(self.cur_idx)
            if self.cur_idx >= len(self.image_path):
                self.cur_idx = len(self.image_path) - 1
            self.load_image(self.cur_idx) if self.image_path else self.clear_image()
    
    def not_nomal_image(self, event):
        if self.image_path:
            path = self.image_path[self.cur_idx]
            file_m = File_Management()
            file_m.set_Not_Nomal_Image(path=path)
            self.image_path.pop(self.cur_idx)
            if self.cur_idx >= len(self.image_path):
                self.cur_idx = len(self.image_path) - 1
            self.load_image(self.cur_idx) if self.image_path else self.clear_image()
    
    def clear_image(self):
        self.image_label.config(image=None)
        self.tk_image = None

if __name__ == "__main__":
    app = Sorter()
    app.mainloop()
