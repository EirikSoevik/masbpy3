import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import time
import numpy as np
import matplotlib.animation as FuncAnimation


""" Plots available:

    - frame_output(coords_x, coords_y, midline_x, midline_y, centroid, frame)
    - midline_animation(x,y)
    - midline_animation_centroid(x, y,centroid)
    - body_midline_centroid_animation(coords_x, coords_y, midlines_x, midlines_y, centroid)
    - spline_plotting(my_splines,spline_x,coords_x, coords_y, midlines_x, midlines_y, centroid)
    - all_splines_plot(spline_x, my_splines, my_title, save_dir, save=False)
    - fourier_plot(f_x,f_y,N, my_title, save_dir, save=False)
    - fourier_animation(f_x, f_y,N)
    - fft_plot(fx, fy)
    - point_in_time(my_array, my_title, save_dir, pos=-1,save=False)
    - all_point_in_time(my_array, my_title, save_dir,save=False)
    - midlines_centroid_in_time(midline_x, midline_y,centroid)
    - histogram(l, my_title, save_dir, save=False)
    - simple_plot(vec, my_title, save_dir, save=False)
"""

def set_plot_position(x=3100,y=100,dx=2000,dy=900):
    """Sets plot position the desired position"""
    # set plot position
    # default is on the 3rd right screen, experiment with the values to get what you want, or comment out
    mngr = plt.get_current_fig_manager()
    # to put it into the upper left corner for example:
    mngr.window.setGeometry(x,y,dx,dy)

def frame_output(coords_x, coords_y, midline_x, midline_y, centroid, start_frame, end_frame, my_title, save, save_dir):

    figure, ax = plt.subplots(figsize=(10, 8))

    plt.plot(coords_x[start_frame,:],coords_y[start_frame,:], 'b-', label="start_pos")
    plt.plot(midline_x[start_frame,:],midline_y[start_frame,:],'r-', label="start midlines")
    plt.plot(centroid[start_frame,0], centroid[start_frame,1],  'bo', label="start centroid")
    plt.plot(coords_x[end_frame, :], coords_y[end_frame, :], 'b--', label="end pos")
    plt.plot(midline_x[end_frame, :], midline_y[end_frame, :],'r--', label="end midline")
    plt.plot(centroid[end_frame, 0], centroid[end_frame, 1],  'g*', label="end centroid")
    plt.legend()
    ax.set_aspect('equal',adjustable='datalim')
    plt.title(my_title)
    plt.xlabel("x-axis")
    plt.ylabel("y-axis")

    if save:
        plt.savefig(save_dir+"start_end_pos.png")


def midline_animation(x, y):

    rows, col = x.shape
    #fig = plt.figure()
    #ax = fig.add_subplot(111)
    #ax.set_aspect('equal', adjustable='datalim')

    plt.ion()
    figure, ax = plt.subplots(figsize=(10, 8))
    line1, = ax.plot(x[0,:],y[0,:])
    ax.set_aspect('equal',adjustable='datalim')
    plt.title("Midline frame 0 of " + str(rows))
    plt.xlabel("x-axis")
    plt.ylabel("y-axis")
    set_plot_position()

    for i in range(1,rows):
        line1.set_xdata(x[i,:])
        line1.set_ydata(y[i,:])
        plt.title("Midline frame " + str(i) +" of " + str(rows))
        figure.canvas.draw()

        figure.canvas.flush_events()

        time.sleep(0.1)


def midline_animation_centroid(x, y,centroid):

    rows, col = x.shape
    #fig = plt.figure()
    #ax = fig.add_subplot(111)
    #ax.set_aspect('equal', adjustable='datalim')

    plt.ion()
    figure, ax = plt.subplots(figsize=(10, 8))
    line1, = ax.plot(x[0,:],y[0,:])
    line2, = ax.plot(centroid[0,0], centroid[0,1],'ro')
    ax.set_aspect('equal',adjustable='datalim')
    plt.title("Midline")
    plt.xlabel("x-axis")
    plt.ylabel("y-axis")
    set_plot_position()

    for i in range(1,rows):

        line1.set_xdata(x[i,:])
        line1.set_ydata(y[i,:])
        line2.set_xdata(centroid[i,0])
        line2.set_ydata(centroid[i,1])

        figure.canvas.draw()

        figure.canvas.flush_events()

        time.sleep(0.1)


