from kafka import KafkaConsumer, KafkaProducer
import json
import time

consumer = KafkaConsumer(
    'stock-req',
    bootstrap_servers=['localhost:9092'],
    group_id='stock-backend-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

res_producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

for message in consumer:
    print(message)
    task_data = message.value
    task_id = task_data['id']
    payload = task_data['payload']
    
    time.sleep(5)  # Heavy processing time
    
    result = {"task_id": task_id, "result": f"Processed {payload}"}
    
    res_producer.send('heavy-tasks-responses', value=result)
    res_producer.flush()
