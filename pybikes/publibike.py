# -*- coding: utf-8 -*-
# Copyright (C) 2010-2022, eskerda <eskerda@gmail.com>
# Copyright (C) 2022-2023, eUgEntOptIc44 (https://github.com/eUgEntOptIc44)
# Distributed under the AGPL license, see LICENSE.txt

import json

from pybikes import BikeShareSystem, BikeShareStation, PyBikesScraper

FEED_URL = 'https://api.publibike.ch/v1/public/partner/stations'


class Publibike(BikeShareSystem):
    sync = True
    unifeed = True  # all 'networks' (instances) share the same feed

    meta = {
        'system': 'PubliBike',
        'company': ['PubliBike AG'],
        'source': 'https://api.publibike.ch/v1/static/api.html'
    }

    def __init__(self, tag, meta, city_uid):
        super(Publibike, self).__init__(tag, meta)
        self.uid = city_uid

    def update(self, scraper=None):
        scraper = scraper or PyBikesScraper()

        stations = json.loads(
            scraper.request(FEED_URL).encode('utf-8')
        )

        assert "stations" in stations, "Failed to find any PubliBike stations"

        stations = stations['stations']

        # currently (Dezember 2022) there is no endpoint available
        # to query only stations for 'city_uid'
        # so we need to filter the data
        stations = filter(lambda s: s['network']['id'] == self.uid, stations)

        self.stations = list(map(PublibikeStation, stations))


class PublibikeStation(BikeShareStation):
    def __init__(self, station):
        super(PublibikeStation, self).__init__()

        self.name = station['name']
        self.latitude = float(station['latitude'])
        self.longitude = float(station['longitude'])
        self.extra = {
            'uid': station['id'],
            'address': station['address'],
            'zip': station['zip'],
            'city': station['city'],
            'slots': station['capacity'],
        }
        self.bikes = len(station['vehicles'])
        self.free = self.extra['slots'] - self.bikes
