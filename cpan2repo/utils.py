import os
import logging
import hashlib


def file_hash(name):
    f = open(name)
    h = hashlib.sha256()
    while True:
        buf = f.read(16384)
        if len(buf) == 0:
            break
        h.update(buf)
    f.close()
    return h.hexdigest()