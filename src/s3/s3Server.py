import boto3
import json
import logging
import socket
import threading
from botocore.exceptions import ClientError

BUFFER = 2048
BUCKETNAME = "nightlightcloud"

conn = boto3.client("s3")

def create_presigned_post(bucket_name, object_name,
                          fields=None, conditions=None, expiration=180):
    """Generate a presigned URL S3 POST request to upload a file

    :param bucket_name: string
    :param object_name: string
    :param fields: Dictionary of prefilled form fields
    :param conditions: List of conditions to include in the policy
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Dictionary with the following keys:
        url: URL to post to
        fields: Dictionary of form fields and values to submit with the POST
    :return: None if error.
    """

    # Generate a presigned S3 POST URL
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_post(bucket_name,
                                                     object_name,
                                                     Fields=fields,
                                                     Conditions=conditions,
                                                     ExpiresIn=expiration)
    except ClientError as err:
        logging.error(err)
        return None

    # The response contains the presigned URL and required fields
    return response

def create_presigned_url(bucket_name, object_name, expiration=180):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as err:
        logging.error(err)
        return None

    # The response contains the presigned URL
    return response

def get_all(cli_sock):
    msg = {}
    names = []
    try:
        for key in conn.list_objects(Bucket=BUCKETNAME)['Contents']:
            names.append(key['Key'])
        
        msg["status"] = True
        msg["names"] =  names

    except Exception as err:
        msg["status"] = False
        msg["err"] = str(err)

    msg = json.dumps(msg).encode()
    cli_sock.send(msg)
    cli_sock.close()

def get_one(cli_sock, data):
    msg = {}
    obj_name = data["name"]
    url = create_presigned_url(bucket_name=BUCKETNAME, object_name=obj_name)

    if url is not None:
        msg["status"] = True
        msg["url"] = url
    else:
        msg["status"] = False
        msg["err"] = "A server error has occured."

    msg = json.dumps(msg).encode()
    cli_sock.send(msg)
    cli_sock.close()

def post_one(cli_sock, data):
    msg = {}
    obj_name = data["name"]
    response = create_presigned_post(bucket_name=BUCKETNAME, object_name=obj_name)

    if response is not None:
        msg["status"] = True
        msg["res"] = response

    else:
        msg["status"] = False
        msg["err"] = "A server error has occured."

    msg = json.dumps(msg).encode()
    cli_sock.send(msg)
    cli_sock.close()

def process(cli_sock):
    cli_sock.settimeout(10)
    raw = cli_sock.recv(BUFFER)
    raw = raw.decode()
    data = json.loads(raw)

    func = data["func"]

    if func == "get_all":
        get_all(cli_sock)
    
    elif func == "get_one":
        get_one(cli_sock, data)
    
    elif func == "post_one":
        post_one(cli_sock, data)


def client_connection():
    addr = '0.0.0.0'
    port = 5674
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_sock.bind((addr, port))
    listen_sock.listen(10)
    print(f"Listening on port: {port}")
    
    while True:
        client, addr = listen_sock.accept()
        print(f"Accepted connection from {addr}")
        
        process_thread = threading.Thread(target=process, args=(client,))
        process_thread.start()

def main():
    _thread = threading.Thread(target=client_connection)
    _thread.start()

if __name__ == "__main__":
    main()
