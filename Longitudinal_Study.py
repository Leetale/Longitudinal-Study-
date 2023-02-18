# program to find files and arrange them into a folder

import csv
import xml.etree.ElementTree as ET
from _datetime import timedelta
from time import strptime
import pathlib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import shutil
import math
import vg
import io
from datetime import datetime
from pathlib import Path
import time

from pandas import read_csv
import csv
import difflib
import os.path

from io import StringIO
import xml.etree.ElementTree as ET
from _datetime import timedelta
from time import strptime
import pathlib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import shutil
import math
import vg
import io
from datetime import datetime
from distutils.dir_util import copy_tree
import sys
from tkinter import filedialog
from cdifflib import CSequenceMatcher
from tkinter import *
from tkinter import filedialog

#Create an instance of Tkinter frame
win= Tk()
#Define the geometry
win.geometry('750x250')

#Create a label and a Button to Open the dialog
Label(win, text="Select Parent Directory", font=('Aerial 18 bold')).pack(pady=20)


path = filedialog.askdirectory(title="Select a File")

Label(win, text=path, font=13).pack()
win.destroy()

# Asks user to select foldr to copy files to
print('please choose directory to copy files to')
# Create an instance of Tkinter frame
win = Tk()
top = Toplevel()

win.geometry('750x250')

# Define the geometry

# Create a label and a Button to Open the dialog
Label(win, text="Select Directory to Copy Files", font=('Aerial 18 bold')).pack(pady=20)

path_new = filedialog.askdirectory()

Label(win, text=path, font=13).pack()
win.destroy()

# Asks user to select folder to save results to
print('please choose directory to save results')
# Define the geometry
win = Tk()
top = Toplevel()

win.geometry('750x250')


# Create a label and a Button to Open the dialog
Label(win, text="Select Directory to Save Results", font=('Aerial 18 bold')).pack(pady=20)

path_data = filedialog.askdirectory()

Label(win, text=path, font=13).pack()
win.destroy()
win.mainloop()
# path_data = "C:\\Users\\leetal\\Desktop\\Zohar results"

# shutil.rmtree(r'C:\Users\leetal\Documents\Test Data')
# os.makedirs(r'C:\Users\leetal\Documents\Test Data')

difflib.SequenceMatcher = CSequenceMatcher


def distance(x1, y1, z1, x2, y2, z2):
    d = 0.0
    d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
    return d


def vector(x1, x2):
    v = 0.0
    v = x2 - x1
    return v


def percentage_change(col1, col2):
    return (((col2 - col1) / col1) * 100)


# Get the folder path in which all patient folders reside

# In the chosen folder create a list of all subfolders (each patient will have RIGHT and LEFT subfolders)
all_files = os.listdir(path)

folder_count = len(all_files)
# creates empty arrays for paths to be generated later
path1 = []
path2 = []
path3 = []
path4 = []
paths = {}
group_ = {}
a_dates = []
# Looks at Simfini output files copies export folder and organizes them in a new path
os.chdir(path)
for Simfini_output in all_files:
    if Simfini_output.endswith('RIGHT') or Simfini_output.endswith(
            'LEFT'):  # find files that end with right our left from SimfiniUniverse
        file_path = path + '\\' + Simfini_output  # identify the specific path where the folder we are looking at is currently
        file_type_part_name_by_ = Simfini_output.split('_')  # split file name to parts
        file_type = file_type_part_name_by_[ 0]  # take first part of split file name which is the patient ID written as "P#"
        # file_type = file_type[1:] #Remove the P from the "P#" and you are left with the patient ID #
        folder_name = 'Patient' + ' ' + file_type  # estbalish a folder name for each patient called "Patient ID"
        new_path = path_new + '\\' + folder_name  # a new path to the folder created above
        folder_in_folder = new_path + '\\' + Simfini_output  # establish a path where the folder will be located after being copied
        export = file_path + '\\' + "export"
         # within this folder establish a path just for the export folder
        if not os.path.exists(new_path):  # if new folder path based on Patient ID doest exist create it
            os.makedirs(new_path)
            if not os.path.exists(
                    folder_in_folder):  # if folder obtaining patient run and assosciated femur doesnt exist create it
                os.makedirs(folder_in_folder)
                copy_tree(export,
                          folder_in_folder)  # copy just the export file into the folder we just created in the new path's location

            else:
                copy_tree(export,
                          folder_in_folder)  # if folder exists just copy the export folder information into the proper folder

        else:
            copy_tree(export,
                      folder_in_folder)  # if the folder for that patient ID does exsit, copy the export file of the patient & femur speficic folder to the patient ID folder

all_files_new = os.listdir(path_new)  # provides a list of all the patient specific folders created
print(len(all_files_new))  # gives you the total number of patients we are looking at by counting the number of patient speficic folders created
os.chdir(path_new)  # change directory to path where all the patient specific export items were copied

for i in range(0, len(all_files_new), 1):  # go through all folders in new path starting at the frist one and looping one by one
    folder_path = path_new + '\\' + all_files_new[i]  # create a folder path based on the ith iteration this will give each Patient ID file
    print(folder_path)  # prints out each patient ID file
    if os.path.exists(folder_path):  # check if this path exists
        all_folders = os.listdir(folder_path)  # and list all the items in this folder
        n = len(all_folders)
        for j in range(0, n, 1):  # loop though all runs in patient specific folder skipping the fist one and counting by 2 this is done to only look at the right femur results as the left and right data are saved there
            path3 = folder_path + '\\' + all_folders[j]  # create a path to the patient, femur, and run specific folder
            os.chdir(path3)  # change path to the folder path idenfitied above
            index = folder_path.rsplit('\\', 1)[-1]  # get the ID of the patient by splitting the folder path and looking just at the folder name
            index = index[8:]  # take out the ID that is written after the word Patient
            Id = pd.read_csv(StringIO(index), header=None)
            for root, dirs, files in os.walk(path3):  # walk through new directory to get and arrange dates of each CT scan for each patient
                tree = ET.parse('seriesProperties.xml')  # find this file
                root = tree.getroot()
                StudyDate = []  # create empty array
                for studyDate in root.iter('StudyDate'):  # within this file look for the line called "Study Date" which is the date the CT scan was taken
                    StudyDate.append(studyDate.text)  # append array with the text of studydate found
                    StudyDate_1st = pd.DataFrame(list(StudyDate))  # create a dataframe listing the study dates

                    date = StudyDate_1st.to_string(columns=None, header=False,
                                                   index=False)  # append these dates to a string
                    date = datetime.strptime(date, '%Y%m%d')  # append string to date and time
                    date = datetime.date(date)  # from date and time take out just the date
                    date = date.strftime('%Y%m%d')
                    a_dates.append([index, path3, date])  # create and append array with patient path, the date of the study, and the patient ID
                break



