#!/bin/bash

virtualenv venv
./venv/bin/python bootstrap.py
./bin/buildout -vvv
