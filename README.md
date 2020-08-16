# aws-chatpost

aws-chatpost sends events to Google Chat webhook URL on changing AWS Step Functions Execution Status.

## Description

Lambda function 'chatpost' is invoked by Amazon Cloudwatch Events when targets changes the state.
This function posts a card-typed messsage to Google Chat webhook URL you configured.

## Install

This app is created to be deployed by AWS SAM(Serverless Application Model).

To install the AWS SAM CLI, see following pages.

[Installing the AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)

```bash
git clone https://github.com/tosh223/aws-chatpost.git
cd ./aws-chatpost
```

## Usage

Please set following configurations to ```template.yaml```.

- Google Chat Webhook URL
- Image URL
- Your stetemachine Arn

```bash
sam build
sam deploy --guided
```
