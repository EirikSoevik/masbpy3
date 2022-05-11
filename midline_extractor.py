import os

import numpy as np

from util import utils
import time
import util.plotting as uplt
import math
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

# def rib_approximator_setup(my_file, outdir, save, plotting, N_midline):
#
#     start_time = time.time()
#     coords = np.load(outdir + "/" + my_file + "/" + my_file + ".npy")
#     #coords = np.load(outdir+"/"+my_file)
#     centroid = utils.find_centroid(coords=coords,outdir=outdir,save=False)
#     midline_rib_approx = utils.midline_rib_approximation(coords, N_midline)
#     midline_angles, midline_angles_change = utils.midline_angles(midline_rib_approx)
#     #spline_x, my_spline = utils.midline_spline(midline=midline_rib_approx,spline_length=N_midline,interp_kind='quadratic')
#     from pathlib import Path
#     if save:
#         path_filename = Path(my_file)
#         my_file_nosuffix = str(path_filename.with_suffix(''))
#
#         if not os.path.exists(outdir):
#             os.makedirs(outdir)
#         #if not os.path.exists(outdir+"/images"):
#         #    os.makedirs(outdir + "/images")
#         #if not os.path.exists(outdir+"/"+my_file):
#         #    os.makedirs(outdir+"/"+my_file)
#
#         np.save(outdir+"/"+my_file_nosuffix+"/coords.npy",coords)
#         np.save(outdir+"/"+my_file_nosuffix+"/midline.npy", midline_rib_approx)
#         np.save(outdir+"/"+my_file_nosuffix+"/midline_angles.npy", midline_angles)
#         np.save(outdir+"/"+my_file_nosuffix+"/midline_angles_change.npy", midline_angles_change)
#         np.save(outdir+"/"+my_file_nosuffix+"/centroid.npy",centroid)
#         print("Saved " + outdir+"/"+my_file)
#     end_time = time.time()
#
#     if plotting:
#         uplt.rib_approx(coords=coords, rib_midline=midline_rib_approx, midline_angles=midline_angles,midline_angles_change=midline_angles_change)
#         #uplt.spline_plot(my_spline,coords,spline_x)
#     print("Finished processing " + my_file + " in {sec:2.4f} seconds".format(sec=end_time - start_time))
#
#
# if __name__ == "__main__":
#
#     #my_dir = "my_data/mask_output_Feb-17-2022_1216/masks/"
#     my_dir = "my_data/mask_output_april_Apr-27-2022_1618/masks"
#     dir_files = os.listdir(my_dir)
#     save = True # set to True to save all calculations, set to False to not save anything
#     N_midline = 20
#     plotting = False
#     start_time = time.time()
#     count = 0
#     for my_file in dir_files:
#         rib_approximator_setup(my_file=my_file, outdir=my_dir, save=save, plotting=plotting, N_midline=N_midline)
#         count += 1
#     end_time = time.time()
#     print("Finished midline_extractor.py, processing " + str(count) + " files in {sec:2.3f} seconds".format(sec=end_time-start_time))




## This is an attempt at finding the midline in a more robust way. It works but the results are less reliable  ###

import util.utils_unused as utils_unused

