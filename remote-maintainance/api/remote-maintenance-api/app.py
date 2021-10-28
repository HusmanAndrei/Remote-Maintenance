"""
Main entrypoint of the api.
"""

import os

# boto3 for working with aws related stuff, in our case: dynamodb
import boto3

# framework to run the API, CORS (Cross origin policy)
from chalice import CORSConfig, ForbiddenError
from chalice import Chalice, Response


# definitions of constants (e.g. aws region, table name)
import defs

# helpers to work with dynamo db, CRUD operations for dynamodb table
import dynamo_helpers as dy_helpers
# create the whole table function
from dynamo_table_creators import create_table

app = Chalice(app_name="remote-maintenance-api")

##################################################
##              CONFIGURATION                   ##
##################################################

# Set configurations
# in case of local development choose
#   dynamodb endpoint = localhost:8000
#   create Device with uuid=id1

# default (online) values
IS_LOCAL = False
origin = "https://maintenance.clothing-industry.digital"

if os.getenv("LOCAL"):
    IS_LOCAL = True
    dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")
    origin = "http://localhost:8080"
    app.debug = True
else:
    dynamodb = boto3.resource("dynamodb", region_name=defs.AWS_REGION)

print("Is Local", IS_LOCAL)

try:
    create_table(dynamodb, defs.DEVICE_TABLE_NAME)
except:
    # table already exists
    print(f"Table {defs.DEVICE_TABLE_NAME} already exists.")
else:
    print(f"Table {defs.DEVICE_TABLE_NAME} created.")

# instance of the Dynamo Table helper type: DynamoTableItem
Device = dy_helpers.get_dynamo_table_item(dynamodb.Table(defs.DEVICE_TABLE_NAME))

# Create Device id1
if IS_LOCAL:
    try:
        Device({"uuid": "id1", "customer_id": "dummy", "verification_key": "supersafe"}).create()
    except KeyError as ke:
        print("Device id1 already exists")
    else:
        print("Device created")

# CORS Policy for API
cors_config = CORSConfig(
    allow_origin=origin,
    allow_headers=["X-Special-Header"],
    max_age=600,
    expose_headers=["X-Special-Header"],
    allow_credentials=True
)


@app.route("/", cors=cors_config)
def index():
    """
    test if api online
    :return:
    """
    return {"hello": "world"}


@app.route("/devices", cors=cors_config)
def list_devices():
    """
    list all devices
    :return:
    """
    return {"devices": Device.list_all()}

def compare_verif_key(request, verif_key_dynamo):
    if request and request.query_params:
        print(request.query_params)
        verif_query_param = request.query_params.get('verification_key')
        if verif_query_param != verif_key_dynamo:
            raise ForbiddenError("Permission denied")
    else:
        raise ForbiddenError("No query params")


@app.route("/check/{device_id}", methods=["GET"], cors=cors_config)
def check_for_request(device_id):
    """
    check if update is requested
    :param device_id: uuid of device
    :return:
    """
    d = Device({"uuid": device_id})
    d.get()
    verification_key_dynamo = d.data["verification_key"]
    compare_verif_key(app.current_request, verification_key_dynamo)
    return {"is_requested": bool(d["is_requested"])}


@app.route("/open/{device_id}", methods=["POST"], cors=cors_config)
def opened_ngrok_session(device_id):
    """
    save url to database as ssh_url
    :param device_id: uuid of device
    :return:
    """
    d = Device({"uuid": device_id})
    d.get()
    verification_key_dynamo = d.data["verification_key"]
    compare_verif_key(app.current_request, verification_key_dynamo)

    print("received request for ", device_id)
    d = Device({"uuid": device_id})
    updated = d.update_sshtunnel(url=app.current_request.json_body["url"])
    return Response(updated)

@app.route("/req_to_open/{device_id}", methods=["POST"], cors=cors_config)
def request_open_ngrok(device_id):
    """
    save url to database as ssh_url
    :param device_id: uuid of device
    :return:
    """
    d = Device({"uuid": device_id})
    d.get()
    verification_key_dynamo = d.data["verification_key"]
    compare_verif_key(app.current_request, verification_key_dynamo)

    print("received request for ", device_id)
    d = Device({"uuid": device_id})
    updated = d.update_request_check(should_open=app.current_request.json_body["is_requested"],
                                     customer_id=app.current_request.json_body["customer_id"])
    return Response(updated)

@app.route("/create", methods=['POST'], cors=cors_config)
def add_device():
    device_dict = Device({ "customer_id": app.current_request.json_body["customer_id"], "is_requested": False,
                           "verification_key": app.current_request.json_body['verification_key']})
    device_dict.create()
    return Response({"created": True})