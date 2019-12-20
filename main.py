#This is a python program that reads a Arduino .ino file and then interprets its pinMode section into baremetal DDR instructions
#In future I will be updating and expanding it to convert more aspects of the ino file into baremetal code. 

# My ultimate goal is to create a piece of code which forms another copy of code file with baremetal code 
#snippets to increase the speed of code and reduce its code size.

#Uptill now it has the ability to read pinMode and also if there are any variable names inside the pinMode it can read that
#too except of #define constants will be working on it and making a commit regarding it soon. 

#I will really appreciate for your valuable feedback or queries regarding the aspects of code and 
#commits or improvement ideas.
#Author: Shahyan Bharucha
#email id: shahyan30@gmail.com
#First commit date: 12/20/19

import os.path
from os import path
#to store if portD &/or PortB are used.
presentD =0
presentB =0
#To ask for the .ino file name which is stored in the project folder
orignal_file = input("please type the .ino file name: ")
#check if file exists else ask for another file
File_Check = path.exists(orignal_file+".ino")
while File_Check == False:
    print("file name invalid or doesnt exists in the directory")
    orignal_file = input("please type the .ino file name: ")
    File_Check = path.exists(orignal_file+".ino")

#saving the ino file data in file
file=open(orignal_file+".ino","r")
#if file exists 
if file.mode == 'r':
    #read its contents and store it in contents
    contents =file.read()
    contents_copy = contents
    #Search for pinMode in the contents and return its count in pinModeCount
    pinModeCount = contents.count("pinMode")
    PORTD = ['0','0','0','0','0','0','0','0']
    PORTB = ['0','0','0','0','0','0','0','0']
    #untill pinModeCount gets to zero run the routine to search and replace it to baremetal code
    while pinModeCount > 0:
        #find the first pinMode instruction
        FindPinMode = contents.index("pinMode")
        #remove the content before pinMode index and store the rest in pinModeStart
        pinModeStart = contents[FindPinMode:]
        #finding the first semicolon which would indicate the whole pinMode instruction
        FindSemi = pinModeStart.index(";")
        #segregating the first pinMode instruction in PinStatement
        PinStatement = pinModeStart[:FindSemi]
        #now finding its pinNumber which is written after open bracket
        FindOpenBracket = PinStatement.index("(")
        #find first comma
        FindComma = PinStatement.index(",")
        #extract pinnumber or pin name assisgnment and store it in PinName
        PinName = PinStatement[FindOpenBracket+1:FindComma]
        #the rest part use to find the PinMode i.e I/p or O/p
        PinMode = PinStatement[FindComma+1:FindSemi-1]
        #tupple to map pins for Arduino UNO
        pinsUno = ('0', '1','2','3','4','5','6','7','8','9','10','11','12','13','LED_BUILTIN')
        #tupple mapping ports for the respective pins on Arduino UNO
        PortUno = ['D', 'D','D','D','D','D','D','D','B','B', 'B', 'B', 'B', 'B',  'B']
        #respective port pins as per atmel3285 used in UNO
        PinsPORT = ['0','1','2','3','4','5','6','7','0','1','2','3','4','5','5']
        #For loop searching for pin numbers used which are mentioned in map  list pinsUno 
        PinDirection = PinMode.count("OUTPUT")
        if (PinName in pinsUno):
            indexPin = pinsUno.index(PinName)
            if PinDirection > 0:
                value = PinsPORT[indexPin]
                if PortUno[indexPin] == "D":
                    PORTD[-(int(value)+1)] = '1'
                    presentD = 1;
                if PortUno[indexPin] == "B":
                    PORTB[-(int(value)+1)] = '1'
                    presentB = 1
            else:
                if PortUno[indexPin] == "D":
                    PORTD[-(int(value)+1)] = '0'
                    presentD = 1;
                if PortUno[indexPin] == "B":
                    PORTB[-(int(value)+1)] = '0'
                    presentB = 1
            
        else:
            #if pinname is not in the list it means a variable is used to store its pin value so the below section
            #will search for variables and extract their pin values
            VariableIndex = contents_copy.index(PinName)
            Variable= contents_copy[VariableIndex:]
            FindEq = Variable.index("=")
            FindSemiVar = Variable.index(";")
            VarWithSpaces = Variable[FindEq+1:FindSemiVar]
            VariablePin = VarWithSpaces.strip()
            #check if valid pins are used for UNO else give a error
            if(VariablePin in pinsUno):
                indexPin = pinsUno.index(VariablePin)
            else:
                print("Pin " + VariablePin+ " doesn't exists in Arduino UNO. Please check your program.")
                exit()
            #if the direction is OUTPUT then make its respective bit one else zero
            if PinDirection > 0:
                value = PinsPORT[indexPin]
                if PortUno[indexPin] == "D":
                    PORTD[-(int(value)+1)] = '1'
                    presentD = 1;
                if PortUno[indexPin] == "B":
                    PORTB[-(int(value)+1)] = '1'
                    presentB = 1
            else:
                if PortUno[indexPin] == "D":
                    PORTD[-(int(value)+1)] = '0'
                    presentD = 1;
                if PortUno[indexPin] == "B":
                    PORTB[-(int(value)+1)] = '0'
                    presentB = 1
            
        contents = pinModeStart[FindSemi:]
        pinModeCount = pinModeCount-1

    PORTDstr = "".join(PORTD)
    PORTBstr = "".join(PORTB)
    if presentD > 0:
        DDRD = "DDRD"+  "="+"DDRD"+" | "+" B"+ PORTDstr + ";"
        print(DDRD)
    if presentB >0:
        DDRB = "DDRB"+ "="+"DDRB"+" | "+" B"+ PORTBstr + ";"
        print(DDRB)
        
#write the concise direction registers assignments in a file for use
DDRWRITE= open("DDRWRITE.ino","w+")
DDRWRITE.write(DDRD + "\n" + DDRB)


    

