import os
from os.path import isfile, join, isdir

import json
from typing import Callable, Any


def getFromDir(path: str, checker: Callable[[str], bool]):
    listDir = os.listdir(path)
    return [os.path.join(path, name) for name in listDir if checker(join(path, name))]


def addFile(to: map, path: list, it: int, getInfo: Callable[[str], Any]):
    if it + 1 < len(path):
        if path[it] not in to.keys():
            to[path[it]] = {}
        addFile(to[path[it]], path, it + 1)
    else:
        to[path[it]] = getInfo(path[it])


def generateProjectMap(path: str, getInfo: Callable[[str], Any]):
    absolute = path.split('/')

    filePaths = []
    paths = [path]
    while len(paths):
        path = paths[-1]
        paths.pop()
        
        for dir in getFromDir(path, isdir):
            paths.append(dir)
        
        for file in getFromDir(path, isfile):
            filePaths.append(file)
    
    result = {}

    for filePath in filePaths:
        addFile(result, filePath.split('/'), len(absolute), getInfo)

    return result


def writeProjectMap(path: str, outFileName: str, getInfo: Callable[[str], Any]):
    pMap = generateProjectMap(path, getInfo)
    with open(outFileName, 'w') as file:
        file.write(json.dumps(pMap, sort_keys=True, indent=4))

