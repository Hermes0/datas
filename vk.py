#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import time
import vk_api


def main():


    login, password 'login', 'pass'
    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()

    response = vk.users.search(
        q="name",
        fields="photo_100",
        has_photo=1,
        count=100
    )

    processed = 0
    total_count = response['count']
    left_processed = total_count

    while left_processed > 0:
        url_data = []
        for row in response['items']:
            url_data.append([row['id'], row['photo_100']])

        left_processed = left_processed - len(response['items'])
        processed = processed + len(response['items'])

        print "RESPONSE. FETCHED {} ROWS. PROCESSED: {}/{}".format(
            len(response['items']),
            processed,
            total_count
        )

        response = vk.users.search(
            q="name",
            fields="photo_100",
            has_photo=1,
            count=100,
            offset=processed
        )

        time.sleep(0.3)

    out = open('urls.csv', 'w')
    with out:
        writer = csv.writer(out)
        writer.writerows(url_data)




if __name__ == '__main__':
    main()
