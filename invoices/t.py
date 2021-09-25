# import os
# # os.system(path)
# import subprocess

# path = '1060.pdf'
# # path = 'my_file.pdf'
# subprocess.Popen([path], shell=True)
# import webbrowser
# path = '1060.pdf'
# webbrowser.open_new(path)
import subprocess
import os

#to get the current working directory
directory = os.getcwd()

print(directory)
path = f'{directory}\\invoices\\1060.pdf'
print(path)
os.system(path)
# subprocess.Popen([path], shell=True)