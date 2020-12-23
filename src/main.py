import client
import logging


logging.basicConfig(level=logging.INFO)
settings: client.Settings = client.Settings()

flooder: client.Flooder = client\
    .Flooder("1FAIpQLSelHnYQUmpSnCb_KPiyTFKGu0qGLEV1CtMAlllknC34zv2fSA")\
    .from_har("docs.google.com_Archive [20-12-23 10-12-45].har")

flooder.run(use_threading=True)
flooder.run(use_threading=True)
flooder.run(use_threading=True)
flooder.run(use_threading=True)
flooder.run(use_threading=True)
