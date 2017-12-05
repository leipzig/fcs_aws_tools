import logging
import subprocess
import fcsparser
import boto3
import json
import requests
import time
import click

logger = logging.getLogger('boto3')
logger.setLevel(logging.INFO)

s3 = boto3.resource('s3')
bucket = s3.Bucket('cytovas-instrument-files')

def extract_record(bucket, key):
    s3 = boto3.resource('s3')
    s3_object = s3.Object(bucket, key)

    s3.Bucket(bucket).download_file(key, '/tmp/'+key)
    
    logger.info("i hope fcsparser can handle {0}".format('/tmp/'+key))
    
    fcs_metadata = fcsparser.parse('/tmp/'+key, reformat_meta=True, meta_data_only=True)
    
    #for some reasons this is in bytes
    fcs_metadata['__header__']['FCS format'] = fcs_metadata['__header__']['FCS format'].decode('ascii')
    
    #dynamo doesn't like tuples
    fcs_metadata['_channel_names_'] = list(fcs_metadata['_channel_names_'])
    
    #pandas dataframe
    channels = fcs_metadata.pop('_channels_', None)
    
    #this gets serialized as json so it can be stored in dynamodb
    fcs_channels=channels.to_json()
    
    return({'fcs_metadata':dict(fcs_metadata),'fcs_channels':fcs_channels,'s3_metadata':s3_object.metadata})

def rename_to_original_name():
    for key in bucket.objects.all():
        print(key.key)
        record = extract_record('cytovas-instrument-files', key.key)
        print(record['s3_metadata']['qqfilename'])

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def greeter(**kwargs):
    output = '{0}, {1}!'.format(kwargs['greeting'],
                                kwargs['name'])
    if kwargs['caps']:
        output = output.upper()
    print(output)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='1.0.0')
def greet():
    pass


@greet.command()
@click.argument('name')
@click.option('--file', default='Hello', help='a specific file')
@click.option('--full', is_flag=True, help='show all fields')
def list(**kwargs):
    greeter(**kwargs)


@greet.command()
@click.argument('name')
@click.option('--greeting', default='Goodbye', help='word to use for the greeting')
@click.option('--rename', is_flag=True, help='rename downloads to their original files name instead of UUID')
def download(**kwargs):
    greeter(**kwargs)

if __name__ == '__main__':
    greet()