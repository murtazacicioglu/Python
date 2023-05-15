import os.path, time
import os
from database import get_last_modify, update_last_modify

files = "C:/Users/svimu/Desktop/asistant/input/intents.json"

last_modify =  time.ctime(os.path.getmtime(files))

def check_last_modify():
    memory_last_modify = get_last_modify()
    if last_modify == memory_last_modify:
        print("Model güncellendi.")
    
    else:
        print("Model güncellenmesi için bekleyiniz.")
        #Model_train.py betiğini arka planda çalıştırmak için pythonw kullanıldı
        cmd = 'pythonw Model_train.py'
        os.system(cmd)
        update_last_modify(last_modify)
        print("Model güncellendi. Teşekkürlerr!!!")