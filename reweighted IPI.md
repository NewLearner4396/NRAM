传统IPI模型由于l1范数不能完全描述稀疏性的缺陷，会过于缩小小目标或在目标图像中留下背景成分。并且由于强边缘也有可能是稀疏的，无法简单地与小目标进行区分。

通过结合结构先验信息，为每个patch自适应权重，提出了名为加权IPI weighted IPI（WIPI）的方法，然而每个patch都要进行计算，十分费时。并且仅能分离某些特定类型的强边缘。

WIPI的作者分析，其性能不令人满意的原因是缺少相似的边缘样本。虽然在奇异值部分和最小化partial sum minimisation of singular values（PSSV）方法的帮助下，可以保留较大的奇异值。然而，该方法仍需准确估计目标的秩，这实际上很难实现。

而且现有的基于低秩的方法没有考虑到亮度较低的非目标稀疏点的存在，很容易误认成为目标。

进一步分析，基于强边缘是否属于核范数最小化假设的相似边缘样本，可以将强边缘划分为强势的强边缘与弱势的强边缘。这两种强边缘都是全局稀疏的，但是只有弱势的强边缘是面片patch之间仍具有稀疏性。通过最后分离的结果来看，只有弱势的强边缘留在了目标图像中，也就是说，面片之间的稀疏性比面片内部的稀疏性更容易使得目标留在目标图像。所以IPI模型性能不足的真实原因是存在具有面片间稀疏性的弱势强边缘同小目标进行混淆。

所以我们急需一种方法可以抑制目标图像中的非目标稀疏点的同时保持背景强边缘。

基于加权核范数最小化weighted  nuclear  norm  minimisation  (WNNM)可以通过较小的权重惩罚较大的奇异值的特点，可以用来得到更为准确的背景图像。并且此方法并不需要准确计算出背景图像的秩。还可以使用加权l1范数weighted l1 norm，通过较大的权重惩罚非目标图像，得到更为准确的目标图像。根据这两种想法，可以提出一种新的IPI模型，reweighted IPI。

加权核范数定义为：

![image-20221023224745792](C:/Users/Administrator/AppData/Roaming/Typora/typora-user-images/image-20221023224745792.png)

加权1范数定义为：

![image-20221023224902789](http://imagebed.krins.cloud/api/image/N86XP0RR.png)

对于噪声图像，我们假设其符合高斯分布，所以有：

![image-20221023225118819](http://imagebed.krins.cloud/api/image/4N0FXD8T.png)

于是ReWIPI可表示成：

![image-20221023225151555](http://imagebed.krins.cloud/api/image/BHVZ486V.png)

参考：[Small target detection based on reweighted
infrared patch-image model](https://ietresearch.onlinelibrary.wiley.com/doi/full/10.1049/iet-ipr.2017.0353)