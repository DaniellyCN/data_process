import json
import pandas as pd
from kafka import KafkaConsumer
import time
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do .env


# Conectar ao Kafka
KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'localhost:9092')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'sensor-topic')

# Configuração do Kafka Consumer
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='earliest',  # Para consumir as mensagens mais antigas
    enable_auto_commit=True,
    group_id='my-group',  # Identificador do grupo de consumidores
)

# Função para calcular a média dos valores recebidos
def calculate_average(data):
    if not data:
        return 0
    return sum(data) / len(data)

# Consumir dados do Kafka e calcular a média
data_buffer = []
start_time = time.time()

try:
    for message in consumer:
        sensor_data = message.value
        print(f"Recebido: {sensor_data}")

        # Adicionar valor ao buffer
        data_buffer.append(sensor_data['value'])

        # Calcular a média a cada 30 segundos
        if time.time() - start_time >= 30:
            average = calculate_average(data_buffer)
            print(f"Média dos últimos 30 segundos: {average}")
            data_buffer.clear()  # Limpar o buffer após calcular a média
            start_time = time.time()  # Reiniciar o timer
except KeyboardInterrupt:
    print("Encerrando o consumidor.")
finally:
    consumer.close()
