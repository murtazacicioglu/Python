from assistant_details import name
from colorama import Fore

#Bu kod, kullanıcıdan komut satırı girişi almak için kullanılır. Kullanıcıya "Me :" şeklinde bir gösterge sunar.ve kullanıcının giriş yapmasını bekler. Kullanıcıdan alınan giriş değeri, işlev tarafından döndürülür.
def take_input():
	i = input(Fore.BLUE + "Ben : " + Fore.RESET)
	return i
