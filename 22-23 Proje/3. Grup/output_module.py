import assistant_details 
from speak_module import speak 
from database import speak_is_on 
from colorama import Fore 
#Yardımcının komut satırı çıktısını yöneten işlev.
def output(o):
    if assistant_details.name is None:
        assistant_details.name = "Asistan"
    if o is None:
        o = ""
    # Yardımcının adı ile birlikte çıktıyı kırmızı renkte yazdır
    print(Fore.RED + assistant_details.name + ": " + str(o) + Fore.RESET)   
    if speak_is_on():
        speak(o)
    print()

