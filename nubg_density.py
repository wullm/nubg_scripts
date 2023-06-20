import numpy as np
import h5py

masses = ["M010", "M060", "M150", "M300", "M450", "M600"]

w_mean = np.zeros((len(masses),9))

with_MW = "MW"
#with_MW = "noMW"

for m, mass in enumerate(masses):
	for k in range(9):
		# Compose the file name
		base_id = 3452 + 432 * k
		fname = with_MW + "/NUBG_" + with_MW + "_" + mass + "_N384_" + str(base_id) + ".hdf5"
		# Open the file
		f = h5py.File(fname, mode = "r")
		# Read the weights
		w = f["Neutrinos/Weights"][:]
		# Close the file
		f.close()
		# Store the mean weight
		w_mean[m, k] = w.mean()

# The density perturbation is the mean weight
print("Mass", "Mean", "S.D.")
for m, mass in enumerate(masses):
	print(mass, w_mean[m].mean(), np.sqrt(w_mean[m].var()))
