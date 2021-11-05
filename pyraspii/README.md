# pyraspii 
* pyraspii is a package to ensure a serial communication with i2c protocol from raspberry Pi*

## Table of Contents
1. [Installation and Usage](#installation-and-usage)
2. [Data Format](#data-format)
3. [Hardware Description](#hardware-description)
4. [Short Tutorial](#short-tutorial)

## Installation and Usage

### Install 
The pyraspii is a package which must be installed in Raspberry OS.
It requires **Python 3.7** or any later version.
For now, user can install **pyraspii** package through wheel files:

* From the [dist directory](./dist) download the .whl file
* Use pip command 

		python3 -m pip install pyraspii-0.1-cp37-cp37m-linux_armv7l.whl
* or 
		sudo apt-get install pyraspii

### Usage 
The **pyraspii** package is composed of modules:

- *send_data* to send data to the Slave device, must define the message to send and the device address, example:
		
		import pyraspii as pii 
		
		## send data :
		pii.send_data(1, 0x44) 

- *getData_from* to get Data from Device, need to define the device address

		## get data from device 0x44
		pii.getData_from(0x44)

## Data Format
 
This allows to take look to data format after data acquisitions from embedded camera
The data format is defined as integers

## Hardware Description

		 Raspberry                                   
		 ______                               Arduino nano / Attiny
		|      |                                    _________
		|      |                                   |         |
		|      - .............>  SDA  ...........> -         | 0x44
		|      - .............>  SCL  ...........> -         |
		|      |                                   |         |
		|      |                                   |         |
		|      - .............>  GND ............> -         |
		|______|                                   |_________|


## Short Tutorial 
To make data transmission, follow this example: 
* Make sure that you have a correct circuit between raspberry and other slave device
* Access to your raspberry from remote desk, use ssh (recommanded)

		ssh pi@192.168.x.x 

You must get the Pi IP address and replace x.x 

* git clone this repository

		git clone git@github.com:Yacine22/dome.git
		cd dome/pyraspii

* install pyraspii 
		
		python3 -m pip install ./dist/pyraspii.whl

* Open a python file

		import pyraspii as pii 
	
		## send data
		pii.send_data(1, 0x44)

		## get data 
		pii.getData_from(0x44)

