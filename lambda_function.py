import json
import requests
from time import sleep
import random
from kafka import KafkaProducer
from constants import *
from utils import *

def lambda_handler(event, context):
    request_payload = json.loads(event['Records'][0]['body'])
    print("Received payload from SQS")
    
    try:
        url = 'http://'+ DS1_HOST +'/text_to_attribution_service/services_multiple_requests'
        response = requests.post(url, json=request_payload)
        response = response.json()
    except Exception as e:
        print(e)
        message = "Couldn't send request to DS machine due to exception {}".format(e)
        print(message)
        put_log_events(message)
        return {'statusCode': 400, 'body': json.dumps(message)}
        
    if response['success']:
        all_responses = response['responses']
        
        # Request and Response in one object
        all_request_response = request_payload['requests']
        for request, response in zip(all_request_response, all_responses):
            request['ds_analysis'] = response
        
        # Initializing Kafka Producer
        try:
            # Kafka Topic & Producers
            producer = KafkaProducer(bootstrap_servers=kafka_host_1, 
            value_serializer=lambda x: json.dumps(x).encode('utf-8'))
        except Exception as e:
            message = "Couldn't connect to Kafka because of exception: {}".format(e)
            error_message = message + '\n\n' +  "Failed paylaod: " + str(request_payload)
            print(error_message)
            put_log_events(error_message)
            producer = KafkaProducer(bootstrap_servers=kafka_host_2, 
            value_serializer=lambda x: json.dumps(x).encode('utf-8'))
            # return {'statusCode': 400, 'body': json.dumps(message)}
          
        # Enqueuing request response object to Kafka queue one by one  
        count = 0
        try:
            for obj in all_request_response:
                producer.send(KAFKA_TOPIC, value=obj)
                count+=1
                sleep(1)
            producer.flush()  
            message = "Payload enqueued in Kafka queue successfully!"
        except Exception as e:
            message = "Couldn't send message to Kafka because of exception: {}".format(e) 
            put_log_events(message)
            
        print("Total Request objects enqueued into Kafka: ", count)
        print(message)
        return {'statusCode': 200, 'body': json.dumps(message)}

    else:
        message = "DS machine didn't return correct response!"
        print(message)
        put_log_events(message)
        return {'statusCode': 400, 'body': json.dumps(message)}
        
    
    