import json
import os 
from kafka import KafkaConsumer 
from database import SessionLocal, TransactionDB, engine, Base

# Worker, tabloların oluşturulduğundan emin olmak için
Base.metadata.create_all(bind=engine)

# Kafka Ayarları
KAFKA_TOPIC = "transaction_events"
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
BOOTSTRAP_SERVERS = [KAFKA_BROKER]

try:
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',
        group_id='finance_worker_group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    print(f"Worker başlatıldı ve Kafka dinleniyor: {KAFKA_BROKER}")
except Exception as e:
    print(f"Kafka Consumer başlatılırken HATA: {e}")
   

for message in consumer:
    data = message.value
    print(f"Mesaj Geldi: {data}")

    # Her mesaj için Veritabanı oturumu aç
    session = SessionLocal()
    
    try:
        # Gelen JSON verisini DB Modeline çevir
        new_transaction = TransactionDB(
            sender=data['sender'],
            receiver=data['receiver'],
            amount=float(data['amount']),
            # Worker, işlemi tamamladığında durumu "Completed" yap
            status="Completed" 
        )
        session.add(new_transaction)
        session.commit()
        print(f"DB'ye Kaydedildi! ID: {new_transaction.id}")
        
    except KeyError as e:
        print(f"Hata: Gelen mesajda eksik alan var: {e}")
        session.rollback()
    except Exception as e:
        print(f"Beklenmeyen İşleme Hatası: {e}")
        session.rollback()
    finally:
        session.close()