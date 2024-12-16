import os
import boto3
from configparser import ConfigParser

def pick_fatura_file():
    dados = os.listdir(f'{os.getcwd()}')
    for dado in dados:
        if dado.startswith('tb_faturas'):
            filename = dado
    return filename

def pick_pagamentos_file():
    dados = os.listdir(f'{os.getcwd()}')
    for dado in dados:
        if dado.startswith('tb_pagamentos'):
            filename = dado
    return filename

def get_s3_credentials():
    config = ConfigParser()
    config_file_dir = f'{os.getcwd()}/aws_s3.cfg'
    config.read_file(open(config_file_dir))
    region = config.get('AWS_S3','region')
    aws_access_key_id = config.get('AWS_S3','aws_access_key_id')
    aws_secret_access_key = config.get('AWS_S3','aws_secret_access_key')

    return region, aws_access_key_id, aws_secret_access_key

def upload_to_s3(filename, bucket_name, object_name):

    region, aws_access_key_id, aws_secret_access_key = get_s3_credentials()

    s3 = boto3.client(
        's3',
        region_name = region,
        aws_access_key_id = aws_access_key_id,
        aws_secret_access_key = aws_secret_access_key
    )

    object_path = object_name + 'dados/' + filename

    try:
        response = s3.upload_file(filename, bucket_name, object_path)
        print(f'File {filename} uploaded to {bucket_name}/{object_name}')
    except Exception as e:
        print(f'Failed to upload {filename} to {bucket_name}/{object_name}. Error: {e}')

faturas_filename = pick_fatura_file()
pagamentos_filename = pick_pagamentos_file()

upload_to_s3(faturas_filename, 'lake-project-588738593313', '0000_ingestion/tb_fatura/')
upload_to_s3(pagamentos_filename, 'lake-project-588738593313', '0000_ingestion/tb_pagamentos/')