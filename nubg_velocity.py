import numpy as np
import h5py

masses = ["M010", "M060", "M150", "M300", "M450", "M600"]

w_mean = np.zeros((len(masses),9))
v_mean = np.zeros((len(masses),9,3))

#with_MW = "MW"
with_MW = "noMW"

for m, mass in enumerate(masses):
	for k in range(9):
		# Compose the file name
		base_id = 3452 + 432 * k
		fname = with_MW + "/NUBG_" + with_MW + "_" + mass + "_N384_" + str(base_id) + ".hdf5"
		# Open the file
		f = h5py.File(fname, mode = "r")
		# Read the weights and final velocity
		w = f["Neutrinos/Weights"][:]
		v = f["Neutrinos/FinalVelocities"][:]
		# Close the file
		f.close()
		# Compute the speed
		u = np.sqrt((v**2).sum(axis=1))
		# Store the mean weight and weighted velocity
		w_mean[m, k] = w.mean()
		v_mean[m, k] = (v.T*w).mean(axis=1)

# The velocity perturbation is the momentum density divided by the density
print("Mass", "Mean", "S.D.")
for m, mass in enumerate(masses):
	print(mass, (np.sqrt((v_mean[m]**2).sum(axis=1))/(1+w_mean[m])).mean(), np.sqrt((np.sqrt((v_mean[m]**2).sum(axis=1))/(1+w_mean[m])).var()))
