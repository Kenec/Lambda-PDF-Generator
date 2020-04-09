import boto3
from fpdf import FPDF

s3 = boto3.client('s3')
sqs = boto3.client('sqs')

def pdf_converter(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        body = s3.get_object(Bucket=bucket, Key=key)

        save_to_s3(bucket, key, body)


def generate_pdf(body, key):
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 12)

    text = body['Body'].read().decode('utf-8', 'backslashreplace')

    pdf.write(8, text)
    pdf_file_name = key.replace('incoming/', '') + ".pdf"
    pdf.output("/tmp/"+pdf_file_name, 'F')

    return pdf_file_name


def save_to_s3(bucket, key, body):
     pdf = generate_pdf(body, key)
     s3.upload_file("/tmp/" + pdf, "kene-test", "incoming_PDF/" + pdf)
