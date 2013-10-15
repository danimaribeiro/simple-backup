'''
Created on 14/10/2013

@author: Danimar
'''
import os
from boto.s3.connection import S3Connection
from boto.s3.key import Key

def upload_to_s3(aws_access_key, aws_secret_key, bucket, file):
    conn = S3Connection(aws_access_key, aws_secret_key)
    bucket = conn.create_bucket(bucket)
    k = Key(bucket)
    k.key = os.path.basename(file)
    k.name = os.path.basename(file)
    k.set_contents_from_filename(file)
    