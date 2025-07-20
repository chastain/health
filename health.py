#!/usr/bin/python3

# URL Health Tester
# This code checks http status codes and md5 checksums of page contents.

import urllib.request
import urllib.error

import hashlib
from os import system, name
from time import sleep, localtime, strftime

refresh_after_seconds = 60 # Clear screen and re-run this script every N seconds.
timeout_in_seconds = 10 # We request timeout

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    GREY = '\033[2m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Value 1: Friendly Name
# Value 2: URL
# Value 3: md5 sum of contents of the page. Optional, if not included http status code is the only criteria.
# Tip: to generate an initial md5 sum just enter a fake value for it in the table and it will be generated and written to the terminal.
data = [
    ["Random"],
    ["chasta.in", "https://chasta.in", "fake"],
    ["google", "https://www.google.com"],
    ["aws", "https://www.aws.com"],
    ["duck", "https://www.duck.com"],
]

def verify(record):
    try:
        if len(record) == 1:
            return "heading"

        response = urllib.request.urlopen(record[1], None, timeout_in_seconds)
        http_status_code = response.getcode()
        compare_md5 = len(record) > 2

        if http_status_code >= 200 and http_status_code <= 299:
            if compare_md5:
                md5 = hashlib.md5(response.read()).hexdigest()
                if md5 != record[2]:
                    return("md5 mismatch: " + md5) # pass the expected md5 back as our result so we can display it

            return "success"
        else:
            return "warn"

    except urllib.error.HTTPError as err:
        # I'm not treating redirects as errors
        if err.code >= 300 and err.code <= 399:
            return "redirection"

        return "error"


if __name__ == "__main__":

    try:
        while True:

            _ = system("cls") if name == "nt" else system("clear")

            print("\n" + colors.OKBLUE + "URL Health Tester" + colors.ENDC)
            print("\n" + colors.OKBLUE + "(Ctrl+C to exit)" + colors.ENDC + "\n")
            print("Updated: " + strftime("%Y-%m-%d %H:%M:%S", localtime()) + "\n")

            for id, record in enumerate(data):

                results = verify(record)

                if results == "heading":
                    color = colors.UNDERLINE + colors.BOLD
                elif results == "success":
                    color = colors.OKGREEN
                elif results == "redirection":
                    color = colors.OKCYAN
                elif results == "error":
                    color = colors.FAIL
                else:
                    color = colors.WARNING

                if results == "heading":
                    n = "\n" if id > 1 else ""
                    print(n + color + record[0] + colors.ENDC + "\n")
                else:
                    print(" -> " + color + record[0] + " " + colors.ENDC + colors.GREY + record[1] + colors.ENDC)
                    if results.startswith("md5 mismatch:"):
                        print("     " + results)

            sleep(refresh_after_seconds)

    except KeyboardInterrupt:
        pass
