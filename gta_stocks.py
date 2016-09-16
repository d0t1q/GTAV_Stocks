#!/usr/bin/python
# coding: utf-8 
#Version 0.04
#Import libs
import sys, re, time, os, datetime, urllib2
#syslib grabs the system arguments(thinking about removing it
#relib is used for the regular expressions
#time is for when we want to sleep until grabbing the file again
#os for running the clear command LINUX FRIENDLY ONLY
#datetime is used for formatting the CSV with the time in which the info is grabbed
#urllib2
from os import path
#os import path is for checking if the folders have been made
#and if the csv file is available 
from colorama import Fore, Back, Style
#so we can make it look pretty 



#define the stock names and throw them in a list
stock_names = ['(AMU)','(BDG)','(BET)','(BFA)','(BIN)','(BTR)','(BLE)','(BRU)','(CNT)','(CRE)','(DGP)','(WAP)','(EYE)','(FAC)','(FRT)','(GOT)','(HAL)','(HVY)','(LSC)','(LST)','(LTD)','(MAI)','(PIS)','(PON)','(PMP)','(RON)','(SHT)','(SHK)','(SHR)','(SPU)','(SUB)','(TNK)','(UMA)','(VAP)','(VOM)','(WZL)','(WIZ)','(WIW)','(ZIT)']
times_repeat = 0#how many times have we done this?
Path1=["data/","created/"]
for x in range (0,2):#start the path checking if the dirs exist
	if path.isdir(Path1[x]):
		pass#do nothing if the path exists
	else:
		os.mkdir(Path1[x])#make the paths if it doesnt

