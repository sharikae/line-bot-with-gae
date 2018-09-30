from google.appengine.ext import vendor
import os.path

def patched_expanduser(path):
    return path

os.path.expanduser = patched_expanduser

vendor.add('lib')
