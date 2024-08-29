# Structura
[![Github All Releases](https://img.shields.io/github/downloads/RavinMaddHatter/Structura/total.svg)]()

简体中文丨[**English**](README.md)
（此Markdown文档由捂脸、YiShengJunn翻译）

这个工具的灵感来自 Litematica 模组。它是一个可以用.mcstructure文件生成资源包的工具。在这个资源包中，盔甲架模型被修改为被投影的方块。它会把结构文件中的所有方块作为模型中的骨骼。然后投影出“幽灵块”用于向用户显示原本方块的位置。

[![介绍视频](https://img.youtube.com/vi/IdKT925LKMM/0.jpg)](https://www.youtube.com/watch?v=IdKT925LKMM)

## 生成 .mcstructure 文件

首先，你必须获得一个结构方块。但它需要在启用作弊的存档中完成，只需在聊天栏输入`/give @s structure_block`即可获得一个结构方块。
![alt text](https://github.com/RavinMaddHatter/Structura/blob/main/docs/give_structure.png?raw=true)
接下来使用GUI配置结构，选择你希望在盔甲架中投影的范围 。请注意，单个支持的最大尺寸为 64x64x64（不修改世界NBT数据的情况下）
![alt text](https://github.com/RavinMaddHatter/Structura/blob/main/docs/select_structure.PNG?raw=true)
接下来单击底部的导出按钮以生成保存文件。将其命名为您想要的任何名称，而不是位置，稍后您将需要它。
![alt text](https://github.com/RavinMaddHatter/Structura/blob/main/docs/export_structure.PNG?raw=true)

## 将结构转换为 .mcpack 文件
首先，你需要下载当前版本的Structura工具。解压zip文件，然后启动可执行文件。启动后，您应该会看到类似于下图的内容。
![alt text](https://github.com/RavinMaddHatter/Structura/blob/main/docs/launch_structura.PNG?raw=true)
接下来使用浏览按钮打开之前导出的结构，或手动输入路径。
![alt text](https://github.com/RavinMaddHatter/Structura/blob/main/docs/browse_file.PNG?raw=true)
输入生成后资源包的名称。
![alt text](https://github.com/RavinMaddHatter/Structura/blob/main/docs/name.PNG?raw=true)
** 如果你错误地将两个文件名重复，它会在下面显示重命名的提示。
![alt text](https://github.com/RavinMaddHatter/Structura/blob/main/docs/already_exists.PNG?raw=true)
如果一切正常，您现在应该有一个mcpack文件。
![alt text](https://github.com/RavinMaddHatter/Structura/blob/main/docs/pack_made.PNG?raw=true)

## 使用资源包
这个包就像任何纹理包一样。要使用它，你必须确保它处于激活状态，以便在全局资源中启用它。
![alt text](https://github.com/RavinMaddHatter/Structura/blob/main/docs/make_pack_active.PNG?raw=true)
该结构将出现在您加载的世界中的每个盔甲架周围。这就是我们能够使其在任何世界上工作的方式。所以拿出一个盔甲架，把它放下来看看你的结构。
![alt text](https://github.com/RavinMaddHatter/Structura/blob/main/docs/example_full.png?raw=true)
如果你愿意，可以通过右击盔甲架来逐层浏览结构。这将最小化除“活动”层之外的所有层。然而对于大型结构，它一次会显示多层（相隔12个方块）
![alt text](https://github.com/RavinMaddHatter/Structura/blob/main/docs/example_layer.png?raw=true)


## Linux

首先，你肯定得安装python3-tk。

选择适合你的方法：

Debian/Ubuntu:
```bash
sudo apt-get install python3.7-tk
```
Fedora:
```bash
sudo dnf install python3-tkinter
```
Arch:
```bash
yay -S python37 # yay or any other AUR component
```
要运行程序，请允许需要的模块，不过运行start.sh可以自动帮你安装：
```bash
chmod +x start.sh && sh start.sh
```

## 更新方块
从1.3版本开始，你可以手动更新方块并贡献回本项目。
[这是一篇关于它如何工作的文章](docs/Editing%20Blocks.md)    


## 贡献

[![GitHub repo Good Issues for newbies](https://img.shields.io/github/issues/RavinMaddHatter/Structura/good%20first%20issue?style=flat&logo=github&logoColor=green&label=Good%20First%20issues)](https://github.com/RavinMaddHatter/Structura/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22) [![GitHub Help Wanted issues](https://img.shields.io/github/issues/RavinMaddHatter/Structura/help%20wanted?style=flat&logo=github&logoColor=b545d1&label=%22Help%20Wanted%22%20issues)](https://github.com/RavinMaddHatter/Structura/issues?q=is%3Aopen+is%3Aissue+label%3A%22help+wanted%22) [![GitHub Help Wanted PRs](https://img.shields.io/github/issues-pr/RavinMaddHatter/Structura/help%20wanted?style=flat&logo=github&logoColor=b545d1&label=%22Help%20Wanted%22%20PRs)](https://github.com/RavinMaddHatter/Structura/pulls?q=is%3Aopen+is%3Aissue+label%3A%22help+wanted%22) [![GitHub repo Issues](https://img.shields.io/github/issues/RavinMaddHatter/Structura?style=flat&logo=github&logoColor=red&label=Issues)](https://github.com/RavinMaddHatter/Structura/issues?q=is%3Aopen)

👋 **欢迎，新的贡献者！**

无论您是经验丰富的开发人员还是新手，您的贡献对我们来说都非常宝贵。不要犹豫，加入进来，探索项目。想要为项目做贡献，请查看[贡献指南](CONTRIBUTING.md). 
