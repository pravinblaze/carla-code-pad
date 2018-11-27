#!/usr/bin/env python

# Copyright (c) 2017 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

# This program is a first attempt at creating NHTSA pre-crash scenarios in Carla

from __future__ import print_function


# ==============================================================================
# -- find carla module ---------------------------------------------------------
# ==============================================================================


import glob
import os
import sys

# ==============================================================================
# -- imports -------------------------------------------------------------------
# ==============================================================================


import carla

from carla import ColorConverter as cc

import argparse
import logging


def od_map_maker(args):
    world = None

    client = carla.Client(args.host, args.port)
    client.set_timeout(2.0)

    world = client.get_world()
    map = world.get_map()
    odmap = map.to_opendrive()
    with open("/home/praveen/Documents/carla-map.xodr", "w+") as f:
        f.write(odmap)
        print("Successfully saved an opendrive representation of world map !")
        f.close()

    pass


# ==============================================================================
# -- main() --------------------------------------------------------------------
# ==============================================================================


def main():
    argparser = argparse.ArgumentParser(
        description='OpenDrive map creator')

    argparser.add_argument(
        '--host',
        metavar='H',
        default='127.0.0.1',
        help='IP of the host server (default: 127.0.0.1)')
    argparser.add_argument(
        '-p', '--port',
        metavar='P',
        default=2000,
        type=int,
        help='TCP port to listen to (default: 2000)')

    args = argparser.parse_args()

    logging.basicConfig(format='%(levelname)s: %(message)s')

    logging.info('listening to server %s:%s', args.host, args.port)

    print(__doc__)

    try:

        od_map_maker(args)

    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')
    except Exception as error:
        logging.exception(error)


if __name__ == '__main__':

    main()
