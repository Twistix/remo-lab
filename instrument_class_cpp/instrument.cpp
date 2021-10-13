#include <iostream>
#include "instrument.h"
using namespace std;

instrument::instrument() {};

void instrument::sendCommand(string command) {
    cout << command << endl;
    checkInstrumentErros(command);
};

void instrument::sendCommandIEEEBlock(string command, char *dataArray) {
    string strDataArray(dataArray);
    cout << command << " " << strDataArray << endl;
    checkInstrumentErros(command);
};

string instrument::doQueryString(string query) {
    cout << query << endl;
    checkInstrumentErros(query);
    return("answerString");
};

float instrument::doQueryNumber(string query) {
    cout << query << endl;
    checkInstrumentErros(query);
    return(12.3);
};

void instrument::doQueryNumbers(float *ans, int sizeAns, string query) {
    int i;
    cout << query << endl;
    checkInstrumentErros(query);
    for(i=0; i<sizeAns; i++) {
        ans[i]=i+0.1;
    }
};

void instrument::doQueryIEEEBlock(char *ans, int sizeAns, string query) {
    int i;
    cout << query << endl;
    checkInstrumentErros(query);
    for(i=0; i<sizeAns; i++) {
        ans[i]='a';
    }
};

void instrument::checkInstrumentErros(string command) {
    cout << ":SYSTem:ERRor?" << endl;
    int errorNumber = 0;
    while (errorNumber != 0) {
        cout << "Error for command : " << command << endl;
    }
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

oscilloscope::oscilloscope() {};

void oscilloscope::initialize() {
    identity = doQueryString("*IDN?");
    cout << "Instrument IDN : " << identity << endl;
    sendCommand("*CLS");
    sendCommand("*RST");
};

void oscilloscope::autoscale() {
    sendCommand(":AUToscale");
};

void oscilloscope::setVertScale(int channel, float vscale) {
    sendCommand(":CHANnel"+std::to_string(channel)+":SCALe "+std::to_string(vscale));
};

void oscilloscope::setVertOffset(int channel, float voffset) {
    sendCommand(":CHANnel"+std::to_string(channel)+":OFFSet "+std::to_string(voffset));
};

void oscilloscope::setHoriScale(float hscale) {
    sendCommand(":TIMebase:SCALe "+std::to_string(hscale));
};

void oscilloscope::setHoriOffset(float hoffset) {
    sendCommand(":TIMebase:POSition "+std::to_string(hoffset));
};

void oscilloscope::setTriggerEdgeLevel(int channel, float level) {
    sendCommand(":TRIGger:MODE EDGE");
    sendCommand(":TRIGger:EDGE:SOURce CHANnel"+std::to_string(channel));
    sendCommand(":TRIGger:EDGE:LEVel "+std::to_string(level));
    sendCommand(":TRIGger:EDGE:SLOPe POSitive");
};

void oscilloscope::setAquisitionMode(int mode) {
    //1:NORMal, 2:PEAK, 3:AVERage, 4:HRESolution
    switch (mode) {
        case 1:
            sendCommand(":ACQuire:TYPE NORMal");
            break;
        case 2:
            sendCommand(":ACQuire:TYPE PEAK");
            break;
        case 3:
            sendCommand(":ACQuire:TYPE AVERage");
            break;
        case 4:
            sendCommand(":ACQuire:TYPE HRESolution");
            break;
        default :
            sendCommand(":ACQuire:TYPE NORMal");
    }
};

void oscilloscope::saveConfig(char *config, int sizeConfig) {
    doQueryIEEEBlock(config, sizeConfig, ":SYSTem:SETup?");
};

void oscilloscope::saveWaveform(char *res, int sizeRes, int channel, int nbPoints) {
    sendCommand(":ACQuire:COMPlete 100");
    sendCommand(":DIGitize CHANnel"+std::to_string(channel));
    sendCommand(":WAVeform:SOURce CHANnel"+std::to_string(channel));
    sendCommand(":WAVeform:FORMat BYTE");
    sendCommand(":WAVeform:POINts "+std::to_string(nbPoints));
    doQueryIEEEBlock(res, sizeRes, ":WAVeform:DATA?");
};

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

funcGen::funcGen() {};

void funcGen::initialize() {
    identity = doQueryString("*IDN?");
    cout << "Instrument IDN : " << identity << endl;
    sendCommand("*CLS");
    sendCommand("*RST");
};

void funcGen::setOutputMode(int outMode) {
    //1:High Z, 2:50 Ohm
    switch (outMode) {
        case 1:
            sendCommand(":OUTPut:LOAD INFinity");
            break;
        case 2:
            sendCommand(":OUTPut:LOAD TERMinated");
            break;
        default :
            sendCommand(":OUTPut:LOAD INFinity");
    }
};

void funcGen::setWaveShape(int wshape) {
    //1:SINusoid, 2:SQUare, 3:RAMP, 4:PULSe, 5:ARBitary
    switch (wshape) {
        case 1:
            sendCommand(":FUNCtion SINusoid");
            break;
        case 2:
            sendCommand(":FUNCtion SQUare");
            sendCommand(":FUNCtion:SQUare:DCYCle 50");
            break;
        case 3:
            sendCommand(":FUNCtion RAMP");
            break;
        case 4:
            sendCommand(":FUNCtion PULSe");
            break;
        case 5:
            sendCommand(":FUNCtion ARBitary");
            break;
        default :
            sendCommand(":FUNCtion SINusoid");
    }
};

void funcGen::setAmplitude(float amplitude) {
    sendCommand(":VOLTage "+std::to_string(amplitude));
};

void funcGen::setFrequency(float freq) {
    sendCommand(":FREQuency "+std::to_string(freq));
};

void funcGen::setDCOffset(float offset) {
    sendCommand(":VOLTage:OFFSet "+std::to_string(offset));
};

void funcGen::setDutyCycle(float dcycle) {
    sendCommand(":FUNCtion:PULSe:DCYCle "+std::to_string(dcycle)); //duty cycle in percent
};

void funcGen::setOutputOnOff(int state) {
    if (state==1) {
        sendCommand(":OUTPut ON");
    }
    else {
        sendCommand(":OUTPut OFF");
    }
};

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

powerSupply::powerSupply() {};

void powerSupply::initialize() {
    identity = doQueryString("*IDN?");
    cout << "Instrument IDN : " << identity << endl;
    sendCommand("*CLS");
    sendCommand("*RST");
};

void powerSupply::setMaxVoltage(int channel, float voltage) {
    sendCommand(":VOLTage "+std::to_string(voltage)+", (@"+std::to_string(channel)+")");
};

void powerSupply::setMaxCurrent(int channel, float current) {
    sendCommand(":CURRent "+std::to_string(current)+", (@"+std::to_string(channel)+")");
};

float powerSupply::measVoltage(int channel) {
    doQueryNumber(":VOLTage?, (@"+std::to_string(channel)+")");
};

float powerSupply::measCurrent(int channel) {
    doQueryNumber(":CURRent?, (@"+std::to_string(channel)+")");
};

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
