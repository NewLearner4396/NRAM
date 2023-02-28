主成分分析principal component analysis(PCA)是一种很好的将原始高维数据投影到低维空间的降维技术。然而，一旦存在一个严重偏离实际的数据，PCA的结果将会不尽人意。

为了增强对异常值或观测时损坏的数据的鲁棒性，我们需要一种算法进行Robust PCA（RPCA），并尽可能保证算法复杂度较低。

通常来说，问题可以建模成：

![image-20221021191620601](http://imagebed.krins.cloud/api/image/48RP2VR0.png)

找到实际低秩矩阵的秩和实际稀疏矩阵的非零元个数，也就是最小化所认定为低秩矩阵的秩以及所认定的稀疏矩阵的非零元个数。

以上问题是一个NP-Hard问题。但可以通过将非凸的秩函数放松成核函数，将l0范数放松成l1范数进行简化成凸函数:

![image-20221023141809913](http://imagebed.krins.cloud/api/image/0R4D0VB6.png)

在不相干假设下，低秩矩阵和稀疏分量可以以压倒性的概率准确恢复。参考：[Robust principal
component analysis?](https://ieeexplore.ieee.org/document/889420)

遇到的问题：

1. 不是所有矩阵都能有一致性保证（满足不相干假设），数据可能会严重损坏，这样求出的最优解会明显偏离真值。
2. 核函数本质上是矩阵奇异值的l1范数，然而l1范数本身就有收缩效应，这会导致得到的估计是有偏的。也就是说，RPCA将所有奇异值平均加权实际上过度惩罚了大的奇异值，导致结果偏离了较多。

虽然我们可以利用对l1范数的非凸惩罚，如截断的l1范数进行修正。但是这些方法只适用于特殊场景。

于是提出利用一种新的非凸函数进行对秩的逼近，通过增强的拉格朗日乘子法 Augmented Lagrange
Multiplier (ALM) 求解此非凸函数。

定义的新$\gamma$范数:

![image-20221023143918447](http://imagebed.krins.cloud/api/image/084TRZ82.png)

问题变成:

![image-20221023154909795](http://imagebed.krins.cloud/api/image/244V0VZD.png)

ALM：

![image-20221023153952105](http://imagebed.krins.cloud/api/image/DVX462R8.png)

Y是拉格朗日乘子，用于消除等式约束，$\mu$是一个正参数，用来稍加约束误差，引入Frobenius 范数计算误差作为二次惩罚项。<·, ·>是两个矩阵的内积，也可以表示成$tr(A^T B)$.

通过以下方程更新L，Y，$\mu$直至收敛：

![image-20221023154604521](http://imagebed.krins.cloud/api/image/24N4R806.png)

![image-20221023155545407](http://imagebed.krins.cloud/api/image/J484LV4B.png)

![image-20221023155507969](http://imagebed.krins.cloud/api/image/6P2XP04P.png)

L的迭代求解：

因为对于优化问题：$\min\limits_Z F(Z) + \frac{\mu}{2}||Z-A||^2_F$的最优解$Z^*$可SVD成$U\sum^*_ZV^T$,$\sum^*_Z=diag(\sigma^*)$,$\sigma*$是优化问题$arg\min\limits_{\sigma \geq 0}f(\sigma)+\frac{\mu}{2}\Vert\sigma-\sigma_A\Vert^2_F$的最优解。

而上述问题又是凹函数和凸函数的联合，可以用差分凸规划 difference of convex (DC)
programing迭代优化,直至收敛：

![image-20221023164609814](http://imagebed.krins.cloud/api/image/8824HH8B.png)

其中$w_k$是$f(\sigma_k)$的梯度

最后$L^{t+1}=Udiag(\sigma^*)V^T$

S的迭代求解：

若方程13用的是S的联合2,1范数，则解可以表示成：

![image-20221023155840951](http://imagebed.krins.cloud/api/image/J8B8NTD8.png)

其中：$Q = X - L^{t+1} - \frac{Y^t}{\mu^t}$,$[S^{t+1}]_{:,i}$ 是$S^{t+1}$的第i列,$||S||_{2,1} = \sum\limits_i\sqrt{\sum\limits_j{S^2_{ij}}}$

若用的S的1范数，则解可以表示成：

![image-20221023160452582](http://imagebed.krins.cloud/api/image/ZJZ2B44N.png)

参数设置

1. $\lambda$

   $\lambda$太大会导致S迭代成0，最后L仍为一个高秩矩阵，$\lambda$太小会导致L最后为0，可以将$\lambda$设置成$1/\sqrt{\max(m,n)}$邻域的任意值，实验证明$\lambda$在相当范围内不敏感，可以设置成10e-3

2. $\rho$

   $\rho>1$，若$\rho$较大，则收敛更快，若$\rho$较小，则结果更精确。通常取1.1。

3. $\mu$

   可分别取1e-4，3e-3，0.5,4进行实验确定效果

参考论文：[Robust PCA via Nonconvex Rank Approximation](https://ieeexplore.ieee.org/document/7373325)