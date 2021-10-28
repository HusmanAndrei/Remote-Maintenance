import requests
import json
API_URL = "http://localhost:3003"

def request_access(key, should_open, device_id, customer_id):
    body = {
        "is_requested": should_open,
        "customer_id" : customer_id
    }
    request = requests.post(API_URL + "/req_to_open/" + device_id + "?verification_key=" + key, data=json.dumps(body),
                            headers={"Content-Type": "application/json"}  ).text
    print(request)

if __name__ == "__main__":
    customer_id = input("Give customer id: ").strip()
    key = input("Give verification key: ").strip()
    should_open = input("Should open connection or close it? Press 1 for open, 2 for close: ").strip()
    should_open = True if should_open == "1" else False
    device_id = input("Give device uuid: ").strip()
    request_access(key, should_open, device_id, customer_id)
