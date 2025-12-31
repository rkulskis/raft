SHELL := /bin/bash

all: run

run:
	source /opt/ros/jazzy/setup.bash && python3 main.py
