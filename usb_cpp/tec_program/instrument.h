#ifndef INSTRUMENT_H_INCLUDED
#define INSTRUMENT_H_INCLUDED
#include "libusb.h"
using namespace std;

class instrument {
protected :
    int VID;
    int PID;
    int epInAdress;
    int epOutAdress;
    int sizeOfPackets;

    libusb_device **devs; //pointer to pointer of device, used to retrieve a list of devices
	libusb_device_handle *dev_handle; //a device handle
	libusb_context *ctx = NULL; //a libusb session

public :

    instrument(int VID_arg, int PID_arg, int epInAdress_arg, int epOutAdress_arg, int sizeOfPackets_arg);
    ~instrument();

    //Commands
    void sendCommand(string command);

    //Querys
    string doQueryString(string query);
};

class tec:public instrument {
protected :
    string identity;

public :
    tec();
    ~tec();

    void reset();

    void setLDDparams(int mode, int range, int bandwidth);
    void LDDoutput(int active, float current);

    void setTECparams(int mode, int sensor);
    void setTECpid(float kp, float ki, float kd, float il);
    void TECoutput(int active, float value);
};


#endif // INSTRUMENT_H_INCLUDED
