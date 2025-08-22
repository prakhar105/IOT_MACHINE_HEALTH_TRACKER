from kafka import KafkaProducer
import json, time, random

# Change this to your laptop's Tailscale IP
<<<<<<< HEAD
BROKER = #<consumer tailscale IP>
=======
BROKER = #<IP>
>>>>>>> 40584b658c01d5f5aa51e686651b09e8b4ad808a

producer = KafkaProducer(
    bootstrap_servers=[BROKER],
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def generate_sensor_data():
    return {
        "temperature": round(random.uniform(15, 30), 2),
        "humidity": round(random.uniform(30, 70), 2),
        "air_quality_index": random.randint(0, 150),
        "light_intensity": random.randint(100, 1000),
        "sound_level": round(random.uniform(30, 90), 2),
        "co2_level": random.randint(300, 1000),
        "vibration": round(random.uniform(0.0, 5.0), 2),
        "pressure": round(random.uniform(950, 1050), 2),
        "motion_detected": random.choice([True, False]),
        "battery_level": round(random.uniform(20, 100), 2)
    }


while True:
    data = generate_sensor_data()
    print("Publishing:", data)
    producer.send("iot_data", data)
    time.sleep(2)
