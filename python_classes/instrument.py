# ============================= Import modules =======================================
import pyvisa
import string
import struct
import sys
import time
import base64

# ===========================  Global variables =======================================
debug = int(1)  # debug global variable

# ============================= Useful functions =========================================
def truncate(f, n):
    # Truncates a float f to n decimal places without rounding
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

# ========================= Instrument class definition =================================
class instrument :
    def __init__(self, instrAdress, errorfunc):
        rm = pyvisa.ResourceManager()   # creating the ressource manager for the instrument
        self.myInst = rm.open_resource(instrAdress) # open the instrument with the specified VISA adress
        self.error = int(0) # setting the error attribute to 0
        self.errorfunc = errorfunc  # passing the callback error function into a function belonging to the object instrument
        
    # --------------------------------------------------------------------------
    # Send a command and check for errors:
    def do_command(self, command, hide_params=False):
        if hide_params:                 # if we want to hide the data from the command, Ex: :CHANnel1:SCALe 2.3 -> :CHANnel1:SCALe
            (header, data) = command.split(" ", 1)
            if debug:                   # if debug = 1, the we print the command sent in the console   
                print("Cmd = ’%s’" % header)
        else:
            if debug:
                print("Cmd = ’%s’" % command)     
        self.myInst.write(command)      # sending the command to the instrument connected
        if hide_params:
            self.check_instrument_errors(header)       # checking if there is an error with the command sent
        else:
            self.check_instrument_errors(command)

    # ---------------------------------------------------------------------------
    # Send a command and binary values and check for errors:
    def do_command_ieee_block(self, command, values, datatype):
        if debug:                          # if debug = 1, the we print the command sent in the console
            print("Cmd b = ’%s’" % command)
        self.myInst.write_binary_values("%s " % command, values, datatype=datatype)  # sending the command to the instrument connected and data in a form of a list of values
        self.check_instrument_errors(command)       # checking if there is an error with the command sent

    # ------------------------------------------------------------------------------
    # Send a query, check for errors, return string:
    def do_query_string(self, query):
        if debug:           # if debug = 1, the we print the query sent in the console
            print("Qys = '%s'" % query)
        result = self.myInst.query(query)   # sending the query to the instrument connected and retrieve the answer in the variable result
        self.check_instrument_errors(query) # checking if there are errors
        return result   # return the result of the query in string format

    # -----------------------------------------------------------------------------
    # Send a query, check for errors, return floating-point value:
    def do_query_number(self, query):
        if debug:       # if debug = 1, the we print the query sent in the console
            print("Qyn = '%s'" % query)
        result = self.myInst.query(query)   # sending the query to the instrument connected and retrieve the answer in the variable result
        self.check_instrument_errors(query) # checking if there are errors
        return float(result)    # return the result of the query in float format

    # ------------------------------------------------------------------------------
    # Send a query, check for errors, return binary values:
    def do_query_ieee_block(self, query, datatype):
        if debug:       # if debug = 1, the we print the query sent in the console
            print("Qys = '%s'" % query)
        result = self.myInst.query_binary_values(query, datatype=datatype)   # sending the query to the instrument connected and retrieve the answer in the variable result in binary form (a list of values) 
        self.check_instrument_errors(query) # checking if there are errors
        return result   # return the result of the query

    # ------------------------------------------------------------------------------
    # Check for instrument errors, updating the attribute self.error and calling a callback error handling function if there is an error :
    def check_instrument_errors(self, command):
        error_string = self.myInst.query(":SYSTem:ERRor?")  # query the instrument the error string
        if error_string:   #If there is an error string value
            if error_string.find("+0,", 0, 3) == -1:   #Not "No error"
                print("ERROR: '%s', command: '%s'" % (error_string, command))   # printing error in the console
                self.error = 1  # setting the attribute error to 1
                self.errorfunc(self.error)  # calling the callback error function
            else:    #"No error"
                if self.error == 1: # if there was an error with the previous command sent
                    self.error = 0  # setting back the attribute error to 0
                    self.errorfunc(self.error)  # calling the callback error function
                # if there was not error with the previous command and we don't have an error with the actual command : then we do nothing (most of the cases)
        else:   # If there is not an error string, :SYSTem:ERRor? should always return string
            print("ERROR: :SYSTem:ERRor? returned nothing, command: '%s'" % command)    # printing error in the console
            self.error = 1  # setting the attribute error to 1
            self.errorfunc(self.error)  # calling the callback error function          


