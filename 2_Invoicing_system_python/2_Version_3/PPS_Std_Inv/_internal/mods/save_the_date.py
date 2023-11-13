from datetime import date, timedelta
import pickle


def std(dat_dir):
    sub_date_original = date.today()
    sub_date_end = sub_date_original + timedelta(days=365)

    save_the_date = open(f"{dat_dir}std.dat", "wb")
    pickle.dump(sub_date_end, save_the_date)
    save_the_date.close()
