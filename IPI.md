IPI模型：

![image-20221021155105726](http://imagebed.krins.cloud/api/image/8T6RPD4X.png)

原图像D由背景B、目标T、噪声N组成。

IPI模型基于两个假设，背景图像是一个低秩矩阵，目标图像是一个稀疏矩阵。论文提到该假设较为符合物理实际，并且现在有很多高效的低秩矩阵恢复的方法，所以这个模型效率和泛用性极高。

该模型通过滑动窗将原图像进行提取，并且每个小窗（Patch）拉伸成一维列向量，n个列向量组合成新的矩阵，即公式中的D。

T是一个稀疏矩阵，即![image-20221021155358366](http://imagebed.krins.cloud/api/image/8VXJ8B66.png)

T的非零元个数小于k，k远小于T矩阵的元素个数

B是一个低秩矩阵，即

![image-20221021155706114](http://imagebed.krins.cloud/api/image/4Z2T68RL.png)

r是一个常数，对于越高复杂度的背景，r越高。实验中，背景图像的奇异值总是迅速收敛到0，印证了该假设的正确性。

由于一张图像较远像素也往往有较高相关性，提取出的D通常可以使用现有的许多非局部自相似性的方法。

N假设为一个i.i.d(独立同分布白噪声)

![image-20221021160520947](http://imagebed.krins.cloud/api/image/L4PDT202.png)

在该模型中的k,r,$\delta$,对不同图像不同，但好消息是我们不需要直接计算出这些值。

**通过该模型小目标检测实际上是从数据矩阵中恢复低秩分量和稀疏分量的问题**

即：

![image-20221021161136496](http://imagebed.krins.cloud/api/image/2JF0JDFT.png)

可转换为对应问题

![image-20221021161216174](http://imagebed.krins.cloud/api/image/RNL8N2J2.png)

因为该问题是一个凸问题，可以使用 Accelerated Proximal Gradient (APG)求解

![image-20221021161435605](http://imagebed.krins.cloud/api/image/8H8FH222.png)

其中

![image-20221021161459558](http://imagebed.krins.cloud/api/image/VBN020ZJ.png)

该模型完整求解过程

![image-20221021161712075](http://imagebed.krins.cloud/api/image/L6N842J8.png)

首先，根据从图像序列获得的原始红外图像fD构建补丁图像D。
其次，将算法1应用于斑块图像D以同时估计低秩背景斑块图像B和稀疏目标斑块图像T。
第三，我们分别从补丁图像B和T重建背景图像fB和目标图像fT。
第四，我们使用一种简单的分割方法来自适应地分割目标图像fT，因为它包含一些小值的误差。最后，通过后处理，对分割结果进行细化，得到最终的检测结果。

在算法1中，选择$\lambda = 1 / {\sqrt{max(m,n)}}$, $\eta = 0.99$, $\mu_0 = s_2$, $\bar{\mu} = 0.05 s_4$, $s_2, s_4$是D的第二和第四奇异值。

第三步中重叠部分的像素使用中值滤波器，比均值滤波器鲁棒性更好。

第四步中设置阈值确定目标：

![image-20221021162522338](http://imagebed.krins.cloud/api/image/NHHR8284.png)

可按需要选择双边阈值：

![](http://imagebed.krins.cloud/api/image/RD4T4HV4.png)

![image-20221021162600732](http://imagebed.krins.cloud/api/image/LR8DB6DV.png)

$v_{max}、v_{min}、k$为经验确定的常数，$\mu、\sigma$为$f_T$的均值和标准差

最后一步的后处理中可使用区域分析方法去删除错误检测目标，可使用形态学方法去提炼目标区域。并且使用统计技术估计目标在重建背景图像中的对应局部区域的复杂度，然后利用估计结果评估器可靠性。

参考链接：[Infrared Patch-Image Model for Small Target
Detection in a Single Image](https://ieeexplore.ieee.org/document/6595533)

然而由于核范数和1范数平等对待所有奇异值，算出来的秩与真秩有些许偏差，所以迭代结果可能只是局部最优解，也就是说，不能精确分离复杂图像的背景和目标。

后人通过 non-convex rank approximation 来改进 principal component analysis（PCA），同时新提出的 alternating direction method of multipliers（ADMM）比 accelerated proximal gradient（APG）收敛更快更精确，可以进一步优化算法。