from datetime import date, timedelta
import pickle
import os

def std():
    
    sub_date_original = date.today()
    sub_date_end = sub_date_original + timedelta(days=730)

    current_dir = os.getcwd()
    save_dir = current_dir + '\\lib\\dat\\'
    save_the_date = open(f'{save_dir}std.dat','wb')
    pickle.dump(sub_date_end, save_the_date)
    save_the_date.close()