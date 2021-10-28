import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

@st.cache
def load_measurement_data():
    return pd.read_csv("SRAM_res.txt", header=None, names =('f_CLK', 'f_SWDCLK', 'phase', 'result'))

@st.cache
def filter_wrt_main_clock(main_clock):
    return df[df['f_CLK'] == main_clock]

@st.cache
def convert_to_2D_array(meas_df):
    meas_data_array = meas_df['result'].to_numpy()
    meas_data_array = np.reshape(meas_data_array, (31,32))
    meas_data_array = ((meas_data_array == "b'0x00000400'") | (meas_data_array == "b'0x00000200'"))
    return meas_data_array

source_clock = 50e6

st.title('Serial Wire Debug (SWD) tester for CM0 testchip')

st.header('Reading SRAM w.r.t. main clock, SWD clock and delay')

df = load_measurement_data()

main_clk_slider = st.slider('Main clock half-period [PCLKs]', min_value = 1, max_value = 32, value = 16)

st.write(f'Main clock frequency is {source_clock/(2.0*main_clk_slider)/1e6:.2f} MHz.')

meas_data_view = st.selectbox('Measurement data view: ', ('Raw data', 'Filtered data', 'Graph'), index=2)

if(meas_data_view == 'Raw data'):
    st.table((filter_wrt_main_clock(main_clk_slider)))

if(meas_data_view == 'Filtered data'):
    st.table(convert_to_2D_array(filter_wrt_main_clock(main_clk_slider)))

if(meas_data_view == 'Graph'):
    fig, ax = plt.subplots()
    ax.imshow(convert_to_2D_array(filter_wrt_main_clock(main_clk_slider)))
    ax.text(28, 2, 'FAIL', color = 'indigo', bbox={'facecolor': 'white', 'pad': 2})
    ax.text(27, 29, 'PASS', color = 'yellow', bbox={'facecolor': 'black', 'pad': 2})
    ax.set_xlabel('SWD clock delay [ns]')
    ax.set_xticks([0, 5, 10, 15, 20, 25, 30])
    ax.set_xticklabels([f'{_:.2f}' for _ in (np.array([0, 5, 10, 15, 20, 25, 30])/source_clock*1e9)])
    ax.set_ylabel('SWD clock [MHz]')
    ax.set_yticks([0, 5, 10, 15, 20, 25, 30])
    ax.set_yticklabels([f'{_:.2f}' for _ in (source_clock/(2.0*(np.array([0, 5, 10, 15, 20, 25, 30])+1))/1e6)])
    st.pyplot(fig)
