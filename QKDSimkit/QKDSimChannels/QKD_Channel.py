# -*- coding: utf-8 -*-
"""
Created on Wed May 12 21:31:42 2021

@author: Alberto Di Meglio
"""

import os
import asyncio
from QKDSimkit.QKDSimChannels.channel import public_channel


async def run_channel():
    # clean up
    _ = os.system('clear')

    # instantiate a receiver channel
    theChannel = public_channel()

    # initiate the channel and listen for connections
    theChannel.initiate_channel()

if __name__ == '__main__':
    asyncio.run(run_channel())
