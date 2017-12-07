import subprocess

import boto3
import json
import requests
import time
import click
import os
from tools import get_full_record, get_s3_metadata
import pandas


s3 = boto3.resource('s3')
#bucket = s3.Bucket('cytovas-instrument-files')

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass

@cli.command()
@click.option('--file', help='a specific file')
@click.option('--full', is_flag=True, help='show all fields')
@click.option('--format', default='json', help='format: json, tsv, csv')
@click.option('--s3_metadata', is_flag=True, help='show s3 object metadata')
@click.option('--bucket', default='cytovas-instrument-files')
def list(file,full,bucket,s3_metadata,format):
    bucket_obj = s3.Bucket(bucket)
    records = {}
    for key in bucket_obj.objects.all():
        if file is None or (file and file == key.key):
            if full == True:
                records[key.key]=get_full_record(bucket, key.key)
            elif s3_metadata:
                records[key.key]=get_s3_metadata(bucket, key.key)
            else:
                print(key.key)
    if format=='json':
        if full or s3_metadata == True:
            print(json.dumps(records))
    elif format=='tsv':
        pjson=pandas.read_json(json.dumps(records))
        print(pjson.T.to_csv())

@cli.command()
@click.option('--file', default = None, help='a specific file')
@click.option('--rename', is_flag=True, help='rename downloads to their original files name instead of UUID')
@click.option('--bucket', default='cytovas-instrument-files')
def download(file,rename,bucket):
    bucket_obj = s3.Bucket(bucket)
    for key in bucket_obj.objects.all():
        record = get_full_record(bucket, key.key)
        if file is None or (file and file == key.key):
            if rename:
                os.system("mv /tmp/{0} ./{1}".format(key.key,record['s3_metadata']['qqfilename']))
            else:
                os.system("mv /tmp/{0} ./{0}".format(key.key))

if __name__ == '__main__':
    cli()