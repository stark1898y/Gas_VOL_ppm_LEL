"""
可燃气体 %VOL、ppm、%LEL 换算工具（支持 8 种常见可燃气体）

气体数据:
    甲烷(CH4)     LEL=5.0%  UEL=15.0%
    乙烷(C2H6)    LEL=3.0%  UEL=15.5%
    丙烷(C3H8)    LEL=2.1%  UEL=9.5%
    丁烷(C4H10)   LEL=1.8%  UEL=8.4%
    氢气(H2)      LEL=4.0%  UEL=75.0%
    乙烯(C2H4)    LEL=2.7%  UEL=36.0%
    乙炔(C2H2)    LEL=2.5%  UEL=81.0%
    一氧化碳(CO)  LEL=12.5% UEL=74.2%

公式:
    1 %VOL = 10000 ppm
    %LEL = %VOL / LEL(%VOL) * 100
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import webbrowser

VERSION = "v2.1.0"

# 气体数据：(LEL %VOL, UEL %VOL)
GAS_DATA = {
    "甲烷 (CH4)":     (5.0,  15.0),
    "乙烷 (C2H6)":    (3.0,  15.5),
    "丙烷 (C3H8)":    (2.1,  9.5),
    "丁烷 (C4H10)":   (1.8,  8.4),
    "氢气 (H2)":      (4.0,  75.0),
    "乙烯 (C2H4)":    (2.7,  36.0),
    "乙炔 (C2H2)":    (2.5,  81.0),
    "一氧化碳 (CO)":  (12.5, 74.2),
}

# 颜色主题
COLORS = {
    "bg":           "#F5F7FA",
    "card_bg":      "#FFFFFF",
    "primary":      "#E67E22",
    "primary_dark": "#D35400",
    "danger":       "#E74C3C",
    "success":      "#27AE60",
    "text":         "#2C3E50",
    "text_light":   "#7F8C8D",
    "border":       "#E0E0E0",
    "result_bg":    "#FFF8F0",
    "header_bg":    "#E67E22",
    "white":        "#FFFFFF",
}


def calculate(gas_name, input_value, input_unit):
    lel_limit, _ = GAS_DATA[gas_name]
    if input_unit == "ppm":
        ppm = input_value
        vol = ppm / 10000
        lel = vol / lel_limit * 100
    elif input_unit == "%LEL":
        lel = input_value
        vol = lel * lel_limit / 100
        ppm = vol * 10000
    else:  # %VOL
        vol = input_value
        ppm = vol * 10000
        lel = vol / lel_limit * 100
    return round(vol, 6), round(ppm, 2), round(lel, 4)


def get_resource_path(filename):
    """获取资源文件路径，兼容 PyInstaller 打包"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)


class GasConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"可燃气体浓度换算工具 {VERSION}")
        self.root.geometry("520x700")
        self.root.minsize(420, 600)
        self.root.configure(bg=COLORS["bg"])

        # 设置图标
        try:
            icon_path = get_resource_path("icon/燃气.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception:
            pass

        self._create_widgets()
        self.root.bind('<Return>', lambda e: self.perform_calculation())

    def _create_widgets(self):
        # ===== 标题栏 =====
        header = tk.Frame(self.root, bg=COLORS["header_bg"], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(
            header, text="可燃气体浓度换算工具",
            font=("Microsoft YaHei UI", 16, "bold"),
            fg=COLORS["white"], bg=COLORS["header_bg"]
        ).pack(expand=True)

        # ===== 主体区域 =====
        main_frame = tk.Frame(self.root, bg=COLORS["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        # --- 输入卡片 ---
        input_card = tk.Frame(main_frame, bg=COLORS["card_bg"],
                              relief=tk.FLAT, bd=0, highlightthickness=1,
                              highlightbackground=COLORS["border"])
        input_card.pack(fill=tk.X, pady=(0, 15))

        inner = tk.Frame(input_card, bg=COLORS["card_bg"])
        inner.pack(padx=20, pady=18)

        # 气体选择
        tk.Label(inner, text="气体类型", font=("Microsoft YaHei UI", 10),
                 fg=COLORS["text_light"], bg=COLORS["card_bg"]).pack(anchor=tk.W)
        self.gas_var = tk.StringVar(value=list(GAS_DATA.keys())[0])
        gas_combo = ttk.Combobox(inner, textvariable=self.gas_var,
                                 values=list(GAS_DATA.keys()),
                                 state="readonly", width=25,
                                 font=("Microsoft YaHei UI", 11))
        gas_combo.pack(fill=tk.X, pady=(2, 12))

        # 输入值 + 单位
        row = tk.Frame(inner, bg=COLORS["card_bg"])
        row.pack(fill=tk.X)

        left = tk.Frame(row, bg=COLORS["card_bg"])
        left.pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Label(left, text="输入值", font=("Microsoft YaHei UI", 10),
                 fg=COLORS["text_light"], bg=COLORS["card_bg"]).pack(anchor=tk.W)
        self.entry_input = tk.Entry(left, font=("Microsoft YaHei UI", 13),
                                    relief=tk.FLAT, bd=2,
                                    highlightthickness=1,
                                    highlightbackground=COLORS["border"],
                                    highlightcolor=COLORS["primary"])
        self.entry_input.pack(fill=tk.X, pady=(2, 0), ipady=6)

        right = tk.Frame(row, bg=COLORS["card_bg"])
        right.pack(side=tk.LEFT, padx=(15, 0))
        tk.Label(right, text="单位", font=("Microsoft YaHei UI", 10),
                 fg=COLORS["text_light"], bg=COLORS["card_bg"]).pack(anchor=tk.W)
        self.unit_var = tk.StringVar(value="%VOL")
        unit_combo = ttk.Combobox(right, textvariable=self.unit_var,
                                  values=["%VOL", "ppm", "%LEL"],
                                  state="readonly", width=8,
                                  font=("Microsoft YaHei UI", 11))
        unit_combo.pack(pady=(2, 0))

        # --- 按钮 ---
        btn_frame = tk.Frame(main_frame, bg=COLORS["bg"])
        btn_frame.pack(fill=tk.X, pady=(0, 15))

        self.calc_btn = tk.Button(
            btn_frame, text="计  算", font=("Microsoft YaHei UI", 12, "bold"),
            fg=COLORS["white"], bg=COLORS["primary"],
            activebackground=COLORS["primary_dark"],
            activeforeground=COLORS["white"],
            relief=tk.FLAT, cursor="hand2",
            command=self.perform_calculation
        )
        self.calc_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 8))

        self.clear_btn = tk.Button(
            btn_frame, text="清  除", font=("Microsoft YaHei UI", 12),
            fg=COLORS["text"], bg="#ECF0F1",
            activebackground="#D5DBDB", activeforeground=COLORS["text"],
            relief=tk.FLAT, cursor="hand2",
            command=self.clear
        )
        self.clear_btn.pack(side=tk.LEFT, ipady=8, padx=(0, 0))

        # --- 结果卡片 ---
        result_card = tk.Frame(main_frame, bg=COLORS["card_bg"],
                               relief=tk.FLAT, bd=0, highlightthickness=1,
                               highlightbackground=COLORS["border"])
        result_card.pack(fill=tk.X, pady=(0, 15))

        result_inner = tk.Frame(result_card, bg=COLORS["card_bg"])
        result_inner.pack(padx=20, pady=15)

        self.result_labels = {}
        for unit_name, desc in [("%VOL", "体积百分比"), ("ppm", "百万分之一体积"), ("%LEL", "爆炸下限百分比")]:
            row_frame = tk.Frame(result_inner, bg=COLORS["result_bg"],
                                 highlightthickness=1,
                                 highlightbackground=COLORS["border"])
            row_frame.pack(fill=tk.X, pady=3)

            tk.Label(row_frame, text=unit_name,
                     font=("Microsoft YaHei UI", 10, "bold"),
                     fg=COLORS["primary"], bg=COLORS["result_bg"],
                     width=8, anchor=tk.W).pack(side=tk.LEFT, padx=(10, 5), pady=8)

            val_label = tk.Label(row_frame, text="--",
                                 font=("Consolas", 16, "bold"),
                                 fg=COLORS["text"], bg=COLORS["result_bg"],
                                 anchor=tk.E)
            val_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=8)

            tk.Label(row_frame, text=desc,
                     font=("Microsoft YaHei UI", 8),
                     fg=COLORS["text_light"], bg=COLORS["result_bg"],
                     anchor=tk.E).pack(side=tk.RIGHT, padx=(5, 10), pady=8)

            self.result_labels[unit_name] = val_label

        # --- 危险提示 ---
        self.warning_label = tk.Label(
            main_frame, text="", font=("Microsoft YaHei UI", 10, "bold"),
            fg=COLORS["danger"], bg=COLORS["bg"], wraplength=460
        )
        self.warning_label.pack(fill=tk.X)

        # --- 底部信息 ---
        formula_label = tk.Label(main_frame, text="1 %VOL = 10,000 ppm  |  %LEL = %VOL / LEL x 100",
                 font=("Microsoft YaHei UI", 8),
                 fg=COLORS["text_light"], bg=COLORS["bg"])
        formula_label.pack(pady=(15, 4))

        copyright_frame = tk.Frame(main_frame, bg=COLORS["bg"])
        copyright_frame.pack()
        tk.Label(copyright_frame,
                 text=f"Gas VOL ppm LEL Calculator {VERSION} © 2023 stark1898y | ",
                 font=("Microsoft YaHei UI", 8),
                 fg=COLORS["text_light"], bg=COLORS["bg"]).pack(side=tk.LEFT)
        github_link = tk.Label(copyright_frame, text="GitHub",
                               font=("Microsoft YaHei UI", 8, "underline"),
                               fg=COLORS["primary"], bg=COLORS["bg"], cursor="hand2")
        github_link.pack(side=tk.LEFT)
        github_link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/stark1898y/Gas_VOL_ppm_LEL"))
        tk.Label(copyright_frame, text=" | ",
                 font=("Microsoft YaHei UI", 8),
                 fg=COLORS["text_light"], bg=COLORS["bg"]).pack(side=tk.LEFT)
        gitee_link = tk.Label(copyright_frame, text="Gitee",
                              font=("Microsoft YaHei UI", 8, "underline"),
                              fg=COLORS["primary"], bg=COLORS["bg"], cursor="hand2")
        gitee_link.pack(side=tk.LEFT)
        gitee_link.bind("<Button-1>", lambda e: webbrowser.open("https://gitee.com/stark1898/Gas_VOL_ppm_LEL"))
        tk.Label(copyright_frame, text=" | MIT License",
                 font=("Microsoft YaHei UI", 8),
                 fg=COLORS["text_light"], bg=COLORS["bg"]).pack(side=tk.LEFT)

        # 焦点到输入框
        self.entry_input.focus_set()

    def perform_calculation(self):
        try:
            input_value = float(self.entry_input.get())
        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的数值")
            self.entry_input.focus_set()
            return

        gas_name = self.gas_var.get()
        input_unit = self.unit_var.get()

        vol, ppm, lel = calculate(gas_name, input_value, input_unit)

        self.result_labels["%VOL"].config(text=f"{vol}")
        self.result_labels["ppm"].config(text=f"{ppm:,.2f}")
        self.result_labels["%LEL"].config(text=f"{lel}")

        # 高亮当前输入的单位
        for name, label in self.result_labels.items():
            if name == input_unit:
                label.config(fg=COLORS["primary"])
            else:
                label.config(fg=COLORS["text"])

        # 危险提示
        lel_val = lel
        if lel_val >= 100:
            self.warning_label.config(
                text="⚠ 极度危险！已达到爆炸下限，遇明火即爆！",
                fg=COLORS["danger"])
        elif lel_val >= 25:
            self.warning_label.config(
                text="⚠ 高危险！浓度已超过25%LEL，严禁明火！",
                fg="#E67E22")
        elif lel_val >= 10:
            self.warning_label.config(
                text="⚠ 注意：浓度已超过10%LEL，需加强通风",
                fg="#F39C12")
        else:
            self.warning_label.config(text="")

    def clear(self):
        self.entry_input.delete(0, tk.END)
        for label in self.result_labels.values():
            label.config(text="--", fg=COLORS["text"])
        self.warning_label.config(text="")
        self.entry_input.focus_set()


if __name__ == "__main__":
    root = tk.Tk()

    # 设置 ttk 主题
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TCombobox",
                     fieldbackground=COLORS["white"],
                     background=COLORS["white"],
                     borderwidth=0)

    app = GasConverterApp(root)
    root.mainloop()
