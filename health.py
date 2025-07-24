#!/usr/bin/env python3

# URL Health Monitor
# This code checks http status codes and md5 checksums of URLs and displays a basic report in the terminal.

import urllib.request
import urllib.error
import json
import hashlib
from os import system, name
from time import sleep, localtime, strftime

# Load the config file so we can pull values from it below
with open('config.json', 'r') as file:
    json_config_data = json.load(file)

# Clear screen and re-run this script every N seconds.
refresh_seconds = json_config_data["refresh_seconds"]
# How long before we time out a request
timeout_seconds = json_config_data["timeout_seconds"]

# This won't work in unsupported terminal emulators, maybe I should make a wrapper for printing output
# that can apply these or not based on config or actually do the work to determine if output is on a tty that supports
# these escape sequences.
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
data = json_config_data["data"]

def verify(record):
    http_status_code = 0
    try:
        if len(record) == 1:
            return None, "heading"

        response = urllib.request.urlopen(record[1], None, timeout_seconds)
        http_status_code = response.getcode()
        compare_md5 = len(record) > 2

        if http_status_code >= 200 and http_status_code <= 299:
            if compare_md5:
                md5 = hashlib.md5(response.read()).hexdigest()
                if md5 != record[2]:
                    return http_status_code, "md5 mismatch: " + md5 # pass the expected md5 back as our result so we can display it

            return http_status_code, "success"
        else:
            return http_status_code, "warn"

    except urllib.error.HTTPError as err:

        # I'm treating "Forbidden" responses as warnings.
        if err.code == 403:
            return 403, "warn"

        # I'm not treating redirects as errors
        if err.code >= 300 and err.code <= 399:
            return http_status_code, "redirection"

        return err.code, "error"
    except Exception as ex:
        # In case the error was in the library we should respond appropriately
        return "???", "error"

if __name__ == "__main__":

    try:
        while True:

            _ = system("cls") if name == "nt" else system("clear")

            print("\n" + colors.OKBLUE + "URL Health Monitor" + colors.ENDC)
            print("Updated: " + strftime("%Y-%m-%d %H:%M:%S", localtime()) + ". Refreshes every " + str(refresh_seconds) + " seconds.\n")

            for id, record in enumerate(data):

                http_status_code, results = verify(record)

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
                    print(" -> " + color + record[0] + " [" + str(http_status_code) + "] " + colors.ENDC + colors.GREY + record[1] + colors.ENDC)
                    if results.startswith("md5 mismatch:"):
                        print("     " + results)

            print(colors.OKCYAN + "\n(Ctrl+C to exit)" + colors.ENDC + "\n")
            sleep(refresh_seconds)

    except KeyboardInterrupt:
        pass
