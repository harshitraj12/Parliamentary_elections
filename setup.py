import cx_Freeze
import sys
import os 
base = None

if sys.platform == 'win32':
    base = "Win32GUI"

os.environ['TCL_LIBRARY'] = r"C:\Users\HARSHIT RAJ\AppData\Local\Programs\Python\Python37\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Users\HARSHIT RAJ\AppData\Local\Programs\Python\Python37\tcl\tk8.6"

executables = [cx_Freeze.Executable("Parliamentary Elections(GUI and Graphs).py", base=base)]


cx_Freeze.setup(
    name = "Parliamentary Election (Harshit Raj)",
    options = {"build_exe": {"packages":["tkinter","os"], "include_files":['tcl86t.dll','tk86t.dll', 'GE_india_2019_results.csv','LS2009Candidate.csv','LS2014Candidate.csv']}},
    version = "0.01",
    description = "Tkinter Application",
    executables = executables
    )