from datetime import datetime
import tkinter as tk
from tkinter import messagebox

hocalar = []
hoca_ofis_zamanlari = {}
ogr_randevulari = {}


def yonetici():
    # Yönetici window
    yonetici_window = tk.Toplevel(window)
    yonetici_window.title("Yönetici İşlemleri")
    yonetici_window.geometry("400x500")

    # Hoca Label ve entry
    hoca_label = tk.Label(yonetici_window, text="Hoca İsmi:")
    hoca_label.pack(padx=10, pady=5)
    hoca_entry = tk.Entry(yonetici_window)
    hoca_entry.pack(padx=10, pady=5)

    # hoca ekle
    def hoca_ekle():
        hoca_ismi = hoca_entry.get()
        if hoca_ismi.strip() == "":
            messagebox.showerror("Hata", "Hoca ismi boş olamaz.")
        elif hoca_ismi in hocalar:
            messagebox.showerror("Hata", "Hoca listede zaten var.")
        else:
            hocalar.append(hoca_ismi)
            hoca_listesi.insert(tk.END, hoca_ismi)
            messagebox.showinfo("Başarılı", "Hoca başarıyla eklendi.")

    # hoca ekle button
    hoca_ekle_btn = tk.Button(yonetici_window, text="Hoca Ekle", command=hoca_ekle)
    hoca_ekle_btn.pack(padx=10, pady=5)

    # hoca sil
    def hoca_sil():
        secilen_hoca_index = hoca_listesi.curselection()
        if not secilen_hoca_index:
            messagebox.showerror("Hata", "Lütfen bir hoca seçiniz.")
            return

        secilen_hoca_index = secilen_hoca_index[0]
        secilen_hoca = hoca_listesi.get(secilen_hoca_index)
        if secilen_hoca in hocalar:
            hocalar.remove(secilen_hoca)
            hoca_listesi.delete(secilen_hoca_index)
            messagebox.showinfo("Başarılı", f"{secilen_hoca} hocası listeden silindi.")
        else:
            messagebox.showerror("Hata", f"{secilen_hoca} hocası listede bulunamadı.")

    # hoca sil button
    hoca_sil_btn = tk.Button(yonetici_window, text="Hoca Sil", command=hoca_sil)
    hoca_sil_btn.pack(padx=10, pady=5)

    # Hoca Listbox
    hoca_listesi = tk.Listbox(yonetici_window)
    hoca_listesi.pack(padx=10, pady=10)
    for h, hoca_adi in enumerate(hocalar, start=1):
        hoca_listesi.insert(tk.END, f"{h}. {hoca_adi}")


def hoca():
    # Hoca window
    hoca_window = tk.Toplevel(window)
    hoca_window.title("Hoca İşlemleri")
    hoca_window.geometry("400x500")

    # Hoca Listbox
    hoca_listesi = tk.Listbox(hoca_window, width=45, height=10)
    hoca_listesi.pack(padx=10, pady=10)
    for h, hoca_adi in enumerate(hocalar, start=1):
        hoca_listesi.insert(tk.END, f"{h}. {hoca_adi}")

    # Ofis Zamanı Oluştur Button
    def ofis_zamani_olustur():
        secilen_hoca = hoca_listesi.get(tk.ACTIVE)
        secilen_hoca = secilen_hoca.split(". ")[1]  # Remove the index number
        tarih_str = tarih_entry.get()
        saat_str = saat_entry.get()
        zaman_str = tarih_str + ' ' + saat_str
        # try-except ile Error handling
        try:
            datetime_obj = datetime.strptime(zaman_str, "%d-%m-%Y %H:%M")
            hoca_ofis_zamani = datetime_obj.strftime("%d-%m-%Y %H:%M")
            if hoca_ofis_zamani in hoca_ofis_zamanlari.get(secilen_hoca, []):
                messagebox.showerror("Hata", "Bu tarih zaten mevcuttur.")
            else:
                if secilen_hoca not in hoca_ofis_zamanlari:
                    hoca_ofis_zamanlari[secilen_hoca] = []
                hoca_ofis_zamanlari[secilen_hoca].append(hoca_ofis_zamani)
                messagebox.showinfo("Başarılı", "Ofis zamanı başarıyla oluşturuldu.")
        except ValueError:
            messagebox.showerror("Hata", "Geçersiz tarih veya saat formatı.")

    # Tarih Label and Entry
    tarih_label = tk.Label(hoca_window, text="Tarih (GG-AA-YYYY):")
    tarih_label.pack(padx=10, pady=5)
    tarih_entry = tk.Entry(hoca_window)
    tarih_entry.pack(padx=10, pady=5)

    # Saat Label and Entry
    saat_label = tk.Label(hoca_window, text="Saat (HH:MM):")
    saat_label.pack(padx=10, pady=5)
    saat_entry = tk.Entry(hoca_window)
    saat_entry.pack(padx=10, pady=5)

    # Ofis Zamanı Oluştur Button
    ofis_zamani_btn = tk.Button(hoca_window, text="Ofis Zamanı Oluştur", command=ofis_zamani_olustur)
    ofis_zamani_btn.pack(padx=10, pady=10)


