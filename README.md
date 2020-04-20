## images crawler 目录
该目录包含从各大图片搜索网站爬取图片的demo脚本。运行脚本后，爬取的图片的链接会被存到一个文档中。threadingDownload.py 可以读取该文档，并用多线程的方式加速下载。

## images process similarity 目录
该目录包含对图片做相似性检索的一些代码。对于一张新图片，可从数据库中检索出相似的图片。

## vgg process 目录
对于将图片用神经网络处理后的feature做相似性检索的一些探索。