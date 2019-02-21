#!/usr/bin/python
import datetime
import os
import re
import sys
import filecmp

#This method prints the files that do fit the options given in arguments. It takes the list of files as parameter.
def printFiles(listOfFiles):
    for f in listOfFiles:
        print(f)
    return None

#This method prints the syntax error on screen then stops the programs execution with sys.exit() method.
def syntaxError():
    print("Syntax Error")
    sys.exit()
    return None

#This mathod takes a list as parameter and sorts its contents with the classical algorithm of bubble sort.
def bubble_sort(seq):
    changed = True
    #changed boolean is used to check if an element swapped places with its next.
    while changed:
        changed = False
        for i in range(len(seq) - 1):
            #nm1 and nm2 are strings that keeps the names of the files.
            nm1 = str(seq[i])[str(seq[i]).rfind("/")+1]
            nm2 = str(seq[i+1])[str(seq[i+1]).rfind("/") + 1]
            if nm1 > nm2:
                seq[i], seq[i + 1] = seq[i + 1], seq[i]
                changed = True
    return None

#This variable is used to see if any options are given or not.
isGivenOptions = False
#qlist is the list that keeps the folders in the given path.
qlist=[]
#Since python takes the path that the program is in as the 0th arguments, if there is no given options or paths
#then that means there is only the path our program is in as argument so the length of the argv list is 1 when there is no argument given.
if len(sys.argv) == 1:
    output = os.getcwd()
    #output is the current working directory.
    qlist.append(output)
    #When there is no given paths in program arguments we put current working directory in qlist.
else:
    #If there is at least one given parameter(option or path) it gets in this else part.
    isGivenDirectory = False
    #isGivenDirectory is the boolean that represents if there is given path as parameter.
    #The for loop below traverses the program arguments.
    for i in range(1,len(sys.argv)):
        #If there is an argument that doesn't start with -, means it is either a path or option parameter.
        if (sys.argv[i][0] != "-"):
            if (os.path.exists(sys.argv[i])):
                #If the argument is a path, isGivenDirectory is true and this path is added to qlist.
                isGivenDirectory = True
                qlist.append(sys.argv[i])
        else:
            #If this argument starts with -, that means it an option.
            isGivenOptions=True
    if not isGivenDirectory:
        #If there is no path given in arguments, the current working directory is added to qlist.
        output=os.getcwd()
        qlist.append(output)
#filelist is the list of paths of files that fits in given options.
fileList = []
while qlist:
    currentdir = qlist.pop()
    dircontents = os.listdir(currentdir)
    #qlist is traversed and the directories in it is taken and their contents are added to filelist.
    for name in dircontents:
        name = str(name)
        currentitem = str(currentdir) + "/" + name
        if os.path.isdir(currentitem):
            qlist.append(currentitem)
        else:
            fileList.append(currentitem)
uniqueFiles = []
#uniqueFiles is the list that keeps the unique files in given directory. This will be used if duplcont or duplname is given.
allFiles = fileList[:]
if not isGivenOptions:
    #If there is no given options, the default action which is to print all files will be exucuted.
    printFiles(fileList)

