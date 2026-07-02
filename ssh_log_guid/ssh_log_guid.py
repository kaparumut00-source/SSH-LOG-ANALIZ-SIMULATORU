import re
import json
import tkinter as tk
from tkinter import scrolledtext, messagebox

loglar = [
    "Failed password for root from 192.168.1.25",
    "Failed password for admin from 192.168.1.25",
    "Accepted password for umut from 192.168.1.10",
    "Failed password for test from 10.0.0.8",
    "Failed password for root from 192.168.1.25",
    "Accepted password for mustafa from 172.16.0.5",
    "Failed password for admin from 10.0.0.8",
    "Failed password for root from 192.168.1.25",
    "Accepted password for merve from 192.168.1.50",
    "Failed password for guest from 10.0.0.8",
    "Failed password for mert from 55.66.77.88",
    "Failed password for ahmet from 11.22.33.44",
    "Accepted password for ayse from 192.168.2.10",
    "Failed password for selin from 66.77.88.99",
    "Accepted password for emre from 172.16.1.15",
    "Failed password for kerem from 88.99.11.22",
    "Accepted password for zeynep from 10.10.10.5",
    "Failed password for can from 99.88.77.66",
    "Accepted password for ece from 192.168.3.25",
    "Failed password for mert from 55.66.77.88",
    "Failed password for mehmet from 55.66.77.88",
    "Accepted password for elif from 172.20.0.8"
]

basarili_girisler = []
basarisiz_girisler = []
supheli_ipler = {}
riskli_kullanicilar = ["root", "admin", "test", "guest"]

for log in loglar:
    ip_bul = re.search(r"\d+\.\d+\.\d+\.\d+", log)
    kullanici_bul = re.search(r"for (\w+)", log)

    if ip_bul and kullanici_bul:
        ip = ip_bul.group()
        kullanici = kullanici_bul.group(1)

        if "Accepted" in log:
            basarili_girisler.append([kullanici, ip])

        elif "Failed" in log:
            basarisiz_girisler.append([kullanici, ip])

            if ip in supheli_ipler:
                supheli_ipler[ip] += 1
            else:
                supheli_ipler[ip] = 1

en_riskli_ip = ""
en_yuksek_sayi = 0

for ip, sayi in supheli_ipler.items():
    if sayi > en_yuksek_sayi:
        en_yuksek_sayi = sayi
        en_riskli_ip = ip

if en_yuksek_sayi >= 4:
    genel_risk = "Yuksek Risk"
elif en_yuksek_sayi >= 2:
    genel_risk = "Orta Risk"
else:
    genel_risk = "Dusuk Risk"

rapor = {
    "toplam_log_sayisi": len(loglar),
    "basarili_giris_sayisi": len(basarili_girisler),
    "basarisiz_giris_sayisi": len(basarisiz_girisler),
    "en_riskli_ip": en_riskli_ip,
    "en_yuksek_basarisiz_deneme": en_yuksek_sayi,
    "genel_risk_seviyesi": genel_risk
}

with open("rapor.json", "w") as dosya:
    json.dump(rapor, dosya, indent=4)

def ekrana_yaz(metin):
    sonuc_alani.delete("1.0", tk.END)
    sonuc_alani.insert(tk.END, metin)

def basarili_goster():
    metin = "BASARILI GIRISLER\n" + "-" * 40 + "\n"
    for giris in basarili_girisler:
        metin += "Kullanici: " + giris[0] + " | IP: " + giris[1] + "\n"
    ekrana_yaz(metin)

def basarisiz_goster():
    metin = "BASARISIZ GIRISLER\n" + "-" * 40 + "\n"
    for giris in basarisiz_girisler:
        metin += "Kullanici: " + giris[0] + " | IP: " + giris[1] + "\n"
    ekrana_yaz(metin)

def supheli_goster():
    metin = "SUPHELI IP ADRESLERI\n" + "-" * 40 + "\n"
    for ip, sayi in supheli_ipler.items():
        if sayi >= 2:
            metin += "Supheli IP: " + ip + " | Basarisiz deneme sayisi: " + str(sayi) + "\n"
    ekrana_yaz(metin)

