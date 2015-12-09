# -*- coding: utf-8 -*-
# Copyright (C) 2015, Eduardo Mucelli Rezende Oliveira <edumucelli@gmail.com>
# Distributed under the AGPL license, see LICENSE.txt

import re

from .base import BikeShareSystem, BikeShareStation
from . import utils


# Each station is formatted as:
# newmark_01(
#    28,
#    45.770958,
#    3.073871,
#    "<div class=\"mapbal\" align=\"left\">022 Jaurès<br>Vélos disponibles: 4
#    <br>Emplacements libres: 10<br>CB: Non<br></div>"
# );

# station_uid, latitude, longitude
STATIONS_RGX = r'newmark_\d+\(\s*(\d+)\s*,\s*(\d+.\d+),\s*(\d+.\d+)\s*,\s*\"{}\"'  # NOQA
# name, available_bikes, free_bike_stands, credit_card_enabled
STATUS_RGX = r'<div.*?>(.*?)<br>.*?:\s*(.*?)<br>.*?:\s*(.*?)<br>.*?:\s*(.*?)<br></div>'  # NOQA
DATA_RGX = STATIONS_RGX.format(STATUS_RGX)


class Smoove(BikeShareSystem):

    sync = True

    meta = {
        'system': 'Smoove',
        'company': 'Smoove'
    }

    def __init__(self, tag, feed_url, meta):
        super(Smoove, self).__init__(tag, meta)
        self.feed_url = feed_url

    def update(self, scraper=None):
        if scraper is None:
            scraper = utils.PyBikesScraper()

        html = scraper.request(self.feed_url)
        stations_data = re.findall(DATA_RGX, html)
        stations = []
        # discards the last element of stations_data
        # which indicates if the station is credit card-enabled
        for uid, latitude, longitude, name, bikes, free, _ in stations_data:
            extra = {
                'uid': int(uid)
            }
            station = BikeShareStation(name, float(latitude), float(longitude),
                                       int(bikes), int(free), extra)
            stations.append(station)
        self.stations = stations
