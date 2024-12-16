import os
import boto3
from configparser import ConfigParser
from datetime import datetime

def get_s3_cliente_credentials():
    config = ConfigParser()
    config_file_dir = f'{os.getcwd()}/aws_cliente.cfg'
    config.read_file(open(config_file_dir))
    region = config.get('AWS_CLIENTE','region')
    aws_access_key_id = config.get('AWS_CLIENTE','aws_access_key_id')
    aws_secret_access_key = config.get('AWS_CLIENTE','aws_secret_access_key')

    return region, aws_access_key_id, aws_secret_access_key

def ref_processing_dates():
    date = datetime.now().strftime('%Y%m%d')
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    return f'{date}_{timestamp}'

def download_data_from_s3_cliente(bucket_name, filename, object_name):
    
    region, aws_access_key_id, aws_secret_access_key = get_s3_cliente_credentials()

    s3_client = boto3.client(
        's3',
        region_name = region,
        aws_access_key_id = aws_access_key_id,
        aws_secret_access_key = aws_secret_access_key
    )

    try:
        response = s3_client.download_file(bucket_name, filename, object_name)
        print(f'File {filename} downloaded from {bucket_name}/{object_name}')
    except Exception as e:
        print(f'Failed to download {filename} from {bucket_name}/{object_name}. Error: {e}')

download_data_from_s3_cliente('bkt-edj-ped-datalake-dev', 'ingestion/tb_faturas/', 'tb_faturas_' + ref_processing_dates() + '.csv')
download_data_from_s3_cliente('bkt-edj-ped-datalake-dev','ingestion/tb_pagamentos/', 'tb_pagamentos_' + ref_processing_dates() + '.csv')