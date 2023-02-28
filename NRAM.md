![image-20221017140935731](http://imagebed.krins.cloud/api/image/0VX04622.png)

提出一种 $\gamma$ norm 

![image-20221017140923454](http://imagebed.krins.cloud/api/image/X84L8D20.png)

$\gamma$趋近0是B的秩，趋于无穷是B的核范数。

显然，$\gamma$范数几乎与真秩一致（此处使用$\gamma$=0.002），解决了传统凸核范数中不同奇异值的不平衡惩罚

 weighted nuclear norm（WNN）的逼近效果也很好，但每次都要重新计算权重时都要重新进行奇异值分解，增加了计算量。总体性能并不能比上$\gamma$范数。

![image-20221021174453131](http://imagebed.krins.cloud/api/image/V4XDV426.png)

加权1范数

![image-20221017140951106](http://imagebed.krins.cloud/api/image/N88B22XN.png)

联合2,1范数

![image-20221017141000213](http://imagebed.krins.cloud/api/image/6FD4J66N.png)

于是目标问题就变成

![image-20221017141013452](http://imagebed.krins.cloud/api/image/ZF640406.png)

引入拉格朗日乘子项和二次惩罚项将问题简化

![image-20221017141130929](http://imagebed.krins.cloud/api/image/2TZD6JJ6.png)

问题进一步转换成一下子问题：

![image-20221017141240575](http://imagebed.krins.cloud/api/image/NBL84BZ4.png)

可以通过最小化加权核范数逐渐求得B

![image-20221017142344020](http://imagebed.krins.cloud/api/image/DV6644L0.png)

对于联合2,1范数，T的迭代解可以表示成：

![image-20221017142409602](http://imagebed.krins.cloud/api/image/HZ6N28PL.png)

![image-20221017142434618](http://imagebed.krins.cloud/api/image/VHLRNL06.png)

![image-20221017142445556](http://imagebed.krins.cloud/api/image/L8RLXZT0.png)

![image-20221017142456163](http://imagebed.krins.cloud/api/image/8680684J.png)

算法流程如下：

![image-20221017173929903](http://imagebed.krins.cloud/api/image/4FPP2R84.png)

![image-20221017173939217](http://imagebed.krins.cloud/api/image/H6L4L6VJ.png)