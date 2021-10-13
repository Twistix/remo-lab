#include <iostream>
#include "instrument.h"
#include "libusb.h"
using namespace std;

int main() {

    instrument tec(0x104d, 0x1009, 0x02, 0x81, 64);

    //tec.doQueryString("*RST");
    cout<<tec.doQueryString("LASer:LIMit:LDI (I)?")<<endl;

    return 0;
}
