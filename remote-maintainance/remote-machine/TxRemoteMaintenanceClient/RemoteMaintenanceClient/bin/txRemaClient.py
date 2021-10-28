"""
Client that runs forever and checks if access requested.
"""
import logging
import os
import sys
import time

import requests
from pyngrok import ngrok

# seconds to wait before next check if remote maintenance requested
check_interval = 300

device_id = "id1"

IS_LOCAL = False
api_base = "https://.com"

if os.getenv("LOCAL"):
    IS_LOCAL = True
    api_base = "http://localhost:3003"
    check_interval = 10
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def main():
    """
    handle the main process as a state machine:
    CHECK_FOR_REQUEST --> START_NGROK
    :return:
    """

    state = "CHECK_FOR_REQUEST"
    while True:

        if state == "CHECK_FOR_REQUEST":
            logging.info("check for request")
            resp = requests.get(f"{api_base}/check/{device_id}?verification_key={os.getenv('verification_key')}")
            if resp.json().get("is_requested"):
                state = "START_NGROK"
            else:
                logging.info(f"wait for {check_interval}")
                time.sleep(check_interval)
                continue

        if state == "START_NGROK":
            logging.info("start ngrok")
            ssh_tunnel = ngrok.connect(22, "tcp")
            print(ssh_tunnel)
            requests.post(f"{api_base}/open/{device_id}?verification_key={os.getenv('verification_key')}",
                          json={"url": ssh_tunnel.public_url})
            time.sleep(600)
            state = "CHECK_FOR_CLOSE_REQUEST"

        if state == "CHECK_FOR_CLOSE_REQUEST":
            logging.info("check for close request")
            resp = requests.get(f"{api_base}/check/{device_id}?verification_key={os.getenv('verification_key')}")
            if not resp.json().get("is_requested"):
                ngrok.disconnect(ssh_tunnel.public_url)
                state = "CHECK_FOR_REQUEST"
                time.sleep(check_interval)
            else:
                logging.info(f"wait for {check_interval}")
                time.sleep(check_interval)
                continue
            pass


if __name__ == "__main__":
    main()
