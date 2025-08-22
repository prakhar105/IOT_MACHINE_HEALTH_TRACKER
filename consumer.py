from kafka import KafkaConsumer
import json, sqlite3
from prometheus_client import start_http_server, Gauge

# Change this to your consumer Tailscale IP
BROKER = "localhost:9092"
#--- Prometheus Metrics ---
start_http_server(8000)
temperature_gauge     = Gauge('iot_temperature_celsius', 'Temperature in Celsius')
humidity_gauge        = Gauge('iot_humidity_percent', 'Humidity in percentage')
vibration_gauge       = Gauge('iot_vibration_units', 'Vibration level')
battery_gauge         = Gauge('iot_battery_percent', 'Battery percentage')
air_quality_gauge     = Gauge('iot_air_quality_index', 'Air Quality Index (AQI)')
light_intensity_gauge = Gauge('iot_light_intensity', 'Light intensity in lumens')
sound_level_gauge     = Gauge('iot_sound_level_db', 'Sound level in decibels')
co2_level_gauge       = Gauge('iot_co2_ppm', 'CO2 level in PPM')
pressure_gauge        = Gauge('iot_pressure_hpa', 'Air pressure in hPa')
motion_gauge          = Gauge('iot_motion_detected', 'Motion detected (0/1)')
device_status         = Gauge('iot_device_active', 'Device heartbeat (1=active)')
device_status.set(1)  # mark device as active

# --- SQLite Database Setup ---
conn = sqlite3.connect("iot_data.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS sensor_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temperature REAL,
    humidity REAL,
    vibration REAL,
    battery REAL,
    air_quality_index REAL,
    light_intensity REAL,
    sound_level REAL,
    co2_level REAL,
    pressure REAL,
    motion_detected INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# --- Kafka Consumer ---
consumer = KafkaConsumer(
    "iot_data",
    bootstrap_servers=[BROKER],
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

print("Listening for messages...")

for msg in consumer:
    data = msg.value
    print("Received:", data)

    cursor.execute("""
        INSERT INTO sensor_data (
            temperature, humidity, vibration, battery,
            air_quality_index, light_intensity, sound_level,
            co2_level, pressure, motion_detected
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["temperature"],
        data["humidity"],
        data["vibration"],
        data["battery_level"],
        data["air_quality_index"],
        data["light_intensity"],
        data["sound_level"],
        data["co2_level"],
        data["pressure"],
        int(data["motion_detected"])  # store boolean as 0/1
    ))
    conn.commit()


    # Update Prometheus gauges
    temperature_gauge.set(data["temperature"])
    humidity_gauge.set(data["humidity"])
    vibration_gauge.set(data["vibration"])
    battery_gauge.set(data["battery_level"])
    air_quality_gauge.set(data["air_quality_index"])
    light_intensity_gauge.set(data["light_intensity"])
    sound_level_gauge.set(data["sound_level"])
    co2_level_gauge.set(data["co2_level"])
    pressure_gauge.set(data["pressure"])
    motion_gauge.set(int(data["motion_detected"]))
    device_status.set(1)  # keep alive heartbeat