try:#watching for CTRL+C
	
	def Downloader(times_repeat):#this is where we will download the data 
		
		os.system('clear')#clean up and extra output
		print (Fore.YELLOW +"STARTING TO EXTRACT AND FORMAT THE DATA FROM ROCKSTAR PUBLIC SERVER STOCK EXCHANGE")
		print (Fore.RESET + Style.RESET_ALL)#call the colour reset
		print (Fore.GREEN + """                                                          
 000000000000000000000000000000000000000   
 000000000000000000000000000000000000000   
 00                   000111111111111 00   
 001011     111  1110 000000000111100 00   
 000  01 1001000110  00000  001101   000   
 00000 001 1111110 000000000 0000 100000   
    100 0  0  1101 000000000 0000 01       
      0100 1101101 000000000 000 00        
      10 001000  1      0 10000100         
       00 0    000000000101   0101         
      100  00 10 00  00  0 00   100        
     10   000 10 00  0000  00  0  00       
    10     0001  00   000  001 0   00      
    00     00   1000  00   00  0    01     
   101     0011            01000   100     
   000          100000000  0  00    001    
   100    11000111100110 00000     000     
    001  0000 001000110  01 0010  1101     
    101 0 110 0001000011000 00 110 00      
    10 0010 00 00100010101 000 101010      
    1011000000 00011010000 00 00 1000      
    1  00011010 011101001 0000100  101     
    1  100  100 001110110 001  100  0      
    100001    00 0111100000     10000      
     111      0010001111 01       11       
               10 00000010                 
                0010100 00                 
                10 0010 01                 
                 00 01 00                  
                 10 11 01                  
                  000000                   
                  100001                   
""")
		print (Fore.RESET + Style.RESET_ALL)
		print "\tDOWNLOADING STOCK INFO NOW";
	        log_file = open("data/stocks.data", 'w')#create the data file, this will override any previously saved stock data
	        try:
			downloaded_data  = urllib2.urlopen("http://socialclub.rockstargames.com/games/gtav/ajax/stockdetail")
			#download the data from the RS server
		except Exception as e:
			print e 
			print 'FILE BLOCKED NO LONGER ALLOWED -- EXITING'
			exit()	
		for line in downloaded_data.readlines():#write to the file
	        	print>> log_file, line#writing
		log_file.close()#close the file
	 	print "\tFile saved to data/stocks.data";
		PATHS = "created/info.csv";#check for previously formatted stock datat
		if path.exists(PATHS) and path.isfile(PATHS):
			Formatting(times_repeat);#send to the formatted if the stock csv file exists
		else:
			FileCreation(times_repeat);#otherwise lets go create the file 
		
	def FileCreation(times_repeat):#this is where we will creat the initial csv file if it doesnt exist

		print "\n\tCREATING THE FILE";
		fmatted_stock = open("created/info.csv", 'w')#create the info file 
        	fmatted_stock.write("Company Name"+",")#csv set first column 'company name'
		for z in xrange(0, len(stock_names)):#write the company names to csv. we use len(array_name) which allows for expansion of new stock names
			    fmatted_stock.write(stock_names[z].upper()+",")#include the , to change to the coloumn 
		fmatted_stock.close();#close the file
		Formatting(times_repeat);#send to formatting 

	def Formatting(times_repeat):
        	
		print "\n\tFORMATTING HAS STARTED"
		symbols_remove = []
		symbols = open("data/words", "r")
		for line in symbols:
			symbols_remove.append(line.strip('\n'))
		with open ("data/stocks.data", "r") as myfile:
			stock_data=myfile.read();
		x=0
		for x in xrange(0,len(symbols_remove)):
			stock_data=stock_data.replace(symbols_remove[x], " ")
		stock_data=stock_data.replace(',','')
		txt=stock_data
		format_date = datetime.datetime.now()
		fmatted_stock = open("created/info.csv", 'a')
		fmatted_stock.write('\n'+format_date.strftime("%d - %H:%M")+",")
		x=0
		money_ammount = []
		for x in xrange(0,len(stock_names)):
			re1='.*?'	# Non-greedy match on filler
			re2=stock_names[x]	# Word 1
			re3='.*?'	# Non-greedy match on filler
			re4='([+-]?\\d*\\.\\d+)(?![-+0-9\\.])'	# Float 1
			rg = re.compile(re1+re2+re3+re4,re.IGNORECASE|re.DOTALL)
			m = rg.search(txt)
			if m:
				word1=m.group(1)
				float1=m.group(2)
				fmatted_stock.write(float1+',')
				money_ammount.append(float1)
				#money_amount =[float(i) for i in float1]
		fmatted_stock.close();	
		print "\n\tFormatting finished file saved to info.csv"
		print "\n\tWaiting 45 minutes  before grabbing next set of stock info\n\tReturning to downloading";
		times_repeat=times_repeat+1
		print ("\n\tTHIS HAS BEEN COMPLETED A TOTAL OF: "+ Fore.RED + str(times_repeat) +" TIMES")
		print(Fore.RESET + Back.RESET + Style.RESET_ALL)
		#previously we would constantly download a new version of the stock market
		#and teh do a bit/bit compairson of the file and check if it was different
		#if it was different then it would append it to the csv file and start the 
		#proccess again. I feel that this wasn't a good idea as it would randomly
		#grab the newest version when ever R* udated it which could be at any time
		#of the day, so for data entry reasons we need this to be at a specific time.
		time.sleep(2700);
		Make_It_Rain(money_ammount, times_repeat);
		
	def Make_It_Rain(money_ammount, times_repeat):
		print float(money_ammount)
		Downloader(times_repeat)



	#define main function and its calls
        def main():
		#this will catch the system arguments into the args var
                args = sys.argv[1:]
 		#if no sys args are present it will display a useage msg
                if not args:
			print """
	    type -h to start the coding brahs
		the csv file is saved to created/info.csv
		the stock data from rockstar is saved to data/stock.data
				
	"""
                	sys.exit(1)
 
 		#send to the help function 
                if sys.argv[1].lower() == "-h":
			times_repeat=0
			Downloader(times_repeat);
#call the main function
	if __name__=='__main__':
		main()
except KeyboardInterrupt:
        sys.exit()
