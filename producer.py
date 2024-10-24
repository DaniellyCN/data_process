from kafka import KafkaProducer
import json
import random
import time
import os

# Carregar variáveis de ambiente do .env


# Conectar ao Kafka no Docker
KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'localhost:9092')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'sensor-topic')

# Função para gerar dados fake de sensor
def generate_sensor_data():
    sensor_id = f"sensor-{random.randint(1, 10)}"
    value = 20 + random.gauss(0, 5)
    timestamp = int(time.time() * 1000)
    return {"sensorId": sensor_id, "value": value, "timestamp": timestamp}

# Configuração do Kafka Producer
producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

try:
    while True:
        sensor_data = generate_sensor_data()
        producer.send(KAFKA_TOPIC, sensor_data)
        print(f"Enviado: {sensor_data}")
        time.sleep(1)
except KeyboardInterrupt:
    producer.close()
