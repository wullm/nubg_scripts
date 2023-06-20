import healpy as hp
import numpy as np
import h5py
from matplotlib import pyplot as plt

masses = ["M010", "M060", "M150", "M300", "M450", "M600"]

#with_MW = "MW"
with_MW = "noMW"

# Create an empty healpix map
nside = 128
npix = hp.nside2npix(nside)
maps = np.zeros((len(masses),9,npix))

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
		# Deposit the particles on the healpix map
		for i in range(len(w)):
			# The position on the sky is in the opposite direction of the velocity
			vec = -v[i]
			pix = hp.vec2pix(nside, vec[0], vec[1], vec[2])
			maps[m, k, pix] += w[i]

def show_map(M):
	# Average pixel value
	Npart = 224**3
	Nside = 128
	Npix = hp.nside2npix(Nside)
	avg = Npart / Npix
	# Compute overdensity map
	map = M / avg
	# Smooth the map
	sigma = np.deg2rad(3) # 3 degree smoothing
	FWHM = 2.0 * np.sqrt(2.0 * np.log(2.0)) * sigma
	smap = hp.smoothing(map, fwhm=FWHM)
	# Show the map without monopole and dipole
	hp.mollview(smap, remove_dip = True)
	plt.show()

# As an example, show the average map for 0.01 eV
show_map(maps[0].mean(axis=0))

