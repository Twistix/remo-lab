# ============================= Import modules =======================================
import time
from http_requests import *
from instrument import *

# ========================== Experiment parameters ===============================
# the 14 variables of the database for the control of the oscilloscope
reset = int(0)
autoscale = int(0)
saveScreen = int(0)
saveWaveform = int(0)
vertScale = float(1) # V per vertical division
vertOffset = float(0) # in V
horiScale = float(0.001) # seconds per horizontal division
horiOffset = float(0) # in seconds
trigEdgelevel = float(0) # in V
aquMode = int(1) # 1:NORMal, 2:PEAK, 3:AVERage, 4:HRESolution
submit = int(0)
waveform = ""
error = int
screen_img = ""

postUrl = "https://idee3d.xyz/remolab/oscilloscope/posttodb.php"    # url adress of the php file to update the data of the database
getUrl = "https://idee3d.xyz/remolab/oscilloscope/dbtoget.php"  # url adress of the php file to get data from the database
instrAdress = "USB0::0x0957::0x1799::MY57230744::INSTR" # VISA adress of the instrument

# ========================== Experiment functions =================================
def getParse(getStr) :  # data out of the database is encoded like param1;param2;param3;...;param_n;  ,here n=14
    index = []  # creation of an array index
    curr = 0    # current position in the get string
    nbSeparators = 13   # number of separators ; with the dbtoget.php file
    for i in range(nbSeparators) :  # there we parcour all the get string and we save the indexes where we find a ";" character
        curr = getStr.index(";",curr+1)
        index.append(curr)
    # then we can slice the get string in differents part with the indexes founds previously and then update the variables
    reset = int(getStr[0:index[0]])
    autoscale = int(getStr[index[0]+1:index[1]])
    saveScreen = int(getStr[index[1]+1:index[2]])
    saveWaveform = int(getStr[index[2]+1:index[3]])
    vertScale = float(getStr[index[3]+1:index[4]])
    vertOffset = float(getStr[index[4]+1:index[5]])
    horiScale = float(getStr[index[5]+1:index[6]])
    horiOffset = float(getStr[index[6]+1:index[7]])
    trigEdgelevel = float(getStr[index[7]+1:index[8]])
    aquMode = int(getStr[index[8]+1:index[9]])
    submit = int(getStr[index[9]+1:index[10]])
    waveform = getStr[index[10]+1:index[11]]
    error = int(getStr[index[11]+1:index[12]])
    screen_img = getStr[index[12]+1:]
    return reset,autoscale,saveScreen,saveWaveform,vertScale,vertOffset,horiScale,horiOffset,trigEdgelevel,aquMode,submit,waveform,error,screen_img

def errorHandler(error) : # error callback function that is called by the class oscilloscope when there is an error with the command sent to the oscilloscope
    if error :  # if there is an error we pass the error variable of the database to 1, and all the others "event variables" to 0, and we reset the oscilloscope
        payload = {"reset": 0, "autoscale": 0, "savewaveform": 0, "saveconfig": 0, "submit": 0, "error": 1}
        httpPost(postUrl, payload) # sending the POST request with the data
        time.sleep(4) # waiting a bit
        osc.reset() # reseting the oscilloscope
        time.sleep(2) # waiting a bit
    else : # if there is no error with the actual command sent but there was an error with the previous
        payload = {"error": 0} # we pass the error variable of the database back to 0
        httpPost(postUrl, payload)  # sending the POST request with the data


# ============================= MAIN PROGRAM ==========================================
osc = oscilloscope(instrAdress, errorHandler)

# setting all the "event variables" to 0 and the waveform to vide (variables in the database)
payload = {"reset": 0, "autoscale": 0, "savewaveform": 0, "savescreen": 0, "submit": 0, "waveform": "vide", "error": 0, "screen_img": "vide"}
httpPost(postUrl, payload)

while True :    # main loop
    # at each turn of the main loop, we update the program variables with the variables of the database : db vars => prgrm vars
    reset,autoscale,saveScreen,saveWaveform,vertScale,vertOffset,horiScale,horiOffset,trigEdgelevel,aquMode,submit,waveform,error,screen_img = getParse(httpGet(getUrl))
    
    if (reset == 1):
        osc.reset() # reseting the oscilloscope
        payload = {"reset": 0}
        httpPost(postUrl, payload) # setting back the reset event variable to 0

    if (autoscale == 1):
        osc.autoscale() # autoscale
        payload = {"autoscale": 0}
        httpPost(postUrl, payload)  # setting back the autoscale event variable to 0

    if (submit == 1):
        osc.setVertScale(1, vertScale)  # setting the differents parameters for the oscilloscope (channel 1)
        osc.setVertOffset(1, vertOffset)
        osc.setHoriScale(horiScale/1000)
        osc.setHoriOffset(horiOffset/1000)
        osc.setTriggerEdgeLevel(1, trigEdgelevel)
        osc.setAquisitionMode(aquMode)
        payload = {"submit": 0}
        httpPost(postUrl, payload)  # setting back the submit event variable to 0

    if (saveWaveform == 1):
        waveform = osc.saveWaveform(1, 300) # saving the waveform with 300 points (channel 1)
        waveform_str = "" # creating a variable to convert the waveform array into a string with csv format
        for i in range(len(waveform[0])) :  # fomating the waveform into a csv format
            waveform_str += str(waveform[0][i])+','+str(waveform[1][i])+'\n'
        payload = {"waveform": waveform_str, "savewaveform": 0}
        httpPost(postUrl, payload)  # setting back the savewaveform event variable to 0, and sending the waveform string
        
    if (saveScreen == 1):
        screen = osc.saveScreen() # saving the screen of the oscilloscope into a base64 string
        payload = {"savescreen": 0, "screen_img": screen}
        httpPost(postUrl, payload)  # setting back the savescreen event variable to 0, and sending the screen image string

        
    time.sleep(3) # delay between each turn of the main loop





#UPDATE `oscillo` SET `reset`=0,`autoscale`=0,`submit`=0 WHERE `id`=1
    
#osc = oscilloscope()
#osc.autoscale()
#print(osc.saveWaveform(1, 200))
            


    

    








        
        
    
