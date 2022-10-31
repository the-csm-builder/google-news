from datetime import date, datetime, timezone, timedelta
from newsapi import NewsApiClient
import os
from json2html import *
import boto3
from botocore.exceptions import ClientError

# Dates
dt = date.today()
iso_date = dt.isoformat()
date_formatted = dt.strftime("%B %d, %Y")
# News API
newsapi = NewsApiClient(api_key='xxxx')
search = 'xxx'

from_date = datetime.now(timezone.utc) + timedelta(days=-3)
end_time = datetime.now(timezone.utc) + timedelta(days=0)

# /v2/everything
all_articles = newsapi.get_everything(q=search,
                                      from_param=from_date,
                                      to=end_time,
                                      language='en',
                                      sort_by='relevancy'
                                      )

# items = all_articles

# convert json to html
bodyconverted = json2html.convert(json=all_articles)

def send_email():
    SENDER = "XXX"  # must be verified in AWS SES Email
    RECIPIENT = "XXX"  # must be verified in AWS SES Email
    RECIPIENT2 = "XXX" # must be verified in AWS SES Email

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "XXX"

    # The subject line for the email.
    SUBJECT = search + "News" + ":" + iso_date

    # The email body for recipients with non-HTML email clients.
    # BODY_TEXT = (itemstring)

    # The HTML body of the email.
    BODY_HTML = bodyconverted
    # """<html>
    # <head></head>
    # <body>
    # <h1>Hey Hi...</h1>
    # <p>This email was sent with
    #     <a href='https://aws.amazon.com/ses/'>Amazon SES CQPOCS</a> using the
    #     <a href='https://aws.amazon.com/sdk-for-python/'>
    #     AWS SDK for Python (Boto)</a>.</p>
    # </body>
    # </html>
    #             """

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses', region_name=AWS_REGION)

    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                    RECIPIENT2
                ],
            },
            Message={
                'Body': {
                    'Html': {

                        'Data': BODY_HTML
                    },
                    # 'Text': {

                    #     'Data': BODY_TEXT
                    # },
                },
                'Subject': {

                    'Data': SUBJECT
                },
            },
            Source=SENDER
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

# uncomment this labmda when moving it to AWS. Will run in container image in lambda

# def lambda_handler(event, context):
send_email()
print('Done')
