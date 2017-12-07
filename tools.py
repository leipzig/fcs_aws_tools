import boto3
import logging
import fcsparser
import os.path

logger = logging.getLogger('boto3')
logger.setLevel(logging.INFO)


def get_full_record(bucket, key):
    s3 = boto3.resource('s3')
    s3_object = s3.Object(bucket, key)
    
    #if not os.path.isfile('/tmp/'+key):
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

def get_s3_metadata(bucket, key):
    s3 = boto3.resource('s3')
    s3_object = s3.Object(bucket, key)
    return(s3_object.metadata)
    #print(s3_object.metadata)
    #return({'s3_metadata':s3_object.metadata})