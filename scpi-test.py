# ============================= Import modules =======================================
import pyvisa
import string
import struct
import sys

# ===========================  Global variables =======================================
debug = 0

# ============================= MAIN PROGRAM ==========================================
# Creating the ressource manager for the instrument
rm = pyvisa.ResourceManager()

myInst = rm.open_resource('instrument visa adress')



# ========================= Instrument class definition =================================
class instrument :
    # --------------------------------------------------------------------------
    # Send a command and check for errors:
    def do_command(command, hide_params=False):
        if hide_params:
            (header, data) = command.split(" ", 1)
            if debug:
                print("\nCmd = ’%s’" % header)
        else:
            if debug:
                print("\nCmd = ’%s’" % command)     
        myInst.write("%s" % command)
        if hide_params:
            check_instrument_errors(header)
        else:
            check_instrument_errors(command)

    # ---------------------------------------------------------------------------
    # Send a command and binary values and check for errors:
    def do_command_ieee_block(command, values):
        if debug:
            print("Cmb = ’%s’" % command)  
        myInst.write_binary_values("%s " % command, values, datatype=’B’)
        check_instrument_errors(command)

    # ------------------------------------------------------------------------------
    # Send a query, check for errors, return string:
    def do_query_string(query):
        if debug:
            print("Qys = '%s'" % query)
        result = myInst.query("%s" % query)
        check_instrument_errors(query)
        return result

    # -----------------------------------------------------------------------------
    # Send a query, check for errors, return floating-point value:
    def do_query_number(query):
        if debug:
            print("Qyn = '%s'" % query)
        result = myInst.query("%s" % query)
        check_instrument_errors(query)
        return float(result)

    # ------------------------------------------------------------------------------
    # Send a query, check for errors, return binary values:
    def do_query_ieee_block(query):
        if debug:
            print("Qys = '%s'" % query)
        result = myInst.query_binary_values("%s" % query, datatype='s')
        check_instrument_errors(query)
        return result[0]

    # ------------------------------------------------------------------------------
    # Check for instrument errors:
    def check_instrument_errors(command):
        while True:
            error_string = myInst.query(":SYSTem:ERRor?")
            if error_string:   #If there is an error string value
                if error_string.find("+0,", 0, 3) == -1:   #Not "No error"
                    print("ERROR: '%s', command: '%s'" % (error_string, command))
                    print("Exited because of error")
                    sys.exit(1)
                else:    #"No error"
                    break
            else:   #:SYSTem:ERRor? should always return string
                print("ERROR: :SYSTem:ERRor? returned nothing, command: '%s'" % command)
                print("Exited because of error")
                sys.exit(1)

# ==================== Oscilloscope class definition (mother=intrument) =================================
class oscilloscope(instrument):
    # --------------------------------------------------------------------------------
    # Initialize the oscilloscope:
    def __init__(self):
        self.identity = do_query_string("*IDN?")
        print("Instrument IDN : %s" % self.identity)
        do_command("*CLS")
        do_command("*RST")

    # ------------------------------------------------------------------------------
    # Autoscale:
    def autoscale:
        do_command(":AUToscale")

    # ------------------------------------------------------------------------------
    # Setting the vertical scale
    def setVertScale(channel, vscale):
        do_command(":CHANnel"+str(channel)+":SCALe "+str(vscale))

    # ------------------------------------------------------------------------------
    # Setting the vertical offset
    def setVertOffset(channel, voffset):
        do_command(":CHANnel"+str(channel)+":OFFSet "+str(voffset))

    # ------------------------------------------------------------------------------
    # Setting the horizontal scale
    def setHoriScale(hscale):
        do_command(":TIMebase:SCALe "+str(hscale))

    # ------------------------------------------------------------------------------
    # Setting the horizontal scale
    def setHoriOffset(hoffset):
        do_command(":TIMebase:POSition "+str(hoffset))

    # ------------------------------------------------------------------------------
    # Setting trigger to edge mode, and setting the level
    def setTriggerEdgeLevel(channel, level):
        do_command(":TRIGger:MODE EDGE")
        do_command(":TRIGger:EDGE:SOURce CHANnel"+str(channel))
        do_command(":TRIGger:EDGE:LEVel "+str(level))
        do_command(":TRIGger:EDGE:SLOPe POSitive")

    # ------------------------------------------------------------------------------
    # Setting the aquisition mode -> 1:NORMal, 2:PEAK, 3:AVERage, 4:HRESolution
    def setAquisitionMode(mode):
        if mode==1:
            do_command(":ACQuire:TYPE NORMal")
        elif mode==2:
            do_command(":ACQuire:TYPE PEAK")
        elif mode==3:
            do_command(":ACQuire:TYPE AVERage")
        elif mode==4:
            do_command(":ACQuire:TYPE HRESolution")
        else:
            do_command(":ACQuire:TYPE NORMal")

    # -------------------------------------------------------------------------------
    # Save the current configuration of the oscilloscope, return a byte array (IEEE block format)
    def saveConfig():
        return do_query_ieee_block(":SYSTem:SETup?")

    # -------------------------------------------------------------------------------
    # Save the current waveform which is displated on the oscillo screen
    def saveWaveform(channel, nbPoints):
        do_command(":ACQuire:COMPlete 100");
        do_command(":DIGitize CHANnel"+str(channel))
        do_command(":WAVeform:SOURce CHANnel"+str(channel))
        do_command(":WAVeform:FORMat BYTE")
        do_command(":WAVeform:POINts "+str(nbPoints))
        do_query_ieee_block(":WAVeform:DATA?")
        
            


    

    








        
        
    
