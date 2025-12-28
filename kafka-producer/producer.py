from kafka import KafkaProducer
import json, time, random

producer = KafkaProducer(
    bootstrap_servers='kafka:29092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

while True:
        data = {
            "deviceId": f"sensor{random.randint(1,10)}",
            "temperature": round(random.uniform(20.0, 35.0), 2),
            "humidity": round(random.uniform(30.0, 70.0), 2),
            "energy_kwh": round(random.uniform(0.5, 5.0), 2),
            "battery_level": random.randint(10, 100),
            "status": random.choice(["OK", "WARNING", "CRITICAL"]),
            "timestamp": int(time.time())
        }
        producer.send('iot-sensors', data)
        time.sleep(5)
        print(f"Sent: {data}")