a_dates = pd.DataFrame(a_dates, columns=['id', 'path', 'date'])  # create dataframe from array
a_dates.sort_values(by=['id', 'date'], inplace=True)  # sort the dataframe by patient ID and by the Date
a_dates = a_dates.groupby('id')  # split the dataframe into groups based on patient ID
# now there are grouped dataframes based on patient ID that are organzied based on date of the CT scan
# right femur analysis
for name, group in a_dates:  # look at each grouped dataframe
    group = group.reset_index()

    path1 = group['path'][0]  # take the frist path in the dataframe and make it the first path which all other paths will be compared to
    print('path1')
    print(path1)
    os.chdir(path1)  # change path to path1 identified
    Id = group['id'][0]
    Id = pd.read_csv(StringIO(Id), header=None)
    tree = ET.parse('.\seriesProperties.xml')  # go into this file to extract the slope, patient ID, weight, and age
    root = tree.getroot()
    usedSlope = []

    for slope in root.iter('UsedSegmentationSlope'):  #extract the slope data
        usedSlope.append(slope.text)
        slope1 = pd.DataFrame(list(usedSlope), columns=['Slope'])

    root = tree.getroot() #extract the patient ID
    PatientID = []
    for Patient_ID in root.iter('PatientId'):
        PatientID.append(Patient_ID.text)
        PatientID = pd.DataFrame(list(PatientID), columns=['Patient ID'])

    root = tree.getroot() #extract the study date
    StudyDate = []
    for studyDate in root.iter('StudyDate'):
        StudyDate.append(studyDate.text)
        StudyDate_1st = pd.DataFrame(list(StudyDate))

        date = StudyDate_1st.to_string(columns=None, header=False, index=False)
        date_1 = datetime.strptime(date, '%Y%m%d')

    Weight = [] #extract patient weight from first run
    for weight in root.iter('PatientWeight'):
        Weight.append(weight.text)
        Weight = pd.DataFrame(list(Weight), columns=['Weight'])
    Age = [] #extract patient age from first run
    for age in root.iter('PatientAge'):
        Age.append(age.text)
        Age = pd.DataFrame(list(Age), columns=['Age'])

    frames_Patient = [Id, Age, Weight]  # combibe ID, age, and weight to greate a dataframe
    df_Patient = pd.concat(frames_Patient, axis=1)
    df_Patient = pd.DataFrame(df_Patient)

    # read the csv file called stance summary and extract the following columns
    Stance_data1 = pd.read_csv('.\Stance summary table.csv',
                               usecols=['fieldName', 'siteName', 'rightValue', 'leftValue', 'highVsLowRatio',
                                        'highVsLowRisk', 'rightVsLeftRisk', 'leftVsRightRisk',
                                        'strainFoldRight', 'strainFoldLeft', 'strainFoldRightRisk',
                                        'strainFoldLeftRisk', 'BWMFRight', 'BWMFLeft', 'BWMFRiskScoreRight',
                                        'BWMFRiskScoreLeft', 'equivalentRiskRight', 'equivalentRiskLeft'])
    # read the anatomicproteries text to obtain the anatomical properties of the femur
    Anatomicprop_1 = pd.read_csv('.\AnatomicProperties.txt',
                                 names=['x', 'y', 'z'],
                                 skiprows=[0, 1, 2, 3, 15, 16])

    HC_1 = pd.DataFrame(Anatomicprop_1.iloc[
                            0])  # extract the x,y,z coordinates from the dataframe and convert the string to a numeric for the head center
    x1_HC = pd.DataFrame(HC_1.iloc[0])
    x1_HC = x1_HC['x'].str[15:32]
    x1_HC = pd.to_numeric(x1_HC, errors='coerce')

    y1_HC = HC_1.iloc[1]
    y1_HC = pd.to_numeric(y1_HC, errors='coerce')
    z1_HC = pd.DataFrame(HC_1.iloc[2])
    z1_HC = z1_HC['z'].str[0:6]
    z1_HC = pd.to_numeric(z1_HC, errors='coerce')
    frame = (x1_HC, y1_HC, z1_HC)
    HC_1 = pd.concat(frame, axis=1)  # create a dataframe for the x,y,z data

    # extract the x,y,z coordinates from the dataframe and convert the string to a numeric for the innercondylar notch
    IC_1 = pd.DataFrame(Anatomicprop_1.iloc[4])
    x1_IC = pd.DataFrame(IC_1.iloc[0])
    x1_IC = x1_IC['x'].str[16:33]
    x1_IC = pd.to_numeric(x1_IC, errors='coerce')
    y1_IC = IC_1.iloc[1]
    y1_IC = pd.to_numeric(y1_IC, errors='coerce')
    z1_IC = pd.DataFrame(IC_1.iloc[2])
    z1_IC = z1_IC['z'].str[0:18]
    z1_IC = pd.to_numeric(z1_IC, errors='coerce')
    frame = (x1_IC, y1_IC, z1_IC)
    IC_1 = pd.concat(frame, axis=1)  # create a dataframe for the x,y,z data
    # attaining volume data from the anatomical properties data, locate the voxel and mesh volume, and convert the string into a numeric
    vox_vol_1 = pd.DataFrame(Anatomicprop_1.iloc[7])
    vox_vol_1 = pd.DataFrame(vox_vol_1.iloc[0])
    vox_vol_1 = vox_vol_1['x'].str[15:24]
    vox_vol_1 = pd.to_numeric(vox_vol_1, errors='coerce')
    vox_vol_1 = vox_vol_1.reset_index(drop=True)

    mesh_vol_1 = pd.DataFrame(Anatomicprop_1.iloc[6])
    mesh_vol_1 = pd.DataFrame(mesh_vol_1.iloc[0])

    mesh_vol_1 = mesh_vol_1['x'].str[14:32]
    mesh_vol_1 = pd.to_numeric(mesh_vol_1, errors='coerce')
    mesh_vol_1 = mesh_vol_1.reset_index(drop=True)

    frame_vol = (vox_vol_1, mesh_vol_1)
    Vol_1 = pd.concat(frame_vol, axis=1)  # create a dataframe from the voxel and mesh volumes
    Vol_1.columns = ['Voxel Volume', 'Mesh Volume']

    for i in range(1, len(group), 1):  # loop through the patient specific group skipping the first item which was already labled as path 1
        path2 = group['path'][i]  # for each consecutive path loop though as path2
        print('path2')
        print(path2)
        os.chdir(path2)  # change path to path2 identified
        for root, dirs, files in os.walk(path2):
            # read the csv file called stance summary and extract the following columns
            Stance_data2 = pd.read_csv('.\Stance summary table.csv',
                                       usecols=['rightValue', 'leftValue', 'highVsLowRatio',
                                                'highVsLowRisk', 'rightVsLeftRisk', 'leftVsRightRisk',
                                                'strainFoldRight', 'strainFoldLeft', 'strainFoldRightRisk',
                                                'strainFoldLeftRisk', 'BWMFRight', 'BWMFLeft', 'BWMFRiskScoreRight',
                                                'BWMFRiskScoreLeft', 'equivalentRiskRight', 'equivalentRiskLeft'])
            # read the anatomicproteries text to obtain the anatomical properties of the right femur
            Anatomicprop_2 = pd.read_csv('.\AnatomicProperties.txt',
                                         names=['x', 'y', 'z'],
                                         skiprows=[0, 1, 2, 3, 15, 16])

            tree = ET.parse('.\seriesProperties.xml')  # obtain the slope used
            root = tree.getroot()
            usedSlope = []

            for slope in root.iter('UsedSegmentationSlope'): #obtain slope from second run
                usedSlope.append(slope.text)
            slope2 = pd.DataFrame(list(usedSlope),
                                  columns=['Slope'])
            StudyDate = [] #obtain study date from second run
            for studyDate in root.iter('StudyDate'):
                StudyDate.append(studyDate.text)
                StudyDate_1st = pd.DataFrame(list(StudyDate))

                date = StudyDate_1st.to_string(columns=None, header=False, index=False)
                date_2 = datetime.strptime(date, '%Y%m%d')
            break
        # Calc time in months between studies
        num_months = (date_2.year - date_1.year) * 12 + (date_2.month - date_1.month)
        num_months = float(num_months)
        df_num_months = pd.Series(num_months) #express the amount of time passed as a series

        # calculating distance
        HC_2 = pd.DataFrame(Anatomicprop_2.iloc[
                                0])  # extract the x,y,z coordinates from the dataframe and convert the string to a numeric for the head center
        x2_HC = pd.DataFrame(HC_2.iloc[0])
        x2_HC = x2_HC['x'].str[15:32]
        x2_HC = pd.to_numeric(x2_HC, errors='coerce')

        y2_HC = HC_2.iloc[1]
        y2_HC = pd.to_numeric(y2_HC, errors='coerce')
        z2_HC = pd.DataFrame(HC_2.iloc[2])
        z2_HC = z2_HC['z'].str[0:6]
        z2_HC = pd.to_numeric(z2_HC, errors='coerce')
        frame = (x2_HC, y2_HC, z2_HC)
        HC_2 = pd.concat(frame, axis=1)  # create a dataframe for the x,y,z data

        IC_2 = pd.DataFrame(Anatomicprop_2.iloc[
                                4])  # extract the x,y,z coordinates from the dataframe and convert the string to a numeric for the innercondylar notch
        x2_IC = pd.DataFrame(IC_2.iloc[0])
        x2_IC = x2_IC['x'].str[16:33]
        x2_IC = pd.to_numeric(x2_IC, errors='coerce')
        y2_IC = IC_2.iloc[1]
        y2_IC = pd.to_numeric(y2_IC, errors='coerce')
        z2_IC = pd.DataFrame(IC_2.iloc[2])
        z2_IC = z2_IC['z'].str[0:18]
        z2_IC = pd.to_numeric(z2_IC, errors='coerce')
        frame = (x2_IC, y2_IC, z2_IC)
        IC_2 = pd.concat(frame, axis=1)  # create a dataframe for the x,y,z data

        # establish dataframes for the head center for path1 and path 2 and resetting the index to be used when calculating distance between the two paths
        HC_1 = pd.DataFrame(HC_1)
        HC_1 = HC_1.reset_index(drop=True)
        IC_1 = pd.DataFrame(IC_1)
        IC_1 = IC_1.reset_index(drop=True)

        HC_2 = pd.DataFrame(HC_2)
        HC_2 = HC_2.reset_index(drop=True)
        IC_2 = pd.DataFrame(IC_2)
        IC_2 = IC_2.reset_index(drop=True)
        # calculating the difference in distance between anatomical properties
        frame = [Id, HC_1, IC_1, HC_2, IC_2]
        dis = pd.concat(frame,
                        axis=1)  # create a dataframe for the patient ID the head center and intercondylar notch coordinates for the first and second run
        dis.columns = ['Patient ID', 'HC_x 1', 'HC_y 1', 'HC_z 1', 'IC_x 1', 'IC_y 1', 'IC_z 1',
                       'HC_x 2', 'HC_y 2', 'HC_z 2', 'IC_x 2', 'IC_y 2', 'IC_z 2']
        # calculate the distance between the head center coordinates of the first run and the head center coordinates of the second run
        dis['HC'] = distance(dis['HC_x 1'], dis['HC_y 1'], dis['HC_z 1'], dis['HC_x 2'], dis['HC_y 2'],
                             dis['HC_z 2'])

        # calculate the distance between the inner condylar notch coordinates of the first run and the head center coordinates of the second run
        dis['IC'] = distance(dis['IC_x 1'], dis['IC_y 1'], dis['IC_z 1'], dis['IC_x 2'], dis['IC_y 2'],
                             dis['IC_z 2'])

        # calculate the distance between the vector running from the head cetner to the inner condylar notch  of the first run and the head center coordinates of the second run
        dis['HC-IC'] = distance(dis['HC_x 2'], dis['HC_y 2'], dis['HC_z 2'], dis['IC_x 2'], dis['IC_y 2'],
                                dis['IC_z 2']) - distance(dis['HC_x 1'], dis['HC_y 1'], dis['HC_z 1'],
                                                          dis['IC_x 1'], dis['IC_y 1'], dis['IC_z 1'])
        # create dataframe with a copy of each resultant value
        dis_HC = dis[['HC']].copy()
        dis_IC = dis[['IC']].copy()
        dis_HC_IC = dis[['HC-IC']].copy()

        PID = dis[['Patient ID']].copy()
        # establish dataframe consolidating data
        Dis = pd.concat([Id, dis_HC, dis_IC, dis_HC_IC], axis=1)

        # calculating angles between the 1st and 2nd run
        vic = dis  # let vic equal the distance dataframe created above

        # establish vectors between the head center to the intercondylar notch
        vic['x_HC_IC_1'] = vector(dis['HC_x 1'], dis['IC_x 1'])
        vic['y_HC_IC_1'] = vector(dis['HC_y 1'], dis['IC_y 1'])
        vic['z_HC_IC_1'] = vector(dis['HC_z 1'], dis['IC_z 1'])
        vic['x_HC_IC_2'] = vector(dis['HC_x 2'], dis['IC_x 2'])
        vic['y_HC_IC_2'] = vector(dis['HC_y 2'], dis['IC_y 2'])
        vic['z_HC_IC_2'] = vector(dis['HC_z 2'], dis['IC_z 2'])
        x_HC_IC_1 = vic[['x_HC_IC_1']].copy()
        y_HC_IC_1 = vic[['y_HC_IC_1']].copy()
        z_HC_IC_1 = vic[['z_HC_IC_1']].copy()
        x_HC_IC_2 = vic[['x_HC_IC_2']].copy()
        y_HC_IC_2 = vic[['y_HC_IC_2']].copy()
        z_HC_IC_2 = vic[['z_HC_IC_2']].copy()

        # make a dataframe of all the vectors x, y, z from the Head center to innercondylar notch for the 1st run
        vec1 = pd.concat([x_HC_IC_1, y_HC_IC_1, z_HC_IC_1], axis=1)
        # make a dataframe of all the vectors x, y, z from the Head center to innercondylar notchfor the 2st run
        vec2 = pd.concat([x_HC_IC_2, y_HC_IC_2, z_HC_IC_2], axis=1)

        # turns dataframe to an array to be able to use in calculating angles
        vec1 = vec1.to_numpy()
        vec2 = vec2.to_numpy()

        # calculate the angle between two vectors
        ang = vg.angle(vec1, vec2, units='deg')
        ang = pd.DataFrame(ang)
        frame_a = [Id, ang]
        ang_r = pd.concat(frame_a, axis=1)  # creates a dataframe from the resulting angle

        # attaining volume data from the anatomical properties' data, locate the voxel and mesh volume, and convert the string into a numeric for the right femur
        vox_vol_2 = pd.DataFrame(Anatomicprop_2.iloc[7])
        vox_vol_2 = pd.DataFrame(vox_vol_2.iloc[0])
        vox_vol_2 = vox_vol_2['x'].str[15:24]
        vox_vol_2 = pd.to_numeric(vox_vol_2, errors='coerce')
        vox_vol_2 = vox_vol_2.reset_index(drop=True)

        mesh_vol_2 = pd.DataFrame(Anatomicprop_2.iloc[6])
        mesh_vol_2 = pd.DataFrame(mesh_vol_2.iloc[0])
        mesh_vol_2 = mesh_vol_2['x'].str[14:32]
        mesh_vol_2 = pd.to_numeric(mesh_vol_2, errors='coerce')
        mesh_vol_2 = mesh_vol_2.reset_index(drop=True)

        frame_vol = (vox_vol_2, mesh_vol_2)
        Vol_2 = pd.concat(frame_vol, axis=1)
        Vol_2.columns = ['Voxel Volume', 'Mesh Volume']
        Vol_1 = pd.DataFrame(Vol_1)
        Vol_2 = pd.DataFrame(Vol_2)
        frame_v = [PatientID, Vol_1, Vol_2]
        Vol = pd.concat(frame_v, axis=1)
        Vol.columns = ['Patient ID', 'V. Volume 1', 'M. Volume 1', 'V. Volume 2', 'M. Volume 2']

        # calculate percent change for the voxel and mesh volume
        Vol_pc = Vol

        Vol_pc['Voxel V'] = percentage_change(Vol_pc['V. Volume 1'], Vol_pc[
            'V. Volume 2'])  # take voxel volume from dataframe of volumes and enter it into equation for precent change
        Vol_pc['Mesh V'] = percentage_change(Vol_pc['M. Volume 1'], Vol_pc[
            'M. Volume 2'])  # take mesh volume from dataframe of volumes and enter it into equation for precent change

        Voxel_V = Vol_pc[['Voxel V']].copy()
        Mesh_V = Vol_pc[['Mesh V']].copy()
        Vol_pc = pd.concat([PatientID, Voxel_V, Mesh_V],
                           axis=1)  # create a dataframe with the precent change from the 1st and 2nd run for voxel and mesh volume to be used later

        # DataFrame for slope from 1st and 2nd run
        slope1 = pd.DataFrame(slope1)
        slope2 = pd.DataFrame(slope2)
        framesS = [slope1, slope2]
        dfS = pd.concat(framesS, axis=1)
        dfS.columns = ['1', '2']

        # Calculate the Percent Change for Slope from 1st and 2nd run
        dfS_pc = pd.concat(framesS, axis=1)
        dfS_pc.columns = ['1', '2']
        conv_cols = dfS_pc.apply(pd.to_numeric, errors='coerce', axis=1)  # convert the data to a numeric
        conv_cols['slope'] = percentage_change(conv_cols['1'], conv_cols['2'])  # calculate the precent change
        Slope_pc = conv_cols['slope'].copy()
        pcS = pd.concat([Slope_pc], axis=1)
        Slope_d = [pcS]
        pcS = pd.concat(Slope_d, axis=1)  # create a dataframe from the slope data

        # Create Dataframe Stance Summaries for the 1st and 2nd run you are comparing

        Stance_data1 = pd.DataFrame(Stance_data1)
        Stance_data2 = pd.DataFrame(Stance_data2)

        framesSS = [Stance_data1, Stance_data2] #combines data extracted for the first run and the consecutive run which is being compaired
        dfSS = pd.concat(framesSS, axis=1)  #creates a dataframe from both datasets

        # lable the columns to call the data as you need it
        dfSS.columns = ['fieldName', 'siteName', 'rightValue 1', 'leftValue 1', 'highVsLowRatio 1',
                        'highVsLowRisk 1', 'rightVsLeftRisk 1', 'leftVsRightRisk 1', 'strainFoldRight 1',
                        'strainFoldLeft 1', 'strainFoldRightRisk 1', 'strainFoldLeftRisk 1', 'BWMFRight 1',
                        'BWMFLeft 1', 'BWMFRiskScoreRight 1', 'BWMFRiskScoreLeft 1', 'equivalentRiskRight 1',
                        'equivalentRiskLeft 1', 'rightValue 2', 'leftValue 2', 'highVsLowRatio 2',
                        'highVsLowRisk 2', 'rightVsLeftRisk 2', 'leftVsRightRisk 2', 'strainFoldRight 2',
                        'strainFoldLeft 2', 'strainFoldRightRisk 2', 'strainFoldLeftRisk 2', 'BWMFRight 2',
                        'BWMFLeft 2', 'BWMFRiskScoreRight 2', 'BWMFRiskScoreLeft 2', 'equivalentRiskRight 2',
                        'equivalentRiskLeft 2']

        # percent change Stance Summary
        dfSS_pc = dfSS  # call the dataframe as pc to denote a datafram for precent change

        # calculate the percent change for the right and left femur for the first dataset and the second run it is being compared to
        dfSS_pc['right'] = percentage_change(dfSS_pc['rightValue 1'], dfSS_pc['rightValue 2'])
        dfSS_pc['left'] = percentage_change(dfSS_pc['leftValue 1'], dfSS_pc['leftValue 2'])
        dfSS_pc['highVsLowRatio'] = percentage_change(dfSS_pc['highVsLowRatio 1'], dfSS_pc['highVsLowRatio 2'])
        dfSS_pc['strainFoldRight'] = percentage_change(dfSS_pc['strainFoldRight 1'], dfSS_pc['strainFoldRight 2'])
        dfSS_pc['strainFoldLeft'] = percentage_change(dfSS_pc['strainFoldLeft 1'], dfSS_pc['strainFoldLeft 2'])
        dfSS_pc['BWMFRight'] = percentage_change(dfSS_pc['BWMFRight 1'], dfSS_pc['BWMFRight 2'])
        dfSS_pc['BWMFLeft'] = percentage_change(dfSS_pc['BWMFLeft 1'], dfSS_pc['BWMFLeft 2'])
        dfSS_pc['BWMFRiskScoreRight'] = percentage_change(dfSS_pc['BWMFRiskScoreRight 1'],
                                                          dfSS_pc['BWMFRiskScoreRight 2'])
        dfSS_pc['BWMFRiskScoreLeft'] = percentage_change(dfSS_pc['BWMFRiskScoreLeft 1'],
                                                         dfSS_pc['BWMFRiskScoreLeft 2'])

        # create a new dataset with the results from the percent change calculation for each measurement
        Names = dfSS_pc[['fieldName', 'siteName']].copy()
        right_pc = dfSS_pc[['right']].copy()
        left_pc = dfSS_pc[['left']].copy()
        highVsLowRatio_pc = dfSS_pc[['highVsLowRatio']].copy()
        strainFoldRight_pc = dfSS_pc[['strainFoldRight']].copy()
        strainFoldLeft_pc = dfSS_pc[['strainFoldLeft']].copy()
        BWMFRight_pc = dfSS_pc[['BWMFRight']].copy()
        BWMFLeft_pc = dfSS_pc[['BWMFLeft']].copy()
        BWMFRiskScoreRight_pc = dfSS_pc[['BWMFRiskScoreRight']].copy()
        BWMFRiskScoreLeft_pc = dfSS_pc[['BWMFRiskScoreLeft']].copy()

        # create a dataframe for the results of percent change for various measurements for stance summary
        pcSS = pd.concat([Names, right_pc, left_pc, highVsLowRatio_pc,
                          strainFoldRight_pc, strainFoldLeft_pc, BWMFRight_pc,
                          BWMFLeft_pc, BWMFRiskScoreRight_pc, BWMFRiskScoreLeft_pc], axis=1)

        # making dataframes for tension (E1) grouping based on region for right and left femur to write into CVS files to later be called upon for plotting
        # Neck Superior
        pc_neckS_E1 = pd.DataFrame(pcSS.iloc[[0]], columns=['right', 'left'])
        pc_neckS_E1 = pc_neckS_E1.reset_index(drop=True)

        # Neck Inferior/Sub Capital
        pc_neckI = pd.DataFrame(pcSS.iloc[[5]], columns=['right', 'left'])
        pc_neckI = pc_neckI.reset_index(drop=True)
        num_months = pd.Series(num_months, copy=False)
        num_months = num_months.reset_index(drop=True)

        loc = pd.Series('Superior Neck', copy=False)
        loc_N = loc.reset_index(drop=True)

        data_N = [Id, num_months, loc_N, pc_neckS_E1, pc_neckI, pcS]
        DataN = pd.concat(data_N, axis=1)
        # Trochanter
        pc_T_E1 = pd.DataFrame(pcSS.iloc[[1]], columns=['right', 'left'])
        pc_T_E1 = pc_T_E1.reset_index(drop=True)
        pc_T_E3 = pd.DataFrame(pcSS.iloc[[6]], columns=['right', 'left'])
        pc_T_E3 = pc_T_E3.reset_index(drop=True)

        loc = pd.Series('Trochanter', copy=False)
        loc_T = loc.reset_index(drop=True)

        data_T = [Id, num_months, loc_T, pc_T_E1, pc_T_E3, pcS]
        DataT = pd.concat(data_T, axis=1)

        # Proximal Shaft
        pc_PS_E1 = pd.DataFrame(pcSS.iloc[[2]], columns=['right', 'left'])
        pc_PS_E1 = pc_PS_E1.reset_index(drop=True)
        pc_PS_E3 = pd.DataFrame(pcSS.iloc[[7]], columns=['right', 'left'])
        pc_PS_E3 = pc_PS_E3.reset_index(drop=True)
        num_months = pd.Series(num_months, copy=False)
        num_months = num_months.reset_index(drop=True)
        loc = pd.Series('Proximal Shaft', copy=False)
        loc_P = loc.reset_index(drop=True)

        data_P = [Id, num_months, loc_P, pc_PS_E1, pc_PS_E3, pcS]
        DataP = pd.concat(data_P, axis=1)

        # Middle Shaft
        pc_MS_E1 = pd.DataFrame(pcSS.iloc[[3]], columns=['right', 'left'])
        pc_MS_E1 = pc_MS_E1.reset_index(drop=True)
        pc_MS_E3 = pd.DataFrame(pcSS.iloc[[8]], columns=['right', 'left'])
        pc_MS_E3 = pc_MS_E3.reset_index(drop=True)
        num_months = pd.Series(num_months, copy=False)
        num_months = num_months.reset_index(drop=True)

        loc = pd.Series('Middle Shaft', copy=False)
        loc_M = loc.reset_index(drop=True)

        data_M = [Id, num_months, loc_M, pc_MS_E1, pc_MS_E3, pcS]
        DataM = pd.concat(data_M, axis=1)

        # Distal Shaft
        pc_DS_E1 = pd.DataFrame(pcSS.iloc[[4]], columns=['right', 'left'])
        pc_DS_E1 = pc_DS_E1.reset_index(drop=True)
        pc_DS_E3 = pd.DataFrame(pcSS.iloc[[9]], columns=['right', 'left'])
        pc_DS_E3 = pc_DS_E3.reset_index(drop=True)
        num_months = pd.Series(num_months, copy=False)
        num_months = num_months.reset_index(drop=True)
        loc = pd.Series('Distal Shaft', copy=False)
        loc_D = loc.reset_index(drop=True)

        data_D = [Id, num_months, loc_D, pc_DS_E1, pc_DS_E3, pcS]
        DataD = pd.concat(data_D, axis=1)

        # writing info into individual CSV files
        timestr = time.strftime("%Y%m%d")
        os.chdir(path_data)
        file = '.csv'
        Patients = 'Patients info' + ' ' + timestr + file
        Strains = '% Change Data' + ' ' + timestr + file

        df_Patient.to_csv(Patients, mode='a', index=False, header=False)
        DataN.to_csv(Strains, mode='a', index=False, header=False)
        DataT.to_csv(Strains, mode='a', index=False, header=False)
        DataP.to_csv(Strains, mode='a', index=False, header=False)
        DataM.to_csv(Strains, mode='a', index=False, header=False)
        DataD.to_csv(Strains, mode='a', index=False, header=False)

