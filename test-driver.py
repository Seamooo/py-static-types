import os

os.chdir('testing')
files = os.listdir(os.getcwd())
for test in files:
	exec(open(test).read())
