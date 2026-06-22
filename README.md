# Gas_VOL_ppm_LEL

<p align="center">
  <strong>可燃气体 %VOL / ppm / %LEL 浓度换算工具</strong>
</p>

<p align="center">
  <a href="https://github.com/stark1898y/Gas_VOL_ppm_LEL/stargazers"><img src="https://img.shields.io/github/stars/stark1898y/Gas_VOL_ppm_LEL?style=flat-square" alt="Stars"></a>
  <a href="https://github.com/stark1898y/Gas_VOL_ppm_LEL/network/members"><img src="https://img.shields.io/github/forks/stark1898y/Gas_VOL_ppm_LEL?style=flat-square" alt="Forks"></a>
  <a href="https://github.com/stark1898y/Gas_VOL_ppm_LEL/issues"><img src="https://img.shields.io/github/issues/stark1898y/Gas_VOL_ppm_LEL?style=flat-square" alt="Issues"></a>
  <a href="https://github.com/stark1898y/Gas_VOL_ppm_LEL/blob/main/LICENSE"><img src="https://img.shields.io/github/license/stark1898y/Gas_VOL_ppm_LEL?style=flat-square" alt="License"></a>
</p>

<p align="center">
  <a href="https://stark1898y.github.io/Gas_VOL_ppm_LEL/">GitHub Pages 在线演示</a> &nbsp;|&nbsp;
  <a href="https://gitee.com/stark1898/Gas_VOL_ppm_LEL">Gitee 国内镜像</a>
</p>

---

## 功能特性

- **8 种常见可燃气体**：甲烷、乙烷、丙烷、丁烷、氢气、乙烯、乙炔、一氧化碳
- **三种单位互转**：%VOL（体积百分比）、ppm（百万分之一体积）、%LEL（爆炸下限百分比）
- **三端统一实现**：C 命令行版、Python GUI 桌面版、纯前端网页版
- **零依赖网页版**：单 HTML 文件，可直接部署到 GitHub Pages

## 在线演示

**GitHub Pages**：[https://stark1898y.github.io/Gas_VOL_ppm_LEL/](https://stark1898y.github.io/Gas_VOL_ppm_LEL/)

**Gitee（国内）**：[https://gitee.com/stark1898/Gas_VOL_ppm_LEL](https://gitee.com/stark1898/Gas_VOL_ppm_LEL)

## 项目结构

```
Gas_VOL_ppm_LEL/
├── docs/
│   └── index.html          # GitHub Pages 纯前端版本
├── c/
│   └── gas_vol_ppm_lel.c   # C 命令行版本
├── python/
│   ├── gas_vol_ppm_lel.py  # Python GUI 版本
│   └── icon/
│       └── 燃气.ico        # 应用图标
├── test.py                 # 自动测试脚本
├── .gitignore
├── LICENSE
└── README.md
```

## 版本说明

| 版本 | 文件 | 技术栈 | 运行方式 |
|:---:|:---:|:---:|:---:|
| **网页版** | `docs/index.html` | HTML + CSS + JavaScript | 直接打开或部署到 GitHub Pages |
| **C 命令行版** | `c/gas_vol_ppm_lel.c` | C + GCC | `gcc gas_vol_ppm_lel.c -o gas && ./gas` |
| **Python 桌面版** | `python/gas_vol_ppm_lel.py` | Python + Tkinter | `python gas_vol_ppm_lel.py` |

## 快速开始

### 1. 网页版（推荐）

直接打开 `docs/index.html` 文件，或部署到 GitHub Pages：

1. Fork 本仓库
2. 仓库 Settings -> Pages -> Source 选择 `main` 分支的 `/docs` 文件夹
3. 访问 `https://你的用户名.github.io/Gas_VOL_ppm_LEL/`

### 2. C 命令行版

```bash
cd c
gcc gas_vol_ppm_lel.c -o gas_vol_ppm_lel -fexec-charset=GBK
./gas_vol_ppm_lel
```

输入格式：`气体编号 单位编号 值`，如 `1 1 5.0` 表示甲烷 %VOL=5.0

### 3. Python 桌面版

```bash
cd python
python gas_vol_ppm_lel.py
```

### 4. 打包 EXE

```bash
cd python
pyinstaller --windowed --icon=.\icon\燃气.ico --onefile .\gas_vol_ppm_lel.py
```

### 5. 运行测试

```bash
python test.py
```

## 支持的气体

| 编号 | 气体名称 | 分子式 | LEL (%VOL) | UEL (%VOL) | 100%LEL = |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | 甲烷 | CH4 | 5.0 | 15.0 | 5.0%VOL = 50000 ppm |
| 2 | 乙烷 | C2H6 | 3.0 | 15.5 | 3.0%VOL = 30000 ppm |
| 3 | 丙烷 | C3H8 | 2.1 | 9.5 | 2.1%VOL = 21000 ppm |
| 4 | 丁烷 | C4H10 | 1.8 | 8.4 | 1.8%VOL = 18000 ppm |
| 5 | 氢气 | H2 | 4.0 | 75.0 | 4.0%VOL = 40000 ppm |
| 6 | 乙烯 | C2H4 | 2.7 | 36.0 | 2.7%VOL = 27000 ppm |
| 7 | 乙炔 | C2H2 | 2.5 | 81.0 | 2.5%VOL = 25000 ppm |
| 8 | 一氧化碳 | CO | 12.5 | 74.2 | 12.5%VOL = 125000 ppm |

## 计算公式

```
1 %VOL = 10000 ppm
%LEL = (%VOL / LEL) x 100
```

**示例（甲烷，LEL = 5.0 %VOL）：**

- 10%LEL = 5.0% x 10% = 0.5%VOL = 5000 ppm
- 100%LEL = 5.0%VOL = 50000 ppm

## 参考

- [PyInstaller：将你的 Python 代码打包成独立应用程序](https://www.bilibili.com/read/cv24488127)
- [PyInstaller](https://github.com/pyinstaller/pyinstaller)

## 许可证

本项目采用 [MIT 许可证](LICENSE)。
