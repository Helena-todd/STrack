import cv2
import math # to compute cosinus of angles
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from skimage import io
import sys
import glob
# scipy package to compute distance between matrices of cell centroid coordinates
from scipy.spatial.distance import cdist
# skimage package to identify objects, export region properties
from skimage.measure import label, regionprops, regionprops_table

# List files in current folder
files_list = sorted(glob.glob("*.tif"))

# Get variables from system env
max_dist = sys.argv[1]
max_angle = sys.argv[2]
output_dir = sys.argv[3]

for tp in range(1,len(files_list)):
    #print('Tp is ', tp)
    # Add a 0 in front of tp if contains only one number
    tp0 = '%02d' % (tp-1,)
    tp1 = '%02d' % (tp,)
    # Import image corresponding to timepoint tp and tp-1
    print('Processing file ', files_list[tp])
    img1 = io.imread(files_list[tp])
    img0 = io.imread(files_list[tp-1])
    
 
    # See how many cells were identified in the images (ranged in the "unique" vectors)
    unique1, counts1 = np.unique(img1, return_counts=True)
    # In registered images, it can happen that one cell gets skipped in the unique1 array, which leads to number of cells in unique1 and counts1 NOT MATCHING the unique1 indices. I thus create a unique11 array with continuous cell indices, to be used to track daughters that are still unmatched.
    unique11 = np.array(range(0, len(unique1)))
    unique0, counts0 = np.unique(img0, return_counts=True)
    unique01 = np.array(range(0, len(unique0)))
    
    ############################################################
    # compute the mask centroids of all cells in img0 and img1 #
    ############################################################
    my_array0 = np.empty((0,2), int)
    for mask_tmp in unique0[1:]:
        # Keep only current mask, replace all other values by 0
        img_tmp = np.where(img0 != mask_tmp, 0, img0)
    
        # compute cell centroid
        M = cv2.moments(img_tmp)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        my_array0=np.append(my_array0,[[cx,cy]], axis=0)
    
    my_array1 = np.empty((0,2), int)
    for mask_tmp in unique1[1:]: # [:1] because I'm not interested in pixels with a value of 0: the background
        # Keep only current mask, replace all other values by 0
        img_tmp = np.where(img1 != mask_tmp, 0, img1)
    
        # compute cell centroid
        M = cv2.moments(img_tmp)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        my_array1=np.append(my_array1,[[cx,cy]], axis=0)
    
    ########################################################################################
    # Compute distances between 2 matrices (in a similar way to R's pdist::pdist function) #
    ########################################################################################
    dist_mat = cdist(my_array0, my_array1)
    
    #################################################################################
    # Compute percentage of matching pixels between masks in img0 and masks in img1 #
    #################################################################################
    # Create empty array, has as many columns as number of cells in img1
    matching_pctgs = np.empty((0,len(unique1)-1), int)

    # Loop over masks in img0
    for idx0 in unique01[:len(unique01)-1]:
        # Keep only current mask, replace all other values by 0
        img_tmp0 = np.where(img0 != unique0[1:][idx0], 0, img0)
    
        # Loop over masks in img1 that are close enough to the current cell in img0
        distances_to_mother = dist_mat[idx0,:]
        line_tmp = np.zeros(len(distances_to_mother)) # create an empty array that will store final percentages
        indices1 = np.where(distances_to_mother <= int(max_dist))
        
        for idx1 in indices1[0]:
            # Keep only current mask, replace all other values by 0
            img_tmp1 = np.where(img1 != unique1[1:][idx1], 0, img1)
        
            # flatten both images, replace all non 0 values by 1
            img_flattened0 = img_tmp0.flatten()
            img_flattened0[img_flattened0 != 0] = 1
            img_flattened1 = img_tmp1.flatten()
            img_flattened1[img_flattened1 != 0] = 1
            # change integers to floats
            img_flattened0 = img_flattened0.astype('float')
            img_flattened1 = img_flattened1.astype('float')
            # replace 0 in previous frame by NaN so that they don't correpond to 0 in current frame
            img_flattened0[img_flattened0 == 0] = 'nan'
            # compute difference between mask in current frame and mask in previous frame
            img_differences = (img_flattened0==img_flattened1)
            # compute percentage of pixels in current masks that match with mask in previous frame
            pctg_matching = (len(img_differences[img_differences==True]))/(len(img_flattened1[img_flattened1!=0]))*100
            # add current pctg matching value to the line for current mask in img0 and in img1
            line_tmp[idx1] = pctg_matching
           
        # Fill in complete line of matching pctgs for current mask in img0
        matching_pctgs = np.append(matching_pctgs, [line_tmp], axis=0)
    
    ##############################################################
    # Compute orientation of the main axis of cell masks in img0 #
    ##############################################################
    # Create an empty array to store cell orientations
    orientations = np.array([])

    # Loop over masks in img0
    for idx0 in unique0[1:]:
        # Keep only current mask, replace all other values by 0
        img_tmp0 = np.where(img0 != idx0, 0, img0)
        # Replace all values different from 0 by 1
        img_tmp0[img_tmp0 != 0] = 1
        # Compute regions
        regions = regionprops(img_tmp0)
        # The 'Orientation' property of REGIONPROPS returns the angle (in degrees)
        # between the x-axis and the major axis of the cell.
        # ranging from `-pi/2` to `pi/2` counter-clockwise
           
        # Fill in orientations vector
        orientations = np.append(orientations, math.degrees(regions[0].orientation)) # math.degrees allows to change radiants into degrees
    
    ###########################################################################################
    # Identify mother-daughter links according to highest pixel matching or distance matching #
    ###########################################################################################
    
    # Create empty result table
    complete_table = pd.DataFrame(columns=['Timepoint', 'Mask_nb', 'Centroid_x', 'Centroid_y',
                                          'Mother_mask', 'Pctg_matching', 'Centroid_x_mother',
                                           'Centroid_y_mother', 'Distance_to_mother'])

    # create vectors with cell indices to keep track of who's still in the tables as rows and columns are being removed
    daughters_still_in_table = unique11[1:]
    mothers_still_in_table = unique01[1:]

    # while there are still cells in the matching_pctgs array, search for mother-daughter links
    while matching_pctgs.size != 0:
        #print("daughters still in tables: ", daughters_still_in_table)
        #print("mothers still in tables: ", mothers_still_in_table)
        # if there are still overlapping cells in tp-1 and current tp
        if(np.amax(matching_pctgs) != 0):
            # find best match: the maximum overlap in the pctgs array
            tmp_match = np.where(matching_pctgs == np.amax(matching_pctgs))
            #print("tmp match [0][0] is ", tmp_match[0][0], " and tmp match [1][0] is ", tmp_match[1][0])
            #print(" pctg matching is ", np.amax(matching_pctgs))

            mother_tmp = mothers_still_in_table[tmp_match[0][0]]
            #print("mother tmp is ", mother_tmp)
            daughter_tmp = daughters_still_in_table[tmp_match[1][0]]
            #print("daughter tmp is ", daughter_tmp)
            # If the mother cell does not have daughters yet
            if (mother_tmp not in complete_table["Mother_mask"].values):
                # create link
                complete_table.loc[daughter_tmp] = [tp, # timepoint
                                                     daughter_tmp, # mask number
                                                     my_array1[daughter_tmp-1][0], # = cx
                                                     my_array1[daughter_tmp-1][1], # = cy
                                                     mother_tmp, # mother mask
                                                     np.amax(matching_pctgs), # pctg matching
                                                     my_array0[mother_tmp-1][0], # cx mother
                                                     my_array0[mother_tmp-1][1], # cy mother
                                                     dist_mat[tmp_match[0][0], tmp_match[1][0]]] # distance btw mother and daughter cell
                # remove daughter cell from matching_pctgs and dist_mat tables
                matching_pctgs = np.delete(matching_pctgs, tmp_match[1][0], 1)
                dist_mat = np.delete(dist_mat, tmp_match[1][0], 1)
                # also remove daughter cell from daughters_still_in_table array
                daughters_still_in_table = np.delete(daughters_still_in_table, tmp_match[1][0])
          
            # else, if the mother cell already has one daughter cell
            elif np.count_nonzero(complete_table["Mother_mask"].values == mother_tmp) == 1:
                # recover info on the cell that has already been asigned to the same mother
                other_daughter_line = complete_table.loc[complete_table['Mother_mask'] == mother_tmp]
                # compute angle between current cell's centroid and its hypothetic sister's centroid
                cell1_centroid = (other_daughter_line["Centroid_x"], other_daughter_line["Centroid_y"])
                cell2_centroid = (my_array1[daughter_tmp-1][0],my_array1[daughter_tmp-1][1])
                # Difference in x coordinates
                dx = cell2_centroid[0] - cell1_centroid[0]
                #print(" cell1 centroids are ", cell1_centroid)
                #print(" cell2 centroids are ", cell2_centroid)
                # Difference in y coordinates
                dy = cell2_centroid[1] - cell1_centroid[1]
                # Angle between cell1 and cell2 in radians
                theta = math.atan2(dy, dx)
                orientation_daughters = math.degrees(theta)
                #print("Orientation of division is ", orientation_daughters, " and its sign is ", np.sign(orientation_daughters + 90))
            
                # Re-scale daughters orientation so that it matches the scale of the mother orientation,
                # which allows to make the angles comparable
                if ((orientation_daughters >= -180) and (orientation_daughters <= -90)):
                    orientation_daughters = -orientation_daughters - 90
                elif ((orientation_daughters >= 0) and (orientation_daughters <= 90)):
                    orientation_daughters = 90 - orientation_daughters
                elif ((orientation_daughters > -90) and (orientation_daughters < 0)):
                    orientation_daughters = -90 - orientation_daughters
                elif ((orientation_daughters > 90) and (orientation_daughters <= 180)):
                    orientation_daughters = - orientation_daughters + 90
                
                orientation_mother = orientations[mother_tmp-1]
                #print("Orientation of mother is ", orientation_mother, " and its sign is ", np.sign(orientation_mother))
                #print("Orientation of division AFTER RE-SCALING is ", orientation_daughters, " and its sign is ", np.sign(orientation_daughters))

                # Compute difference between 2 angles:
                # If they have the same sign, simply substact them
                if np.sign(orientation_mother) == np.sign(orientation_daughters):
                    diff_btw_angles = abs(orientation_mother - (orientation_daughters))
                # If they have opposite signs, sum up their absolute values
                else:
                    diff_btw_angles = abs(orientation_mother) + abs((orientation_daughters))

                # If angle between mother cell orientation and division into 2 daughters is small enough, add daughter cell link
                #print("difference between angles is ", diff_btw_angles)
                if(diff_btw_angles < int(max_angle)):
                    #print("Angle is small enough, daughter cell will be added")
                    complete_table.loc[daughter_tmp] = [tp, # timepoint
                                                         daughter_tmp, # mask number
                                                         my_array1[daughter_tmp-1][0], # = cx
                                                         my_array1[daughter_tmp-1][1], # = cy
                                                         mother_tmp, # mother mask
                                                         np.amax(matching_pctgs), # pctg matching
                                                         my_array0[mother_tmp-1][0], # cx mother
                                                         my_array0[mother_tmp-1][1], # cy mother
                                                         dist_mat[tmp_match[0][0], tmp_match[1][0]]] # distance btw mother and daughter cell
                    # remove daughter cell from matching_pctgs and dist_mat tables
                    matching_pctgs = np.delete(matching_pctgs, tmp_match[1][0], 1)
                    dist_mat = np.delete(dist_mat, tmp_match[1][0], 1)
                    # also remove daughter cell from daughters_still_in_table array
                    daughters_still_in_table = np.delete(daughters_still_in_table, tmp_match[1][0])
                    # remove mother cell from matching_pctgs and dist_mat tables
                    matching_pctgs = np.delete(matching_pctgs, tmp_match[0][0], 0)
                    dist_mat = np.delete(dist_mat, tmp_match[0][0], 0)
                    # also remove mother cell from mothers_still_in_table array
                    mothers_still_in_table = np.delete(mothers_still_in_table, tmp_match[0][0])
                else:
                    # if angle between mother cell and its 2 possible daughter cells is too large,
                    # remove the tmp_match from the dist_mat and pctgs_matching tables because
                    # this mother-daughter link cannot exist
                    #print("Angle is too large, removing this mother-daughter combination from the tables")
                    #print(" matching_pctgs is ", matching_pctgs)
                    #print("tmp mother is ", tmp_match[0][0], " and tmp daughter is ", tmp_match[1][0])
                    matching_pctgs[tmp_match[0][0],tmp_match[1][0]] = 0

            
            # else, if the mother cell already has more than one daughter cell (should never happen)
            else:
                print("Rows haven't been deleted properly and one mother cell has been assigned more than 2 daughter cells")
        # else if there are no more overlapping cells, look at distances
        else:
            # if all matching_pctgs == 0
            #print("No more overlapping cells, look at distances to match remaining cells, or assign new tracks to them")
            # find best match: the minimum distance in the dist matrix
            tmp_match = np.where(dist_mat == np.amin(dist_mat))
            #print("tmp match [0][0] is ", tmp_match[0][0], " and tmp match [1][0] is ", tmp_match[1][0])
            #print(" dist_mat is ", np.amin(dist_mat))

            mother_tmp = mothers_still_in_table[tmp_match[0][0]]
            #print("mother tmp is ", mother_tmp)
            daughter_tmp = daughters_still_in_table[tmp_match[1][0]]
            #print("daughter tmp is ", daughter_tmp)

            # If the distance between mother and daughter is small enough
            if (dist_mat[tmp_match[0][0], tmp_match[1][0]] < int(max_dist)):

                # If the mother cell does not have daughters yet
                if (mother_tmp not in complete_table["Mother_mask"].values):
                    # create link
                    complete_table.loc[daughter_tmp] = [tp, # timepoint
                                                             daughter_tmp, # mask number
                                                             my_array1[daughter_tmp-1][0], # = cx
                                                             my_array1[daughter_tmp-1][1], # = cy
                                                             mother_tmp, # mother mask
                                                             0, # pctg matching
                                                             my_array0[mother_tmp-1][0], # cx mother
                                                             my_array0[mother_tmp-1][1], # cy mother
                                                             dist_mat[tmp_match[0][0], tmp_match[1][0]]] # distance btw mother and daughter cell
                    # remove daughter cell from matching_pctgs and dist_mat tables
                    matching_pctgs = np.delete(matching_pctgs, tmp_match[1][0], 1)
                    dist_mat = np.delete(dist_mat, tmp_match[1][0], 1)
                    # also remove daughter cell from daughters_still_in_table array
                    daughters_still_in_table = np.delete(daughters_still_in_table, tmp_match[1][0])

                # else, if the mother cell already has one daughter cell
                elif np.count_nonzero(complete_table["Mother_mask"].values == mother_tmp) == 1:
                    # recover info on the cell that has already been asigned to the same mother
                    other_daughter_line = complete_table.loc[complete_table['Mother_mask'] == mother_tmp]
                    # compute angle between current cell's centroid and its hypothetic sister's centroid
                    cell1_centroid = (other_daughter_line["Centroid_x"], other_daughter_line["Centroid_y"])
                    cell2_centroid = (my_array1[daughter_tmp-1][0],my_array1[daughter_tmp-1][1])
                    # Difference in x coordinates
                    dx = cell2_centroid[0] - cell1_centroid[0]
                    #print(" cell1 centroids are ", cell1_centroid)
                    #print(" cell2 centroids are ", cell2_centroid)
                    # Difference in y coordinates
                    dy = cell2_centroid[1] - cell1_centroid[1]
                    # Angle between cell1 and cell2 in radians
                    theta = math.atan2(dy, dx)
                    orientation_daughters = math.degrees(theta)
                    orientation_mother = orientations[mother_tmp-1]
                    #print("Orientation of mother is ", orientation_mother, " and its sign is ", np.sign(orientation_mother))
                    #print("Orientation of division is ", orientation_daughters, " and its sign is ", np.sign(orientation_daughters))

                    # Re-scale daughters orientation so that it matches the scale of the mother orientation,
                    # which allows to make the angles comparable
                    if ((orientation_daughters >= -180) and (orientation_daughters <= -90)):
                        orientation_daughters = -orientation_daughters - 90
                    elif ((orientation_daughters >= 0) and (orientation_daughters <= 90)):
                        orientation_daughters = 90 - orientation_daughters
                    elif ((orientation_daughters > -90) and (orientation_daughters < 0)):
                        orientation_daughters = -90 - orientation_daughters
                    elif ((orientation_daughters > 90) and (orientation_daughters <= 180)):
                        orientation_daughters = - orientation_daughters + 90

                    #print("Orientation of division AFTER RESCALING is ", orientation_daughters, " and its sign is ", np.sign(orientation_daughters))

                    # Compute difference between 2 angles:
                    # If they have the same sign, simply substact them
                    if np.sign(orientation_mother) == np.sign(orientation_daughters):
                        diff_btw_angles = abs(orientation_mother - (orientation_daughters))
                    # If they have opposite signs, sum up their absolute values
                    else:
                        diff_btw_angles = abs(orientation_mother) + abs((orientation_daughters))

                    # If angle between mother cell orientation and division into 2 daughters is small enough, add daughter cell link
                    #print("difference between angles is ", diff_btw_angles)
                    if(diff_btw_angles < int(max_angle)):
                        #print("Angle is small enough, daughter cell will be added")
                        complete_table.loc[daughter_tmp] = [tp, # timepoint
                                                             daughter_tmp, # mask number
                                                             my_array1[daughter_tmp-1][0], # = cx
                                                             my_array1[daughter_tmp-1][1], # = cy
                                                             mother_tmp, # mother mask
                                                             np.amax(matching_pctgs), # pctg matching = 0
                                                             my_array0[mother_tmp-1][0], # cx mother
                                                             my_array0[mother_tmp-1][1], # cy mother
                                                             dist_mat[tmp_match[0][0], tmp_match[1][0]]] # distance btw mother and daughter cell
                        # remove daughter cell from matching_pctgs and dist_mat tables
                        matching_pctgs = np.delete(matching_pctgs, tmp_match[1][0], 1)
                        dist_mat = np.delete(dist_mat, tmp_match[1][0], 1)
                        # also remove daughter cell from daughters_still_in_table array
                        daughters_still_in_table = np.delete(daughters_still_in_table, tmp_match[1][0])
                        # remove mother cell from matching_pctgs and dist_mat tables
                        matching_pctgs = np.delete(matching_pctgs, tmp_match[0][0], 0)
                        dist_mat = np.delete(dist_mat, tmp_match[0][0], 0)
                        # also remove mother cell from mothers_still_in_table array
                        mothers_still_in_table = np.delete(mothers_still_in_table, tmp_match[0][0])
                    else:
                        # if angle between mother cell and its 2 possible daughter cells is too large,
                        # remove the tmp_match from the dist_mat and pctgs_matching tables because
                        # this mother-daughter link cannot exist
                        #print("Angle is too large, removing this mother-daughter combination from the tables")
                        #print(" matching_pctgs is ", matching_pctgs)
                        #print("tmp mother is ", tmp_match[0][0], " and tmp daughter is ", tmp_match[1][0])
                        dist_mat[tmp_match[0][0],tmp_match[1][0]] = 1000 # set distance to an extremely high value so it never gets picked again

            # if distance between mother and daughter cell is too large, create a new track
            else:
                complete_table.loc[daughter_tmp] = [tp, # timepoint
                                                             daughter_tmp, # mask number
                                                             my_array1[daughter_tmp-1][0], # = cx
                                                             my_array1[daughter_tmp-1][1], # = cy
                                                             0, # mother mask
                                                             np.amax(matching_pctgs), # pctg matching = 0
                                                             my_array1[daughter_tmp-1][0], # cx mother = cx
                                                             my_array1[daughter_tmp-1][1], # cy mother = cy
                                                             dist_mat[tmp_match[0][0], tmp_match[1][0]]] # distance btw mother and daughter cell
                # remove daughter cell from matching_pctgs and dist_mat tables
                matching_pctgs = np.delete(matching_pctgs, tmp_match[1][0], 1)
                dist_mat = np.delete(dist_mat, tmp_match[1][0], 1)
                # also remove daughter cell from daughters_still_in_table array
                daughters_still_in_table = np.delete(daughters_still_in_table, tmp_match[1][0])

    
    
    ##########################################################################
    # Export tracking info and matching cells info for the current timepoint #
    ##########################################################################
    complete_table.to_csv(output_dir + f"tracking_table_time{tp}.csv")
    
    ################################################################
    # Export corresponding image with tracking info plotted on top #
    ################################################################
    plt.figure(figsize=(10, 10))
    ax = plt.gca()
    im = ax.imshow(img1)
    nb_cells = complete_table.shape[0]
    if(nb_cells != 1):
        complete_table.index = list(range(1, nb_cells+1))
    for row_idx in range(1,nb_cells+1):
        # draw vertical line from (70,100) to (70, 250)
        plt.plot([complete_table.loc[row_idx]['Centroid_x_mother'], complete_table.loc[row_idx]['Centroid_x']], [complete_table.loc[row_idx]['Centroid_y_mother'], complete_table.loc[row_idx]['Centroid_y']], 'r-', lw=2)
    #plt.show()
    plt.savefig(output_dir + f"tracking_figure_time{tp}.png")
