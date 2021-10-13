#ifndef INSTRUMENT_H_INCLUDED
#define INSTRUMENT_H_INCLUDED
using namespace std;

class instrument {

protected :

public :
    string identity;

    instrument();

    //Commands
    void sendCommand(string command);
    void sendCommandIEEEBlock(string command, char *dataArray);

    //Querys
    string doQueryString(string query);
    float doQueryNumber(string query);
    void doQueryNumbers(float *ans, int sizeAns, string query);
    void doQueryIEEEBlock(char *ans, int sizeAns, string query);

    //Checks
    void checkInstrumentErros(string command);
};

class oscilloscope:public instrument {

public :
    oscilloscope();

    void initialize();
    void autoscale();
    void setVertScale(int channel, float vscale);
    void setVertOffset(int channel, float voffset);
    void setHoriScale(float hscale);
    void setHoriOffset(float hoffset);
    void setTriggerEdgeLevel(int channel, float level);
    void setAquisitionMode(int mode);
    void saveConfig(char *config, int sizeConfig);
    void saveWaveform(char *res, int sizeRes, int channel, int nbPoints);
};

class funcGen:public instrument {

public :
    funcGen();

    void initialize();
    void setOutputMode(int outMode);
    void setWaveShape(int wshape);
    void setAmplitude(float amplitude);
    void setFrequency(float freq);
    void setDCOffset(float offset);
    void setDutyCycle(float dcycle);
    void setOutputOnOff(int state);
};

class powerSupply:public instrument {

public :
    powerSupply();

    void initialize();
    void setMaxVoltage(int channel, float voltage);
    void setMaxCurrent(int channel, float current);
    float measVoltage(int channel);
    float measCurrent(int channel);
};


#endif // INSTRUMENT_H_INCLUDED
