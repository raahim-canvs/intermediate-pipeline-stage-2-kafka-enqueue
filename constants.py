import os

kafka_host_1 = "ip-172-30-64-110.ec2.internal:9092"
kafka_host_2 = "ip-172-30-0-144.ec2.internal:9092"

KAFKA_HOSTS = [
    "ip-172-30-64-110.ec2.internal:9092",
    "ip-172-30-0-144.ec2.internal:9092",
    "ip-172-30-196-101.ec2.internal:9092"
]
KAFKA_TOPIC = 'social-element-json'
DS1_HOST = 'ec2-3-88-28-40.compute-1.amazonaws.com'
# DS1_HOST = 'test.datascience.canvs.tv'

WRITE_LOG_GROUP = os.environ['WRITE_LOG_GROUP']
WRITE_LOG_STREAM = os.environ['WRITE_LOG_STREAM']