# -*- coding: utf-8 -*-
"""
Created on Wed May 12 21:31:42 2021

@author: Alberto Di Meglio
"""

import os
from channel import public_channel

# clean up
_ = os.system('clear')

# instantiate a receiver channel
theChannel = public_channel()

# initiate the channel and listen for connections
theChannel.initiate_channel()