else:
#That means there is options given.
    #The booleans in below means if these options are given before. It is an error to give the same option more than once.
    before = False
    after = False
    match = False
    bigger = False
    smaller = False
    delete = False
    zipp = False
    duplcont = False
    duplname = False
    stats = False
    nofilelist = False
    #All options are false at the start since they are not traversed yet.
    #nofFiles that keeps the number of all files in directory given, sizeFiles is the total size of given files and sizeListed
    #keeps the total size of the files listed. These variables will be used afterwards if -stats option will be given.
    nofFiles=len(fileList)
    sizeFiles=0
    sizeListed=0
    #Arguments are traversed.
    for i in range(0, len(sys.argv)):
        s = sys.argv[i]
        if s[0] == "-":
            #If an argument starts with -, that means it is an option.
            if s == "-before":
                if before:
                    #If an option is traversed before that means it is given more than once, meaning there is an error.
                    syntaxError()
                givenTime = sys.argv[i + 1]
                #The argument after the option is parameter of option.
                i += 1
                # If the given time is in YYYYMMDD format it is converted to the YYYYMMDDHHMMSS format.
                if len(givenTime) == 8:
                    givenTime = givenTime + "T235959"
                # Here we traverse the list's copy in for loop because we modify the list in for loop and this is more convenient.
                for f in fileList[:]:
                    modtime = os.path.getmtime(f)
                    modtime = datetime.datetime.fromtimestamp(modtime).strftime('%Y%m%dT%H%M%S')
                    #fileList is traversed and its contents' mod time is taken.
                    if modtime > givenTime:
                        #If the moderation time is bigger than given time it is removed from fileList.
                        fileList.remove(f)
                before = True

            elif s == "-after":
                if after:
                    syntaxError()
                    # If an option is traversed before that means it is given more than once, meaning there is an error.
                givenTime = sys.argv[i + 1]
                i+=1
                # If the given time is in YYYYMMDD format it is converted to the YYYYMMDDHHMMSS format.
                if len(givenTime) == 8:
                    givenTime = givenTime + "T000000"
                # Here we traverse the list's copy in for loop because we modify the list in for loop and this is more convenient.
                for f in fileList[:]:
                    modtime = os.path.getmtime(f)
                    modtime = datetime.datetime.fromtimestamp(modtime).strftime('%Y%m%dT%H%M%S')
                    # fileList is traversed and its contents' mod time is taken.
                    if modtime < givenTime:
                        #If the moderation time is smaller than given time it is removed from fileList.
                        fileList.remove(f)
                after = True

            elif s == "-match":
                if match:
                    # If an option is traversed before that means it is given more than once, meaning there is an error.
                    syntaxError()
                # We take the pattern from arguments and add ".\w+\Z" at the end of it because we are looking for that pattern at the end of path since it is file name
                pattern = sys.argv[i + 1] + ".\w+\Z"
                i+=1
                # Here we traverse the list's copy in for loop because we modify the list in for loop and this is more convenient.
                for f in fileList[:]:
                    found = re.search(pattern, f)
                    if not found:
                        #If the file f's name does not match the pattern it is removed from the list.
                        fileList.remove(f)
                match = True
            elif s == "-bigger":
                if bigger:
                    # If an option is traversed before that means it is given more than once, meaning there is an error.
                    syntaxError()
                # We take the given size in givenSize
                givenSize = sys.argv[i + 1]
                i += 1
                # If all characters of givenSize are not digits that means there is either k,m or g in given size. We convert it to bytes.
                #givenSize is converted to int everytime because it is given as string and we want to use it as integer to do mathematical operations.
                if not givenSize.isdigit():
                    if givenSize[-1] == "K" or givenSize[-1] == "k":
                        givenSize = int(givenSize[:-1]) * 1024
                    elif givenSize[-1] == "M" or givenSize[-1] == "m":
                        givenSize = int(givenSize[:-1]) * 1048576
                    elif givenSize[-1] == "G" or givenSize[-1] == "g":
                        givenSize = int(givenSize[:-1]) * 1073741824
                    else:
                        syntaxError()
                else:
                    givenSize = int(givenSize)
                for f in fileList[:]:
                    # If the size of the file in fileList is smaller than given size, this file is removed from fileList
                    fileSize = os.path.getsize(f)
                    if fileSize < givenSize:
                        fileList.remove(f)
                bigger = True
            elif s == "-smaller":
                if smaller:
                    # If an option is traversed before that means it is given more than once, meaning there is an error.
                    syntaxError()
                givenSize = sys.argv[i + 1]
                i += 1
                # givenSize is converted to int everytime because it is given as string and we want to use it as integer to do mathematical operations.
                if not givenSize.isdigit():
                    # Here k or m or g is converted to bytes.
                    if givenSize[-1] == "K" or givenSize[-1] == "k":
                        givenSize = int(givenSize[:-1]) * 1024
                    elif givenSize[-1] == "M" or givenSize[-1] == "m":
                        givenSize = int(givenSize[:-1]) * 1048576
                    elif givenSize[-1] == "G" or givenSize[-1] == "g":
                        givenSize = int(givenSize[:-1]) * 1073741824
                    else:
                        syntaxError()
                else:
                    givenSize = int(givenSize)
                for f in fileList[:]:
                    # If the size of the file in fileList is bigger than given size, that file is removed from fileList
                    fileSize = os.path.getsize(f)
                    if fileSize > givenSize:
                        fileList.remove(f)
                smaller = True
            elif s == "-delete":
                if delete:
                    # If an option is traversed before that means it is given more than once, meaning there is an error.
                    syntaxError()
                for f in fileList[:]:
                    # Files in fileList is deleted using the terminal command rm.
                    command = 'rm -f ' + f
                    os.system(command)
                delete = True
            elif s == "-zip":
                if zipp:
                    # If an option is traversed before that means it is given more than once, meaning there is an error.
                    syntaxError()
                    #name of the zip file
                zipfile = sys.argv[i + 1]
                i += 1
                for f in fileList[:]:
                    # Files in fileList is zipped in zipfile using the terminal command zip
                    command = "zip " + zipfile + " " + f
                    os.system(command)
                zipp = True
            elif s == "-duplcont":
                # if either duplcont or duplname given before,it is syntax error
                if duplcont or duplname:
                    syntaxError()
                contList = []  # contList is a control list to hold the visited files
                tempList = fileList[
                           :]  # templist is the copy of the fileList,to prevent changes on fileList during modifications
                bubble_sort(tempList)  # sorts the list according to their name
                check = False
                for f in tempList:
                    b = tempList.index(f) + 1
                    if f not in contList:  # for f in tempList but not in contList means the files that haven't got compared before
                        temp = []  # this list is used for temporary holds
                        for g in tempList[b:]:
                            if filecmp.cmp(f, g,
                                           shallow=False):  # if g has the same content with f then append g to temp
                                check = True
                                temp.append(g)
                        uniqueFiles.append(f)
                        temp.append(f)
                        if check:  # if more than one file appended to the temp,then sorts them
                            bubble_sort(temp)
                        contList.extend(temp)
                        contList.append("------")  # the string "------" to seperate the files when printing them
                    check = False
                fileList = contList  # new fileList is the contList
                duplcont = True
            elif s == "-duplname":
                # if either duplcont or duplname given before,it is syntax error
                if duplcont or duplname:
                    syntaxError()
                nmList = []  # nmList is a control list to hold the visited files
                tempList = fileList[
                           :]  # templist is the copy of the fileList,to prevent changes on fileList during modifications
                bubble_sort(tempList)  # sorts the list according to their name
                for f in tempList:
                    b = tempList.index(f) + 1
                    if f not in nmList:  # for f in tempList but not in contList means the files that haven't got compared before
                        nmf = str(f)[str(f).rfind("/") + 1]  # nameof f
                        for g in tempList[b:]:
                            nmg = str(g)[str(g).rfind("/") + 1]  # nameof g
                            if nmf == nmg:  # if names are same,then append g to nmList
                                nmList.append(g)
                        uniqueFiles.append(f)
                        nmList.append(f)
                        nmList.append("------")  # the string "------" to seperate the files when printing them
                fileList = nmList  # new fileList is the contList
                duplname = True
            elif s == "-stats":
                if stats:
                    # If an option is traversed before that means it is given more than once, meaning there is an error.
                    syntaxError()
                stats=True
            elif s == "-nofilelist":
                if nofilelist:
                    # If an option is traversed before that means it is given more than once, meaning there is an error.
                    syntaxError()
                nofilelist=True

    # if nofilelist option isn't given that print the files
    if not nofilelist:
        #fileList holds the files that satisfies the given conditions
        printFiles(fileList)
    # if stats options is given and nofilelist option is not given, writes files with statistical information
    if stats and not nofilelist:
        #prints number of files visited
        print(nofFiles)
        #calculates the size of files visited
        for f in allFiles:
            fileSize = os.path.getsize(f)
            sizeFiles += fileSize
            #prints the size of files visited
        print(sizeFiles)
        #no is for number of files listed
        no = 0
        #calculates the size of files listed
        for f in fileList:
            if f!="------":
                no+=1
                fileSize = os.path.getsize(f)
                sizeListed += fileSize
        #prints the number of files listed
        print(no)
        #prints the size of files listed
        print(sizeListed)
        #if duplcont option is given then prints the total number of unique files listed and total size of unique files
        if duplcont:
            #sizeUnique holds the total size of unique files
            sizeUnique=0
            for f in uniqueFiles:
                fileSize = os.path.getsize(f)
                sizeUnique+=fileSize
            #prints the number of uniqueFiles
            print(len(uniqueFiles))
            #prints the total size of unique files
            print(sizeUnique)
        #if duplname option is given then prints the total number of unique files with names
        if duplname:
            #nameList holds the name of files
            nameList=[]
            for f in uniqueFiles:
                nm = str(f)[str(f).rfind("/")+1]
                nameList.append(nm)
            #prints the total number of unique files
            print(len(uniqueFiles))
            #prints the names of the files
            for f in nameList:
                print(f )



