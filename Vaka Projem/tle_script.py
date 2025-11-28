import requests 
import os

url = "https://celestrak.org/NORAD/elements/gp.php?NAME=CONNECTA&FORMAT=tle"
url = os.getenv("TLE_URL", url)
response = requests.get(url)


if response.status_code == 200:
    data = response.text
    print("TLE verisi başarıyla alındı!")
    print(data[:300])   



    lines = [ln.strip() for ln in data.splitlines() if ln.strip()]
    for i in range(0, len(lines), 3):
        if i + 2 >= len(lines):
            break
        name = lines[i]
        line1 = lines[i + 1]
        line2 = lines[i + 2]
        print("Uydu:", name)
        print(line1)
        print(line2)
        print("-" * 40)

        
        import os, re
        outdir = "tles"
        outdir = os.getenv("TLE_OUTDIR", outdir)
        os.makedirs(outdir, exist_ok=True)  
        safe_name = re.sub(r'[^A-Za-z0-9._-]+', '_', name)
        filepath = os.path.join(outdir, f"{safe_name}.tle")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(name + "\n")
            f.write(line1 + "\n")
            f.write(line2 + "\n")
        print(f"→ Kaydedildi: {filepath}")

else:
    print("Veri alınamadı:", response.status_code)

    
import subprocess


DEST_HOST ="192.168.1.50"       
DEST_USER = "kullaniciadi"      
DEST_PATH = "/home/kullaniciadi/tles"  
DEST_PORT = 22              
SSH_KEY   = None

DEST_HOST = os.getenv("DEST_HOST", DEST_HOST)
DEST_USER = os.getenv("DEST_USER", DEST_USER)
DEST_PATH = os.getenv("DEST_PATH", DEST_PATH)
DEST_PORT = int(os.getenv("DEST_PORT", DEST_PORT))
SSH_KEY   = os.getenv("SSH_KEY", SSH_KEY)



cmd = ["scp", "-P", str(DEST_PORT)]
if SSH_KEY:
    cmd += ["-i", SSH_KEY]
cmd += ["tles/*", f"{DEST_USER}@{DEST_HOST}:{DEST_PATH}/"]

print("→ SCP komutu çalıştırılıyor:", " ".join(cmd))
res = subprocess.run(" ".join(cmd), shell=True)
if res.returncode == 0:
    print(" Dosyalar başarıyla gönderildi.")
else:
    print(" Gönderimde hata oluştu.")





#  Periyodik çalıştırma (Linux - cron) için yaptım
# Örnek: Her saat başı otomatik çalıştırmak için düzenledim
# crontab -e bir cron örneği
# 0 * * * * TLE_URL=https://celestrak.org/NORAD/elements/stations.txt TLE_OUTDIR=/tmp/tles DEST_HOST=192.168.1.50 DEST_USER=kullaniciadi DEST_PATH=/home/kullaniciadi/tles /usr/bin/python3 /path/tle_script.py >> /var/log/tle_job.log 2>&1
#
# Not: Değerleri ENV ile verdiğimiz için kodu değiştirmeden farklı URL/host/klasör kullanılabilir hale getirdim


