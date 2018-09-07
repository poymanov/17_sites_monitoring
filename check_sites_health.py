import argparse
import os
import sys
import re
import requests
import whois
from datetime import datetime, timedelta


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='File with urls')

    parsed_args = parser.parse_args()
    return parsed_args


def get_urls_list(filepath):
    if not os.path.isfile(filepath):
        return None

    with open(filepath) as file:
        urls_list = file.read().splitlines()

    return urls_list


def validate_urls(urls_list):
    pattern = r'^(https?)://.'
    for url in urls_list:
        if not re.match(pattern, url):
            return url

    return True


def is_server_available(url):
    try:
        response = requests.get(url)
        return response.ok
    except requests.ConnectionError:
        return False


def get_expiration_info(url):
    domain_info = whois.whois(url)

    expiration_date = domain_info.expiration_date

    if type(expiration_date) is list:
        expiration_date = expiration_date[0]
    elif type(expiration_date) is not datetime:
        expiration_date = None

    return expiration_date


def get_expiration_description(expiration_date, expires_period=30):
    if not expiration_date:
        return 'N/A'

    date_delta = datetime.today() - expiration_date
    date_delta_days = date_delta.days

    if date_delta_days < 0 and abs(date_delta_days) >= expires_period:
        description = 'Not expired in {} days'.format(expires_period)
    else:
        description = 'Expires'

    return description


def get_server_status_description(availability):
    if availability:
        description = 'OK'
    else:
        description = 'Connection error'

    return description


def get_urls_info(urls_list):
    urls_info = []

    for url in urls_list:
        url_data = {}

        url_data['address'] = url
        url_data['availability'] = is_server_available(url)
        url_data['expiration_info'] = get_expiration_info(url)

        urls_info.append(url_data)

    return urls_info


def output_to_console(urls_info):
    template = ('Url: {}\nServer status: {}\n Domain expiration: {}\n')

    for url in urls_info:
        address = url['address']
        server_status = get_server_status_description(url['availability'])
        expiration = get_expiration_description(url['expiration_info'])
        print(template.format(address, server_status, expiration))


if __name__ == '__main__':
    args = parse_args()

    urls_list = get_urls_list(args.file)

    if urls_list is None:
        sys.exit("File doesn't exists")

    validation_result = validate_urls(urls_list)

    if validation_result is not True:
        sys.exit('Invalid URL: {}'.format(validation_result))

    urls_info = get_urls_info(urls_list)

    output_to_console(urls_info)
