# IoT Machine Health Tracker 🚀

This project demonstrates a complete **IoT data pipeline** for monitoring machine health using **Kafka, SQLite, Prometheus, and Grafana**.  

- An **SBC (Single Board Computer)** generates random sensor data and streams it via **Kafka** over Tailscale.  
- A **laptop** consumes the Kafka data, stores it in an **SQLite database**, and exposes metrics through a **Prometheus exporter**.  
- **Prometheus** scrapes the metrics, and **Grafana** visualizes them in real-time dashboards (gauges, charts, alerts).  
   - Contains gauges for temperature, humidity, AQI, battery, etc.  
![](https://github.com/prakhar105/IOT_MACHINE_HEALTH_TRACKER/blob/master/assets/architecture.png)
---

## 📦 Features

- 🔹 Synthetic IoT sensor simulator  
- 🔹 Kafka-based data streaming (SBC → Laptop)  
- 🔹 SQLite database storage  
- 🔹 Prometheus metrics exporter at `:8000/metrics`  
- 🔹 Grafana dashboards with gauges & alerts  

---

## 🛠️ Tech Stack

- **Python** (`kafka-python`, `sqlite3`, `prometheus-client`)  
- **Apache Kafka** (data streaming)  
- **SQLite** (lightweight DB for sensor data)  
- **Prometheus** (metrics collection)  
- **Grafana** (real-time visualization)  
- **Tailscale** (secure network connection)  

---

## ⚙️ Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/<your-repo>/iot-machine-health-tracker.git
cd iot-machine-health-tracker
```

### 2. Install Dependencies
```bash
pip install kafka-python prometheus-client
```

---

### 3. Start Kafka Broker (on SBC or Laptop)
1. Download and extract Kafka (binary release).  
2. Format storage and start broker in **KRaft mode** (no ZooKeeper):
- For Ubuntu  
   ```bash
   bin/kafka-storage.sh random-uuid > cluster.id
   bin/kafka-storage.sh format -t $(cat cluster.id) -c config/kraft/server.properties
   bin/kafka-server-start.sh config/kraft/server.properties
   ```
- For Windows
  ```
   bin\windows\kafka-storage.bat random-uuid
   bin\windows\kafka-storage.bat format -t <YOUR_CLUSTER_ID> -c config\kraft\server.properties
   bin\windows\kafka-server-start.bat config\kraft\server.properties

  ```
3. Create Kafka topic:  
   ```bash
   bin/kafka-topics.sh --create --topic iot_data --bootstrap-server localhost:9092
   ```

---

### 4. Run Producer (on SBC)
- Publishes synthetic IoT sensor data (temperature, humidity, vibration, battery, etc.)  
- Sends JSON messages to Kafka topic `iot_data`  
- Uses the **laptop’s Tailscale IP** as Kafka broker address  

---

### 5. Run Consumer (on Laptop)
- Subscribes to Kafka topic `iot_data`  
- Stores received messages into an **SQLite database** (`iot_data.db`)  
- Exposes Prometheus metrics at `http://localhost:9092/metrics`  

---

### 6. Setup Prometheus
- Install Prometheus and edit `prometheus.yml`:  

```yaml
scrape_configs:
  - job_name: "iot_sensor"
    static_configs:
      - targets: ["localhost:8000"]
```

- Restart Prometheus and verify targets at:  
  [http://localhost:8000/targets](http://localhost:8000/targets)

---

### 7. Setup Grafana
1. Install Grafana and open: [http://localhost:3000](http://localhost:3000)  
   - Default login: `admin / admin`  
2. Add **Prometheus data source** (`http://localhost:8000`)  
3. Import dashboard JSON (`iot_gauges.json`)  
   - Contains gauges for temperature, humidity, AQI, battery, etc.  
![](https://github.com/prakhar105/IOT_MACHINE_HEALTH_TRACKER/blob/master/assets/grafana.png)
---

## 📊 Available Metrics

| Metric Name              | Description                    |
|---------------------------|--------------------------------|
| `iot_temperature_celsius` | Temperature in °C             |
| `iot_humidity_percent`    | Humidity in %                 |
| `iot_vibration_units`     | Vibration level               |
| `iot_battery_percent`     | Battery level (%)             |
| `iot_air_quality_index`   | Air Quality Index (AQI)       |
| `iot_light_intensity`     | Light intensity (lumens)      |
| `iot_sound_level_db`      | Sound level (dB)              |
| `iot_co2_ppm`             | CO₂ level (ppm)               |
| `iot_pressure_hpa`        | Pressure (hPa)                |
| `iot_motion_detected`     | Motion detected (0/1)         |
| `iot_device_active`       | Device heartbeat (0=down, 1=up)|

---

## 📈 Dashboard

- Real-time **gauges** for each metric  
- Motion & device status shown as binary states (Active/Inactive)  
- Configurable thresholds (battery low, AQI unsafe, CO₂ high)  

---

## 🔮 Next Steps

- Add **alerts** (battery < 20%, AQI > 100, CO₂ > 1000 ppm)  
- Migrate from **SQLite → PostgreSQL/MySQL** for scaling  
- Deploy stack via **Docker Compose / Kubernetes**  
- Integrate with **real sensor hardware (MQTT)**  

---

## 👨‍💻 Author

Built by **Prakhar Awasthi** – Master’s in AI, Adelaide 🇦🇺  
