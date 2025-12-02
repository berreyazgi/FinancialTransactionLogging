import pandas as pd
import sys
import time 


from database import TransactionDB, Base, engine, SessionLocal 



print("Veritabanı bağlantısı bekleniyor...")
time.sleep(10) 

try:
    Base.metadata.create_all(bind=engine)
    print("Veritabanı tabloları başarıyla oluşturuldu/kontrol edildi.")
except Exception as e:
    print(f"HATA: Tablolar oluşturulamadı: {e}")
    sys.exit(1)



csv_file_path = "paysim_data.csv"  
try:
    df = pd.read_csv(csv_file_path).head(100) 
    print(f"'{csv_file_path}' dosyasından ilk 100 satır okundu.")
except FileNotFoundError:
    print(f"HATA: {csv_file_path} dosyası bulunamadı. Lütfen dosyanın kök dizinde olduğundan emin olun.")
    sys.exit(1)

session = SessionLocal()

try:
    count = 0
    for index, row in df.iterrows():
    
        new_transaction = TransactionDB(
            sender=row['nameOrig'],      
            receiver=row['nameDest'],    
            amount=float(row['amount']), 
            status="Historical"          
        )
        
        session.add(new_transaction)
        count += 1
    
    session.commit()
    print(f"Başarılı! Toplam {count} adet işlem veritabanına 'Historical' olarak yüklendi.")

except KeyError as e:
   
    print(f"HATA: CSV'de {e} sütunu bulunamadı. Lütfen CSV'deki sütun adlarının doğru olduğundan emin olun.")
    session.rollback()
    sys.exit(1)
    
except Exception as e:
   
    print(f"Beklenmeyen Veritabanı Hatası: {e}")
    session.rollback()
    sys.exit(1)
    
finally:
    session.close()