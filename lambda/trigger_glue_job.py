import boto3

def lambda_handler(event, context):
    glue = boto3.client('glue')

    response = glue.start_job_run(
        JobName='sales_raw_to_processed'
    )

    return {
        'statusCode': 200,
        'body': 'Glue job triggered successfully'
    }
