possible_commandlist = ['install','download','download_dir','mkdir','custom']


#Removes an operation
def edit_remove(index,commandlist):
    if len(commandlist) > 0:
        if index in range(len(commandlist)):
            del commandlist[index]
            return commandlist
        else:
            print("Check your index.")
            return commandlist
    else:
        print("There are no commands to remove!")
        return commandlist

#Replace an operation
def edit_replace(index,commandlist):
    if len(commandlist) > 0:
        if index in range(len(commandlist)):
            print("You are now editing the command '" + str(commandlist[index]) + "'")
            print("Enter how you want the command to be stored.")
            print("1st column must be one of: " + str(possible_commandlist))
            edit_line = input("Separate the command and each arguments by commas: ")
            if edit_line:
                edit_line = edit_line.split(',')
                commandlist[index] = edit_line
            return commandlist
            
        else:
            print("Check your index.")
            return commandlist
    else:
        print("There are no commands to replace!")
        return commandlist

#Switches two operations
def edit_switch(index1,index2,commandlist):
    if len(commandlist) > 0:
        if index1 in range(len(commandlist)) and index2 in range(len(commandlist)):
            msg = "Switching " + str(commandlist[index1]) + " and " + str(commandlist[index2])
            print(msg)
            tempitem = commandlist[index1]
            commandlist[index1] = commandlist[index2]
            commandlist[index2] = tempitem
            return commandlist
            
        else:
            print("Check your index.")
            return commandlist
    else:
        print("There are no commands to replace!")
        return commandlist

def edit_insert(index, commandlist):
    if len(commandlist) > 0:
        if index in range(len(commandlist)):
            print("You are inserting a command at index " + str(index) + "; 1st column must be one of: " + str(possible_commandlist))
            edit_line = input("Separate the command and each arguments by commas: ")
            edit_line = edit_line.split(',')
            commandlist.insert(index,edit_line)
            return commandlist
            
        else:
            print("Check your index.")
            return commandlist
    else:
        print("There are no commands to replace!")
        return commandlist








#Converting commands into bash
def bashconvert(command,host_address,username,password):
    #Check what type of command it is.
    if command[0] in possible_commandlist:
        if command[0] == 'install':
            return 'sudo apt install ' + command[1] + ' -y'
        elif command[0] == 'download':
            bashline = 'sshpass -p ' + password + ' scp ' + username + '@' + host_address + ':"' + command[1] + '" "' + command[2] + '"'
            return bashline
        elif command[0] == 'mkdir':
            return 'mkdir "' + command[1] + '"'
        elif command[0] == 'custom':
            return command[1]
        elif command[0] == 'download_dir':
            bashline = 'sshpass -p ' + password + ' scp -r ' + username + '@' + host_address + ':"' + command[1] + '" "' + command[2] + '"'
            return bashline
        else:
            print("Unknown command.")
    else:
        print("Unknown error in the command list.")