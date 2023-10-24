from mods.create_apw_pysg import set_apw
import os
import pickle

current_dir = os.getcwd()
dll_dir = current_dir + '\\lib\\dll\\'
dat_dir = current_dir + '\\lib\\dat\\'
media_dir = current_dir + '\\lib\\media\\'

# Theme setup
theme = 'LightGrey1' # Theme

# Icon
pps_icon = media_dir + '0_icon.ico'

# Font, and font size
main_font = 'Calibri'
hf_size = 25 # Heading
tf_size = 20 # text
btf_size = 20 # button
ebf_size = 15 # Exit and Back buttons
p_std = (10,10) # Std padding
p_ext = (15,15) # Exit Button padding

# Element size
i_size = 20 # Inputbox size
b_size = 20 # Button size
eb_size = 15 # Exit button size

# Invoice elements
inv_t = 10 # Text size
p_inv = 1 # padding
inv_s = 9 # Input element size
p_inv_cb = [(3,3),(6,6)] # Combo box padding
pc_size = 11 # Procedure codes Combo box size
cs_size = 22 # Client select Combo box size

load_inv_num = open(f'{dll_dir}inumdb.dll', 'rb')
inv_num_dict = pickle.load(load_inv_num)
print(inv_num_dict)