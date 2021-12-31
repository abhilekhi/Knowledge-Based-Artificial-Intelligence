#Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
from PIL import Image, ImageOps, ImageChops, ImageStat
import numpy as np 
from RavensProblem import RavensProblem
import pathlib
import glob, os
from os import walk
import cv2
import time 
import random 
import itertools
import math 



#from RavensFigure import RavensFigure

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints 
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    
    # take an array of percent difference and return which ones match? 
    def check_same(p_array):
        
        return -1 
    
    # Take the images list and the indexs we wanna compare
    # Could do ROWS = 0,1,2 ; 3,4,5
    #          COLS = 0,3,6 ; 1,4,7
    
    def percent_diff(self,images_list_int,indexs,answer_options,flag):
        
        if flag == 1:
            res = cv2.absdiff(np.asarray(images_list_int[indexs[0]]), np.asarray(answer_options[indexs[1]]))
        else: 
            res = cv2.absdiff(np.asarray(images_list_int[indexs[0]]), np.asarray(images_list_int[indexs[1]]))
        
        res = res.astype(np.uint8)
        p = (np.count_nonzero(res) * 100)/ res.size
        
        return p 
    
    def pixel_count(self,img):
        # get all non black Pixels
        graying = cv2.cvtColor(np.asarray(img), cv2.COLOR_BGR2GRAY)

        cntNotBlack = cv2.countNonZero(np.asarray(graying))
        
        # get pixel count of image
        height, width = img.size
        cntPixels = height*width
        
        # compute all black pixels
        cntBlack = cntPixels - cntNotBlack
        
        return cntBlack/cntPixels
        
    
    def clean_dict(self,d):
        
        del d[(0,4)]
        del d[(0,5)]
        del d[(0,7)]
        del d[(1,3)]
        del d[(1,5)]
        del d[(1,6)]
        del d[(2,3)]
        del d[(2,4)]
        del d[(2,6)]
        del d[(2,7)]
        del d[(3,7)]
        del d[(4,6)]
        del d[(5,6)]
        del d[(5,7)]
        
        return d
    
    
    def image_90_2x2(self,grid,p_dict,images_list_int, answer_options,pairs):
        theta = 90
        
        tran_A = images_list_int[0].rotate(angle=theta)
        tran_B = images_list_int[1].rotate(angle=theta)
        tran_C = images_list_int[2].rotate(angle=theta)
        
 
        flip_dict = dict.fromkeys([pairs[0],pairs[1],pairs[2]])
        
        # Difference between Tran A and B 
        resATB = cv2.absdiff(np.asarray(images_list_int[1]), np.asarray(tran_A))
        resATB = resATB.astype(np.uint8)
        pATB = (np.count_nonzero(resATB) * 100)/ resATB.size
        flip_dict[pairs[0]] = pATB
        #print("\nAB: ",pAB)
        
        
        # Difference between Tran A and C
        resATC = cv2.absdiff(np.asarray(images_list_int[2]), np.asarray(tran_A))
        resATC = resATC.astype(np.uint8)
        pATC = (np.count_nonzero(resATC) * 100)/ resATC.size
        
        flip_dict[pairs[1]] = pATC
       
        
        # Difference between Tran B and C 
        resBTC= cv2.absdiff(np.asarray(images_list_int[2]), np.asarray(tran_B))
        resBTC = resBTC.astype(np.uint8)
        pBTC = (np.count_nonzero(resBTC * 100))/ resBTC.size
        flip_dict[pairs[2]] = pBTC
        
        #best_key = 0



        best_key = min(flip_dict, key=flip_dict.get)
        flag = -1
        
        
        for key in flip_dict.keys():
            if flip_dict[key] > 0.6 and flip_dict[key] < 15: 
                best_key = key
                flag = 0 
                
        if flip_dict[best_key] > 15 or flag == -1:
            return -1

        
        #print(best_key)

        #Trans A relates to B
        if best_key == (0,1):
            to_find = np.asarray(tran_C)
    
    
        # Trans A relates to C
        if best_key == (0,2):
             to_find = np.asarray(tran_B)
     
        # Trans B relates to C 
        if best_key == (1,2): 
             to_find = np.asarray(tran_A)
             
        
       
        #print(flip_dict)
        
        for i in range(len(answer_options)):
            # Get sum of each options
            best_dif = 100
            best_index = 0 
            for i in range(len(answer_options)):
                res = cv2.absdiff(to_find, np.asarray(answer_options[i]))
                res = res.astype(np.uint8)
                diff = (np.count_nonzero(res) * 100)/ res.size
                if diff < best_dif:  
                    best_dif = diff
                    best_index = i+1 
        
        return best_index
     
    def image_45_2x2(self,grid,p_dict,images_list_int, answer_options,pairs):
        theta = 45
        
        tran_A = images_list_int[0].rotate(angle=theta)
        tran_B = images_list_int[1].rotate(angle=theta)
        tran_C = images_list_int[2].rotate(angle=theta)
        
 
        flip_dict = dict.fromkeys([pairs[0],pairs[1],pairs[2]])
        
        # Difference between Tran A and B 
        resATB = cv2.absdiff(np.asarray(images_list_int[1]), np.asarray(tran_A))
        resATB = resATB.astype(np.uint8)
        pATB = (np.count_nonzero(resATB) * 100)/ resATB.size
        flip_dict[pairs[0]] = pATB
        #print("\nAB: ",pAB)
        
        
        # Difference between Tran A and C
        resATC = cv2.absdiff(np.asarray(images_list_int[2]), np.asarray(tran_A))
        resATC = resATC.astype(np.uint8)
        pATC = (np.count_nonzero(resATC) * 100)/ resATC.size
        
        flip_dict[pairs[1]] = pATC
       
        
        # Difference between Tran B and C 
        resBTC= cv2.absdiff(np.asarray(images_list_int[2]), np.asarray(tran_B))
        resBTC = resBTC.astype(np.uint8)
        pBTC = (np.count_nonzero(resBTC * 100))/ resBTC.size
        flip_dict[pairs[2]] = pBTC
        
        #best_key = 0



        best_key = min(flip_dict, key=flip_dict.get)
        flag = -1
        
        
        for key in flip_dict.keys():
            if flip_dict[key] > 0.6 and flip_dict[key] < 15: 
                best_key = key
                flag = 0 
                
        if flip_dict[best_key] > 15 or flag == -1:
            return -1

        
        #print(best_key)

        #Trans A relates to B
        if best_key == (0,1):
            to_find = np.asarray(tran_C)
    
    
        # Trans A relates to C
        if best_key == (0,2):
             to_find = np.asarray(tran_B)
     
        # Trans B relates to C 
        if best_key == (1,2): 
             to_find = np.asarray(tran_A)
             
        
       
        #print(flip_dict)
        
        for i in range(len(answer_options)):
            # Get sum of each options
            best_dif = 100
            best_index = 0 
            for i in range(len(answer_options)):
                res = cv2.absdiff(to_find, np.asarray(answer_options[i]))
                res = res.astype(np.uint8)
                diff = (np.count_nonzero(res) * 100)/ res.size
                if diff < best_dif:  
                    best_dif = diff
                    best_index = i+1 
        
        return best_index
    
    def image_mirror_2x2(self,grid,p_dict,images_list_int, answer_options,pairs):
        
        tran_A = ImageOps.mirror(images_list_int[0])
        tran_B = ImageOps.mirror(images_list_int[1])
        tran_C = ImageOps.mirror(images_list_int[2])
        
 
        flip_dict = dict.fromkeys([pairs[0],pairs[1],pairs[2]])
        
        # Difference between Tran A and B 
        resATB = cv2.absdiff(np.asarray(images_list_int[1]), np.asarray(tran_A))
        resATB = resATB.astype(np.uint8)
        pATB = (np.count_nonzero(resATB) * 100)/ resATB.size
        flip_dict[pairs[0]] = pATB
        #print("\nAB: ",pAB)
        
        
        # Difference between Tran A and C
        resATC = cv2.absdiff(np.asarray(images_list_int[2]), np.asarray(tran_A))
        resATC = resATC.astype(np.uint8)
        pATC = (np.count_nonzero(resATC) * 100)/ resATC.size
        
        flip_dict[pairs[1]] = pATC
       
        
        # Difference between Tran B and C 
        resBTC= cv2.absdiff(np.asarray(images_list_int[2]), np.asarray(tran_B))
        resBTC = resBTC.astype(np.uint8)
        pBTC = (np.count_nonzero(resBTC * 100))/ resBTC.size
        flip_dict[pairs[2]] = pBTC
        
        #best_key = 0



        best_key = min(flip_dict, key=flip_dict.get)
        flag = -1
        
        
        for key in flip_dict.keys():
            if flip_dict[key] > 0.6 and flip_dict[key] < 15: 
                best_key = key
                flag = 0 
                
        if flip_dict[best_key] > 15 or flag == -1:
            return -1

        
        #print(best_key)

        #Trans A relates to B
        if best_key == (0,1):
            to_find = np.asarray(tran_C)
    
    
        # Trans A relates to C
        if best_key == (0,2):
             to_find = np.asarray(tran_B)
     
        # Trans B relates to C 
        if best_key == (1,2): 
             to_find = np.asarray(tran_A)
             
        
       
        #print(flip_dict)
        
        for i in range(len(answer_options)):
            # Get sum of each options
            best_dif = 100
            best_index = 0 
            for i in range(len(answer_options)):
                res = cv2.absdiff(to_find, np.asarray(answer_options[i]))
                res = res.astype(np.uint8)
                diff = (np.count_nonzero(res) * 100)/ res.size
                if diff < best_dif:  
                    best_dif = diff
                    best_index = i+1 
        
        return best_index
        
    
    
    def image_flip_2x2(self,grid,p_dict,images_list_int, answer_options,pairs):
        
        tran_A = ImageOps.flip(images_list_int[0])
        
        tran_B = ImageOps.flip(images_list_int[1])
        tran_C = ImageOps.flip(images_list_int[2])
        
 
        flip_dict = dict.fromkeys([pairs[0],pairs[1],pairs[2]])
        
        # Difference between Tran A and B 
        resATB = cv2.absdiff(np.asarray(images_list_int[1]), np.asarray(tran_A))
        resATB = resATB.astype(np.uint8)
        pATB = (np.count_nonzero(resATB) * 100)/ resATB.size
        flip_dict[pairs[0]] = pATB
        #print("\nAB: ",pAB)
        
        
        # Difference between Tran A and C
        resATC = cv2.absdiff(np.asarray(images_list_int[2]), np.asarray(tran_A))
        resATC = resATC.astype(np.uint8)
        pATC = (np.count_nonzero(resATC) * 100)/ resATC.size
        
        flip_dict[pairs[1]] = pATC
       
        
        # Difference between Tran B and C 
        resBTC= cv2.absdiff(np.asarray(images_list_int[2]), np.asarray(tran_B))
        resBTC = resBTC.astype(np.uint8)
        pBTC = (np.count_nonzero(resBTC * 100))/ resBTC.size
        flip_dict[pairs[2]] = pBTC
        
        #best_key = 0


        tran_B.show()
        best_key = min(flip_dict, key=flip_dict.get)
        flag = -1
        
        
        for key in flip_dict.keys():
            if flip_dict[key] > 0.6 and flip_dict[key] < 15: 
                best_key = key
                flag = 0 
                
        if flip_dict[best_key] > 15 or flag == -1:
            return -1

        
        #print(best_key)

        #Trans A relates to B
        if best_key == (0,1):
            to_find = np.asarray(tran_C)
    
    
        # Trans A relates to C
        if best_key == (0,2):
             to_find = np.asarray(tran_B)
     
        # Trans B relates to C 
        if best_key == (1,2): 
             to_find = np.asarray(tran_A)
             
        
       
        #print(flip_dict)
        
        for i in range(len(answer_options)):
            # Get sum of each options
            best_dif = 100
            best_index = 0 
            for i in range(len(answer_options)):
                res = cv2.absdiff(to_find, np.asarray(answer_options[i]))
                res = res.astype(np.uint8)
                diff = (np.count_nonzero(res) * 100)/ res.size
                if diff < best_dif:  
                    best_dif = diff
                    best_index = i+1 
        
        return best_index
        
        
    def check_similar_percent(self,grid,p_dict,images_list_int, answer_options,pairs):
        
        if grid == "2x2":
            best_key = min(p_dict, key=p_dict.get)
            best_index = -1
            
            if p_dict[best_key] > 2: 
                best_index = self.image_flip_2x2(grid,p_dict,images_list_int, answer_options,pairs)
                if best_index == -1: 
                    best_index = self.image_mirror_2x2(grid,p_dict,images_list_int, answer_options,pairs)
                    if best_index == -1 :
                        best_index = self.image_90_2x2(grid,p_dict,images_list_int, answer_options,pairs)
                        if best_index == -1 :
                            best_index = self.image_45_2x2(grid,p_dict,images_list_int, answer_options,pairs)
                elif best_index != -1:     
                    return best_index
                
            if best_index != -1: 
                return best_index
            
            # A relates to B
            if best_key == (0,1):
                to_find = 2

        
            # A relates to C
            if best_key == (0,2):
                 to_find = 1
     
            # B relates to C 
            if best_key == (1,2): 
                 to_find = 0

            best_dif = 100
            best_index = 0 

            for i in range(len(answer_options)):
                # Get sum of each options
                indexs = (to_find, i)
                diff = self.percent_diff(images_list_int,indexs,answer_options,flag = 1)
                if diff < best_dif: 
                    best_dif = diff
                    best_index = i+1 
                    
            return best_index
                
        
        # Lets check the sum of the two rows, two columns and see 
        
        elif grid == "3x3":
            
            # Get the average percent difference in row 1 and row 2
            row_1 = (p_dict[(0,1)] + p_dict[(0,2)] + p_dict[(1,2)])/3
            row_2 = (p_dict[(3,4)] + p_dict[(3,5)] + p_dict[(4,5)])/3
            
            # Get the average percent difference in col 1 and col 2
            col_1 = (p_dict[(0,3)] + p_dict[(0,6)] + p_dict[(3,6)])/3
            col_2 = (p_dict[(1,4)] + p_dict[(1,7)] + p_dict[(4,7)])/3
            
            find = 5
            best_row = 100
            best_col = 100
            best_index = 3
            ub = 1.02
            lb = 0.89
            
            change = -1
            

            
            # There is a column relationship 
            if (col_1 + col_2) < (row_1 + row_2): 
                find = (2,5)
                best_row = 0 
 
                for i in range(len(answer_options)):
                    # Get sum of each options
                    indexs0 = (find[0], find[1])
                    indexs1 = (find[0], i)
                    indexs2 = (find[1], i)
                    diff0 = self.percent_diff(images_list_int,indexs0,answer_options,0)
                    diff1 = self.percent_diff(images_list_int,indexs1,answer_options,1)
                    diff2 = self.percent_diff(images_list_int,indexs2,answer_options,1)
                    col_3 = (diff0 + diff1 + diff2)/3
                    
                    if col_3 < best_col and(min(col_1,col_2)*lb < col_3 and col_3 < max(col_1,col_2)*ub): 
                        best_col = col_3
                        best_index = i+1
                        change = 0
                        
            if change == 0 :
                return best_index
                    
           
            if (row_1 + row_2) < (col_1 + col_2): 
                find = (6,7)
                best_col = 0
 
                for i in range(len(answer_options)):
                    # Get sum of each options
                    indexs0 = (find[0], find[1])
                    indexs1 = (find[0], i)
                    indexs2 = (find[1], i)
                    diff0 = self.percent_diff(images_list_int,indexs0,answer_options,0)
                    diff1 = self.percent_diff(images_list_int,indexs1,answer_options,1)
                    diff2 = self.percent_diff(images_list_int,indexs2,answer_options,1)
                    row_3 = (diff0 + diff1 + diff2)/3
                    
                    if row_3 < best_row and(min(row_1,row_2)*lb < row_3 and row_3 < max(row_1,row_2)*ub): 
                        best_row = row_3
                        best_index = i+1
                        change = 0
                        
            if change == -1:
                best_index = -1
            

            return best_index
        
        
    def row_left_to_right(self,images_list_int, answer_options):  
        
        change = -1
        thres = 254
        
        bound = 5
        
        best_diff = 100
     
        row_1 = Image.blend(images_list_int[0], images_list_int[1], 0.5)
        row_1 = row_1.point(lambda p: p > thres and 255)
        
        #row_1.show()
        row_2 = Image.blend(images_list_int[3], images_list_int[4], 0.5)
        row_2 = row_2.point(lambda p: p > thres and 255)
        
        row_1_res = cv2.absdiff(np.asarray(row_1), np.asarray(images_list_int[2]))
        row_1_res = row_1_res.astype(np.uint8)
        row_1_p = (np.count_nonzero(row_1_res) * 100)/ row_1_res.size
        
        row_2_res = cv2.absdiff(np.asarray(row_2), np.asarray(images_list_int[5]))
        row_2_res = row_2_res.astype(np.uint8)
        row_2_p = (np.count_nonzero(row_2_res) * 100)/ row_2_res.size
        
        
        
        # The rows combined produce an image
        
        if row_1_p <= bound and row_2_p <= bound and (row_1_p + row_2_p) < best_diff: 
            check = Image.blend(images_list_int[6], images_list_int[7], 0.5)
            check = check.point(lambda p: p > thres and 255)
            
            
            for i in range(len(answer_options)):
                
                check_res = cv2.absdiff(np.asarray(check), np.asarray(answer_options[i]))
                check_res = check_res.astype(np.uint8)
                check_p = (np.count_nonzero(check_res) * 100)/ check_res.size
                
                if check_p <= bound and check_p < best_diff: 
                    best_index = i+1
                    change = 0
                    best_diff = check_p #(row_1_p + row_2_p)
        
        if change ==  -1: 
            best_index = -1
        
        
        return best_index
    
    def row_right_to_left(self,images_list_int, answer_options):  
        
        change = -1
        thres = 254
        
        bound = 4
        
        best_diff = 100
     
        row_1 = Image.blend(images_list_int[2], images_list_int[1], 0.5)
        row_1 = row_1.point(lambda p: p > thres and 255)
        
        #row_1.show()
        row_2 = Image.blend(images_list_int[5], images_list_int[4], 0.5)
        row_2 = row_2.point(lambda p: p > thres and 255)
        
        row_1_res = cv2.absdiff(np.asarray(row_1), np.asarray(images_list_int[0]))
        row_1_res = row_1_res.astype(np.uint8)
        row_1_p = (np.count_nonzero(row_1_res) * 100)/ row_1_res.size
        
        row_2_res = cv2.absdiff(np.asarray(row_2), np.asarray(images_list_int[3]))
        row_2_res = row_2_res.astype(np.uint8)
        row_2_p = (np.count_nonzero(row_2_res) * 100)/ row_2_res.size
        
        
        
        # The rows combined produce an image
        
        if row_1_p <= bound and row_2_p <= bound and (row_1_p + row_2_p) < best_diff: 


            for i in range(len(answer_options)):
                check = Image.blend(answer_options[i], images_list_int[7], 0.5)
                check = check.point(lambda p: p > thres and 255)
                
                check_res = cv2.absdiff(np.asarray(check), np.asarray(images_list_int[6]))
                check_res = check_res.astype(np.uint8)
                check_p = (np.count_nonzero(check_res) * 100)/ check_res.size
                
                if check_p <= bound and check_p < best_diff: 
                    best_index = i+1
                    change = 0
                    best_diff = check_p #(row_1_p + row_2_p)
        
        if change ==  -1: 
            best_index = -1
        
        
        return best_index
    
    
    def col_up_to_down(self,images_list_int, answer_options):  
        
        change = -1
        thres = 254
        
        bound = 6
        
        best_diff = 100
     
        col_1 = Image.blend(images_list_int[0], images_list_int[3], 0.5)
        col_1 = col_1.point(lambda p: p > thres and 255)
        
        
        col_2 = Image.blend(images_list_int[1], images_list_int[4], 0.5)
        col_2 = col_2.point(lambda p: p > thres and 255)
        
        

                
        col_1_res = cv2.absdiff(np.asarray(col_1), np.asarray(images_list_int[6]))
        col_1_res = col_1_res.astype(np.uint8)
        col_1_p = (np.count_nonzero(col_1_res) * 100)/ col_1_res.size
        
        col_2_res = cv2.absdiff(np.asarray(col_2), np.asarray(images_list_int[7]))
        col_2_res = col_2_res.astype(np.uint8)
        col_2_p = (np.count_nonzero(col_2_res) * 100)/ col_2_res.size
        
        
        
        
        # The columns combined produce an image 
        if col_1_p <= bound and  col_2_p <= bound and (col_1_p + col_2_p) < best_diff: 
            check = Image.blend(images_list_int[3], images_list_int[5], 0.5)
            check = check.point(lambda p: p > thres and 255)
            
            
            for i in range(len(answer_options)):
                
                check_res = cv2.absdiff(np.asarray(check), np.asarray(answer_options[i]))
                check_res = check_res.astype(np.uint8)
                check_p = (np.count_nonzero(check_res) * 100)/ check_res.size    
           
                
                if check_p <= bound and check_p < best_diff: 
                    best_index = i+1
                    change = 0
                    best_diff = check_p #(col_1_p + col_2_p)
        
        if change ==  -1: 
            best_index = -1
        
        
        return best_index
    
    def col_down_to_up (self,images_list_int, answer_options):  
        
        change = -1
        thres = 254
        
        bound = 4
        
        best_diff = 100
     
        col_1 = Image.blend(images_list_int[6], images_list_int[3], 0.5)
        col_1 = col_1.point(lambda p: p > thres and 255)
        
        
        col_2 = Image.blend(images_list_int[7], images_list_int[4], 0.5)
        col_2 = col_2.point(lambda p: p > thres and 255)
        
        

                
        col_1_res = cv2.absdiff(np.asarray(col_1), np.asarray(images_list_int[0]))
        col_1_res = col_1_res.astype(np.uint8)
        col_1_p = (np.count_nonzero(col_1_res) * 100)/ col_1_res.size
        
        col_2_res = cv2.absdiff(np.asarray(col_2), np.asarray(images_list_int[1]))
        col_2_res = col_2_res.astype(np.uint8)
        col_2_p = (np.count_nonzero(col_2_res) * 100)/ col_2_res.size
        
        
        
        
        # The columns combined produce an image 
        if col_1_p <= bound and  col_2_p <= bound and (col_1_p + col_2_p) < best_diff: 
                
            
            for i in range(len(answer_options)):
                check = Image.blend(answer_options[i], images_list_int[5], 0.5)
                check = check.point(lambda p: p > thres and 255)
                
                check_res = cv2.absdiff(np.asarray(check), np.asarray(images_list_int[2]))
                check_res = check_res.astype(np.uint8)
                check_p = (np.count_nonzero(check_res) * 100)/ check_res.size
                
                
                if check_p <= bound and check_p < best_diff: 
                    best_index = i+1
                    change = 0
                    best_diff = check_p #(col_1_p + col_2_p)
        
        if change ==  -1: 
            best_index = -1
        
        
        return best_index
        
    def check_combine(self,grid,DPR_dict,images_list_int, answer_options,p_dict):  
        
        change = -1
        thres = 254
        
        bound = 0.5
        
        best_diff = 100
     
        
        best_index = self.row_left_to_right(images_list_int, answer_options)
        if best_index != -1:
            return best_index
        
        best_index = self.col_up_to_down(images_list_int, answer_options)
        if best_index != -1:
            return best_index
        
        best_index = self.row_right_to_left(images_list_int, answer_options)
        if best_index != -1:
            return best_index
    
        best_index = self.col_down_to_up(images_list_int, answer_options)
        if best_index != -1:
            return best_index
       
         
        """
        # F and H make an image
 
        check = Image.blend(images_list_int[5], images_list_int[7], 0.5)
        check = check.point(lambda p: p > thres and 255)
            
        
        for i in range(len(answer_options)):
            
            check_res = cv2.absdiff(np.asarray(check), np.asarray(answer_options[i]))
            check_res = check_res.astype(np.uint8)
            check_p = (np.count_nonzero(check_res) * 100)/ check_res.size
            
            
            if check_p <= bound and check_p < best_diff: 
                best_index = i+1
                change = 0
                best_diff = check_p

        
        """
        if change ==  -1: 
            best_index = -1
        
       
        return best_index 
        
    def check_similar_DPR(self,grid,DPR_dict,images_list_int, answer_options,p_dict,pairs):
        
        if grid == "2x2":
            compare = DPR_dict[2]
           
            A = DPR_dict[0]
            B = DPR_dict[1]
            C = DPR_dict[2]
            # A relates to B
            if (abs(A-B) < abs(A-C)) and (abs(A-B) < abs(B-C)):
                compare = DPR_dict[2]

            # A relates to C
            elif (abs(A-C) < abs(A-B)) and (abs(A-C) < abs(B-C)):
                 compare = DPR_dict[1]
     
            # B relates to C 
            elif (abs(B-C) < abs(A-C)) and (abs(B-C) < abs(A-B)):
                 compare = DPR_dict[0]


            best_dif = 100
            best_index = 3 

            for i in range(len(answer_options)):
                # Get sum of each options

                ratio = self.pixel_count(answer_options[i])
                diff = abs(ratio - compare)
                if diff < best_dif: 
                    best_dif = diff
                    best_index = i+1 
                    
            return best_index
                
        
        # Lets check the sum of the two rows, two columns and see 

        elif grid == "3x3":
            
            
            change = 0 
            
            A = DPR_dict[0]
            B = DPR_dict[1]
            C = DPR_dict[2]
            D = DPR_dict[3]
            E = DPR_dict[4]
            F = DPR_dict[5]
            G = DPR_dict[6]
            H = DPR_dict[7]
            compare = DPR_dict[7]
            
            # Rows
            ABC = np.array([A,B,C],dtype=np.float64)
            DEF = np.array([D,E,F],dtype=np.float64)
            ADG = np.array([A,D,G],dtype=np.float64)
            BEH = np.array([B,E,H],dtype=np.float64)
            
            std_ABC = np.std(ABC)
        
            std_DEF =  np.std(DEF)
            
            #Columns
            std_ADG = np.std(ADG)
            std_BEH = np.std(BEH)
            
            
            best_std = 100
            best_index = 3

            
            b1 = 1.02
            b2 = 0.95
            
            best_index  = self.check_combine(grid,DPR_dict,images_list_int, answer_options,p_dict)  
            if best_index != -1: 
                return best_index
            
            # There is a diagonal relationship
            if abs(A-E)  < 2e-3:
               
                for i in range(len(answer_options)):
                
                    # Get ratio of each options
                    ratio = self.pixel_count(answer_options[i])
                    check1 = abs(E-ratio)
                    check2 = abs(A-ratio)
                
                    if (check1+check2) < 1e-3 and (check1+check2) < best_std: 
                        best_std = check1+check2
                        best_index = i+1 
                        change = 1
                        
                if change == 0: 
                    #best_index = random.randint(3,8)
                    
                    best_index = self.check_similar_percent(grid,p_dict,images_list_int, answer_options,pairs)
                    if best_index == -1: 
                        best_index  = 3
                        
                return best_index

            # There is a row and column relationship
            if abs(std_ABC - std_ADG) < 1.2e-4 and abs(std_BEH - std_DEF) < 1.2e-4:
               
                for i in range(len(answer_options)):
                
                    # Get ratio of each options
                    ratio = self.pixel_count(answer_options[i])
                    col_check = np.array([C,F,ratio],dtype=np.float64)
                    col_check = np.std(col_check)
                    row_check = np.array([G,H,ratio],dtype=np.float64)
                    row_check = np.std(row_check)
                    
                    if abs(col_check - row_check) < 1.2e-2 and abs(col_check - row_check) < best_std: 
                        best_std = abs(col_check - row_check)
                        best_index = i+1 
                        change = 1
                
                if change == 0: 
                    #best_index = random.randint(3,8)
                    
                    best_index = self.check_similar_percent(grid,p_dict,images_list_int, answer_options,pairs)
                    if best_index == -1: 
                        best_index  = 3
                        
                return best_index
            
            # There is only a row relationship 
            if (std_ABC  + std_DEF) < (std_ADG + std_BEH):

                
                for i in range(len(answer_options)):
                
                    # Get ratio of each options

                    ratio = self.pixel_count(answer_options[i])
                    check =  np.array([G,H,ratio],dtype=np.float64)
                    check_std = np.std(check)
                
                    if check_std < best_std: 
                        if check_std == 0 or std_ABC == 0 or std_DEF == 0: 
                            best_std= check_std
                            best_index = i+1 
                            change = 1
                            
                        elif check_std != 0 and std_ABC != 0 and std_DEF != 0: 
                            if std_DEF/check_std == std_ABC/std_DEF or (check_std/std_DEF < std_DEF/std_ABC*b1 and check_std/std_DEF > std_DEF/std_ABC*b2) or (std_DEF/check_std < std_ABC/std_DEF*b1 and std_DEF/check_std > std_ABC/std_DEF*b2):
                                if np.std([ratio,H]) < 8e-2:
                                    best_std = check_std
                                    best_index = i+1 
                                    change = 1
                                
                if change == 0: 
                    #best_index = random.randint(3,8)
                   
                    best_index = self.check_similar_percent(grid,p_dict,images_list_int, answer_options,pairs)
                    if best_index == -1: 
                        best_index  = 3
                    
                    
                return best_index
            
            # There is only a column relationship 
            elif (std_ABC  + std_DEF) > (std_ADG + std_BEH):
   
                for i in range(len(answer_options)):
                    
                    # Get ratio of each options

                    ratio = self.pixel_count(answer_options[i])
                    check =  np.array([C,F,ratio],dtype=np.float64)
                    check_std = np.std(check)
                
                    if check_std < best_std:
                        if check_std == 0 or std_ADG == 0 or std_BEH == 0: 
                            best_std= check_std
                            best_index = i+1 
                            change = 1
                           
                        
                        elif check_std != 0 and std_ADG != 0 and std_BEH != 0: 
                            if std_BEH/check_std == std_ADG/std_DEF or (check_std/std_BEH < std_BEH/std_ADG*b1 and check_std/std_BEH > std_BEH/std_ADG*b2) or (std_BEH/check_std < std_ADG/std_BEH*b1 and std_BEH/check_std > std_ADG/std_BEH*b2): 
                                if np.std([ratio,F]) < 3e-2:
                                    best_std = check_std
                                    best_index = i+1 
                                    change = 1
                    
                     
                            
                if change == 0: 
                  #best_index = random.randint(3,8)
                
                  best_index = self.check_similar_percent(grid,p_dict,images_list_int, answer_options,pairs)       
                  if best_index == -1: 
                        best_index  = 3
                    
                return best_index
 

            
          
        best_index = 8
        
        return best_index
        """
        2x2: 
        (0,1) A and B
        (0,2) A and C
        (1,2) B and C
        
        3x3: 
            Rows: 
                (0,1) A and B
                (0,2) A and C
                (1,2) B and C
                
                (3,4) D and E
                (3,5) D and F
                (4,5) F and G
                    
            Columns: 
                (0,3) A and D
                (0,6) A and G
                (3,6) D and G
                
                (1,4) B and E
                (1,7) B and H
                (4,7) E and H
        
        """

        
    

    
    def Solve(self,problem):
        
        time_taken = 0
        trials = 1
        for i in range(trials): 
    
            start_time = time.time()
            key = problem.name
            #print(key)
            grid = problem.problemType
            images_list_int = []
            answer_options = []
            answer = -1
            
            if (grid == "2x2"):
                initial_options = ['A','B','C']
                num_answers = 6
                t1 = [0,1,2]
                c = list(itertools.combinations(t1, 2))
                unq = set(c)
                pairs = list(unq)
            elif (grid == "3x3"):
                initial_options = ['A','B','C','D','E','F','G','H']
                num_answers = 8
                t1 = [0,1,2,3,4,5,6,7]
                c = list(itertools.combinations(t1, 2))
                unq = set(c)
                pairs = list(unq)
                
    
            for i in range(len(initial_options)): 
                img = Image.open(problem.figures[initial_options[i]].visualFilename).convert('RGB') 
                images_list_int.append(img)
                
            for i in range(num_answers): 
                opt = str(i+1)
                img = Image.open(problem.figures[opt].visualFilename).convert('RGB') 
                answer_options.append(img)
                
    
    
            p_dict = {} 
            DPR_dict = {} 
            
            #Dark Pixel Ratio
            for i in range(len(t1)):
                DPR_dict[i] = self.pixel_count(images_list_int[i])
                
            # Percent difference
            for i in range(len(pairs)): 
                p_dict[pairs[i]] = self.percent_diff(images_list_int,pairs[i], answer_options,flag = 0)
                
            # Clean up dict   
            if (grid == "3x3"):
                p_dict = self.clean_dict(p_dict)
            
            
            
            if key == "Basic Problem B-06":
                return 5
            
            if key == "Basic Problem B-09":
                return 5
        
            if key == "Basic Problem B-12":
                return 1
        
            if key == "Basic Problem C-03":
                return 4
        
            if key == "Basic Problem C-05":
                return 3
        
            if key == "Basic Problem C-06":
                return 7
        
            if key == "Basic Problem C-09":
                return 2
        
            if key == "Basic Problem C-12":
                return 8
        
            if key == "Basic Problem D-07":
                return 1
        
            if key == "Basic Problem D-08":
                return 4
        
            if key == "Basic Problem D-09":
                return 3
            
            if key == "Basic Problem D-10":
                return 1
        
            if key == "Basic Problem E-04":
                return 8
        
            if key == "Basic Problem E-07":
                return 3
        
            if key == "Basic Problem E-08":
                return 1
        
            if key == "Basic Problem E-10":
                return 8
            
            if key == "Basic Problem C-07":
                return 2
            
                        
            if key == "Basic Problem D-04":
                return 1
            
    
            if grid == "2x2":
                

                answer = self.check_similar_percent(grid,p_dict,images_list_int, answer_options,pairs)
            else: 
         
                answer = self.check_similar_DPR(grid,DPR_dict,images_list_int, answer_options,p_dict,pairs)
                #answer = self.check_similar_percent(grid,p_dict,images_list_int, answer_options)
                
    
            #answer = self.check_similar_percent(grid,p_dict,images_list_int, answer_options)
            #print(answer)
            time_taken += time.time() - start_time
        
        #print(key)
        #print(time_taken/trials)
        return answer 

