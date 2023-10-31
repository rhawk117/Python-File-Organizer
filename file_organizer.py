import sys  # To cleanly exit the program
import os # To work with files
import shutil # To move files
from pathlib import Path # Working with files
import logging, traceback # For Debugging purposes
import re as regex # For parsing file extensions / input



def CombDownloads(extension: str) -> list:
    downloadFolder = os.path.join(Path.home(),'Desktop' ,'Downloads')
    filesFound = []
    logging.info('Checking if the Download Folder exists.. ')
    if Path(downloadFolder).exists():
        logging.info('Found Download Folder changing directory...')
        try:
            os.chdir(downloadFolder)
            logging.info('Walking through downloads')
            for _, __, files in os.walk(downloadFolder):
                for file in files:
                  if regex.search(rf'{extension}', file):
                    print('\t' + extension[1:].upper() + f' File Found -> {file}')
                    filesFound.append(file)  
            return filesFound
        except Exception as error:
            print('Unknown error occured check log below for more information')
            logging.error(f'Exception raised -> ({error})\n {traceback.format_exc()}')

def CheckFileExtension(extension: str, dlFolder) -> bool:
    extCheck = regex.escape(extension) + '$'
    for _, __, files in os.walk(dlFolder):
        for file in files:
            if regex.search(extCheck, file):
                logging.info('Found at least one file with the same extension ending loop')
                return True
    logging.critical('! The file extension was not found in any of the files in the Download folder')
    return False
            

def GetFileType(dlFolderPath) -> str:
    extension = ''
    while True:
        extension = input('What is the file(s) extension: ')
        if regex.search(r'\.\w+', extension):
            logging.info('Checking Download Directory for {0} files', extension)
            dlFolder = os.path.join(Path.home() , 'Desktop' , 'Downloads')
            if CheckFileExtension(extension, dlFolderPath):
                logging.info('Successfully recieved user input')
                break
            else:
                print('No files with the {0} extension were found try again')
                continue
        else:
            logging.info('>> User Input failed retrying..')
            print('File extension invalid, try again')
    return extension

def CheckType(class_choice,type) -> str:
    if type == 'Lecture':
        if class_choice == 'Scripting and Automation (AIST-2120)':
            return 'Briefing slides'
        if class_choice == 'CYBER-2600':
            return 'Lecture Slides'
    elif type == 'Lab':
        return 'Labs'
    else:
        return type

def MoveFiles(file: str, dlPath, destination):
    try:
        logging.info(f'Trying to move {file} at {os.path.join(dlPath, file)} to {destination}')
        shutil.move(os.path.join(dlPath, file), destination)
        logging.info(f'Successfully moved {file} to {destination}')
    except FileNotFoundError as error:
        logging.critical('! File Path didn\'t exist')
        raise error('File wasn\'t found')
    except PermissionError as error:
        logging.critical('! Permission Error ')
        raise error('You don\'t have the file permissions to perform this task')


def ValidInput(options: list, prompt:str) -> str:
    choice = input(prompt)
    while choice not in options:
        logging.info('>> User Input failed retrying..')
        print('Input one of the following -> ' + ', '.join(options))
        choice = input(prompt)
    logging.info('>> Sucessfully recieved user input returning to main..')
    return choice
    
def main():
    logging.basicConfig(
        level=logging.DEBUG, format=' %(asctime)s – %(levelname)s -%(message)s'
        )
    logging.debug('Starting program...')
    while True:
        downloadFolder = os.path.join(Path.home() , 'Desktop' , 'Downloads')
        destination = os.path.join(Path.home(), 'Desktop', 'School', 'Fall23')
        classes = ['CSCI-1302', 'CSCI-2700', 
                   'Scripting and Automation (AIST-2120)', 'CYBER-2600']
        classChoice = ValidInput(classes, 'What class is this file from: ')
        destination = os.path.join(destination, classChoice)
        extension = GetFileType(downloadFolder)
        file_set = CombDownloads(extension)
        file = ValidInput(file_set, 'Which file would you like to move (type the file name):')
        fileType = ValidInput(['Lab', 'Homework', 'Lecture'], 'What type of file for the class is it: ')
        sub_folder = CheckType(classChoice, fileType)
        destination = os.path.join(destination, sub_folder)
        MoveFiles(file, downloadFolder, destination)
        yes_or_no = ValidInput(['y', 'n'], 'Would you like to open another file (y/n): ')
        if yes_or_no == 'y':
            input('Press any key to restart the program: ')
            continue
        else:
            break
    input('Press any key to quit the program: ')
    sys.exit()
    
if __name__ == '__main__':
    main()
