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
    response = requests.get(url)
    return response.ok


def get_expiration_info(url):
    domain_info = whois.whois(url)
    return domain_info.expiration_date


def get_expiration_description(expiration_date, expires_period=30):
    if type(expiration_date) is list:
        expiration_date = expiration_date[0]
    elif type(expiration_date) is not datetime:
        return 'N/A'

    today = datetime.today()
    date_delta = today - expiration_date
    date_delta_days = date_delta.days

    if date_delta_days < 0 and abs(date_delta_days) >= expires_period:
        today_format = today.strftime('%d-%m-%Y')
        period = today + timedelta(days=expires_period)
        period_format = period.strftime('%d-%m-%Y')
        description = 'Not expired ({}-{})'.format(today_format, period_format)
    else:
        description = 'Expires'

    return description


def get_server_response_description(availability):
    if availability:
        description = 'OK'
    else:
        description = 'Connection error'

    return description


def get_urls_info(urls_list):
    urls_info = []

    for url in urls_list:
        url_data = {}

        availability = is_server_available(url)
        expiration_info = get_expiration_info(url)

        url_data['url'] = url
        url_data['http_status'] = get_server_response_description(availability)
        url_data['expiration'] = get_expiration_description(expiration_info)

        urls_info.append(url_data)

    return urls_info


def output_to_console(urls_info):
    template = ('Url: {url}\nHTTP-status: {http_status}\n'
                'Domain expiration: {expiration}\n')

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
