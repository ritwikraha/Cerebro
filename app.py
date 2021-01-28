import pandas as pd
import numpy as np
from pyedflib import highlevel
import scipy.interpolate
from scipy import signal
from matplotlib import patches
from scipy.signal import butter, lfilter
import matplotlib.pyplot as plt
import streamlit as st

# a function to fetch the power spectral density of the signals
# change the sampling frequency (fs) and range on the basis of headset
def get_psds(data, fs=256, f_range=[0.5, 30]):
    '''
    Calculate signal power using Welch method.
    Input: data- mxn matrix (m: number of channels, n: samples of signals)
           fs- Sampling frequency (default 128Hz)
           f_range- Frequency range (default 0.5Hz to 30Hz)
    Output: Power values and PSD values
    '''
    powers = []
    psds = list()
    for sig in data:
        freq, psd = signal.welch(sig, fs)
        idx = np.logical_and(freq >= f_range[0], freq <= f_range[1])
        powers = np.append(powers, sum(psd[idx]))
        psds.append(psd[idx])
    return powers, psds
# function to plot the topographical map of the brain according to Emotiv 14 channel headset
def plot_topomap(data, ax, fig, draw_cbar=True):
    '''
    Plot topographic plot of EEG data. This specialy design for Emotiv 14 electrode data. 
    This can be change for any other arrangement by changing ch_pos (channel position array)
    Input: data- 1D array 14 data values
           ax- Matplotlib subplot object to be plotted every thing
           fig- Matplot lib figure object to draw colormap
           draw_cbar- Visualize color bar in the plot
    '''
    N = 300            
    xy_center = [2,2]  
    radius = 2 

    # AF3, F7, F3, FC5, T7, P7, O1, O2, P8, T8, FC6, F4, F8, AF4
    ch_pos = [[1,4],[0.1,3], [1.5,3.5], [0.5,2.5], 
             [-0.1,2], [0.4,0.4], [1.5,0], [2.5,0], 
             [3.6,0.4], [4.1,2], [3.5,2.5], [2.5,3.5], 
             [3.9,3], [3,4]]
    x,y = [],[]
    for i in ch_pos:
        x.append(i[0])
        y.append(i[1])

    xi = np.linspace(-2, 6, N)
    yi = np.linspace(-2, 6, N)
    zi = scipy.interpolate.griddata((x, y), data, (xi[None,:], yi[:,None]), method='cubic')

    dr = xi[1] - xi[0]
    for i in range(N):
        for j in range(N):
            r = np.sqrt((xi[i] - xy_center[0])**2 + (yi[j] - xy_center[1])**2)
            if (r - dr/2) > radius:
                zi[j,i] = "nan"
    
    dist = ax.contourf(xi, yi, zi, 60, cmap = plt.get_cmap('coolwarm'), zorder = 1)
    ax.contour(xi, yi, zi, 15, linewidths = 0.5,colors = "grey", zorder = 2)
    
    if draw_cbar:
        cbar = fig.colorbar(dist, ax=ax, format='%.1e')
        cbar.ax.tick_params(labelsize=8)

    ax.scatter(x, y, marker = 'o', c = 'b', s = 15, zorder = 3)
    circle = patches.Circle(xy = xy_center, radius = radius, edgecolor = "k", facecolor = "none", zorder=4)
    ax.add_patch(circle)

    for loc, spine in ax.spines.items():
        spine.set_linewidth(0)
    
    ax.set_xticks([])
    ax.set_yticks([])

    circle = patches.Ellipse(xy = [0,2], width = 0.4, height = 1.0, angle = 0, edgecolor = "k", facecolor = "w", zorder = 0)
    ax.add_patch(circle)
    circle = patches.Ellipse(xy = [4,2], width = 0.4, height = 1.0, angle = 0, edgecolor = "k", facecolor = "w", zorder = 0)
    ax.add_patch(circle)
    
    xy = [[1.6,3.6], [2,4.3],[2.4,3.6]]
    polygon = patches.Polygon(xy = xy, edgecolor = "k", facecolor = "w", zorder = 0)
    ax.add_patch(polygon) 
    
    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(-0.5, 4.5)

    return ax
    

# functions to create a butterworth filter
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y
#function to load the raw data from the edf file selected
def load_raw_data(session_name):
  file_loc = 'data/S001/S001'+ session_name+'.edf'
  signals, signal_headers, header = highlevel.read_edf(file_loc)
  return signals, signal_headers, header

def main():
  st.title("CEREBRO")
  st.subheader("An interactive web app to visualise EEG Data")
  st.markdown("A tool for gifted youngsters, mutant and human alike :wink: ")
  # creating the sidebar with all it's glorious options
  st.sidebar.subheader("Session Selection")
  session_list = ['E01', 'E02', 'E03', 'E04']
  session_name = st.sidebar.selectbox("Select the Session", session_list)
  show_topo = st.sidebar.checkbox("Show Topo Map")

  # fetching the input data from the files and calculating parameters for charts
  signals_raw, signals_head, _ = load_raw_data(session_name)
  signals = pd.DataFrame(signals_raw)
  headers = pd.DataFrame(signals_head)

  st.sidebar.subheader("Channel Selection")
  channel_names_list = headers['label']
  selected_channel = st.sidebar.selectbox("Select the Channel", channel_names_list)
  freq_bands = ['alpha', 'beta', 'delta', 'theta', 'gamma', 'none']
  st.sidebar.subheader("Frequency Band Selection")
  selected_frequency = st.sidebar.selectbox("Select the Frequency Band", freq_bands)
  #show_psd = st.sidebar.checkbox("Show Power Spectral Density")

  pwrs, _ = get_psds(signals_raw)
  fig, ax = plt.subplots(figsize=(10,8))
  plot_topomap(pwrs, ax, fig)

   

  id =  headers.index[headers['label'] == selected_channel].tolist()[0]
  #f = plt.psd(signals.iloc[id], 256, 1 / 0.001)

  # code which I could have refactored a lot

  if selected_frequency == 'alpha':
    lowcut = 8
    highcut = 12
  elif selected_frequency == 'beta':
    lowcut = 13
    highcut = 30
  elif selected_frequency == 'delta':
    lowcut = 1
    highcut = 4
  elif selected_frequency == 'theta':
    lowcut = 4
    highcut = 8
  elif selected_frequency == 'gamma':
    lowcut = 30
    highcut = 100
  elif selected_frequency == 'none':
    lowcut = 1
    highcut = 100
  sampled_channel = butter_bandpass_filter(signals.iloc[id].to_numpy(), lowcut, highcut, 256, order=6)
  if session_name:
    st.write("Showing the first five channels of the session ", session_name)
    st.dataframe(signals.head())
  if show_topo:
    st.write("Showing the topographical data of the brain as per Emotiv 14 channel headset")
    st.pyplot(fig)
  if selected_channel:
    st.write("The data of channel ",selected_channel," in the band -  ",selected_frequency)
    st.line_chart(sampled_channel)
  st.markdown('The data for this project has been used from - [EEG dataset of Fusion relaxation and concentration moods”, Mendeley Data, V1, doi: 10.17632/8c26dn6c7w.1](https://data.mendeley.com/datasets/8c26dn6c7w/1#__sid=js0)')



if __name__ == '__main__':
	main()