def body_midline_centroid_animation(coords_x, coords_y, midlines_x, midlines_y, centroid):


    rows, col = midlines_x.shape
    #fig = plt.figure()
    #ax = fig.add_subplot(111)
    #ax.set_aspect('equal', adjustable='datalim')

    plt.ion()
    figure, ax = plt.subplots(figsize=(10, 8))
    line1, = ax.plot(midlines_x[0,:],midlines_y[0,:], 'r*')
    line2, = ax.plot(centroid[0,0], centroid[0,1],'ro')
    line3, = ax.plot(coords_x[0,:], coords_y[0,:])
    ax.set_aspect('equal',adjustable='datalim')
    plt.title("Midline")
    plt.xlabel("x-axis")
    plt.ylabel("y-axis")
    set_plot_position()


    for i in range(1,rows):

        line1.set_xdata(midlines_x[i,:])
        line1.set_ydata(midlines_y[i,:])
        line2.set_xdata(centroid[i,0])
        line2.set_ydata(centroid[i,1])
        line3.set_xdata(coords_x[i,:])
        line3.set_ydata(coords_y[i,:])

        figure.canvas.draw()

        figure.canvas.flush_events()

        time.sleep(0.1)


def spline_plotting(my_splines,spline_x,coords_x, coords_y, midlines_x, midlines_y, centroid):

    rows, col = midlines_x.shape
    #fig = plt.figure()
    #ax = fig.add_subplot(111)
    #ax.set_aspect('equal', adjustable='datalim')

    plt.ion()
    figure, ax = plt.subplots(figsize=(10, 8))
    line1, = ax.plot(midlines_x[0,:],midlines_y[0,:])
    line2, = ax.plot(centroid[0,0], centroid[0,1],'ro')
    line3, = ax.plot(coords_x[0,:], coords_y[0,:])
    line4, = ax.plot(spline_x, my_splines[0](spline_x))
    ax.set_aspect('equal',adjustable='datalim')
    plt.title("Midline spline, i= " + str(0))
    plt.xlabel("x-axis")
    plt.ylabel("y-axis")
    set_plot_position()

    for i in range(1,rows):

        line1.set_xdata(midlines_x[i,:])
        line1.set_ydata(midlines_y[i,:])
        line2.set_xdata(centroid[i,0])
        line2.set_ydata(centroid[i,1])
        line3.set_xdata(coords_x[i,:])
        line3.set_ydata(coords_y[i,:])
        line4.set_ydata(my_splines[i](spline_x))
        line4.set_xdata(spline_x)
        plt.title("Midline spline, i= " + str(i))
        figure.canvas.draw()

        figure.canvas.flush_events()

        time.sleep(0.1)

    figure.canvas.flush_events()


def all_splines_plot(spline_x, my_splines, my_title, save_dir, save=False):

    plt.figure()

    for i in range(len(my_splines)):
        #plt.plot(spline_x,my_splines[i])
        plt.plot(spline_x, my_splines[i](spline_x))

    plt.title("all splines")
    plt.show()

    if save:
        plt.savefig(save_dir+my_title+".png")

