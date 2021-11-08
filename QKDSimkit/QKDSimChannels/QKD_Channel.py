# -*- coding: utf-8 -*-
"""
Created on Wed May 12 21:31:42 2021

@author: Alberto Di Meglio
"""

import os
import asyncio
import sys

this_file_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, this_file_dir + "/../..")

from QKDSimkit.QKDSimChannels.channel import public_channel


def run_channel():
    # clean up
    _ = os.system('clear')

    # instantiate a receiver channel
    theChannel = public_channel()

    # initiate the channel and listen for connections
    theChannel.initiate_channel()


if __name__ == '__main__':
    run_channel()
