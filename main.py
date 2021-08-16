#!/usr/bin/env python3
import app_logger
import xml.etree.ElementTree as ET
import os
import shutil
from tqdm import tqdm
from pathlib import Path
logger = app_logger.get_logger(__name__)

def main():    
    try:
        tree = ET.parse("config_file.xml")
        root = tree.getroot()

        for current_file in tqdm(root):
            source_path = current_file.get("source_path")
            source_path = os.path.abspath(source_path.replace("\\", "/"))
            destination_path = current_file.get("destination_path")
            destination_path = os.path.abspath(destination_path.replace("\\", "/"))
            file_name = current_file.get("file_name")

            source_file_path = os.path.join(source_path, file_name)
            destination_file_path = os.path.join(destination_path, file_name)
            try:
                valid_open = open(source_file_path , mode="r")
                valid_open.close()

            except FileNotFoundError:
                logger.warning(f"Can not find the file {file_name}.")
                continue
                
            if not os.path.exists(destination_file_path):
                try:
                    shutil.copy(source_file_path, destination_file_path)
                    logger.info(f"File {file_name} copied successfully.")
                    
                except shutil.SameFileError:
                    logger.warning(f"Source and destination represents the same file {file_name}")

                except IOError:
                    logger.warning(f"File {file_name} is not read.")
                    
                except PermissionError:
                    logger.warning(f"{file_name} Permission denied.")
                     
                except Exception as e:
                    logger.warning(f"Error {e} occurred while copying file {file_name}")
                    
            else:
                try:
                    command = input('The file already exists at the you want to overwrite the package at destination? Y/R(Rename): ')
                    if command == "Y":
                        os.remove(destination_file_path)
                        shutil.copy(source_file_path, destination_file_path)
                        logger.info(f"File {file_name} overwritten.")
                    
                    if command == "R":
                        file_suffix = Path(destination_file_path).suffix
                        new_file_name = input('Enter a new filename: ')
                        new_file_name = os.path.join(destination_path, new_file_name + file_suffix)
                        while os.path.exists(new_file_name):
                            new_file_name = input('A file with the same name already exists in the folder. Please enter a different filename: ')
                            new_file_name = os.path.join(destination_path, new_file_name + file_suffix)
                        shutil.copy(source_file_path, new_file_name)
                        logger.info(f"File {new_file_name} copied successfully.") 
                except Exception as e:
                    logger.warning(f"Error {e} occurred while copying file {file_name}")

    except FileNotFoundError:
        logger.warning("Can not find the config")

if "__main__" == __name__:
    main()
