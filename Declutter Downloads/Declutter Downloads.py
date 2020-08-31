import os
import shutil

downloads_path = '/Users/joshualee/Downloads'
directory_list = ['/Images', '/Excel', '/PSD', '/DMG']

for directory in directory_list:
    if not os.path.isdir(downloads_path + directory):
        os.mkdir(downloads_path + directory)

file_names = os.listdir(downloads_path)
for file in file_names:
    path_of_file = os.path.join(downloads_path,file)
    file_extension = os.path.splitext(file)[1]

    if file_extension == '.jpeg' or file_extension == '.jpg' or file_extension == '.png' or file_extension == '.gif':
        shutil.move(path_of_file,downloads_path+directory_list[0])
    elif file_extension == '.csv' or file_extension == '.xls' or file_extension == '.xlsx':
        shutil.move(path_of_file,downloads_path+directory_list[1])
    elif file_extension == '.psd':
        shutil.move(path_of_file,downloads_path+directory_list[2])
    elif file_extension == '.dmg':
        shutil.move(path_of_file,downloads_path+directory_list[3])
   
# Add a function to move everything out of folder