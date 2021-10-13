# ============================= Import modules =======================================
from instrument import *

# ========================== Experiment functions =================================
def errorHandler(error) : # error callback function that is called by the class oscilloscope when there is an error with the command sent to the oscilloscope
    if error :  # if there is an error we pass the error variable of the database to 1, and all the others "event variables" to 0, and we reset the oscilloscope
        osc.reset() # reseting the oscilloscope
        time.sleep(2) # waiting a bit
    else : # if there is no error with the actual command sent but there was an error with the previous
        # we do nothing in this case


# ============================= MAIN PROGRAM ==========================================
instrAdress = "USB0::0x0957::0x1799::MY57230744::INSTR" # VISA adress of the instrument

osc = oscilloscope(instrAdress, errorHandler)
time.sleep(1)

osc.autoscale()
time.sleep(0.5)

waveform = osc.savewaveform(1, 300)






        


            


    

    








        
        
    