def main(my_file, outdir, save, plotting, N_midline=15):
    '''Midline extraction function: creates midline of fish and centroid from input geometry

     This function takes in a segmented mask generated by detectron2 and extracts the midline as well as
     geometric center. There are some variables, found below, that are available for fine tuning to get the desired
     results. The program works in the following way:

     Step 1:    Set variables as indicated
     Step 2:    Change size of input mask to less points
     Step 3:    Compute normal vectors with the new number of points and save
     Step 4:    Change size of coords and normals to better accomodate ma point calculations
     Step 5:    Calculate internal and external ma coords and save
     Step 6:    Calculate geometric center of mass (only needs input coords, unrelated to other steps)

    Variables that MUST be set:
        outdir  directory to save everything
        save    set to True to save everything, False to not save anything
        use_ma  set to True to use the masbpy.ma utility, set to False to use ma_mp utility. For calculating internal
                points

    Variables that CAN be changed (for optimization)
        norm_neighbours     number of neighbours used when calculating normal vectors
        N                   decrease coordinate vector by 1/N

        ma_mp variables:

        ma variables:
        denoise
        denoise_delta
        denoise_absmin
        detect_planar

     Variables that SHOULD NOT be changed:
        D                   dictionary for relevant data
        D['coords']         coordinates of fish mask
        D['normals']        normal vectors of unit length, corresponding to coordinate vectors
        D['angles']         angle in radians for each normal vector, from the x-axis
        D['ma_coords_in']   internal medial axis ball points, i.e. internal midpoints
        D['ma_coords_ext']  external medial axis ball points, i.e. external symmetry line (not so relevant here)
        D['ma_q_in']        don't know!
        D['ma_q_out']       don't know!

     Functions:
        elliptic_geom_maker    creates an elliptic geometry, used for testing on simple geometry


     '''
    start_time = time.time()
    D = {}
    #outdir = "mask_optimizer_dir/"
    #outdir = "my_data/masby_unused_output/"  # "simple_example/"

    use_ma = True
    #35/200
    neighbours = 20
    N_normals = 80  # Original length 400
    N_ma = 15
    plotting = True

    denoise = 30
    denoise_delta = 30
    detect_planar = 30

    denoise_absmin = 30
    denoise_min = 30

    # Might need to find more robust way of loading original coords
    D['coords'] = np.load(outdir + my_file + "/coords.npy")
    coords = np.load(outdir + my_file + "/coords.npy")

    # coords = D['coords']

    #Reduce number of elements and calculate normals
    D['coords_normals'] = utils_unused.array_decimator_set_len(outdir=outdir, input_array=D['coords'], new_len=N_normals,
                                                       save_name="coords_normals", save=True)
    D['normals_normals'] = utils_unused.compute_normals_my_func(coord=D['coords_normals'], outfile=outdir, k=neighbours)

    #MANUALLY TURNED OFF PLOTTING
    D_k = utils_unused.k_ma_iterator(input_coords=D['coords_normals'], input_normals=D['normals_normals'], N_ma=N_ma,
                             outdir=outdir,save=save,N_normals=N_normals, neighbours=neighbours,plotting=False)

    midlines_unfiltered = utils_unused.ma_points_fitter(D_k)
    #TODO: why is midlines_unfiltered changed when it should not be????
    midlines_filtered = utils_unused.ma_filter(midlines_unfiltered,coords)
    midlines_interpolated = utils_unused.midline_interpolation(midlines_filtered,N_midline-1)

    #midline_rib_approx = utils.midline_rib_approximation(coords, N_midline, save=save)
    #midline_angles, midline_angles_change = utils.midline_angles(midline_rib_approx, save=save)

    end_time = time.time()
    print("Calculations took : " + str(end_time - start_time) + " seconds")

    if plotting:
        #plt.plot(midline_angles * (180 / np.pi))
        #plt.show()
        #uplt.rib_approx(coords=coords, rib_midline=midline_rib_approx,midline_angles=midline_angles,midline_angles_change=midline_angles_change)
        uplt.midlines(midlines_unfiltered,midlines_filtered,midlines_interpolated,coords)
    if save:
        plt.savefig()
    print("Finished midline_extractor.py")

if __name__ == "__main__":


    #my_dir = "my_data/mask_output_Feb-17-2022_1216/masks/"
    my_dir = "my_data/mask_output_april_Apr-27-2022_1618/masks/"
    dir_files = os.listdir(my_dir)
    save = False # set to True to save all calculations, set to False to not save anything
    N_midline = 20
    plotting = False
    start_time = time.time()
    count = 0
    for my_file in dir_files:
        main(my_file=my_file, outdir=my_dir, save=save, plotting=plotting, N_midline=N_midline)
        count += 1
    end_time = time.time()
    print("Finished midline_extractor.py, processing " + str(count) + " files in {sec:2.3f} seconds".format(sec=end_time-start_time))
