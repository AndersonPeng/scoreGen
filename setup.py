from cx_Freeze import setup, Executable

setup(name = 'Score Generator', 
	  version = '1.0', 
	  description = 'fft', 
	  executables = [Executable("main.py")])