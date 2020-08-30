import os
import shutil

trash_location = '/Users/user_name/.Trash'
# listdir gives names of all files in trash can
files_in_trash = os.listdir(trash_location)

def notify(title, text):
    os.system("""osascript -e 'display notification "{}" with title "{}"'""".format(text, title))

for file in files_in_trash:
    # Joining trash path directory with each document file
    path_of_files_in_trash = os.path.join(trash_location, file)
    try:
        if os.path.isfile(path_of_files_in_trash):
            os.remove(path_of_files_in_trash)
        elif os.path.isdir(path_of_files_in_trash):
            shutil.rmtree(path_of_files_in_trash,True)
    except Exception as e:
        print(e)

notify("Trash", "Successfully Emptied")