def ogr():
    # Öğrenci window
    ogrenci_window = tk.Toplevel(window)
    ogrenci_window.title("Öğrenci İşlemleri")
    ogrenci_window.geometry("400x550")

    # Hoca Listbox
    hoca_label = tk.Label(ogrenci_window, text="Hocalar:")
    hoca_label.pack(padx=10, pady=5)
    hoca_listesi = tk.Listbox(ogrenci_window)
    hoca_listesi.pack(padx=10, pady=10)
    for h, hoca_adi in enumerate(hocalar, start=1):
        hoca_listesi.insert(tk.END, f"{h}. {hoca_adi}")

    # Tarih Listbox
    tarih_label = tk.Label(ogrenci_window, text="Tarihler:")
    tarih_label.pack(padx=10, pady=5)
    tarihler_listesi = tk.Listbox(ogrenci_window)
    tarihler_listesi.pack(padx=10, pady=10)

    secilen_hoca = None

    # hoca seçme button
    def hoca_sec():
        nonlocal secilen_hoca
        secilen_hoca_index = hoca_listesi.curselection()
        if not secilen_hoca_index:
            messagebox.showerror("Hata", "Lütfen bir hoca seçiniz.")
            return

        secilen_hoca_index = secilen_hoca_index[0]
        secilen_hoca = hocalar[secilen_hoca_index]

        randevulari = hoca_ofis_zamanlari.get(secilen_hoca, [])
        tarihler_listesi.delete(0, tk.END)
        for tarih in randevulari:
            tarihler_listesi.insert(tk.END, tarih)

    hoca_sec_btn = tk.Button(ogrenci_window, text="Tarihleri Göster", command=hoca_sec)
    hoca_sec_btn.pack(padx=10, pady=5)

    # Randevu al button
    def rendevu_al():
        nonlocal secilen_hoca
        secilen_tarih_index = tarihler_listesi.curselection()

        if not secilen_hoca or not secilen_tarih_index:
            messagebox.showerror("Hata", "Lütfen önce bir hoca seçiniz ve ardından bir tarih seçiniz.")
            return

        secilen_tarih_index = secilen_tarih_index[0]
        secilen_tarih = hoca_ofis_zamanlari[secilen_hoca][secilen_tarih_index]

        if secilen_hoca in ogr_randevulari:
            messagebox.showerror("Hata", "Zaten bir randevunuz bulunmaktadır.")
            return

        ogr_randevulari[secilen_hoca] = secilen_tarih
        messagebox.showinfo("Başarılı", "Randevu başarıyla alındı.")

    rendevu_al_btn = tk.Button(ogrenci_window, text="Randevu Al", command=rendevu_al)
    rendevu_al_btn.pack(padx=10, pady=5)

    # randevularım button
    def randevularim_goruntule():
        appointments = "\n".join([f"{hoca_tarih}: {tarih}" for hoca_tarih, tarih in ogr_randevulari.items()])
        messagebox.showinfo("Randevu Listesi", appointments)

    randevularim_goruntule_btn = tk.Button(ogrenci_window, text="Randevularım", command=randevularim_goruntule)
    randevularim_goruntule_btn.pack(padx=10, pady=5)


def program_sonladir():
    window.destroy()


def main():
    global window
    window = tk.Tk()
    window.title("e-Randevu Sistemi")
    window.geometry("300x300")

    # Main window buttons
    admin_button = tk.Button(window, text="Yönetici Girişi", command=yonetici, width=17, height=3)
    admin_button.grid(row=0, pady=5, columnspan=2)

    professor_button = tk.Button(window, text="Hoca Girişi", command=hoca, width=17, height=3)
    professor_button.grid(row=1, pady=5, columnspan=2)

    student_button = tk.Button(window, text="Öğrenci Girişi", command=ogr, width=17, height=3)
    student_button.grid(row=2, pady=5, columnspan=2)

    exit_button = tk.Button(window, text="Program Sonlandır", command=program_sonladir, width=17, height=3)
    exit_button.grid(row=3, pady=5, columnspan=2)

    # Centering the buttons
    window.update_idletasks()
    window_width = window.winfo_width()
    button_width = max(admin_button.winfo_width(), professor_button.winfo_width(), student_button.winfo_width(), exit_button.winfo_width())

    for i in range(4):
        window.grid_rowconfigure(i, minsize=0, weight=1)

    window.grid_columnconfigure(0, minsize=(window_width - button_width) // 2, weight=1)
    window.grid_columnconfigure(1, minsize=(window_width - button_width) // 2, weight=1)

    window.mainloop()


if __name__ == "__main__":
    main()
