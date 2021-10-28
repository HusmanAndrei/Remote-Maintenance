# API

see https://aws.github.io/chalice

API Endpoints:

`open/{device_id}` If a remote machine opened a ngrok session. The payload contains the endpoint.

`check/{device_id}` Called by the remote machine to check if maintenance is requested.

## Local Development

`pip install -r requirements`

run DynamoDB locally:
`docker run -p 8000:8000 amazon/dynamodb-local`

[optional] DynamoDB Viewer (https://github.com/aaronshaf/dynamodb-admin)

run api:
`LOCAL=1 chalice local --port 3003`
