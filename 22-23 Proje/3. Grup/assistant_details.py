#İlk olarak, database modülünden get_name fonksiyonunu içeri aktarırız. Bu fonksiyon, veritabanından bir isim alır ve bu ismi name değişkenine atar.
from database import get_name
import os
from sys import platform

name = get_name()

