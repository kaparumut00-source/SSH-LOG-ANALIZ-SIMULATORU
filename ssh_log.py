import os
import re

print("SSH LOG ANALIZ SIMULATORU")
print("-" * 40)

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
    "Failed password for guest from 10.0.0.8" ]

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

print("BASARILI GIRISLER")
print("-" * 40)

for giris in basarili_girisler:
    print("Kullanici:", giris[0], "| IP:", giris[1])

print("\nBASARISIZ GIRISLER")
print("-" * 40)

for giris in basarisiz_girisler:
    print("Kullanici:", giris[0], "| IP:", giris[1])

print("\nSUPHELI GIRISLER")
print("-" * 40)

for ip, sayi in supheli_ipler.items():
    if sayi >= 2:
        print("Supheli IP:", ip, "| Basarisiz deneme sayisi:", sayi)

print("\nRISKLI KULLANICI ADI DENEMELERI")
print("-" * 40)

for giris in basarisiz_girisler:
    kullanici = giris[0]
    ip = giris[1]

    if kullanici in riskli_kullanicilar:
        print("Riskli kullanici:", kullanici, "| IP:", ip)

en_riskli_ip = ""
en_yuksek_sayi = 0

for ip, sayi in supheli_ipler.items():
    if sayi > en_yuksek_sayi:
        en_yuksek_sayi = sayi
        en_riskli_ip = ip

print("\nEN RISKLI IP ADRESI")
print("-" * 40)
print("IP:", en_riskli_ip)
print("Basarisiz deneme sayisi:", en_yuksek_sayi)
print("\nRISK SEVIYELI SUPHELI GIRISLER")
print("-" * 40)

for ip, sayi in supheli_ipler.items():

    if sayi >= 4:
        risk_seviyesi = "Yuksek Risk"

    elif sayi >= 2:
        risk_seviyesi = "Orta Risk"

    else:
        risk_seviyesi = "Dusuk Risk"

    print("Supheli IP:", ip, "| Basarisiz deneme sayisi:", sayi, "| Risk seviyesi:", risk_seviyesi)

print("\nGENEL RAPOR")
print("-" * 40)
print("Toplam log sayisi:", len(loglar))
print("Basarili giris sayisi:", len(basarili_girisler))
print("Basarisiz giris sayisi:", len(basarisiz_girisler))
print("En riskli IP:", en_riskli_ip)
print("En yuksek basarisiz deneme:", en_yuksek_sayi)

if en_yuksek_sayi >= 4:
    genel_risk = "Yuksek Risk"

elif en_yuksek_sayi >= 2:
    genel_risk = "Orta Risk"

else:
    genel_risk = "Dusuk Risk"    
print("Genel risk seviyesi:", genel_risk)
print("Analiz tamamlandi.")

while True:
    os.system("cls")

    print("SSH LOG ANALIZ MENU")
    print("-" * 40)
    print("1 - Basarili girisleri goster")
    print("2 - Basarisiz girisleri goster")
    print("3 - Supheli IP adreslerini goster")
    print("4 - Riskli kullanicilari goster")
    print("5 - En riskli IP adresini goster")
    print("6 - Risk seviyeli supheli girisleri goster")
    print("7 - Genel raporu goster")
    print("8 - Cikis")

    secim = input("\nSeciminizi girin: ")

    os.system("cls")

    if secim == "1":
        print("BASARILI GIRISLER")
        print("-" * 40)

        for giris in basarili_girisler:
            print("Kullanici:", giris[0], "| IP:", giris[1])

        input("\nMenuye donmek icin Enter'a basin...")

    elif secim == "2":
        print("BASARISIZ GIRISLER")
        print("-" * 40)

        for giris in basarisiz_girisler:
            print("Kullanici:", giris[0], "| IP:", giris[1])

        input("\nMenuye donmek icin Enter'a basin...")

    elif secim == "3":
        print("SUPHELI IP ADRESLERI")
        print("-" * 40)

        for ip, sayi in supheli_ipler.items():
            print("Supheli IP:", ip, "| Basarisiz deneme sayisi:", sayi)

        input("\nMenuye donmek icin Enter'a basin...")

    elif secim == "4":
        print("RISKLI KULLANICI ADI DENEMELERI")
        print("-" * 40)

        for giris in basarisiz_girisler:
            kullanici = giris[0]
            ip = giris[1]

            if kullanici in riskli_kullanicilar:
                print("Riskli kullanici:", kullanici, "| IP:", ip)

        input("\nMenuye donmek icin Enter'a basin...")

    elif secim == "5":
        print("EN RISKLI IP ADRESI")
        print("-" * 40)
        print("IP:", en_riskli_ip)
        print("Basarisiz deneme sayisi:", en_yuksek_sayi)

        input("\nMenuye donmek icin Enter'a basin...")

    elif secim == "6":
        print("RISK SEVIYELI SUPHELI GIRISLER")
        print("-" * 40)

        for ip, sayi in supheli_ipler.items():

            if sayi >= 4:
                risk_seviyesi = "Yuksek Risk"

            elif sayi >= 2:
                risk_seviyesi = "Orta Risk"

            else:
                risk_seviyesi = "Dusuk Risk"

            print("Supheli IP:", ip, "| Basarisiz deneme sayisi:", sayi, "| Risk seviyesi:", risk_seviyesi)

        input("\nMenuye donmek icin Enter'a basin...")

    elif secim == "7":
        print("GENEL RAPOR")
        print("-" * 40)
        print("Toplam log sayisi:", len(loglar))
        print("Basarili giris sayisi:", len(basarili_girisler))
        print("Basarisiz giris sayisi:", len(basarisiz_girisler))
        print("En riskli IP:", en_riskli_ip)
        print("En yuksek basarisiz deneme:", en_yuksek_sayi)
        print("Genel risk seviyesi:", genel_risk)

        input("\nMenuye donmek icin Enter'a basin...")

    elif secim == "8":
        print("Programdan cikiliyor.")
        break

    else:
        print("Hatali secim yaptiniz.")
        input("\nMenuye donmek icin Enter'a basin...")