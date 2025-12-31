SHELL := /bin/bash

all: run

run_client:
	source /opt/ros/jazzy/setup.bash && python3 main.py --client
run:
	source /opt/ros/jazzy/setup.bash && python3 main.py

