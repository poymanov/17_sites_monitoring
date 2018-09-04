import argparse
import os
import sys
import re
import requests
import whois
from datetime import datetime


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


def get_http_status_description(url):
    response = requests.get(url)

    if response.ok:
        status_description = 'OK'
    else:
        status_description = 'Connection error'

    return status_description


def get_domain_expiration_description(url, expires_period=30):
    domain_info = whois.whois(url)

    expires_date = domain_info.expiration_date
    date_delta = datetime.today() - expires_date
    date_delta_days = date_delta.days

    if date_delta_days < 0 and abs(date_delta_days) >= expires_period:
        expiration_description = 'Not expired'
    else:
        expiration_description = 'Expires'

    return expiration_description


def get_urls_info(urls_list):
    urls_info = []

    for url in urls_list:
        url_data = {}

        url_data['url'] = url
        url_data['http_status'] = get_http_status_description(url)
        url_data['domain_expiration'] = get_domain_expiration_description(url)

        urls_info.append(url_data)

    return urls_info


def output_to_console(urls_info):
    template = ('Url: {url}\nHTTP-status: {http_status}\n'
                'Domain expiration: {domain_expiration}\n')

    for url in urls_info:
        print(template.format(**url))


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
