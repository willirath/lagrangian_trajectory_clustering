# Lagrangian Trajectory Clustering

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/willirath/lagrangian_trajectory_clustering/main)
Look at the [rendered notebooks](https://nbviewer.jupyter.org/github/willirath/lagrangian_trajectory_clustering/tree/main/notebooks/).

We aim at applying clustering to Lagrangian trajectories in the ocean.

## Environment

To start Jupyter, run
```shell
$ docker build -t lagtrajclus:latest -f Dockerfile .
$ docker run -p8888:8888 -v $PWD:/work -w /work lagtrajclus:latest
```
and open the link <http://127.0.0.1:8888/lab...> displayed in the terminal.

## Existing approaches

There's two review articles [1], [2] which come with code and examples [3] and a standalone package for trajectory distances [4].

## References

[1] Besse, P. C., Guillouet, B., Loubes, J. M., & Royer, F. (2016). Review and perspective for distance-based clustering of vehicle trajectories. IEEE Transactions on Intelligent Transportation Systems, 17(11), 3306-3317. doi [10.1109/TITS.2016.2547641](https://doi.org/10.1109/TITS.2016.2547641). [[PDF](https://hal.archives-ouvertes.fr/hal-01305993/file/bare_jrnl.pdf)]

[2] BESSE, Philippe C., GUILLOUET, Brendan, LOUBES, Jean-Michel, et al. Destination Prediction by Trajectory Distribution-Based Model. IEEE Transactions on Intelligent Transportation Systems, 2017. doi: [10.1109/TITS.2017.2749413](https://doi.org/10.1109/TITS.2017.2749413). [[PDF](https://hal.archives-ouvertes.fr/hal-01309337/file/Destination_Prediction_by_Trajectory_Distribution_Based_Model%20(2).pdf)]

[3] https://github.com/bguillouet/trajectory_classification

[4] https://github.com/bguillouet/traj-dist

## Reading list

(entirely copied from [4])

[5] B. Lin and J. Su, “Shapes based trajectory queries for moving objects,” in Proceedings of the 13th annual ACM international workshop on Geographic information systems . ACM, 2005, pp. 21–30. doi: [/10.1145/1097064.1097069](https://doi.org/10.1145/1097064.1097069). 

[6] H. Alt and M. Godau, “Computing the frechet distance between two polygonal curves,” International Journal of Computational Geometry & Applications , vol. 5, no. 01n02, pp. 75–91, 1995. doi: [10.1142/S0218195995000064](https://doi.org/10.1142/S0218195995000064) [[PDF](https://www.researchgate.net/profile/Helmut-Alt-2/publication/220669649_Computing_the_Frechet_Distance_between_Two_Polygonal_Curves/links/00b7d518a824cbfe5f000000/Computing-the-Frechet-Distance-between-Two-Polygonal-Curves.pdf)]

[7] T. Eiter and H. Mannila, “Computing discrete fréchet distance,” Citeseer, Tech. Rep., 1994. [[PDF](http://www.kr.tuwien.ac.at/staff/eiter/et-archive/cdtr9464.pdf)]

[8] D. J. Berndt and J. Clifford , “Using dynamic time warping to find patterns in time series.” in KDD workshop, vol. 10, no. 16. Seattle, WA, 1994, pp. 359–370 [[PDF](https://www.aaai.org/Papers/Workshops/1994/WS-94-03/WS94-03-031.pdf)]

[9] M. Vlachos, G. Kollios, and D. Gunopulos, “Discovering similar multi-dimensional trajectories,” in Data Engineering, 2002. Proceedings. 18th International Conference on .IEEE, 2002, pp. 673–684 [[PDF](http://people.cs.aau.dk/~simas/teaching/trajectories/00994784.pdf)]

[10] L. Chen and R. Ng, “On the marriage of lp-norms and edit distance,” in Proceedings of the Thirtieth international conference on Very large data bases-Volume 30 . VLDB Endowment, 2004, pp. 792–803. doi: [10.5555/1316689.1316758](https://doi.org/10.5555/1316689.1316758). [[PDF](https://dl.acm.org/doi/pdf/10.5555/1316689.1316758)]

[11] L. Chen, M. T. ̈ Ozsu, and V. Oria, “Robust and fast similarity search for moving object trajectories,” in Proceedings of the 2005 ACM SIGMOD international conference on Management of data . ACM, 2005, pp. 491–502. doi: [10.1145/1066157.1066213](https://doi.org/10.1145/1066157.1066213). [[PDF](https://dl.acm.org/doi/pdf/10.1145/1066157.1066213)]

[12] Wichmann, D., Kehl, C., Dijkstra, H. A., and van Sebille, E.: Ordering of trajectories reveals hierarchical finite-time coherent sets in Lagrangian particle data: detecting Agulhas rings in the South Atlantic Ocean, Nonlin. Processes Geophys., 28, 43–59, https://doi.org/10.5194/npg-28-43-2021, 2021. [[PDF](https://npg.copernicus.org/articles/28/43/2021/npg-28-43-2021.pdf)]
