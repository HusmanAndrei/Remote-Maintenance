# Remote Maintenance

This repository contains all code to handle remote maintenance tasks.

## Infrastructure:

API with DB with table of all machines (customer_id, machine_id, last_online, ...)

Remote Machines with internet connection and ssh server and ngrok installed.

## Tools/Frameworks:

AWS Lambda, AWS DynamoDB, ngrok, chalice (for aws lambda api), frontend framework of your choice (e.g. VueJS).

## Workflow:

Dev-Team wants remote access to customer machine

- Send to request to API
    - customer machine queries every 5 minutes if remote access requested.
    - if yes: start ngrok and send host and port of connection to API
    - Finally, Dev-Team is able to connect with remote machine using the url from the API


- Dev-Team wants to deploy updates to a specific machine.
    - Use ansible to execute playbook with updates (take parameter from API

## Getting Started

The folder `api` contains everything that runs on aws. (AWS Lambda, DynamoDB)

The folder `remote-machine` contains everything that runs on the local machines.

See Readme in subfolders for more details.