#read the file where each patient's info was written and add a header to that file
Patients_fix = pd.read_csv(Patients, names =['Patient ID', 'Age', 'Weight'] )
Patients_fix.T.reset_index(drop=True)
Patients_fix = Patients_fix.sort_values(by=["Patient ID"], ascending=True)
Patients_fix.drop_duplicates(subset=None, keep="first", inplace=True) #drop any duplicate values that may appear
Patients_fix.to_csv(Patients, mode='w', index=False, header=True) #rewrite the altered file with a header and without duplicates

Strains_Fix = pd.read_csv(Strains,  names =['ID', 'months', 'region', 'right E1', 'left E1', 'right E3', 'left E3', 'slope']) #read file where all the data is located for all runs and add headers
Strains_Fix.T.reset_index().T.reset_index(drop=True)

Strains_Fix.drop_duplicates(subset=None, keep="first", inplace=True) #drop any duplicate values
Strains_Fix.to_csv(Strains, mode='w', index=True, header=True) #rewrite the file as a CSV file with proper header and without duplicates


for (ID), group in Strains_Fix.groupby(['ID']): #take the data from the CSV file that has the % change values for each comparative run for each patient and create groups based on patient name
    group.to_csv(f'{ID}.csv', index=False, header=True) #for each patient made an idividual CSV file with the data for each compative run

