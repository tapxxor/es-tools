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
from time import sleep

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

exceptNUM = 0

def handler(signum, frame):
    logger.info('Shutting down... SIGTERM received!!! ciao! bye! au revoir!')
    logger.warn('{} exceptions detected'.format(exceptNUM))
    sys.exit(1)

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

def searchPeople(lim = 100):
    res = 0
    try:
        es.search(index='people', 
                    doc_type='post', 
                    body={"query": {"match": { "prefix": 'Mr'}}})
    except Exception as e: 
        res = res + 1
        logger.error(searchPeople + ':' + e)
    
    return res

def searchMisc(lim = 100):
    res = 0
    try:
        es.search(index='misc', 
                    doc_type='post', 
                    body={"query": {"match": { "language_code": 'nso'}}})
    except Exception as e: 
        res = res + 1
        logger.error(searchMisc + ':' + e)

    return res

def searchInternet(lim = 100):
    res = 0
    try:
        es.search(index='internet', 
                    doc_type='post', 
                    body={"query": {"match": { "mac": 'f'}}})
    except Exception as e: 
        res = res + 1
        logger.error(searchInternet + ':' + e)
    
    return res

def writeDoc():
    choice = randint(1,3)
    if choice == 1:
        logger.info('    Insert people')
        populatePeople(1)
    elif choice == 2:
        logger.info('    Insert misc')
        populateMisc(1)
    else:
        logger.info('    Insert internet')
        populateInternet(1)

def searchDoc(indexSize):
    choice = randint(1,3)
    res = 0
    if choice == 1:
        logger.info('    Search people')
        res = searchPeople(indexSize)
    elif choice == 2:
        logger.info('    Search misc')
        res = searchMisc(indexSize)
    else:
        logger.info('    Search internet')
        res = searchInternet(indexSize)
    return res

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
            [ '192.168.99.100:30200'],
            sniff_on_start=True,
            sniff_on_connection_fail=True,
            sniffer_timeout=60
        )
    except ConnectionError as e:
        logger.error(e)
        sys.exit(1)

    while True:
        if randint(1,2) %2 == 0:
            # create an entry
            logger.info('Action write')
            writeDoc()
        else:
            # search for an entry
            logger.info('Action search')
            tmp = searchDoc(indexSize)
            if tmp != 0:
                exceptNUM = exceptNUM + 1
                logger.warn('{} exceptions detected'.format(exceptNUM))
        sleep(0.5)