# ==================== Oscilloscope class definition (mother=intrument) =================================
class oscilloscope(instrument):
    # --------------------------------------------------------------------------------
    # Reset the oscilloscope:
    def reset(self):
        self.identity = self.do_query_string("*IDN?")   # query the oscilloscope identity
        print("Instrument IDN : %s" % self.identity)    # printing the oscilloscope identity in the console
        self.do_command("*CLS") # clearing oscilloscope status
        self.do_command("*RST") # reseting the oscilloscope

    # ------------------------------------------------------------------------------
    # Autoscale:
    def autoscale(self):
        self.do_command(":AUToscale")   # sending autoscale command

    # ------------------------------------------------------------------------------
    # Setting the vertical scale
    def setVertScale(self, channel, vscale):
        self.do_command(":CHANnel"+str(channel)+":SCALe "+str(vscale))  # sending vertical scale command for the specified channel

    # ------------------------------------------------------------------------------
    # Setting the vertical offset
    def setVertOffset(self, channel, voffset):
        self.do_command(":CHANnel"+str(channel)+":OFFSet "+str(voffset))    # sending vertical offset command for the specified channel

    # ------------------------------------------------------------------------------
    # Setting the horizontal scale
    def setHoriScale(self, hscale):
        self.do_command(":TIMebase:SCALe "+str(hscale)) # sending horizontal scale command

    # ------------------------------------------------------------------------------
    # Setting the horizontal scale
    def setHoriOffset(self, hoffset):
        self.do_command(":TIMebase:POSition "+str(hoffset)) # sending horizontal offset command

    # ------------------------------------------------------------------------------
    # Setting trigger to edge mode, and setting the level with a particular channel source
    def setTriggerEdgeLevel(self, channel, level):
        self.do_command(":TRIGger:MODE EDGE")   # setting trigger to edge mode
        self.do_command(":TRIGger:EDGE:SOURce CHANnel"+str(channel))    # setting the source for the trigger
        self.do_command(":TRIGger:EDGE:LEVel "+str(level))  # setting the level of the trigger
        self.do_command(":TRIGger:EDGE:SLOPe POSitive")     # setting the trigger to positive mode

    # ------------------------------------------------------------------------------
    # Setting the aquisition mode -> 1:NORMal, 2:PEAK, 3:AVERage, 4:HRESolution
    def setAquisitionMode(self, mode):
        if mode==1:
            self.do_command(":ACQuire:TYPE NORMal") # setting the aquisition mode to normal
        elif mode==2:
            self.do_command(":ACQuire:TYPE PEAK")   # setting the aquisition mode to peak
        elif mode==3:
            self.do_command(":ACQuire:TYPE AVERage")    # setting the aquisition mode to average
        elif mode==4:
            self.do_command(":ACQuire:TYPE HRESolution")    # setting the aquisition mode to high resolution
        else:
            self.do_command(":ACQuire:TYPE NORMal") # setting the aquisition mode to normal

    # -------------------------------------------------------------------------------
    # Save the current waveform which is displated on the oscillo screen
    def saveWaveform(self, channel, nbPoints):
        self.do_command(":ACQuire:COMPlete 100")    # affects the :DIGitize command. It specifies the minimum completion criteria for an acquisition, here setting it to 100%
        self.do_command(":DIGitize CHANnel"+str(channel))   # the :DIGitize command captures data that meets the specifications set up by the :ACQuire subsystem
        self.do_command(":WAVeform:SOURce CHANnel"+str(channel))    # setting the channel for the aquisition
        self.do_command(":WAVeform:FORMat BYTE")    # setting the format in what we want to retrieve the data, byte = each point is coded on an octet, -100=bottom of the screen and 100=top of the screen
        self.do_command(":WAVeform:POINts "+str(nbPoints))  # setting the number of points on the horizontal
        self.do_command(":WAVeform:UNSigned 0") # we don't want unsigned bytes
        data = self.do_query_ieee_block(":WAVeform:DATA?", 'b')  # query the oscilloscope to retrieve the data of the points
        waveform = [[],[]]  # creating a waveform variable as an array of size 2, first list = the voltage and second list = the time
        VScale = float(self.do_query_number(":CHANnel"+str(channel)+":SCALe?")) # querying the vertical scale in V/div (8 
        VOffset = float(self.do_query_number(":CHANnel"+str(channel)+":OFFSet?")) # querying the vertical offset in V/div
        HScale = float(self.do_query_number(":TIMebase:SCALe?")) # querying the horizontal scale in sec/div
        for i in range(len(data)) : # parcouring the data retrieve from the oscilloscope
            waveform[0].append(float(truncate((float(data[i])*(4*VScale)/100)+VOffset, 5))) # in V, voltage = data * ((4 Vscale)/100) + Voffset 
            waveform[1].append(float(truncate(float(i*((10*HScale)/nbPoints)*1000), 5)))    # in ms, time = i * ((10 Hscale)/nbPoints) * 1000(to be in ms)
        self.do_command(":RUN") # the :DIGitize command stop the aquisition so we run back the achisition at the end
        return waveform # returning the waveform

    # -------------------------------------------------------------------------------
    # Save the current screen of the oscilloscope in PNG format and transform it into a base64 encoded string
    def saveScreen(self):
        im_bytes_list = self.do_query_ieee_block(":DISPlay:DATA? PNG, COLor", 'c')  # saving the data of the screen image into a list of bytes
        im_bytes = b''  # creating a new variable for concatenate all the bytes into just one bytes variable
        for i in range(len(im_bytes_list)) :
            im_bytes += im_bytes_list[i]    # concatenate all the bytes
        im_b64 = base64.b64encode(im_bytes).decode("utf8")  # converting the image bytes into a base64 encoded string
        return im_b64
