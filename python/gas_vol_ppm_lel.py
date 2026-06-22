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
from tkinter import messagebox

# 气体数据：(名称, 分子式, LEL VOL%, UEL VOL%)
GAS_DATA = {
    "甲烷(CH4)":     (5.0,  15.0),
    "乙烷(C2H6)":    (3.0,  15.5),
    "丙烷(C3H8)":    (2.1,  9.5),
    "丁烷(C4H10)":   (1.8,  8.4),
    "氢气(H2)":      (4.0,  75.0),
    "乙烯(C2H4)":    (2.7,  36.0),
    "乙炔(C2H2)":    (2.5,  81.0),
    "一氧化碳(CO)":  (12.5, 74.2),
}


def calculate(gas_name, input_value, input_unit):
    """根据输入气体、数值和单位，计算另外两个单位的值"""
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

    return round(vol, 4), round(ppm, 2), round(lel, 4)


class GasConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("可燃气体 %VOL / ppm / %LEL 换算工具")
        self.root.geometry("420x420")
        self.root.resizable(False, False)

        self._create_menu()
        self._create_widgets()

        # 回车键触发计算
        self.root.bind('<Return>', lambda e: self.perform_calculation())

    def _create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="关于", command=self.show_help)

    def _create_widgets(self):
        # 气体类型
        tk.Label(self.root, text="气体类型:", font=("Arial", 10, "bold")).pack(pady=(10, 2))
        self.gas_var = tk.StringVar(value=list(GAS_DATA.keys())[0])
        tk.OptionMenu(self.root, self.gas_var, *GAS_DATA.keys()).pack()

        # 输入区域
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="输入值:").pack(side=tk.LEFT)
        self.entry_input = tk.Entry(input_frame, width=12)
        self.entry_input.pack(side=tk.LEFT, padx=5)

        tk.Label(input_frame, text="单位:").pack(side=tk.LEFT)
        self.unit_var = tk.StringVar(value="%VOL")
        tk.OptionMenu(input_frame, self.unit_var, "%VOL", "ppm", "%LEL").pack(side=tk.LEFT)

        # 结果显示
        result_frame = tk.Frame(self.root)
        result_frame.pack(pady=10)

        self.result_vol = self._create_result_row(result_frame, "%VOL:")
        self.result_ppm = self._create_result_row(result_frame, "ppm:")
        self.result_lel = self._create_result_row(result_frame, "%LEL:")

        # 按钮
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="计算", command=self.perform_calculation, width=8).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="清除", command=self.clear, width=8).pack(side=tk.LEFT, padx=5)

    def _create_result_row(self, parent, label_text):
        frame = tk.Frame(parent)
        frame.pack(fill=tk.X, pady=2)
        tk.Label(frame, text=label_text, width=8, anchor=tk.E).pack(side=tk.LEFT)
        entry = tk.Entry(frame, state=tk.DISABLED, fg="black", width=20)
        entry.pack(side=tk.LEFT, padx=5)
        return entry

    def _set_result(self, entry, value):
        entry.config(state=tk.NORMAL)
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(value))
        entry.config(state=tk.DISABLED)

    def perform_calculation(self):
        try:
            input_value = float(self.entry_input.get())
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数值")
            return

        gas_name = self.gas_var.get()
        input_unit = self.unit_var.get()

        vol, ppm, lel = calculate(gas_name, input_value, input_unit)

        self._set_result(self.result_vol, vol)
        self._set_result(self.result_ppm, ppm)
        self._set_result(self.result_lel, lel)

    def clear(self):
        self.entry_input.delete(0, tk.END)
        for entry in (self.result_vol, self.result_ppm, self.result_lel):
            self._set_result(entry, "")

    def show_help(self):
        help_text = """可燃气体 %VOL / ppm / %LEL 换算工具

支持 8 种常见可燃气体:
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
  %LEL = %VOL / LEL(%VOL) x 100

示例(甲烷):
  10%LEL = 5.0% x 10% = 0.5%VOL = 5000 ppm
  100%LEL = 5.0%VOL = 50000 ppm"""
        messagebox.showinfo("帮助", help_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = GasConverterApp(root)
    root.mainloop()
