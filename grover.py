from pyquil import Program
from pyquil.gates import H, I
from pyquil.api import WavefunctionSimulator, QVMConnection
from pyquil.quil import DefGate

import numpy as np
import math
import json
import time


def wavefunction(p):  # for testing purpose
    wfs = WavefunctionSimulator()
    return wfs.wavefunction(p)

def grover(dataset, target):
    if(type(target) is str):
        target = ord(target)

    for i in range(len(dataset)):
        if i == 0:
            if(type(dataset[i]) is int):
                max_value = dataset[i]
            elif (type(dataset[i]) is str):
                max_value = ord(dataset[i])
        else :
            if(type(dataset[i]) is int):
                if(max_value < dataset[i]):
                    max_value = dataset[i]
            elif (type(dataset[i]) is str):
                if(max_value < ord(dataset[i])):
                    max_value = ord(dataset[i])
    bitstring = bin(max_value)[2:]

    nQubit = len(bitstring)
    nState = 2**nQubit

    dataTarget = bin(target)[2:]
    
    # store all the possible state
    listState = []
    for i in range(nState):
        listState.append(bin(i)[2:].zfill(nQubit))
        
    initialState = 1/math.sqrt(nState)
    otherInitialState = 1/math.sqrt(nState)

    # define oracle function
    oracle = np.zeros((nState, nState))
    for i in range(nState):
        for j in range(nState):
            if(i == j):
                if(bin(i)[2:].zfill(nQubit) == dataTarget.zfill(nQubit)[::-1]):
                    oracle[i][j] = -1
                else:
                    oracle[i][j] = 1

    # define new gate oracle function
    oracle_definition = DefGate("Oracle_Function", oracle)
    Oracle_Function = oracle_definition.get_constructor()

    ### define new gate diffusion
    diffusion = np.zeros((nState, nState))
    for i in range(nState):
        for j in range(nState):
            if(i == j):
                diffusion[i][j] = -1+(2/nState)
            else:
                diffusion[i][j] = 2/nState
    diffusion_definition = DefGate("Diffusion_Matrix", diffusion)
    Diffusion_Matrix = diffusion_definition.get_constructor()
    
    # initialize n qubits in state 0
    p = Program()
    p += oracle_definition
    p += diffusion_definition
    # start of Grover Algorithm

    # step i : apply hadamard gates to all qubits
    for i in range(nQubit):
        p += H(i)
        
    # step ii : Grover iteration
    nIteration = int(np.pi / 4 * math.sqrt(nState))

    listAmplitude = list()
    
    for i in range(nIteration):
    # apply oracle function
        p += tuple(["Oracle_Function"] + list(qubit for qubit in range(nQubit)))
        initialState = -initialState

    # apply diffusion matrix
        p += tuple(["Diffusion_Matrix"] + list(qubit for qubit in range(nQubit)))
        averageState = (otherInitialState * (nState-1) + initialState) / nState
        initialState += 2*(averageState - initialState)
        otherInitialState += 2*(averageState - otherInitialState)

        
    # step iii : measure
    ### declare classical bit to store result
    ro = p.declare('ro', 'BIT', nQubit) 
    for i in range(nQubit):
        p.measure(i, ro[i])
    #     wavefunction(p)
    qvm = QVMConnection()
    startTime = time.time()
    try:
        grover = qvm.run(p)
    except Exception as e:
        print(str(e))
    result = ""
    # reverse the qubit index
    for i in reversed(range(len(grover[0]))):
        result += str(grover[0][i])
    print(result)
    
    listAmplitude = []
    for i in range(nState):
        if(listState[i] == result):
            listAmplitude.append(initialState)
        else:
            listAmplitude.append(otherInitialState)
        
        
    endTime = time.time()
    chartColor = []
    borderColor = []
    for i in range(nState):
        chartColor.append("rgba(54, 162, 235, 0.2)")
        borderColor.append("rgba(54, 162, 235, 1)")
        
    userTime = round(endTime-startTime, 2)
    return json.dumps({"binary": dataTarget.zfill(nQubit), "qubit": nQubit, "result": result, "found": result == dataTarget.zfill(nQubit), "time": userTime, "state": listState, "amplitude": listAmplitude, "chartColor": chartColor, "borderColor": borderColor})
#     print("Dataset : ", dataset)
#     print("Data target : ", target, type(target))
#     print("Binary representation of data target : ", dataTarget.zfill(nQubit))
#     print("Number of qubit : ", nQubit)
#     print("Result Grover's search : ", result)
#     if(result == dataTarget.zfill(nQubit)):
#     print("Data target found")
#     else:
#     print("Data target not Found")

#     endTime = time.time()
#     print("User Time : ", endTime - startTime)
