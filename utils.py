import boto3
import time
from constants import *
import os

#region Print results on CloudWatch
def put_log_events(log_message):
    client_logs = boto3.client('logs')
    
    # Create log group and log stream if doesn't exists!
    try:
        client_logs.create_log_group(logGroupName=WRITE_LOG_GROUP)
        client_logs.create_log_stream(logGroupName=WRITE_LOG_GROUP, logStreamName=WRITE_LOG_STREAM)
    except:
        pass
    
    timestamp_for_log_msg = int(round(time.time() * 1000))
    sequence_token = None
    
    # Get sequence token if there are some logs in stream already
    token = client_logs.describe_log_streams(logGroupName=WRITE_LOG_GROUP)
    if 'uploadSequenceToken' in token['logStreams'][0]:
        sequence_token = token['logStreams'][0]['uploadSequenceToken']
    
    #region Write output to log stream
    if sequence_token:
        response = client_logs.put_log_events(
            logGroupName=WRITE_LOG_GROUP,
            logStreamName=WRITE_LOG_STREAM,
            logEvents=[
                {
                    'timestamp': timestamp_for_log_msg,
                    'message': log_message
                }
            ],
            sequenceToken=sequence_token
        )
    else:
        response = client_logs.put_log_events(
            logGroupName=WRITE_LOG_GROUP,
            logStreamName=WRITE_LOG_STREAM,
            logEvents=[
                {
                    'timestamp': timestamp_for_log_msg,
                    'message': log_message
                }
            ]
        )
#endregion