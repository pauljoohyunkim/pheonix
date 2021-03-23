#!/bin/python3

import cmd
import os
import sys
import getpass
import pheonix_file_op
import pheonix_edit_op

class MainShell(cmd.Cmd):
	intro = 'Welcome to Pheonix!\n\nThis script creates a bash script which will attempt set up your machine as you configured.\nThe bash script will utilize ssh.\nRun \'cred\' first to enter username password.\nRun \'load [session name]\' to load up a previous session.\n'
	prompt = 'Pheonix > '
	commandlist = []
	addr = ''
	username = ''
	password = ''
	loadpath = ''
	#For entering server information.
	def do_cred(self,arg):
		'Syntax: cred\nYou will be prompted to enter your server info.\n'
		if not self.addr:
			self.addr = input("Enter the IP ADDRESS of the server: ")
			self.username = input("Enter the USERNAME of the server: ")
			self.password = getpass.getpass("Enter the PASSWORD corresponding to the username: ")
		else:
			print("[Address, Username, Password] = " + str([self.addr,self.username,'*' * len(self.password)]))
			option = input("Would you like to change? [y/N]")
			if option.lower() == 'y':
				self.addr = input("Enter the IP ADDRESS of the server: ")
				self.username = input("Enter the USERNAME of the server: ")
				self.password = getpass.getpass("Enter the PASSWORD corresponding to the username: ")
			elif option.lower() == 'n':
				print("I'm guessing you don't want to change anything...")
			else:
				print("Since it wasn't a 'y', I'm guessing you don't want to change anything...")

	#For viewing the information entered so far.
	def do_view(self,arg):
		'View information entered so far.\nSyntax: view\n'
		option = input('With pass? (Make sure no one is behind you!) [y/N]: ')
		if option.lower() == 'y':
			print("Server Address: " + self.addr)
			print("Username: " + self.username)
			print("Password: " + self.password)
			print("Commands: ")
			for index in range(len(self.commandlist)):
				print(str(index) + "\t" + str(self.commandlist[index]))
		elif option.lower() == 'n':
			print("Server Address: " + self.addr)
			print("Username: " + self.username)
			print("Password: " + "*" * len(self.password))
			print("Commands: ")
			for index in range(len(self.commandlist)):
				print(str(index) + "\t" + str(self.commandlist[index]))
		else:
			print("Well, it wasn't a 'yes'...\n")
			print("Server Address: " + self.addr)
			print("Username: " + self.username)
			print("Password: " + "*" * len(self.password))
			print("Commands: ")
			for index in range(len(self.commandlist)):
				print(str(index) + "\t" + str(self.commandlist[index]))

	def do_edit_remove(self,arg):
		'Removes a command by index from \'view\' command.\nSyntax: edit_remove [index]'
		if arg:
			#Temporarily storing what is being removed for info text
			tempitem = self.commandlist[int(arg)]
			self.commandlist = pheonix_edit_op.edit_remove(int(arg),self.commandlist)
			print("Removed '" + str(tempitem) + "' from the command list!")	#info text here
			#Prints command list after the operation
			print("Commands: ")
			for index in range(len(self.commandlist)):
				print(str(index) + "\t" + str(self.commandlist[index]))
		else:
			print("No index specified.")

	def do_edit_replace(self,arg):
		'Replaces a command by index from \'view\' command.\nSyntax: edit_replace [index]'
		if arg:
			self.commandlist = pheonix_edit_op.edit_replace(int(arg),self.commandlist)
			print("Commands: ")
			for index in range(len(self.commandlist)):
				print(str(index) + "\t" + str(self.commandlist[index]))
		else:
			print("No index specified.")

	def do_edit_switch(self,arg):
		'Switches two commands by index from \'view\' command.\nSyntax: edit_switch [index1] [index2]'
		indices = arg.split()
		for i in range(len(indices)):
			indices[i] = int(indices[i])
		if len(indices) == 2:
			self.commandlist = pheonix_edit_op.edit_switch(indices[0],indices[1],self.commandlist)
			print("Commands: ")
			for index in range(len(self.commandlist)):
				print(str(index) + "\t" + str(self.commandlist[index]))
		else:
			print("Check argument again!")
	
	def do_edit_insert(self,arg):
		'Inserts a command by index from \'view\' command.\nSyntax: edit_insert [index]'
		if arg:
			self.commandlist = pheonix_edit_op.edit_insert(int(arg),self.commandlist)
			print("Commands: ")
			for index in range(len(self.commandlist)):
				print(str(index) + "\t" + str(self.commandlist[index]))
		else:
			print("No index specified.")

	#For installing application via apt
	def do_install(self,arg):
		'Installs application via apt\nSyntax: install [package name]\neg) install python3\n'
		
		#Adding command to the list
		if arg:
			self.commandlist.append(['install',arg.strip()])
	

	#For downloading files from your server
	def do_download(self,arg):
		'Syntax: download [source path on server] [destination path on client]'
		if len(arg.split()) != 2:
			print("Follow the syntax!")
			return 0
		if self.addr == '':
			print("Enter server information first by 'cred' command.")
			return 0
		else:
			paths = arg.split()
			self.commandlist.append(['download',paths[0],paths[1]])
		

	#For downloading directories (recursively)
	def do_download_dir(self,arg):
		'Syntax: download_dir [source path on server] [destination path on client]'
		if len(arg.split()) != 2:
			print("Follow the syntax!")
			return 0
		if self.addr == '':
			print("Enter server information first by 'cred' command.")
			return 0
		else:
			paths = arg.split()
			self.commandlist.append(['download_dir',paths[0],paths[1]])
		pass

	#For creating a directory
	def do_mkdir(self,arg):
		'Syntax: mkdir [directory name]'
		if arg:
			self.commandlist.append(['mkdir',arg.strip()])

	#For custom commands. Adding the line directly.
	def do_custom(self,arg):
		'Adds the argument as given directly to the file.'
		if arg:
			self.commandlist.append(['custom',arg.strip()])

	#For saving sessions
	def do_save(self,arg):
		savedata = savedata = [self.addr,self.username,self.password] + self.commandlist
		if savedata == ['','','']:
			sys.exit()
		option = input("Would you like to save progress? [y/N/cancel]")
		if option.lower() == 'y':
			if self.loadpath == '':
				savepath = input("Enter save file path (without extension): ")
			else:
				savepath = self.loadpath
			savedata = [self.addr,self.username,self.password] + self.commandlist
			pheonix_file_op.jsonsave(savedata,savepath + '.json')
			self.loadpath = savepath
			print("Saved as: " + savepath)
		elif option.lower() == 'cancel':
			return 0

	#QUITTING
	def do_quit(self,arg):
		'Exits the shell.'

		#Data to save
		savedata = [self.addr,self.username,self.password] + self.commandlist
		#Checks if there are any data to save to start with...
		if savedata == ['','','']:
			print("Good bye!")
			sys.exit()
		#If there is data to save, ask the user if they want to save
		option = input("Would you like to save progress? [y/N/cancel]")
		#If yes,
		if option.lower() == 'y':
			#Check if we've already loaded from another json file.
			#If not, ask for save location
			if self.loadpath == '':
				savepath = input("Enter save file path (without extension): ")
			#Otherwise, overwrite the session json file.
			else:
				savepath = self.loadpath
			pheonix_file_op.jsonsave(savedata,savepath + '.json')
			print("Next time you start up, run 'load " + savepath + '\'')
		#If cancel, return to the commandline.
		elif option.lower() == 'cancel':
			return 0
		#Else, exit
		print("Good bye!")
		sys.exit()

	def do_exit(self,arg):
		'Exits the shell.'
		self.do_quit('')

	#For loading sessions
	def do_load(self,arg):
		'Loads previous session\nSyntax: load [filename (without extension)]'
		#Current data
		currentdata = [self.addr,self.username,self.password] + self.commandlist
		#Read from the json
		tempdata = pheonix_file_op.jsonload(arg + '.json')
		#If no data was given, load.
		if currentdata == ['','','']:
			self.addr = tempdata[0]
			self.username = tempdata[1]
			self.password = tempdata[2]
			self.commandlist = tempdata[3:]
			self.loadpath = arg
			print('Loaded ' + arg + ' session.')
			return 0
		#If we already have data, check if current data is the json data.
		#If different, give warning
		if currentdata != tempdata:
			option = input("Modified data detected! Would you like to load again? [y/N]")
			if option.lower() == 'y':
				self.addr = tempdata[0]
				self.username = tempdata[1]
				self.password = tempdata[2]
				self.commandlist = tempdata[3:]
				self.loadpath = arg
			else:
				#Cancel load operation
				return 0
		#Otherwise, we don't actually need to load anything
		print('Loaded ' + arg + ' session.')
	
	def do_clear(self,arg):
		'Clears screen'
		os.system('clear')

	#Outputting .sh file
	def do_output(self,arg):
		'Outputs to a file.\nSyntax: output'
		filetext = "#!/bin/bash\n"
		filetext += "sudo apt install sshpass -y\n"


		#Converting each command into a bash command and appending it to filetext
		for command in self.commandlist:
			filetext += pheonix_edit_op.bashconvert(command,self.addr,self.username,self.password) + "\n"
		
		#By default, this script also updates the system.
		filetext += 'sudo apt autoremove\n'
		filetext += 'sudo apt update && sudo apt upgrade -y'

		#Show a preview
		print("Preview:\n" + filetext)
		#Ask user if they want to save it.
		option = input("Save it? [y/N]")
		if option.lower() == 'y':
			filename = input("Filename (without extension): ")
			#Writing to file.
			with open(filename + '.sh','w') as file_obj:
				file_obj.write(filetext)
				print("Output complete!")
		else:
			return 0

#Start shell
if __name__ == '__main__':
	MainShell().cmdloop()