path = os.chdir(path_data) #change directory to the directory where the results are located
path1 = path_data

all_files = os.listdir(path)
print(all_files)

folder_count = len(all_files)

for i in range(0, folder_count, 1): #run through the files in the folder where the results are stored
    directory = 'Patient' + ' ' + all_files[i]
    info = 'Study Info'
    parent_dir = path_data
    #create folders for each patient file where a patient name cannot be more than 9 characters long
    if len(all_files[i]) == 5: #if file is 5 characters long
        path = os.path.join(parent_dir, directory[:9]) #create a new path combining folder path with the new file path
        os.mkdir(path) #make this folder
        source = all_files[i]
        destination = path
        new_path = shutil.move (source, destination) #move the file to the new created folder
    if len(all_files[i]) == 6:
        path = os.path.join(parent_dir, directory[:10])
        os.mkdir(path)
        source = all_files[i]
        destination = path
        new_path = shutil.move(source, destination)
    if len(all_files[i]) == 7:
        path = os.path.join(parent_dir, directory[:11])
        os.mkdir(path)
        source = all_files[i]
        destination = path
        new_path = shutil.move(source, destination)
    if len(all_files[i]) == 8:
        path = os.path.join(parent_dir, directory[:12])
        os.mkdir(path)
        source = all_files[i]
        destination = path
        new_path = shutil.move(source, destination)
    if len(all_files[i]) == 9:
        path = os.path.join(parent_dir, directory[:13])
        os.mkdir(path)
        source = all_files[i]
        destination = path
        new_path = shutil.move(source, destination)
    if len(all_files[i]) == 10:
        path = os.path.join(parent_dir, directory[:14])
        os.mkdir(path)
        source = all_files[i]
        destination = path
        new_path = shutil.move(source, destination)
    if len(all_files[i]) == 11:
        path = os.path.join(parent_dir, directory[:15])
        os.mkdir(path)
        source = all_files[i]
        destination = path
        new_path = shutil.move(source, destination)
    if len(all_files[i]) == 12:
        path = os.path.join(parent_dir, directory[:16])
        os.mkdir(path)
        source = all_files[i]
        destination = path
        new_path = shutil.move(source, destination)
    if len(all_files[i]) == 26:
        path = os.path.join(parent_dir, info)
        os.makedirs(path, exist_ok = True)
        source = all_files[i]
        destination = path
        new_path = shutil.move(source, destination)

