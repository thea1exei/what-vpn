import urllib3
import warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.simplefilter('ignore', category=ResourceWarning)

import logging
from requests import exceptions as rex
from random import shuffle

from what_vpn.requests import SnifferSession
from what_vpn.sniffers import Hit, sniffers

session = SnifferSession()
session.timeout = 10

matched_vpns = ['vpn.{}.edu'.format(d) for d in (
    'drew',
    'syr',
    'northeastern',
    'yale',
    'fau',
    'uca',
    'simmons',
    'nl',
    'ycp',
    'smcvt',
    'louisville',
    'usmma',
    'tcu',
    'brown',
    )] + ['vpn.{}.com'.format(d) for d in (
    'yonyou',
    )] + [
    'cpvpn.its.hawaii.edu',
    'remote.princeton.edu',
    'uod.vpn.dundee.ac.uk',
    ]
unmatched_vpns = ['vpn.{}.edu'.format(d) for d in (
    'acu',
    'aurora',
    'brown',
    'wisc',
    'whitworth',
    'valpo',
    'uu',
    )]

def _count_hits(server):
    hits = 0
    shuffle(sniffers)
    for sniffer in sniffers:
        try:
            logging.debug('sniffing {} for {}'.format(server, sniffer.__name__))
            session.cookies.clear()
            hits += bool(sniffer(session, server))
        except (rex.Timeout, rex.SSLError, rex.ConnectionError) as e:
            pass
    return hits

def test_matched_vpns():
    for server in matched_vpns:
        hits = _count_hits(server)
        if hits != 1:
            raise AssertionError("got {} hits for {}, instead of expected 1".format(hits, server))

def test_unmatched_vpns():
    for server in unmatched_vpns:
        hits = _count_hits(server)
        if hits != 0:
            raise AssertionError("got {} hits for {}, instead of expected 0".format(hits, server))
