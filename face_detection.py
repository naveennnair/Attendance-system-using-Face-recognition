# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 14:54:21 2019

@author: naveenn
"""

from imutils import paths
import face_recognition
import pickle
import cv2
import os

class student_face_identifier:
    
    def face_train(base_path = "C:/Users/Public/Documents/Python Scripts/Attendence_system/Student_img", class_name = "BSc_Computer"):
        os.chdir(base_path)
        # grab the paths to the input images in our dataset
        print("[INFO] quantifying faces...")
        imagePaths = list(paths.list_images(class_name))
        
        # initialize the list of known encodings and known names
        knownEncodings = []
        knownNames = []
        
        # loop over the image paths
        for (i, imagePath) in enumerate(imagePaths):
        	# extract the person name from the image path
        	print("[INFO] processing image {}/{}".format(i + 1, len(imagePaths)))
        	name = imagePath.split(os.path.sep)[-1][:-6]
        
        	# load the input image and convert it from BGR (OpenCV ordering)
        	# to dlib ordering (RGB)
        	image = cv2.imread(imagePath)
        	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        	# detect the (x, y)-coordinates of the bounding boxes
        	# corresponding to each face in the input image
        	boxes = face_recognition.face_locations(rgb,	model='hog')
        
        	# compute the facial embedding for the face
        	encodings = face_recognition.face_encodings(rgb, boxes)
        
        	# loop over the encodings
        	for encoding in encodings:
        		# add each encoding + name to our set of known names and
        		# encodings
        		knownEncodings.append(encoding)
        		knownNames.append(name)
                         
        # dump the facial encodings + names to disk
        print("[INFO] serializing encodings...")
        data = {"encodings": knownEncodings, "names": knownNames}
        f = open(os.path.join(class_name,'encodings.pkl'), "wb")
        f.write(pickle.dumps(data))
        f.close()
        print('encodings saved...')
    
    ####============= Finished training ===================
    ####=============== Testing phase =====================
    def getting_names(class_name, img):
        global names
        pickle_in = open(os.path.join('Student_img',class_name,'encodings.pkl'),"rb")
        data = pickle.load(pickle_in)
        # load the input image and convert it from BGR to RGB
        image = cv2.imread(img)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # detect the (x, y)-coordinates of the bounding boxes corresponding
        # to each face in the input image, then compute the facial embeddings
        # for each face
        print("[INFO] recognizing faces...")
        boxes = face_recognition.face_locations(rgb,	model='hog')
        encodings = face_recognition.face_encodings(rgb, boxes)
        
        # initialize the list of names for each face detected
        names = []
        
        # loop over the facial embeddings
        for encoding in encodings:
            	# attempt to match each face in the input image to our known
            	# encodings
            	matches = face_recognition.compare_faces(data["encodings"], encoding, 0.55)
            	name = "Unknown"
                
            	# check to see if we have found a match
            	if True in matches:
            		# find the indexes of all matched faces then initialize a
            		# dictionary to count the total number of times each face
            		# was matched
            		matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            		counts = {}
            
            		# loop over the matched indexes and maintain a count for
            		# each recognized face face
            		for i in matchedIdxs:
            			name = data["names"][i]
            			counts[name] = counts.get(name, 0) + 1
            
            		# determine the recognized face with the largest number of
            		# votes (note: in the event of an unlikely tie Python will
            		# select first entry in the dictionary)
            		name = max(counts, key=counts.get)
        	
        	# update the list of names
            	names.append(name)  
        return names
              
    #    # loop over the recognized faces
    #    for ((top, right, bottom, left), name) in zip(boxes, names):
    #    # draw the predicted face name on the image
    #    cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
    #    y = top - 15 if top - 15 > 15 else top + 15
    #    cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
    #    		0.75, (0, 255, 0), 2)
    #    
    #    # show the output image
    #    cv2.imshow("Image", image)
    #    cv2.waitKey(0)    

#def attendance_table(class_name):
#        
#
#names = getting_names('test1.jpg')

#import pandas as pd
#from datetime import date
#df = pd.read_csv(r'C:\Users\Public\Documents\Python Scripts\Attendence_system\Student_names\BSc_Computer\names.csv')
#df[str(date.today())] = 'Absent'
#df[str(date.today())].loc[df['Name'].isin(names),] = 'Present'
#df[str(date.today())].apply(lambda x: x in names df[str(date.today())]  'Present' )



