import os
from dotenv import load_dotenv

load_dotenv()

class File_Management():
    """
        이미지 경로 불러오기
        정상, 비정상 이미지를 저장
    """
    def __init__(self) -> None:
        self.NORMAL_IMAGE:str =  os.getenv("NORMAL_IMAGE")
        self.NOT_NORMAL_IMAGE:str =  os.getenv("NOT_NORMAL_IMAGE")
        
        
    def get_Image(self, path)-> list[str]:
        res:list[str] = []
        try:
            for (root, _, files)in os.walk(path):
                for file in files:
                    image_path:str = os.path.join(root, file)
                    res.append(image_path)
        except:
            return None
        return res
    
    def set_Nomal_Image(self, path:str) -> bool:
        try:
            with open(self.NORMAL_IMAGE, 'a', encoding='utf8') as txt:
                txt.write(path + '\n')
                
        except:
            return False
        return True
    
    def set_Not_Nomal_Image(self, path:str)-> bool:
        try:
            with open(self.NOT_NORMAL_IMAGE, 'a', encoding='utf8') as txt:
                txt.write(path + '\n')
        except:
            return False
        return True

