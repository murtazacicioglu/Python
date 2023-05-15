import random
from output_module import output

'''kodun genel işlevi: Kod, rastgele görev listelerini kullanarak kullaniciya çeşitli yardım seçenekleri sunar. 
Yardim menüsü, kullanicinin isteğine bağli olarak kisa veya tam bir liste olarak görüntülenebilir.'''

task_list1 = ["Müzik oynatıldı", "Duvar kağıdını değiştir", "Haberleri göster", "Sohbet et", "Matematiksel İfade Çözücü", "Daha Fazlası"]
task_list2 = ["Youtube'da ara", "Google'da ara", "Google Harita aç", "Daha Fazlası"]
task_list3 = ["Asistan adını değiştir", "mail gönder", "Konuş","konuşmayı durdur", "Daha fazlası"]
task_list4 = ["Hava Durumu", "internet bağlantısını kontrol et", "Müzik kontrolü", "Zaman/Tarih bilgisi", "Yeni Sorular Öğrenebilir", "Daha Fazlası"]
task_list5 = ["Konumumu bul", "Google'da ara", "Daha Fazlası"]

task = [task_list1, task_list2, task_list3, task_list4, task_list5]
task2 = [task_list1[:-1], task_list2[:-1], task_list3[:-1], task_list4[:-1], task_list5[:-1]]

def help_greet():
    for x in random.choice(task):
        print("-> ", x) 
    print("For short help list: type --y") 
    print("For complete help list: type --yardım") 
    print()


def yardım(s):
    if s == "--y":
        for x in random.choice(task):
            print("-> ", x)
    else:
        for x in task2:
            for i in x:
                print("-> ", i)