def fourier_plot(f_x,f_y,N, my_title, save_dir, save=False):
    #TODO: fix plot
    plt.figure()
    #plt.plot(f_x, 2.0 / N * np.abs(f_y[1:N // 2]))
    plt.plot(f_x, f_y[0:N//2])
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("FFT amplitude")
    plt.title("Fourier plot ")
    set_plot_position()
    plt.show()
    if save:
        plt.savefig(save_dir+my_title+".png")


def fourier_animation(f_x, f_y,N):

    freq_dim, space_dim = f_y.shape

    plt.ion()
    figure, ax = plt.subplots(figsize=(10, 8))
    line1, = ax.plot(f_x,f_y[:,0])
    #ax.set_aspect('equal',adjustable='datalim')
    plt.xlim([0,max(f_x)*1.1])
    plt.ylim([0, f_y.max()*1.1])
    plt.title("Midline point fourier analysis for index 0")
    plt.xlabel("f [Hz]")
    plt.ylabel("|f_y|")
    set_plot_position()

    for s in range(1,space_dim):
        line1.set_xdata(f_x)
        line1.set_ydata(f_y[:,s])
        figure.canvas.draw()
        plt.title("Midline point fourier analysis for index " + str(s))
        figure.canvas.flush_events()

        time.sleep(1)

    figure.canvas.flush_events()


def fft_plot(fx, fy):

    ftime, N = fy.shape

    plt.ion()
    figure, ax = plt.subplots(figsize=(10, 8))
    #line1, = ax.plot(fx[0,:],fy[0,:])
    line1, = ax.plot(fx[0, :], 2.0 / N * np.abs(fy[0, 0:N//2]))

    #ax.set_aspect('equal',adjustable='datalim')
    plt.title("Fourier analysis of midline for frame: 0" )
    plt.xlabel("frequency")
    plt.ylabel("amplitude")
    set_plot_position()


    #2.0 / N * np.abs(f_y[i, 0:N // 2])
    for i in range(1,ftime):
        #line1.set_xdata(fx[i,:])
        #line1.set_ydata(fy[i,:])
        line1.set_xdata(fx[i,:])
        line1.set_ydata(2.0 / N * np.abs(fy[i, 0:N//2]))
        figure.canvas.draw()
        plt.title("Fourier analysis of midline for frame: " + str(i))
        figure.canvas.flush_events()

        time.sleep(0.1)

    figure.canvas.flush_events()


def point_in_time(my_array, my_title, save_dir, pos=-1,save=False):
    """Plot a single midline point in time to evaluate swimming period"""

    plt.figure()
    plt.plot(my_array[:, pos])
    plt.title(my_title + " : position " + str(pos))
    plt.xlabel("frame from start, [s * 1/50]")
    plt.ylabel("Position")
    plt.show()
    if save:
        plt.savefig(save_dir+my_title+".png")

def all_point_in_time(my_array, my_title, save_dir,save=False):
    """Plot a single midline point in time to evaluate swimming period"""

    plt.figure()
    plt.plot(my_array)
    plt.title(my_title)
    plt.xlabel("frame from start, [s * 1/50]")
    plt.ylabel("Position")
    plt.show()
    if save:
        plt.savefig(save_dir+my_title+".png")


def midlines_centroid_in_time(midline_x, midline_y,centroid, my_title, save_dir, save=False):

    fig, axs = plt.subplots(2,2)
    plt.tight_layout()

    axs[0, 0].plot(midline_x)
    axs[0, 0].set_title("midline x")
    axs[0, 0].set(ylabel="x-direction")
    axs[0, 0].set(xlabel="timeframes")

    axs[0, 1].plot(midline_y)
    axs[0, 1].plot(centroid[:,1],'rv')
    axs[0, 1].set_title("midline y")
    axs[0, 1].set(ylabel="y-direction")
    axs[0, 1].set(xlabel="timeframes")

    axs[1, 0].plot(centroid[:,0])
    axs[1, 0].set_title("centroid x")
    axs[1, 0].set(xlabel="timeframes")
    axs[1, 0].set(ylabel="x-direction")

    axs[1, 1].plot(centroid[:,1])
    axs[1, 1].set_title("centroid y")
    axs[1, 1].set(xlabel="timeframes")
    axs[1, 1].set(ylabel="y-direction")

    plt.show()

    if save:
        plt.savefig(save_dir+my_title+".png")


def histogram(l, my_title, save_dir, save=False):
    plt.figure()
    n, bins, patches = plt.hist(l)
    plt.title(my_title)
    set_plot_position()
    plt.show()

    if save:
        plt.savefig(save_dir+my_title+".png")


def simple_plot(x_vec, y_vec, my_title, save_dir, save=False):

    plt.figure()
    plt.plot(x_vec, y_vec)
    plt.title(my_title)
    set_plot_position()
    plt.show()

    if save:
        plt.savefig(save_dir+my_title+".png")


def local_maxima_plot(xfit, yfit_t, yfit_f, y_max_f, y_max_t, polynomial_t, polynomial_f, save_dir, save=False):
    # TODO: normalise fft plot


    plt.figure()
    plt.plot(xfit, yfit_t, '-', label='Curve fit from time')
    plt.plot(xfit, yfit_f, '--', color='blue', label='Curve fit from fft')
    plt.plot(xfit, y_max_t, 'ro', label='Amplitude avgeraged over time')
    plt.plot(xfit, y_max_f, 'rv', label='Amplitudes from fft analysis')

    plt.xlabel("Position along bodylength")
    plt.ylabel("Lateral displacement / bodylength")
    plt.legend()
    plt.title("Average displacement amplitude along midline")
    set_plot_position()
    plt.show()

    if save:
        plt.savefig(save_dir+"avg_displacement_prBL"+".png")


def all_midlines_in_one(midlines_x, midlines_y, save_dir, my_title, longitudinal_lines=False,  save=False):

    if longitudinal_lines==False:
        plt.figure()
        plt.plot(midlines_x,midlines_y)
        plt.title("All midlines")
        plt.show()
    if longitudinal_lines==True:
        time_dim, space_dim = midlines_x.shape

        plt.figure()
        for t in range(time_dim):
            plt.plot(midlines_x[t,:],midlines_y[t,:])
        plt.title("All midlines")
        plt.show()

    if save:
        plt.savefig(save_dir+my_title+".png")

def phase_animation(phase):

    time_dim, space_dim = phase.shape

    plt.ion()
    figure, ax = plt.subplots(figsize=(10, 8))
    #line1, = ax.plot(fx[0,:],fy[0,:])
    line1, = ax.plot(phase[:,0])

    ax.set_aspect('equal',adjustable='datalim')
    plt.title("Phase of midlines points for frame: 0" )
    plt.xlabel("X-pos")
    plt.ylabel("Phase")
    set_plot_position()

    for i in range(1,space_dim):
        line1.set_ydata(phase[:,i])
        figure.canvas.draw()
        plt.title("Phase of midlines points for frame: " + str(i))
        figure.canvas.flush_events()

        time.sleep(0.1)

    figure.canvas.flush_events()

    for i in range(0,space_dim):
        plt.plot(phase[:,i])
    plt.show()

def fft_evaluation(old_y, midlines_y, filtered_y, scale_factor, wait=0.2):

    m_time, m_space = midlines_y.shape

    ymin = min(np.min(old_y), np.min(midlines_y), np.min(filtered_y))
    ymax = max(np.max(old_y), np.max(midlines_y), np.max(filtered_y))

    plt.ion()
    figure, ax = plt.subplots(figsize=(10, 8))
    ax.set_ylim([ymin*0.95, ymax*1.05])
    #ax.set_aspect('equal', adjustable='datalim') #datalim

    plt.title("Midline and fourier approx. for pos: " + str(0) + " scale factor: " + str(scale_factor))
    plt.xlabel("time")
    plt.ylabel("y-axis")


    line1, = ax.plot(old_y[:,0], 'b''')
    line2, = ax.plot(filtered_y[:,0], 'b--')
    line3, = ax.plot(midlines_y[:,0], 'r*')

    for s in range(1, m_space):

        line1.set_ydata(old_y[:, s])
        line2.set_ydata(filtered_y[:, s])
        line3.set_ydata(midlines_y[:, s])
        plt.title("Midline and fourier approx. for frame: " + str(s) + " scale factor: " + str(scale_factor))
        figure.canvas.draw()
        figure.canvas.flush_events()

        time.sleep(wait)

    figure.canvas.flush_events()

def thingy_plot(Pm, norm_x, xfit, yfit, save_dir, my_title, save=False):

    print("thingy plot")
    plt.figure()
    plt.plot(norm_x, Pm, 'ro', label='Pm(x)')
    plt.plot(xfit, yfit, 'b-', label='3rd degree curve fit')
    plt.title("Pm(x)=k*phase*x/BL")
    plt.xlabel("x/BL")
    plt.ylabel("Pm(x)")
    plt.show()

    if save:
        plt.savefig(save_dir+my_title+".png")


def fft_evaluation2(midlines_y, filtered_y, time_vec, wait=0.2):
    m_time, m_space = midlines_y.shape

    ymin = min(np.min(midlines_y), np.min(filtered_y))
    ymax = max(np.max(midlines_y), np.max(filtered_y))

    plt.ion()
    figure, ax = plt.subplots(figsize=(10, 8))
    ax.set_ylim([ymin * 0.95, ymax * 1.05])
    # ax.set_aspect('equal', adjustable='datalim') #datalim

    plt.title("Midline and fourier approx. for pos: " + str(0))
    plt.xlabel("time")
    plt.ylabel("y-axis")

    line1, = ax.plot(time_vec, filtered_y[:, 0], 'b--')
    line2, = ax.plot(time_vec, midlines_y[:, 0], 'r-')

    for s in range(1, m_space):
        line1.set_ydata(filtered_y[:, s])
        line2.set_ydata(midlines_y[:, s])
        plt.title("Midline and fourier approx. for frame: " + str(s))
        figure.canvas.draw()
        figure.canvas.flush_events()

        time.sleep(wait)

    figure.canvas.flush_events()

def fish_characteristics(s1,s2,s3,s4,trav_ind):

    s1_arr = np.array([1,	0.9,	0.517-0.957,	0.816,	0.63-0.91,	0.882,	0.772,	0.667,	0.698,	0.85-0.97,	1,	0.98-1.16,	0.95,	0.5-1.0,	0.85-0.97,	0.9])
    s2_arr = np.array([0,0.25,0.02,0.0413,0,0.0518,0.0535,0.0562,0.0958,0,0,0,0.156,0.018,0.147,0.358])
    s3_arr = np.array([0.12,	1,	0.1,	0.2004,	0.2,	0.1744,	0.1497,	0.152,	0.1617,	0.2,	0.275,	0.18,	0.936,	0.126,	1.018,	0.994])
    s4_arr = np.array([0,	0.3,	0.3,	0.24,	0,	0.3372,	0.3209,	0.4045,	0.4371,	0,	0.2,	0,	0.25,	0.25,	0,	0.2])

    trav_ind_arr = np.array([0.61-0.77,	0.627,	0.58-0.76,	0.6692,	0.68-0.78,	0.623,	0.72,	0.623,	0.77,	0.67-0.71,	0.665,	0.62-0.67,	0.626,	0.6-0.78,	0.769,	0.777])

    plt.figure()
    plt.hist(s2_arr)
    plt.plot(s2,'ro')
    plt.title("s2")

    plt.figure()
    plt.plot(s3_arr)
    plt.plot(s3,'ro')
    plt.title("s3")

    plt.figure()
    plt.scatter(s2_arr/s3_arr, trav_ind_arr)
    plt.show()
    #plt.plot(s2/s3, trav_ind,'ro')

    s1_mean = np.mean(s1_arr)
    s2_mean = np.mean(s2_arr)
    s3_mean = np.mean(s3_arr)
    s4_mean = np.mean(s4_arr)
    trav_ind_mean = np.mean(trav_ind_arr)

    s1_std = np.std(s1_arr)
    s2_std = np.std(s2_arr)
    s3_std = np.std(s3_arr)
    s4_std = np.std(s4_arr)
    trav_ind_std = np.std(trav_ind_arr)

    print("Means: s1    s2  s3  s4  trav_ind")
    print(s1_mean, s2_mean, s3_mean, s4_mean, trav_ind_mean)
    print("Stds: ")
    print(s1_std, s2_std, s3_std, s4_std, trav_ind_std)

    print("")



