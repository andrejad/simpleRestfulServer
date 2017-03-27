#!/bin/bash

clear
nohup python3 -u ./restServer.py &> restServer.log &
./mem
