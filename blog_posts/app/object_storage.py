import boto3

class ObjectStorage:
    def __init__(self):
        self.s3_client = None
        self.bucket_name = None

    def init_app(self, app):
        self.s3_client = boto3.client(
            's3',
            region_name=app.config['AWS_REGION'],
            aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY'],
            endpoint_url=app.config.get('AWS_S3_ENDPOINT_URL')
        )
        self.bucket_name = app.config['AWS_S3_BUCKET_NAME']

    def upload_file(self, file_content, filename):
        return self.s3_client.put_object(Bucket=self.bucket_name, Key=filename, Body=file_content)

    def delete_file(self, filename):
        return self.s3_client.delete_object(Bucket=self.bucket_name, Key=filename)

    def generate_file_url(self, filename):
        return f'{self.s3_client.meta.endpoint_url}/{self.bucket_name}/{filename}'
    

object_storage = ObjectStorage()


def initialize_object_storage(app):
    object_storage.init_app(app)    
