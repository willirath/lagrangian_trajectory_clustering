# Tech notes

## Pre-processing steps

- Load trajectory data from an example dataset. Currently there is a medsea dataset and a labsea dataset. The result is a data frame with columns "traj", "obs", "longitude", "latitude" with "traj" and "obs" being used as a multi-index.

- Find the maximally needed h3 resolution. Depending on the resolution (min typical step size) of the trajectory data, we'll need different max. h3 resolutions.

- Add the highest resolution cell id to the data frame.  (This is done, because it's a lot cheaper to sub-sample to parent cells from here than running the trafo to any desired resolution later.)

## Clustering

- Start from the lowest desired h3 resolution. (Use 0?) `working_resolution`
- For all locations, find the corresponding h3 cell at this working resolution.
- Along each trajectory, drop subsequent duplicates (this removes time info)
- Fill in intermediate cells? (Use [`h3.h3_line()`](https://uber.github.io/h3-py/api_reference.html#h3.h3_line)?)
- Transform to series of sequences (lists?) of h3 cells. The result is a pandas series where the index is a multi-index from the orignal trajectory number and an integer enumerating the steps along the (filled in) trajectory at the current `working_resolution`. For each of the trajectory, id's we have a sequence which can be an argument to a sequence-comparison metric like the Levenshtein distances, LCS or similar.
- For each cluster go to next higher working resolution and repeat (from the raw data).
- Build a tree.