def riskli_goster():
    metin = "RISKLI KULLANICI ADI DENEMELERI\n" + "-" * 40 + "\n"
    for giris in basarisiz_girisler:
        kullanici = giris[0]
        ip = giris[1]

        if kullanici in riskli_kullanicilar:
            metin += "Riskli kullanici: " + kullanici + " | IP: " + ip + "\n"
    ekrana_yaz(metin)

def en_riskli_goster():
    metin = "EN RISKLI IP ADRESI\n" + "-" * 40 + "\n"
    metin += "IP: " + en_riskli_ip + "\n"
    metin += "Basarisiz deneme sayisi: " + str(en_yuksek_sayi)
    ekrana_yaz(metin)

def risk_seviyesi_goster():
    metin = "RISK SEVIYELI SUPHELI GIRISLER\n" + "-" * 40 + "\n"

    for ip, sayi in supheli_ipler.items():
        if sayi >= 4:
            risk_seviyesi = "Yuksek Risk"
        elif sayi >= 2:
            risk_seviyesi = "Orta Risk"
        else:
            risk_seviyesi = "Dusuk Risk"

        metin += "Supheli IP: " + ip + " | Basarisiz deneme sayisi: " + str(sayi) + " | Risk seviyesi: " + risk_seviyesi + "\n"

    ekrana_yaz(metin)

def genel_rapor_goster():
    metin = "GENEL RAPOR\n" + "-" * 40 + "\n"
    metin += "Toplam log sayisi: " + str(len(loglar)) + "\n"
    metin += "Basarili giris sayisi: " + str(len(basarili_girisler)) + "\n"
    metin += "Basarisiz giris sayisi: " + str(len(basarisiz_girisler)) + "\n"
    metin += "En riskli IP: " + en_riskli_ip + "\n"
    metin += "En yuksek basarisiz deneme: " + str(en_yuksek_sayi) + "\n"
    metin += "Genel risk seviyesi: " + genel_risk + "\n"
    metin += "JSON raporu olusturuldu: rapor.json"
    ekrana_yaz(metin)

def cikis_yap():
    pencere.destroy()

pencere = tk.Tk()
pencere.title("SSH Log Analiz Simulatoru")
pencere.geometry("760x560")

baslik = tk.Label(pencere, text="SSH Log Analiz Simulatoru", font=("Arial", 18, "bold"))
baslik.pack(pady=10)

buton_alani = tk.Frame(pencere)
buton_alani.pack(pady=5)

tk.Button(buton_alani, text="Basarili Girisler", width=28, command=basarili_goster).grid(row=0, column=0, padx=5, pady=5)
tk.Button(buton_alani, text="Basarisiz Girisler", width=28, command=basarisiz_goster).grid(row=0, column=1, padx=5, pady=5)
tk.Button(buton_alani, text="Supheli IP Adresleri", width=28, command=supheli_goster).grid(row=1, column=0, padx=5, pady=5)
tk.Button(buton_alani, text="Riskli Kullanicilar", width=28, command=riskli_goster).grid(row=1, column=1, padx=5, pady=5)
tk.Button(buton_alani, text="En Riskli IP", width=28, command=en_riskli_goster).grid(row=2, column=0, padx=5, pady=5)
tk.Button(buton_alani, text="Risk Seviyeleri", width=28, command=risk_seviyesi_goster).grid(row=2, column=1, padx=5, pady=5)
tk.Button(buton_alani, text="Genel Rapor", width=28, command=genel_rapor_goster).grid(row=3, column=0, padx=5, pady=5)
tk.Button(buton_alani, text="Cikis", width=28, command=cikis_yap).grid(row=3, column=1, padx=5, pady=5)

sonuc_alani = scrolledtext.ScrolledText(pencere, width=88, height=20)
sonuc_alani.pack(pady=10)

genel_rapor_goster()

pencere.mainloop()