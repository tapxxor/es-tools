from elasticsearch import Elasticsearch
from elasticsearch import exceptions
import signal
import sys
import os

import logging
import logging.handlers

from faker import Faker
from random import shuffle
from random import randint

# Configure logger
#   create logger
logger = logging.getLogger(__name__)    
logger.setLevel(logging.DEBUG)

#   create console handler and set level to debug
stream = logging.StreamHandler()
stream.setLevel(logging.INFO)

#   create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#   add formatter to console handler
stream.setFormatter(formatter)

#   add console handler to logger
logger.addHandler(stream)

# PUT twitter
peopleSettings = {
    "settings" : {
        "index" : {
            "number_of_shards" : 2, 
            "number_of_replicas" : 1 
        }
    }
}
# PUT misc
miscSettings = {
    "settings" : {
        "index" : {
            "number_of_shards" : 2, 
            "number_of_replicas" : 1 
        }
    }
}


# PUT people
internetSettings = {
    "settings" : {
        "index" : {
            "number_of_shards" : 2, 
            "number_of_replicas" : 1 
        }
    }
}

def populatePeople(size=100):
    logger.info("Populating index people")
    for i in range(0,size):
        if randint(1,2) %2 == 0:
            es.index(index='people', doc_type='post', body={
                'name': fake.name_male(),
                'prefix': fake.prefix_male(),
                'address': fake.address(),
                'text': fake.text()
                })
        else:
            es.index(index='people', doc_type='post', body={
                'name': fake.name_female(),
                'prefix': fake.prefix_female(),
                'address': fake.address(),
                'prefix': fake.text()
                })
    logger.info("{} docs added at people index".format(size))

def populateMisc(size=100):
    logger.info("Populating index misc")
    for i in range(0,size):
        es.index(index='misc', doc_type='post', body={
               'language_code': fake.language_code(),
               'binary': fake.text()
            })
    logger.info("{} docs added at misc index".format(size))

def populateInternet(size=100):
    logger.info("Populating index internet")
    for i in range(0,size):
        es.index(index='internet', doc_type='post', body={
               'ipv4': fake.ipv4_private(network=False, address_class=None),
               'ipv6': fake.ipv6(network=False),
               'mac': fake.mac_address()
           })
    logger.info("{} docs added at internet index".format(size))


def handler(signum, frame):
    logger.info('Shutting down... SIGTERM received!!! ciao! bye! au revoir!')
    sys.exit(1)

if __name__ == '__main__':

    signal.signal(signal.SIGTERM, handler)
    logger.info("aplication started")
    fake= Faker()
    indexList =  ['people' ,'misc' , 'internet']
    shuffle(indexList)

    indexSize=1000
    if 'INDEXSIZE' in os.environ:
        indexSize = int(os.environ.get('INDEXSIZE'))
    
    esUrl = 'es-elasticsearch-client:9200'
    if 'ESURL' in os.environ:
        esUrl = os.environ.get('ESURL')

    try:
        es = Elasticsearch(
            [ 'es-elasticsearch-client:9200'],
            sniff_on_start=True,
            sniff_on_connection_fail=True,
            sniffer_timeout=60
        )
    except ConnectionError as e:
        logger.error(e)
        sys.exit(1)

    try:
        es.indices.create(index="people", body=peopleSettings)
        logger.info("people index created")
    except exceptions.RequestError as e:
        logger.warn("people index already exist")
        pass

    try:
        es.indices.create(index="misc", body=miscSettings)
        logger.info("misc index created")
    except exceptions.RequestError as e:
        logger.warn("misc index already exist")
        pass

    try:
        es.indices.create(index="internet", body=internetSettings)
        logger.info("internet index created")
    except exceptions.RequestError as e:
        logger.warn("internet index already exists")
        pass

    for index in indexList:
        if index == 'people':
            populatePeople(indexSize)
        elif index == 'misc':
            populateMisc(indexSize)
        else:
            populateInternet(indexSize)

    logger.info("Program finished")



