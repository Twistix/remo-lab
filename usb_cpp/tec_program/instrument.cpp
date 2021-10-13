#include <iostream>
#include "instrument.h"
#include "libusb.h"
using namespace std;

//==================================== CONSTRUCTOR ==============================================
instrument::instrument(int VID_arg, int PID_arg, int epInAdress_arg, int epOutAdress_arg, int sizeOfPackets_arg) {
    VID = VID_arg;
    PID = PID_arg;
    epInAdress = epInAdress_arg;
    epOutAdress = epOutAdress_arg;
    sizeOfPackets = sizeOfPackets_arg;

	int r; //for return values
	ssize_t cnt; //holding number of devices in list
	r = libusb_init(&ctx); //initialize the library for the session we just declared
	if(r < 0) {
		cout<<"Init Error "<<r<<endl; //there was an error
	}
	libusb_set_debug(ctx, 3); //set verbosity level to 3, as suggested in the documentation
	cnt = libusb_get_device_list(ctx, &devs); //get the list of devices
	if(cnt < 0) {
		cout<<"Get Device Error"<<endl; //there was an error
	}
	cout<<cnt<<" devices in list."<<endl;

	dev_handle = libusb_open_device_with_vid_pid(ctx, VID, PID); //these are vendorID and productID I found for my usb device
	if(dev_handle == NULL) {
		cout<<"Cannot open device"<<endl;
	} else {
		cout<<"Device Opened"<<endl;
	}
	libusb_free_device_list(devs, 1); //free the list, unref the devices in it

	if(libusb_kernel_driver_active(dev_handle, 0) == 1) { //find out if kernel driver is attached
		cout<<"Kernel Driver Active"<<endl;
		if(libusb_detach_kernel_driver(dev_handle, 0) == 0) //detach it
			cout<<"Kernel Driver Detached!"<<endl;
	}
};

//==================================== DESTRUCTOR ===============================================
instrument::~instrument() {
    libusb_close(dev_handle); //close the device we opened
    libusb_exit(ctx); //needs to be called to end the
};

//======================================= SEND COMMAND ===========================================
void instrument::sendCommand(string command) {
    int r; //for return values
    int cmdLen = command.length(); //length of the command
    unsigned char *data = new unsigned char[cmdLen+2]; //data to write
    for (int i = 0; i < cmdLen; i++ ){
       data[i]=command[i];
    }
    data[cmdLen]='\r';
    data[cmdLen+1]='\n';
    int transmited; //used to find out how many bytes were written
    r = libusb_claim_interface(dev_handle, 0); //claim interface 0 (the first) of device
	if(r != 0) {    //Cannot Claim Interface
		cout<<libusb_error_name(r)<<endl;
	}
	cout<<"Command = "<<command<<endl; //just to see the data we want to write
	r = libusb_bulk_transfer(dev_handle, epInAdress, data, cmdLen+2, &transmited, 0); //my device's IN endpoint was 2
	if(r != 0 || transmited != cmdLen+2) { //we don't wrote the (cmdLen) bytes successfully
		cout<<libusb_error_name(r)<<endl;
	}
	r = libusb_release_interface(dev_handle, 0); //release the claimed interface
	if(r !=0 ) {    // Cannot Release Interface
		cout<<libusb_error_name(r)<<endl;
	}
};

//================================================ QUERY STRING =======================================================
string instrument::doQueryString(string query) {
    int r;  //for return values
    int cmdLen = query.length();    //length of the query
    unsigned char *data = new unsigned char[cmdLen+2];  //data to write
    for (int i = 0; i < cmdLen; i++ ){
       data[i]=query[i];
    }
    data[cmdLen]='\r';
    data[cmdLen+1]='\n';
    int transmited = 0; //used to find out how many bytes were transmited
    r = libusb_claim_interface(dev_handle, 0); //claim interface 0 (the first) of device
	if(r != 0) {    //Cannot Claim Interface
		cout<<libusb_error_name(r)<<endl;
	}
	cout<<"Query = "<<query<<endl; //just to see the query we want to write
	r = libusb_bulk_transfer(dev_handle, epInAdress, data, cmdLen+2, &transmited, 5000); //my device's IN endpoint was 2
	if(r != 0 || transmited != cmdLen+2) {  //we don't wrote the (cmdLen) bytes successfully
		cout<<libusb_error_name(r)<<endl;
	}
    unsigned char *buffer = new unsigned char[sizeOfPackets]; //buffer to put the readed data into
    int index;  //index to save the position of "\r\n" in the packet transmitted
    string dataOut = "";    //string to store the data recieved from the instrument
    transmited = 0;
    r = libusb_bulk_transfer(dev_handle, epOutAdress, buffer, sizeOfPackets, &transmited, 3000); //my device's OUT endpoint was 129
	if (r != 0) {   //Read error
        cout<<libusb_error_name(r)<<endl;
	}
	string strBuffer(reinterpret_cast<char const*>(buffer), 64); //convert the buffer char array to a string
	index = strBuffer.find("\r\n"); //return the position of "\r\n" in the buffer string, if not found return std::string::npos
	while (index == std::string::npos) {
        dataOut += strBuffer; //appending string buffer variable to string dataOut
        transmited = 0;
        r = libusb_bulk_transfer(dev_handle, epOutAdress, buffer, sizeOfPackets, &transmited, 3000); //my device's OUT endpoint was 2
        if (r != 0) {   // Read error
            cout<<libusb_error_name(r)<<endl;
        }
        strBuffer = string(reinterpret_cast<char const*>(buffer), 64); //updating the string buffer variable
        index = strBuffer.find("\r\n");
	}
	dataOut += strBuffer.substr(0, index);
	r = libusb_release_interface(dev_handle, 0); //release the claimed interface
	if(r !=0 ) {    // Cannot Release Interface
		cout<<libusb_error_name(r)<<endl;
	}
	return dataOut;
};
