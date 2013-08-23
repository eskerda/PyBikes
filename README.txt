=======
PyBikes
=======

PyBikes provides a set of tools to scrape bike sharing data from different 
websites and APIs, thus providing a coherent and generalized set of classes
and methods to access this sort of information. 

This library is distributed and intended mainly for statistics and data 
sharing projects. More importantly, it powers the CityBikes project[1].

The library is composed of a set of classes (under pybikes), and a pack of 
data files that provide instances for all different systems.

Usual usage(:):
    #! /usr/bin/env python

    >>> import pybikes
    
    # Capital BikeShare instantiation data is in bixi.json file
    >>> capital_bikeshare = pybikes.getBikeShareSystem('bixi','capital-bikeshare')

    # The instance contains all possible metadata regarding this system
    >>> print(capital_bikeshare.meta)
    {
        'name': 'Capital BikeShare', 
        'city': 'Washington, DC - Arlington, VA', 
        'longitude': -77.0363658, 
        'system': 'Bixi', 
        'company': 'PBSC', 
        'country': 'USA', 
        'latitude': 38.8951118
    }
    # The update method retrieves the list of stations
    >>> print(len(capital_bikeshare.stations))
    0
    >>> capital_bikeshare.update()
    >>> print(len(capital_bikeshare.stations))
    191
    >>> print(capital_bikeshare.stations[0])
    --- 31000 - 20th & Bell St ---
    bikes: 7
    free: 4
    latlng: 38.8561,-77.0512
    extra: {
        'installed': True, 
        'uid': 1, 
        'locked': False, 
        'removalDate': '', 
        'installDate': '1316059200000', 
        'terminalName': '31000', 
        'temporary': False, 
        'name': '20th & Bell St', 
        'latestUpdateTime': '1353454305589'
    }

    # Note that pybikes works as an instance factory and, alternately, you 
    # could get the same instance by passing the right arguments to a
    # desired class

    >>> from pybikes import BixiSystem
    >>> capital_bikeshare = BixiSystem(
            tag = 'foo_tag', 
            root_url = 'http://capitalbikeshare.com/data/stations/', 
            meta = {'foo':'bar'})


[1]: http://www.citybik.es
