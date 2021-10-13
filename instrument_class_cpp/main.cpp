#include <iostream>
#include "instrument.h"
using namespace std;

int main()
{
    oscilloscope test;

    test.initialize();
    cout << '\n' << test.identity << '\n' << endl;

    test.setTriggerEdgeLevel(1, 0.5);
    cout << '\n' << endl;

    int i;
    char waveForm[10];
    test.saveWaveform(waveForm, sizeof(waveForm), 1, 200);
    for(i=0; i<sizeof(waveForm); i++) {
        cout << waveForm[i];
    }
    cout << '\n' << endl;

    return 0;
}
