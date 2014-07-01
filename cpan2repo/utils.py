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


def dir_digest(path):
    h = hashlib.sha256()

    try:
        objects = os.listdir(path)
    except:
        return ""

    for obj in objects:
        obj_path = "{0}/{1}".format(path, obj)
        if os.path.isdir(obj_path):
            h.update('dir ' + obj_path + '\n')
            h.update(dir_digest(obj_path))
        elif os.path.isfile(obj_path):
            h.update(file_hash(obj_path))
        else:
            h.update('reg ' + obj_path + '\n')

    return h.hexdigest()