import numpy as np
import os

VARS =  14           # number of columns, after one hot encoding
MAX_SIZE = 15        # number of rows = maximum number of particles in the events in the data set 
N_EVENTS = 100000    # total number of events per file

def one_hot(event):          
    #replaces pid and btag with one-hot encoding; do this before padding!

    n_particles = event.shape[0]

    temp = np.pad(event, ((0, 0), (6, 0)), constant_values= 0)
    temp[:,6] = 0
    temp[np.arange(n_particles), event[:,1].astype(int)] = 1  #one-hot encoding for pid
    temp = np.delete(temp, [5,7,-2,-1], axis=1)               #there is no pid = 5; 15 and 16 are dummy vars we don't need

    temp = np.insert(temp, 11, 0, axis=1)
    for i in np.arange(n_particles):
        if event[i,7]==1 or event[i,7]==2:
            temp[i,12]=1
        else:
            temp[i,11]=1                                      #one-hot encoding for btag  
    return temp

def pad_event(event):
    #pad each event with zeros

    if event.shape[0] < MAX_SIZE:
        pad_width = MAX_SIZE - event.shape[0] 
        event = np.pad(event, ((0, pad_width), (0, 0)), constant_values= 0)
        return event

    elif event.shape[0] == MAX_SIZE:
        return event

    else:
        print("MAX_SIZE is too small! Use:", event.shape[0])
        return event[:MAX_SIZE, :]


def print_event(event):
    #prints event, before padding and one-hot encoding

    np.set_printoptions(linewidth=400)
    print("          pid    eta    phi   pt      jmass  ntrk   btag   had/em ") 
    print(event[:,:-2])
    print("\n")

def extract_events(inputfilename, outputfile):
    #opens LHCO file, separates and processes events, writes onto .npy file 
    
    f = open(inputfilename, "r")

    event = []

    for line in f:
        if "jmas" in line and "ntrk" in line:
            break
    
    _, event_no, _ = f.readline().split()

    while int(event_no) < N_EVENTS:
        for line in f:
            temp = line.split()
            if temp[0] == '0':
                _, event_no, _ = temp
                break
            else:
                event.append([float(i) for i in temp])
        event = np.array(event)

        event = one_hot(event)
        event = pad_event(event)
        event = event.reshape((1,-1))
        
        np.savetxt(outputfile, event, delimiter=',')

        event = []

    #last event is treated separately to handle EOF properly
    temp = f.readlines()
    for line in temp:
        event.append([float(i) for i in line.split()])
    
    event = np.array(event)
    event = one_hot(event)
    event = pad_event(event)
    event = event.reshape((1,-1))
    
    np.savetxt(outputfile, event, delimiter=',')

    f.close()

def drop_columns(array, col_list, col):
    array = array.reshape((-1, MAX_SIZE, col))
    array = np.delete(array, col_list, axis=2)
    col = col - len(col_list)
    array = array.reshape((-1, MAX_SIZE*col))
    return array

def main():

    with open("bkg.csv","wb") as outputfile:
        for filename in os.listdir('bkg'):
            extract_events("bkg/"+filename, outputfile)

    with open("sig.csv","wb") as outputfile:
        for filename in os.listdir('sig'):
            extract_events("sig/"+filename, outputfile)

if __name__=="__main__":
	main(); 

