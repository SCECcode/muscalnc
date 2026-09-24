#!/usr/bin/env python3

import numpy as np
from netCDF4 import Dataset

# 1. File path configuration (update filenames to match your local paths)
file_zlist = "so2_zlist"
file_ylist = "so2_ylist"
file_xlist = "so2_xlist"

file_vp = "so2.mesh_vp"
file_vs = "so2.mesh_vs"
file_rho = "so2.mesh_rho"

output_nc = "model_CVMSI_taper_so2.nc"

# 2. Read ASCII coordinate files
zlist = np.loadtxt(file_zlist, dtype=np.float32)
ylist = np.loadtxt(file_ylist, dtype=np.float32)
xlist = np.loadtxt(file_xlist, dtype=np.float32)

# Extract dimension sizes dynamically from coordinate lists
n_depth = len(zlist)      # Expecting 210
n_lat = len(ylist)        # Expecting 1251
n_lon = len(xlist)        # Expecting 1301

# 3. Read raw binary 3D data files and reshape to (depth, latitude, longitude)
# Note: Adjust byteorder if needed (e.g., dtype='>f4' for big-endian)
vp_data = np.fromfile(file_vp, dtype=np.float32).reshape((n_depth, n_lat, n_lon))
vs_data = np.fromfile(file_vs, dtype=np.float32).reshape((n_depth, n_lat, n_lon))
rho_data = np.fromfile(file_rho, dtype=np.float32).reshape((n_depth, n_lat, n_lon))

# 4. Create and write NetCDF4 dataset
with Dataset(output_nc, mode="w", format="NETCDF4") as ncfile:

    # Define dimensions
    ncfile.createDimension("depth", n_depth)
    ncfile.createDimension("latitude", n_lat)
    ncfile.createDimension("longitude", n_lon)

    # Define coordinate variables
    var_depth = ncfile.createVariable("depth", "f4", ("depth",), fill_value=np.nan)
    var_depth.units = "meters"

    var_lat = ncfile.createVariable("latitude", "f4", ("latitude",), fill_value=np.nan)
    var_lat.units = "degrees_north"

    var_lon = ncfile.createVariable("longitude", "f4", ("longitude",), fill_value=np.nan)
    var_lon.units = "degrees_east"

    # Define 3D data variables
    var_vp = ncfile.createVariable("vp", "f4", ("depth", "latitude", "longitude"), fill_value=np.nan)
    var_vp.units = "m/s"

    var_vs = ncfile.createVariable("vs", "f4", ("depth", "latitude", "longitude"), fill_value=np.nan)
    var_vs.units = "m/s"

    var_rho = ncfile.createVariable("rho", "f4", ("depth", "latitude", "longitude"), fill_value=np.nan)
    var_rho.units = "kg/m^3"

    # Assign values
    var_depth[:] = zlist
    var_lat[:] = ylist
    var_lon[:] = xlist

    var_vp[:] = vp_data
    var_vs[:] = vs_data
    var_rho[:] = rho_data

print(f"NetCDF file '{output_nc}' successfully written.")

