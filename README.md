# aws-lambda-unzip-py
Python AWS Lambda function to extract zip files after a virus scan is completed and marked clean.

Virus scan can be done by the Lambda function found https://github.com/upsidetravel/bucket-antivirus-function

To setup in AWS Lambda, create a new Lambda function with Python 2.7 environment and include this Python script, inline for convenience.

Create an SNS notification trigger from the one you created for the virus scan, details can be found in the link above.

Contents of zip file will be extracted to the same location and then will be deleted at the end of the operation.

## Permissions
To remove the uploaded zip file, the role configured in your Lambda function should have a policy similar to this:

```
{
    "Effect": "Allow",
    "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
    ],
    "Resource": [
        "arn:aws:s3:::mybucket"
    ]
}
```

# TODO
You might know the limitations of AWS Lambda. The limitation of maximum execution duration per request could cause problems when unzipping large files, also consider the memory usage.

* Improve performance (if possible) for large files