"""
Licensed under the MIT license.

Copyright © 2022 Olfactomics Oy

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the “Software”), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial
portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import json
import time
from urllib import request, error as url_error
import argparse

# The IP address of IonVision
DEFAULT_IONVISION_ADDRESS = "localhost"
# Sleep this many minutes between scan finishing and another one starting
DEFAULT_SLEEP_TIME_MINUTES = 5.0

# Add support for command line parameters
parser = argparse.ArgumentParser(description="Data loader for Olfactomics database HTTP API.")
parser.add_argument("comment", type=str, nargs="?", help="Comment that gets posted to each started scan. Remember to wrap a comment with spaces with co")
parser.add_argument( "-a", "--address", dest="address", nargs=1, default=[DEFAULT_IONVISION_ADDRESS], type=str, help="The IP address of the IonVision device. e.g. 192.168.10.12")
parser.add_argument( "-s", "--sleep", dest="sleep", nargs=1, default=[DEFAULT_SLEEP_TIME_MINUTES], type=float, help="Sleep for this many minutes between scans.")

# The base address format for the IonVision HTTP API
API_ADDRESS_FORMAT = "http://{}/api"

def start_scan(address: str):
    """
    Start a new scan with IonVision.

    :param address: IP address of the IonVision device.
    """
    scan_url = API_ADDRESS_FORMAT.format(address) + "/currentScan"

    scan_request = request.Request(scan_url, method="POST")

    try:
        response = request.urlopen(scan_request)
    except url_error.HTTPError as error:
        if error.code == 409:
            raise ValueError("IonVision is still scanning, is the set delay long enough for the used parameter preset?")
        elif error.code == 507:
            raise ValueError("IonVision internal memory is full")
        else:
            raise error

def post_comment(address: str, comment_string: str):
    """
    Post a new comment to the IonVision scan comments object.

    :param address: IP address of the IonVision device.
    :param comment_string: The comment string to post.
    """
    comments_url = API_ADDRESS_FORMAT.format(address) + "/currentScan/comments"

    get_comments_request = request.Request(comments_url)

    get_comments_response = request.urlopen(get_comments_request)
    get_comments_response_encoding = get_comments_response.info().get_content_charset("utf-8")
    comments = json.loads(get_comments_response.read().decode(get_comments_response_encoding))
    comments["sequenceComment"] = comment_string

    post_comments_request = request.Request(comments_url, method="PUT")
    post_comments_request.add_header("Content-Type", "application/json")
    comments_json = json.dumps(comments).encode("utf-8")
    post_comments_request.add_header("Content-Length", len(comments_json))

    request.urlopen(post_comments_request, comments_json)

def main():
    """
    The main control loop of the script.
    """
    loop_number = 1
    arguments = parser.parse_args()
    comment = arguments.comment
    address = arguments.address[0]
    sleep_time = arguments.sleep[0]
    print("Trying to connect to IonVision at address {}".format(API_ADDRESS_FORMAT.format(address)))

    while True:
        print("Staring new scan")
        start_scan(address)
        time.sleep(4)

        if comment != None:
            formatted_comment = "{} {}".format(comment, loop_number)
            print("Posting comment \"{}\" to scan".format(formatted_comment))
            post_comment(address, formatted_comment)
        time.sleep((sleep_time * 60) - 4)

        loop_number += 1

if __name__ == "__main__":
    main()