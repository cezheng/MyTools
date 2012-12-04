#!/usr/bin/python

# 12/05/2012 - v0.1 
# By Ce Zheng
# Only support Linux since it relies badly on bash. Windows support will be considered lately.

# configurables
PATH = '/home/adamzheng/Software/goagent/goagent' # please change it to your GoAgent directory
REFRESH_INTERVAL = 1000 #ms, time interval between each time the GUI refreshes its status label

# non-configurables
__version__ = 'v0.1'
TITLE = '  GoAgent GUI Starter  '
AUTHOR = 'Ce Zheng'
EMAIL = 'cezheng.cs@gmail.com'
SUFFIX = '/local/proxy.py'
RUNNING = "GoAgent Status:  Running"
STOPPED = "GoAgent Status:  Stopped"

def startGoAgent():
        return os.system("python "+PATH+SUFFIX+'&')

def stopGoAgent():
        return os.system("ps -ef | grep proxy.py | grep -v grep | awk '{print $2}' | xargs kill -9")

def checkRunning():
        return [s.split() for s in commands.getstatusoutput("ps -ef | grep proxy.py | grep -v grep")[1].split('\n') if s!= '']

class GUI(object):
        def __init__(self,error=False,**kw):
                if error: self.error_init(**kw)
                else: self.normal_init()
        def normal_init(self):
                self.root = tk.Tk()
                self.root.title(TITLE)
                self.frame = tk.Frame(self.root, relief=RIDGE, borderwidth = 2)
                self.frame.pack(fill = BOTH,expand = 1)
                self.titleLabel = tk.Label(self.frame, text = TITLE, font = ("Helvetica", 20)) 
                self.titleLabel.pack(fill = X, expand = 1)
                self.authorLabel = tk.Label(self.frame, text = 'By ' + AUTHOR + ' - ' + EMAIL + '\n', font = ("Helvetica", 11)) 
                self.authorLabel.pack(fill = X, expand = 1)
                self.statusLabel = tk.Label(self.frame, text = RUNNING, font = ("Helvetica",14))
                self.statusLabel.after(REFRESH_INTERVAL,func = lambda: self.refresh())
                self.statusLabel.pack(fill = X, expand = 1)
                self.button1 = tk.Button(self.frame,text = "Start",command = lambda: self.startClick())
                self.button1.pack()
                self.button2 = tk.Button(self.frame,text = "Stop",command = lambda: self.stopClick())
                self.button2.pack()
        def error_init(self,errmsg,**kw):
                self.root = tk.Tk()
                self.root.title("Error")
                self.msgLabel = tk.Label(self.root,text = errmsg)
                self.msgLabel.pack(fill = X, expand = 1)
                self.button = tk.Button(self.root,text = "OK",command = self.root.destroy)
                self.button.pack()

        def mainloop(self):
                self.root.mainloop()
        def startClick(self):
                if not checkRunning():startGoAgent()
                if checkRunning():self.statusLabel.config(text = RUNNING)
                else:self.statusLabel.config(text = STOPPED)
                self.statusLabel.update_idletasks()
        
        def stopClick(self):
                if checkRunning():
                        stopGoAgent()
                        if not checkRunning():
                                self.statusLabel.config(text = STOPPED)
                                self.statusLabel.update_idletasks()
        
        def refresh(self):
                if checkRunning():self.statusLabel.config(text = RUNNING)
                else: self.statusLabel.config(text = STOPPED)
                self.statusLabel.update_idletasks()
                self.statusLabel.after(REFRESH_INTERVAL,func = lambda: self.refresh())


 
if __name__=='__main__':
        ENABLE_GUI = True
        # check if packages required by GUI are installed
        try:
                import os,sys,commands
                import Tkinter as tk
                from Tkconstants import *
        except:
                print "require Python module Tkinter for GUI."
                ENABLE_GUI = False
        # check if PATH is properly configured 
        if not os.path.isfile(PATH + SUFFIX):
                errmsg = PATH + SUFFIX + " does not exist. Please configure your PATH correctly."
                print errmsg
                if ENABLE_GUI:
                        window=GUI(error = True,errmsg = errmsg)
                        window.mainloop()
                exit(0)
        # check what kinda action is to performed and do it
        if len(sys.argv)==1:
                print "Trying to starting GoAgent."
                if not checkRunning():
                        startGoAgent()
                        if checkRunning(): print "GoAgent started."
                        else: print "GoAgent Failed to start."
                else:
                        print "GoAgent started"
        elif sys.argv[1]=='stop':
                print "Trying to stop GoAgent."
                if checkRunning():
                        stopGoAgent()
                        if checkRunning(): print "GoAgent Failed to stop."
                        else: print "GoAgent stopped."
                else:
                        print "GoAgent stopped."
                        exit(0)
        else:
                print "Unknown action. No action performed."
                exit(0)
        # if GUI is enabled, run it
        if ENABLE_GUI:
                window=GUI()
                window.refresh()
                window.mainloop()
