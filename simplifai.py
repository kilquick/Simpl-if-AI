import os
import shutil
import hashlib
import time
import PySimpleGUI as sg

def create_file(path):
    with open(path, 'w') as f:
        pass

def create_folder(path):
    os.makedirs(path)

def delete_file(path):
    os.remove(path)

def delete_folder(path):
    shutil.rmtree(path)

def move_file(src, dst):
    shutil.move(src, dst)

def copy_file(src, dst):
    shutil.copy2(src, dst)

def rename_file(src, dst):
    os.rename(src, dst)

def search_file(directory, file_name):
    for root, dirs, files in os.walk(directory):
        if file_name in files:
            return os.path.join(root, file_name)
    return None

def find_duplicate_files(directory):
    files_seen = {}
    duplicate_files = []
    total_files = 0
    start_time = time.time()
    layout_popup = [[sg.Text('Scanning files...')],
                    [sg.Text('Time Elapsed: '), sg.Text('', key='time_elapsed')],
                    [sg.Text('File Progress: '), sg.Text('', key='file_progress')],
                    [sg.Text('ETA: '), sg.Text('', key='eta')],
                    [sg.ProgressBar(1000, key='progressbar')],
                    [sg.Text('Duplicates found: '), sg.Text('', key='duplicates')],
                    [sg.Text('Files Checked: '), sg.Text('', key='files_checked')],
                    [sg.Button('Cancel')]]
    popup = sg.Window('Scan Progress', layout_popup)
    try:
        for foldername, subfolders, filenames in os.walk(directory):
            for filename in filenames:
                total_files += 1
                file_path = os.path.join(foldername, filename)
                file_hash = hash_file(file_path)
                file_start_time = time.time()
                event, values = popup.read(timeout=10)
                if event == 'Cancel':
                    raise SystemExit
                if file_hash in files_seen:
                    files_seen[file_hash].append(file_path)
                    duplicate_files.append(file_path)
                else:
                    files_seen[file_hash] = [file_path]
                time_elapsed = round(time.time() - start_time, 2)
                file_time = round(time.time() - file_start_time, 2)
                eta = round((total_files / (time_elapsed/file_time)) - time_elapsed, 2)
                progress = round((total_files / (time_elapsed/file_time))/100, 2)
                popup['time_elapsed'].Update(time_elapsed)
                if file_time > 5:
                    popup['file_progress'].Update(file_time)
                popup['eta'].Update(eta)
                popup['progressbar'].UpdateBar(int(progress))
                popup['duplicates'].Update(len(duplicate_files))
                popup['files_checked'].Update(total_files)

    except SystemExit:
        pass
    finally:
        popup.Close()
    if duplicate_files:
        layout_result = [[sg.Text('Duplicate Files')],
                 [sg.Listbox(values=duplicate_files, size=(None, None), key='list')],
                 [sg.Button('Move'), sg.Button('Merge'), sg.Button('Delete'),sg.Button('Log')],
                 [sg.Button('Close')]]
        result_window = sg.Window('Results', layout_result, resizable=True)

        while True:
            event, values = result_window.Read()
            if event in (None, 'Close'):
                result_window.Close()
                break
            elif event == 'Move':
                # code to move the selected file
                pass
            elif event == 'Merge':
                # code to merge the selected file
                pass
            elif event == 'Delete':
                # code to delete the selected file
                pass
            elif event == 'Log':
                # code to log the activity
                pass


           


def hash_file(file_path):
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

    sha1 = hashlib.sha1()

    with open(file_path, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)

    return sha1.hexdigest()


layout = [[sg.Text('Please select a folder:')],
          [sg.Input(), sg.FolderBrowse()],
          [sg.Text('Please select a file:')],
          [sg.Input(), sg.FileBrowse()],
          [sg.Text('Please select a destination folder:')],
          [sg.Input(), sg.FolderBrowse()],
          [sg.Text('Please select a file name:')],
          [sg.Input()],
          [sg.Button('Create'), sg.Button('Delete'), sg.Button('Rename'), sg.Button('Move'), sg.Button('Copy'), sg.Button('Search'), sg.Button('Find duplicate files')]
         ]

window = sg.Window('File Manager', layout)

while True:
    event, values = window.read()
    if event in (None, 'Exit'):
        break
    if event == 'Create':
        if os.path.isfile(values[1]):
            create_file(values[1])
        elif os.path.isdir(values[1]):
            create_folder(values[1])
    elif event == 'Delete':
        if os.path.isfile(values[1]):
            delete_file(values[1])
        elif os.path.isdir(values[1]):
            delete_folder(values[1])
    elif event == 'Rename':
        rename_file(values[1], values[2])
    elif event == 'Move':
        move_file(values[1], values[2])
    elif event == 'Copy':
        copy_file(values[1], values[2])
    elif event == 'Search':
        result = search_file(values[0], values[3])
        if result:
            sg.popup(f'File found at: {result}')
        else:
            sg.popup('File not found')
    elif event == 'Find duplicate files':
        duplicate_files = find_duplicate_files(values[0])
        if duplicate_files:
            sg.popup(f'Duplicate files: {duplicate_files}')
        else:
            sg.popup('No duplicate files found')

window.close()
