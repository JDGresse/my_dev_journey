import pickle


open_std = open(
    "E:\\2_PPStartUp\\1_Invoicing\\00_Git_restore\\00_Standard_core\\lib\\dll\\services.dll",
    "rb",
)

std = pickle.load(open_std)

std.append("Training")
std.append("Supervision")

print(std)
