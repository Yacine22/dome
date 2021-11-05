/* 
 This a serial i2c protocol from Raspberry Pi
 * By yme @ mercurioimaging   
*/
#include<stdio.h>
#include<unistd.h>
#include<fcntl.h>
#include<sys/ioctl.h>
#include<linux/i2c.h>
#include<linux/i2c-dev.h>
#include<pybind11/pybind11.h> // For Python Lib Creation 
// #include "rasp_master.hpp"

namespace py = pybind11;

void openI2CBus(int& file){
	/* Open the i2c serial communication bus*/
    if((file = open("/dev/i2c-1", O_RDWR)) < 0){
        perror("Failed to open the bus\n");
        return;
    }
}

void connecttoSlave(int& file, unsigned char slaveAddr){
	/* Enable the i2c serial connection with a slave device */ 
    if (ioctl(file, I2C_SLAVE, slaveAddr) < 0){
        perror("Failed to connect to the Arduino\n"); 
        return; 
    }
}

void sendLong(int& file, long data){
	/*
	 * send data to Slave Device
	*/
    unsigned char bytes[sizeof(long)];

    for (int j = 0; j < sizeof(long); ++j)
        bytes[j] = data >> j * 8;
    
    if (write(file, bytes, sizeof(long)) != sizeof(long)) {
        perror("Failed to send data\n"); 
        return; 
    }
}

void receiveLong(int& file, long& value){
	/* Receive data from Slave device */ 
    unsigned char bytes[sizeof(long)];

    if (read(file, bytes, sizeof(long)) != sizeof(long)){
        perror("Failed to receive data\n");
        return; 
    }

    value = 0; 

    for (int j = 0; j < sizeof(long); ++j)
        value += bytes[j] << j * 8;

}

void send_dataTo(long s, unsigned char addr){
	/* enable the data sender */ 
    int fd; 
    openI2CBus(fd); 
    connecttoSlave(fd, addr); 
    sendLong(fd, s); 
    close(fd);
}

long data_from(unsigned char addr){
	/* enable the data reception from slave device */ 
    int fd;
    long received;
    
    openI2CBus(fd); 
    connecttoSlave(fd, addr); 
    receiveLong(fd, received);
    close(fd);
    
    return received; 
}



PYBIND11_MODULE(pyraspii, handle) {

    handle.doc() = "I2C Communication between Raspberry master device and an arduino nano /or attiny digispark";
    handle.def("getData_from", & data_from, "Get Data from Slave Device <data_from(char)>"); 
    handle.def("send_data", & send_dataTo, "Send Data to Slave Device <send_data(int, char)>"); 
}


