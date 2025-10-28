import requests as rq
from typing import TypedDict, List
from dotenv import load_dotenv
import os

load_dotenv()


class DataItem(TypedDict):
    _id: str

class intDataItem(TypedDict):
    count: int

class delDataItem(TypedDict):
    _id: str

BASE = "https://lively-escarpment-5c9e.codehooks.io"
HEADERS = {"x-apikey": os.getenv('API_TOKEN')}


def addToCollection(collection: str, data: dict) -> DataItem:
    """Add a Object/Dict to a collection (which can have multiple objects/dicts)"""
    r = rq.post('%s/%s' % (BASE, collection), headers=HEADERS, json=data)
    return r.json()

def getAllObjectsOfCollection(collection: str) -> List[DataItem]:
    """Get all Object/Dict from a collection (which can have multiple objects/dicts)"""
    r = rq.get('%s/%s' % (BASE, collection), headers=HEADERS)
    return r.json()

def getSingleObjectFromCollection(collection: str, object_id: str) -> DataItem:
    """Get Single Object/Dict by its ID from a collection (which can have multiple objects/dicts)"""
    r = rq.get('%s/%s/%s' % (BASE, collection, object_id), headers=HEADERS)
    return r.json()

def editSingleObjectOfCollection(collection: str, object_id: str, data: dict, fulloverride: bool = False) -> DataItem:
    """Edit Single Object/Dict by its ID from a collection (which can have multiple objects/dicts)"""
    r = ( rq.put if fulloverride else rq.patch )('%s/%s/%s' % (BASE, collection, object_id), headers=HEADERS, json=data)
    return r.json()

def editAllOfCollection(collection: str, data: dict) -> intDataItem:
    """Merge given data with each Object/Dict from a collection (which can have multiple objects/dicts)"""
    r = rq.patch('%s/%s/_byquery' % (BASE, collection), headers=HEADERS, json=data)
    return r.json()

def deleteAllOfCollection(collection: str) -> intDataItem:
    """Delete all Object/Dict from a collection (which can have multiple objects/dicts)"""
    r = rq.delete('%s/%s/_byquery' % (BASE, collection), headers=HEADERS)
    return r.json()

def deleteSingleObjectFromCollection(collection: str, object_id: str) -> delDataItem:
    """Delete a single Object/Dict by its ID from a collection (which can have multiple objects/dicts)"""
    r = rq.delete('%s/%s/%s' % (BASE, collection, object_id), headers=HEADERS)
    return r.json()


if __name__ == '__main__':
    # print(addToCollection('fb-automation', dict(lastRun=0)))
    print(getSingleObjectFromCollection('fb-automation', '6900629fb029f9be5510e815'))
    # print(editSingleObjectOfCollection('fb-automation', '6900629fb029f9be5510e815', dict(lastRun=9)))