# assign directory
directory = path_data

# iterate over files in
# that directory

for (root, dirs, files) in os.walk(directory, topdown=True):
    if "Study Info" in dirs:
        dirs.remove("Study Info")
    for file in files:
        patientname = str(file)
        patientname = pathlib.Path(file).with_suffix("")

        df = pd.read_csv(f'{root}\\{file}', sep=',')
        testD = pd.DataFrame(
            {"ID": [patientname], "months": [0], "region": ['Distal Shaft'], "right E1": [0], 'left E1': [0],
             "right E3": [0],
             "left E3": [0], "slope": [0]})
        testM = pd.DataFrame(
            {"ID": [patientname], "months": [0], "region": ['Middle Shaft'], "right E1": [0], 'left E1': [0],
             "right E3": [0],
             "left E3": [0], "slope": [0]})
        testP = pd.DataFrame(
            {"ID": [patientname], "months": [0], "region": ['Proximal Shaft'], "right E1": [0], 'left E1': [0],
             "right E3": [0],
             "left E3": [0], "slope": [0]})
        testSN = pd.DataFrame(
            {"ID": [patientname], "months": [0], "region": ['Superior Neck'], "right E1": [0], 'left E1': [0],
             "right E3": [0],
             "left E3": [0], "slope": [0]})
        testT = pd.DataFrame(
            {"ID": [patientname], "months": [0], "region": ['Trochanter'], "right E1": [0], 'left E1': [0],
             "right E3": [0],
             "left E3": [0], "slope": [0]})
        test = pd.concat([testD, testM, testP, testSN, testT])

        df = pd.concat([test, df], ignore_index=True)
        # Distal Shaft
        # x = df.loc[df['region'] == 'Distal Shaft', 'months']
        # y = df.loc[df['region'] == 'Distal Shaft', 'right E1']

        # plt.scatter(x, y, s=20, alpha=0.6, color='black', linewidth=1, label="DS right")
        # plt.plot(x, y, 'o-', alpha=0.6, linewidth=1, color='black')
        # plt.xticks(np.arange(min(x), max(x) + 1, 1.0), fontsize=8)
        # for x, y in zip(x, y):
        #  label = "{:.0f}".format(y)

        # plt.annotate(label,  # this is the text
        #            (x, y),  # these are the coordinates to position the label
        #             textcoords="offset points",  # how to position the text
        #           xytext=(5, 5),  # distance from text to points (x,y)
        #            ha='left')  # horizontal alignment can be left, right or center

        # x = df.loc[df['region'] == 'Distal Shaft', 'months']
        # y = df.loc[df['region'] == 'Distal Shaft', 'left E1']
        # plt.scatter(x, y, s=20, alpha=0.6, color='blue', linewidth=1, label="DS left")
        # plt.plot(x, y, 'o-', alpha=0.6, linewidth=1, color='blue')
        ## for x, y in zip(x, y):
        #  label = "{:.0f}".format(y)

        # plt.annotate(label,  # this is the text
        #            (x, y),  # these are the coordinates to position the label
        #            textcoords="offset points",  # how to position the text
        #            xytext=(5, 5),  # distance from text to points (x,y)
        #           ha='left')  # horizontal alignment can be left, right or center

        # Middle Shaft
        x = df.loc[df['region'] == 'Middle Shaft', 'months']
        y = df.loc[df['region'] == 'Middle Shaft', 'right E1']
        plt.scatter(x, y, s=20, alpha=0.6, color='green', linewidth=1, label="MS right")
        plt.plot(x, y, 'o-', alpha=0.6, linewidth=1, color='green')
        plt.xticks(np.arange(min(x), max(x) + 1, 1.0), fontsize=8)
        for x, y in zip(x, y):
            label = "{:.0f}".format(y)

            plt.annotate(label,  # this is the text
                         (x, y),  # these are the coordinates to position the label
                         textcoords="offset points",  # how to position the text
                         xytext=(5, 5),  # distance from text to points (x,y)
                         ha='left')  # horizontal alignment can be left, right or center

        x = df.loc[df['region'] == 'Middle Shaft', 'months']
        y = df.loc[df['region'] == 'Middle Shaft', 'left E1']
        plt.scatter(x, y, s=20, alpha=0.6, color='yellow', linewidth=1, label="MS left")
        plt.plot(x, y, 'o-', alpha=0.6, linewidth=1, color='yellow')
        plt.xticks(np.arange(min(x), max(x) + 1, 1.0), fontsize=8)
        for x, y in zip(x, y):
            label = "{:.0f}".format(y)

            plt.annotate(label,  # this is the text
                         (x, y),  # these are the coordinates to position the label
                         textcoords="offset points",  # how to position the text
                         xytext=(5, 5),  # distance from text to points (x,y)
                         ha='left')  # horizontal alignment can be left, right or center

        # Trochanter
        x = df.loc[df['region'] == 'Trochanter', 'months']
        y = df.loc[df['region'] == 'Trochanter', 'right E1']
        plt.scatter(x, y, s=20, alpha=0.6, color='pink', linewidth=1, label="T right")
        plt.plot(x, y, 'o-', alpha=0.6, linewidth=1, color='pink')
        plt.xticks(np.arange(min(x), max(x) + 1, 1.0), fontsize=8)
        for x, y in zip(x, y):
            label = "{:.0f}".format(y)

            plt.annotate(label,  # this is the text
                         (x, y),  # these are the coordinates to position the label
                         textcoords="offset points",  # how to position the text
                         xytext=(5, 5),  # distance from text to points (x,y)
                         ha='left')  # horizontal alignment can be left, right or center

        x = df.loc[df['region'] == 'Trochanter', 'months']
        y = df.loc[df['region'] == 'Trochanter', 'left E1']
        plt.scatter(x, y, s=20, alpha=0.6, color='springgreen', linewidth=1, label="T left")
        plt.plot(x, y, 'o-', alpha=0.6, linewidth=1, color='springgreen')
        plt.xticks(np.arange(min(x), max(x) + 1, 1.0), fontsize=8)
        for x, y in zip(x, y):
            label = "{:.0f}".format(y)

            plt.annotate(label,  # this is the text
                         (x, y),  # these are the coordinates to position the label
                         textcoords="offset points",  # how to position the text
                         xytext=(5, 5),  # distance from text to points (x,y)
                         ha='left')  # horizontal alignment can be left, right or center

        # Proximal Shaft
        x = df.loc[df['region'] == 'Proximal Shaft', 'months']
        y = df.loc[df['region'] == 'Proximal Shaft', 'right E1']
        plt.scatter(x, y, s=20, alpha=0.6, color='peru', linewidth=1, label="PS right")
        plt.plot(x, y, 'o-', alpha=0.6, linewidth=1, color='peru')
        plt.xticks(np.arange(min(x), max(x) + 1, 1.0), fontsize=8)
        for x, y in zip(x, y):
            label = "{:.0f}".format(y)

            plt.annotate(label,  # this is the text
                         (x, y),  # these are the coordinates to position the label
                         textcoords="offset points",  # how to position the text
                         xytext=(5, 5),  # distance from text to points (x,y)
                         ha='left')  # horizontal alignment can be left, right or center

        x = df.loc[df['region'] == 'Proximal Shaft', 'months']
        y = df.loc[df['region'] == 'Proximal Shaft', 'left E1']
        plt.scatter(x, y, s=20, alpha=0.6, color='orange', linewidth=1, label="PS left")
        plt.plot(x, y, 'o-', alpha=0.6, linewidth=1, color='orange')
        plt.xticks(np.arange(min(x), max(x) + 1, 1.0), fontsize=8)
        for x, y in zip(x, y):
            label = "{:.0f}".format(y)

            plt.annotate(label,  # this is the text
                         (x, y),  # these are the coordinates to position the label
                         textcoords="offset points",  # how to position the text
                         xytext=(5, 5),  # distance from text to points (x,y)
                         ha='left')  # horizontal alignment can be left, right or center
        # Superior Neck
        x = df.loc[df['region'] == 'Superior Neck', 'months']
        y = df.loc[df['region'] == 'Superior Neck', 'right E1']
        plt.scatter(x, y, s=20, alpha=0.6, color='rosybrown', linewidth=1, label="SN right")
        plt.plot(x, y, 'o-', alpha=0.6, linewidth=1, color='rosybrown')
        plt.xticks(np.arange(min(x), max(x) + 1, 1.0), fontsize=8)
        for x, y in zip(x, y):
            label = "{:.0f}".format(y)

            plt.annotate(label,  # this is the text
                         (x, y),  # these are the coordinates to position the label
                         textcoords="offset points",  # how to position the text
                         xytext=(5, 5),  # distance from text to points (x,y)
                         ha='left')  # horizontal alignment can be left, right or center

        x = df.loc[df['region'] == 'Superior Neck', 'months']
        y = df.loc[df['region'] == 'Superior Neck', 'left E1']
        plt.scatter(x, y, s=20, alpha=0.6, color='silver', linewidth=1, label="SN left")
        plt.plot(x, y, 'o-', alpha=0.6, linewidth=1, color='silver')
        plt.xticks(np.arange(min(x), max(x) + 1, 1.0), fontsize=8)
        for x, y in zip(x, y):
            label = "{:.0f}".format(y)

            plt.annotate(label,  # this is the text
                         (x, y),  # these are the coordinates to position the label
                         textcoords="offset points",  # how to position the text
                         xytext=(5, 5),  # distance from text to points (x,y)
                         ha='left')  # horizontal alignment can be left, right or center

        patientname = str(file)
        patientname = pathlib.Path(file).with_suffix("")
        patientname = str(patientname)

        plotname = 'Patient' + ' ' + patientname
        plot_path = path_data + '\\' + 'Patient ' + patientname + '\\' + patientname + 'E1.png'

        plt.title(plotname + ' ' + 'E1')
        plt.ylabel('% Change in Strains')
        plt.xlabel('Months Between Scans')
        y1 = 10
        y2 = -10
        plt.axhspan(y1, y2, color='lightgrey', alpha=0.75, lw=0)

        plt.legend(loc='upper right', bbox_to_anchor=(1.35, 1.35))
        plt.grid()
        plt.savefig(plot_path, bbox_inches='tight')
        plt.clf()
        # E3
        # Distal Shaft
        # x = df.loc[df['region'] == 'Distal Shaft', 'months']
        # y = df.loc[df['region'] == 'Distal Shaft', 'right E3']
        # plt.scatter(x, y, s=20, alpha=0.6, color='black', linewidth=1, label="DS right")
        # plt.plot(x, y, 'o-', alpha=0.6, linewidth=1, color='black')
        # plt.xticks(np.arange(min(x), max(x) + 1, 1.0), fontsize=8)
        # for x, y in zip(x, y):
        #    label = "{:.0f}".format(y)

        # plt.annotate(label,  # this is the text
        #             (x, y),  # these are the coordinates to position the label
        #              textcoords="offset points",  # how to position the text
        #               xytext=(5, 5),  # distance from text to points (x,y)
        #                ha='left')  # horizontal alignment can be left, right or center

        # x = df.loc[df['region'] == 'Distal Shaft', 'months']
        # y = df.loc[df['region'] == 'Distal Shaft', 'left E3']
        # plt.scatter(x, y, s=20, alpha=0.6, color='blue', linewidth=1, label="DS left")
        # plt.plot(x, y, 'o-', alpha=0.6, linewidth=1, color='blue')
        # plt.xticks(np.arange(min(x), max(x) + 1, 1.0), fontsize=8)
        # for x, y in zip(x, y):
        #    label = "{:.0f}".format(y)

        #  plt.annotate(label,  # this is the text
        #               (x, y),  # these are the coordinates to position the label
        #                textcoords="offset points",  # how to position the text
        #                 xytext=(5, 5),  # distance from text to points (x,y)
        #                  ha='left')  # horizontal alignment can be left, right or center

        # Middle Shaft
        x = df.loc[df['region'] == 'Middle Shaft', 'months']
        y = df.loc[df['region'] == 'Middle Shaft', 'right E3']
        plt.scatter(x, y, s=20, alpha=0.6, color='green', linewidth=1, label="MS right")
        plt.plot(x, y, 'o-', alpha=0.6, linewidth=1, color='green')
        plt.xticks(np.arange(min(x), max(x) + 1, 1.0), fontsize=8)
        for x, y in zip(x, y):
            label = "{:.0f}".format(y)

            plt.annotate(label,  # this is the text
                         (x, y),  # these are the coordinates to position the label
                         textcoords="offset points",  # how to position the text
                         xytext=(5, 5),  # distance from text to points (x,y)
                         ha='left')  # horizontal alignment can be left, right or center

        x = df.loc[df['region'] == 'Middle Shaft', 'months']
        y = df.loc[df['region'] == 'Middle Shaft', 'left E3']
        plt.scatter(x, y, s=20, alpha=0.6, color='yellow', linewidth=1, label="MS left")
        plt.plot(x, y, 'o-', alpha=0.6, linewidth=1, color='yellow')
        plt.xticks(np.arange(min(x), max(x) + 1, 1.0), fontsize=8)
        for x, y in zip(x, y):
            label = "{:.0f}".format(y)

            plt.annotate(label,  # this is the text
                         (x, y),  # these are the coordinates to position the label
                         textcoords="offset points",  # how to position the text
                         xytext=(5, 5),  # distance from text to points (x,y)
                         ha='left')  # horizontal alignment can be left, right or center

        # Trochanter
        x = df.loc[df['region'] == 'Trochanter', 'months']
        y = df.loc[df['region'] == 'Trochanter', 'right E3']
        plt.scatter(x, y, s=20, alpha=0.6, color='pink', linewidth=1, label="T right")
        plt.plot(x, y, 'o-', alpha=0.6, linewidth=1, color='pink')
        plt.xticks(np.arange(min(x), max(x) + 1, 1.0), fontsize=8)
        for x, y in zip(x, y):
            label = "{:.0f}".format(y)

            plt.annotate(label,  # this is the text
                         (x, y),  # these are the coordinates to position the label
                         textcoords="offset points",  # how to position the text
                         xytext=(5, 5),  # distance from text to points (x,y)
                         ha='left')  # horizontal alignment can be left, right or center

        x = df.loc[df['region'] == 'Trochanter', 'months']
        y = df.loc[df['region'] == 'Trochanter', 'left E3']
        plt.scatter(x, y, s=20, alpha=0.6, color='springgreen', linewidth=1, label="T left")
        plt.plot(x, y, 'o-', alpha=0.6, linewidth=1, color='springgreen')
        plt.xticks(np.arange(min(x), max(x) + 1, 1.0), fontsize=8)
        for x, y in zip(x, y):
            label = "{:.0f}".format(y)

            plt.annotate(label,  # this is the text
                         (x, y),  # these are the coordinates to position the label
                         textcoords="offset points",  # how to position the text
                         xytext=(5, 5),  # distance from text to points (x,y)
                         ha='left')  # horizontal alignment can be left, right or center

        # Proximal Shaft
        x = df.loc[df['region'] == 'Proximal Shaft', 'months']
        y = df.loc[df['region'] == 'Proximal Shaft', 'right E3']
        plt.scatter(x, y, s=20, alpha=0.6, color='peru', linewidth=1, label="PS right")
        plt.plot(x, y, 'o-', alpha=0.6, linewidth=1, color='peru')
        plt.xticks(np.arange(min(x), max(x) + 1, 1.0), fontsize=8)
        for x, y in zip(x, y):
            label = "{:.0f}".format(y)

            plt.annotate(label,  # this is the text
                         (x, y),  # these are the coordinates to position the label
                         textcoords="offset points",  # how to position the text
                         xytext=(5, 5),  # distance from text to points (x,y)
                         ha='left')  # horizontal alignment can be left, right or center

        x = df.loc[df['region'] == 'Proximal Shaft', 'months']
        y = df.loc[df['region'] == 'Proximal Shaft', 'left E3']
        plt.scatter(x, y, s=20, alpha=0.6, color='orange', linewidth=1, label="PS left")
        plt.plot(x, y, 'o-', alpha=0.6, linewidth=1, color='orange')
        plt.xticks(np.arange(min(x), max(x) + 1, 1.0), fontsize=8)
        for x, y in zip(x, y):
            label = "{:.0f}".format(y)

            plt.annotate(label,  # this is the text
                         (x, y),  # these are the coordinates to position the label
                         textcoords="offset points",  # how to position the text
                         xytext=(5, 5),  # distance from text to points (x,y)
                         ha='left')  # horizontal alignment can be left, right or center
        # Superior Neck
        x = df.loc[df['region'] == 'Superior Neck', 'months']
        y = df.loc[df['region'] == 'Superior Neck', 'right E3']
        plt.scatter(x, y, s=20, alpha=0.6, color='rosybrown', linewidth=1, label="SN right")
        plt.plot(x, y, 'o-', alpha=0.6, linewidth=1, color='rosybrown')
        plt.xticks(np.arange(min(x), max(x) + 1, 1.0), fontsize=8)
        for x, y in zip(x, y):
            label = "{:.0f}".format(y)

            plt.annotate(label,  # this is the text
                         (x, y),  # these are the coordinates to position the label
                         textcoords="offset points",  # how to position the text
                         xytext=(5, 5),  # distance from text to points (x,y)
                         ha='left')  # horizontal alignment can be left, right or center

        x = df.loc[df['region'] == 'Superior Neck', 'months']
        y = df.loc[df['region'] == 'Superior Neck', 'left E3']
        plt.scatter(x, y, s=20, alpha=0.6, color='silver', linewidth=1, label="SN left")
        plt.plot(x, y, 'o-', alpha=0.6, linewidth=1, color='silver')
        plt.xticks(np.arange(min(x), max(x) + 1, 1.0), fontsize=8)
        for x, y in zip(x, y):
            label = "{:.0f}".format(y)

            plt.annotate(label,  # this is the text
                         (x, y),  # these are the coordinates to position the label
                         textcoords="offset points",  # how to position the text
                         xytext=(5, 5),  # distance from text to points (x,y)
                         ha='left')  # horizontal alignment can be left, right or center

        patientname = str(file)
        patientname = pathlib.Path(file).with_suffix("")
        patientname = str(patientname)

        plotname = 'Patient' + ' ' + patientname
        plot_path = path_data + '\\' + 'Patient ' + patientname + '\\' + patientname + 'E3.png'

        plt.title(plotname + ' ' + 'E3')
        plt.ylabel('% Change in Strains')
        plt.xlabel('Months Between Scans')
        y1 = 10
        y2 = -10
        plt.axhspan(y1, y2, color='lightgrey', alpha=0.75, lw=0)

        plt.legend(loc='upper right', bbox_to_anchor=(1.32, 1.32))
        plt.plot(x, y)
        plt.grid()
        plt.savefig(plot_path, bbox_inches='tight')
        plt.clf()

        # Slope
        x = df.loc[df['region'] == 'Superior Neck', 'months']
        y = df.loc[df['region'] == 'Superior Neck', 'slope']
        plt.scatter(x, y, s=20, alpha=0.6, color='black', linewidth=1, label="Slope")
        plt.plot(x, y, 'o-', alpha=0.6, linewidth=1, color='black')
        plt.xticks(np.arange(min(x), max(x) + 1, 1.0), fontsize=8)
        for x, y in zip(x, y):
            label = "{:.0f}".format(y)

            plt.annotate(label,  # this is the text
                         (x, y),  # these are the coordinates to position the label
                         textcoords="offset points",  # how to position the text
                         xytext=(5, 5),  # distance from text to points (x,y)
                         ha='left')  # horizontal alignment can be left, right or center

        patientname = str(file)
        patientname = pathlib.Path(file).with_suffix("")
        patientname = str(patientname)

        plotname = 'Patient' + ' ' + patientname
        plot_path = path_data + '\\' + 'Patient ' + patientname + '\\' + patientname + 'Slope.png'

        plt.title(plotname + ' ' + 'Slope')
        plt.ylabel('% Change in Slope')
        plt.xlabel('Months Between Scans')
        y1 = 5
        y2 = -5
        plt.axhspan(y1, y2, color='lightgrey', alpha=0.75, lw=0)

        plt.legend(loc='upper right', bbox_to_anchor=(1.32, 1.32))
        plt.plot(x, y)
        plt.grid()
        plt.savefig(plot_path, bbox_inches='tight')
        plt.clf()