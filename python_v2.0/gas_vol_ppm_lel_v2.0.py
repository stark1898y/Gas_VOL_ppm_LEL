import tkinter as tk
from tkinter import messagebox

# 计算函数
def calculate(gas_type, input_value, input_unit):
    
    if gas_type == "甲烷":
        factor = 0.05
    elif gas_type == "乙烷":
        factor = 0.03
    else :
        factor = 0.021

    if input_unit == "ppm":
        ppm = input_value 
        vol = ppm / 10000
        lel = vol / factor
    elif input_unit == "LEL":
        lel = input_value
        vol = lel * factor
        ppm = 10000 * vol
    else :
        vol = input_value
        ppm = 10000 * vol
        lel = vol / factor

    return round(lel, 4), round(vol, 4), round(ppm, 4)

# 清除所有输入和结果
def clear():
    entry_input_value.delete(0, tk.END)
    entry_lel.delete(0, tk.END)
    entry_vol.delete(0, tk.END)
    entry_ppm.delete(0, tk.END)

# 创建主窗口
root = tk.Tk()
root.title("燃气爆炸下限计算器")
root.geometry("400x400")

# 气体类型下拉菜单
label_gas_type = tk.Label(root, text="气体类型：")
label_gas_type.pack()
gas_types = ["甲烷", "乙烷", "丙烷"]
variable = tk.StringVar(root)
variable.set(gas_types[0])
gas_type_menu = tk.OptionMenu(root, variable, *gas_types)
gas_type_menu.pack()

# 添加输入值和单位选择
input_frame = tk.Frame(root)
input_frame.pack()

label_input_value = tk.Label(input_frame, text="输入值:")
label_input_value.pack(side=tk.LEFT)
entry_input_value = tk.Entry(input_frame)
entry_input_value.pack(side=tk.LEFT)

label_unit = tk.Label(input_frame, text="单位:")
label_unit.pack(side=tk.LEFT)
unit_variable = tk.StringVar(root)
unit_variable.set("VOL%")  # 默认单位
unit_menu = tk.OptionMenu(input_frame, unit_variable, "VOL%", "ppm", "LEL")
unit_menu.pack(side=tk.LEFT)


def perform_calculation():
    gas_type = variable.get()
    input_value = entry_input_value.get()
    input_unit = unit_variable.get()

    try:
        input_value = float(input_value)
    except ValueError:
        messagebox.showerror("错误", "输入值必须是一个有效的数值。")
        return

    lel, vol, ppm = calculate(gas_type, input_value, input_unit)

    entry_lel.config(state=tk.NORMAL)  # 允许编辑
    entry_vol.config(state=tk.NORMAL)  # 允许编辑
    entry_ppm.config(state=tk.NORMAL)  # 允许编辑

    entry_lel.delete(0, tk.END)
    entry_lel.insert(tk.END, str(lel))
    entry_vol.delete(0, tk.END)
    entry_vol.insert(tk.END, str(vol))
    entry_ppm.delete(0, tk.END)
    entry_ppm.insert(tk.END, str(ppm))

    # entry_lel.config(state=tk.DISABLED)  # 设置为只读
    # entry_vol.config(state=tk.DISABLED)  # 设置为只读
    # entry_ppm.config(state=tk.DISABLED)  # 设置为只读


# 添加结果显示
result_frame = tk.Frame(root)
result_frame.pack()

label_lel = tk.Label(result_frame, text="LEL:")
label_lel.pack()

entry_lel = tk.Entry(result_frame, state=tk.DISABLED, fg="black")  # 设置文本颜色为蓝色
entry_lel.pack()

label_vol = tk.Label(result_frame, text="VOL%:")
label_vol.pack()

entry_vol = tk.Entry(result_frame, state=tk.DISABLED, fg="black")  # 设置文本颜色为蓝色
entry_vol.pack()

label_ppm = tk.Label(result_frame, text="ppm:")
label_ppm.pack()

entry_ppm = tk.Entry(result_frame, state=tk.DISABLED, fg="black")  # 设置文本颜色为蓝色
entry_ppm.pack()

# 设置初始状态为只读
entry_lel.config(state=tk.DISABLED)
entry_vol.config(state=tk.DISABLED)
entry_ppm.config(state=tk.DISABLED)


# 显示帮助信息
def show_help():
    help_text = """
燃气爆炸下限计算器

计算三种气体（甲烷、乙烷、丙烷）的爆炸下限（LEL）、体积百分比（VOL%）和百万分之一体积（ppm）之间的转换关系。

爆炸浓度 (V%)
物质名称    分子式   下限 LEL   上限 UEL
甲烷        CH4         5          15
乙烷        C2H6        3          15.5
丙烷       C3H8        2.1        9.5

例如，甲烷的爆炸下限为 5.0VOL%，即 100% LEL=5.0VOL%
那么 10% LEL = 5.0VOL% * 10% = 0.5 VOL%
10000 ppm = 1 Vol%

计算公式：
甲烷：LEL = VOL% * 0.05，VOL% = LEL / 0.05，ppm = VOL% * 10000
乙烷：LEL = VOL% * 0.03，VOL% = LEL / 0.03，ppm = VOL% * 10000
丙烷：LEL = VOL% * 0.021，VOL% = LEL / 0.021，ppm = VOL% * 10000

使用方法：
1. 选择气体类型。
2. 输入已知值（LEL、VOL%或ppm）。
3. 点击“计算”按钮，即可自动计算其他两个值。
4. 若要清除所有输入和结果，点击“清除”按钮。


注意事项：
- 请在输入框中只输入数字。
- 计算结果保留小数点后四位。

有任何问题，请点击菜单栏中的“帮助”查看帮助信息。
"""
    messagebox.showinfo("帮助", help_text)

# 创建菜单栏
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# 创建“帮助”菜单
help_menu = tk.Menu(menu_bar)
menu_bar.add_cascade(label="帮助", command=show_help)

# 添加计算和清除按钮
button_frame = tk.Frame(root)
calculate_button = tk.Button(button_frame, text="计算", command=perform_calculation)
calculate_button.pack(side=tk.LEFT, padx=5)
clear_button = tk.Button(button_frame, text="清除", command=clear)
clear_button.pack(side=tk.LEFT, padx=5)

# 将计算和清除按钮放在结果的下方
button_frame.pack(pady=10)

# 将回车键绑定到计算按钮功能
root.bind('<Return>', lambda event=None: perform_calculation())

# 主循环
root.mainloop()