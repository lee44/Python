import os
import shutil

downloads_path = 'C:/Users/Lee/Downloads'
directory_list = ['/IMAGES', '/EXCEL', '/PSD', '/APPLICATIONS', '/PDF', '/WORD DOCUMENTS']

for directory in directory_list:
    if not os.path.isdir(downloads_path + directory):
        os.mkdir(downloads_path + directory)

file_names = os.listdir(downloads_path)

# Moves everything into folders specified in directory_list
def Categorize():
    for file in file_names:
        old_file_path = os.path.join(downloads_path,file)
        file_name_no_extension = os.path.splitext(file)[0]
        file_extension = os.path.splitext(file)[1]

        if file_extension == '.jpeg' or file_extension == '.jpg' or file_extension == '.JPG' or file_extension == '.png' or file_extension == '.PNG' or file_extension == '.gif':
            try:
                shutil.move(old_file_path,downloads_path+directory_list[0])
            except shutil.Error:
                new_file_path = os.path.join(downloads_path,file_name_no_extension+'_new'+file_extension)
                os.rename(old_file_path,new_file_path)
                shutil.move(new_file_path,downloads_path+directory_list[0])
        elif file_extension == '.csv' or file_extension == '.xls' or file_extension == '.xlsx':
            try:
                shutil.move(old_file_path,downloads_path+directory_list[1])
            except shutil.Error:
                new_file_path = os.path.join(downloads_path,file_name_no_extension+'_new'+file_extension)
                os.rename(old_file_path,new_file_path)
                shutil.move(new_file_path,downloads_path+directory_list[1])
        elif file_extension == '.psd':
            try:
                shutil.move(old_file_path,downloads_path+directory_list[2])
            except shutil.Error:
                new_file_path = os.path.join(downloads_path,file_name_no_extension+'_new'+file_extension)
                os.rename(old_file_path,new_file_path)
                shutil.move(new_file_path,downloads_path+directory_list[2])
        elif file_extension == '.exe':
            try:
                shutil.move(old_file_path,downloads_path+directory_list[3])
            except shutil.Error:
                new_file_path = os.path.join(downloads_path,file_name_no_extension+'_new'+file_extension)
                os.rename(old_file_path,new_file_path)
                shutil.move(new_file_path,downloads_path+directory_list[3])
        elif file_extension == '.pdf':
            try:
                shutil.move(old_file_path,downloads_path+directory_list[4])
            except shutil.Error:
                new_file_path = os.path.join(downloads_path,file_name_no_extension+'_new'+file_extension)
                os.rename(old_file_path,new_file_path)
                shutil.move(new_file_path,downloads_path+directory_list[4])
        elif file_extension == '.docx':
            try:
                shutil.move(old_file_path,downloads_path+directory_list[5])
            except shutil.Error:
                new_file_path = os.path.join(downloads_path,file_name_no_extension+'_new'+file_extension)
                os.rename(old_file_path,new_file_path)
                shutil.move(new_file_path,downloads_path+directory_list[5])

# Moves everything out of folders specified in directory_list
def deCategorize():
    for directory in directory_list:
        directory_path = downloads_path+directory
        for file in os.listdir(directory_path):
            try:
                shutil.move(os.path.join(directory_path,file),downloads_path)
            except shutil.Error:
                file_name = os.path.splitext(file)
                old_file_name = os.path.join(directory_path,file)
                # file_name[0] is name of file without extension
                # file_name[1] is the extension e.g .pdf or .csv
                new_file_name = os.path.join(directory_path,file_name[0]+'_old'+file_name[1])
                os.rename(old_file_name,new_file_name)
                shutil.move(new_file_name,downloads_path)

# deCategorize()
Categorize()