import argparse
import os
import sys
import re
import requests
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
        content = file.read().splitlines()

    return content


def validate_urls(urls_list):
    pattern = r'^(https?)://[^\s/$.?#].[^\s]*$'
    for url in urls_list:
        if not re.match(pattern, url):
            return url

    return True


def get_http_status_description(url):
    try:
        response = requests.get(url)
        status_code = response.status_code
        status_code_descripton = requests.status_codes._codes[status_code][0]
        return '{} ({})'.format(status_code, status_code_descripton)
    except requests.exceptions.ConnectionError:
        return None


def get_domain_expiration_description(url, expires_period=30):
    api_url = 'http://api.whois.vu/'
    params = {'q': url}
    response = requests.get(api_url, params)

    if response.status_code != requests.codes.ok:
        return 'N/A'

    response_data = response.json()

    if 'expires' not in response_data.keys():
        return 'N/A'

    expires_timestamp = response_data['expires']
    expires_date = datetime.fromtimestamp(expires_timestamp)
    date_delta = datetime.today() - expires_date
    date_delta_days = date_delta.days

    expires_date_format = expires_date.strftime('%d-%m-%Y')

    if date_delta_days < 0:
        if abs(date_delta_days) >= expires_period:
            expiration_description = 'Will expire not soon'
        else:
            expiration_description = 'Expires soon'
    else:
        expiration_description = 'Expired'

    return '{} ({})'.format(expiration_description, expires_date_format)


def get_urls_info(urls_list):
    urls_info = []

    for url in urls_list:
        url_data = {}

        http_status = get_http_status_description(url)

        if http_status is None:
            http_status = 'Connection error'
            domain_expiration = 'N/A'
        else:
            domain_expiration = get_domain_expiration_description(url)

        url_data['url'] = url
        url_data['http_status'] = http_status
        url_data['domain_expiration'] = domain_expiration

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
