"""
可燃气体 VOL% / ppm / LEL 换算工具 - 自动测试脚本

测试所有 8 种气体 x 3 种输入单位 = 24 组测试用例
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

# 气体数据：(名称, LEL VOL%)
GASES = [
    ("甲烷",     5.0),
    ("乙烷",     3.0),
    ("丙烷",     2.1),
    ("丁烷",     1.8),
    ("氢气",     4.0),
    ("乙烯",     2.7),
    ("乙炔",     2.5),
    ("一氧化碳", 12.5),
]

# 测试用例：(气体索引, 输入单位, 输入值, 期望VOL%, 期望ppm, 期望LEL%)
# 以 100% LEL 为基准测试
TEST_CASES = [
    # (gas_idx, "vol", input, expect_vol, expect_ppm, expect_lel)
    (0, "vol", 5.0,    5.0,    50000, 100.0),   # 甲烷 VOL%=5.0
    (0, "ppm", 50000,  5.0,    50000, 100.0),   # 甲烷 ppm=50000
    (0, "lel", 100.0,  5.0,    50000, 100.0),   # 甲烷 LEL%=100
    (1, "vol", 3.0,    3.0,    30000, 100.0),   # 乙烷 VOL%=3.0
    (1, "ppm", 30000,  3.0,    30000, 100.0),   # 乙烷 ppm=30000
    (1, "lel", 100.0,  3.0,    30000, 100.0),   # 乙烷 LEL%=100
    (2, "vol", 2.1,    2.1,    21000, 100.0),   # 丙烷 VOL%=2.1
    (2, "ppm", 21000,  2.1,    21000, 100.0),   # 丙烷 ppm=21000
    (2, "lel", 100.0,  2.1,    21000, 100.0),   # 丙烷 LEL%=100
    (3, "vol", 1.8,    1.8,    18000, 100.0),   # 丁烷 VOL%=1.8
    (3, "ppm", 18000,  1.8,    18000, 100.0),   # 丁烷 ppm=18000
    (3, "lel", 100.0,  1.8,    18000, 100.0),   # 丁烷 LEL%=100
    (4, "vol", 4.0,    4.0,    40000, 100.0),   # 氢气 VOL%=4.0
    (4, "ppm", 40000,  4.0,    40000, 100.0),   # 氢气 ppm=40000
    (4, "lel", 100.0,  4.0,    40000, 100.0),   # 氢气 LEL%=100
    (5, "vol", 2.7,    2.7,    27000, 100.0),   # 乙烯 VOL%=2.7
    (5, "ppm", 27000,  2.7,    27000, 100.0),   # 乙烯 ppm=27000
    (5, "lel", 100.0,  2.7,    27000, 100.0),   # 乙烯 LEL%=100
    (6, "vol", 2.5,    2.5,    25000, 100.0),   # 乙炔 VOL%=2.5
    (6, "ppm", 25000,  2.5,    25000, 100.0),   # 乙炔 ppm=25000
    (6, "lel", 100.0,  2.5,    25000, 100.0),   # 乙炔 LEL%=100
    (7, "vol", 12.5,   12.5,   125000, 100.0),  # 一氧化碳 VOL%=12.5
    (7, "ppm", 125000, 12.5,   125000, 100.0),  # 一氧化碳 ppm=125000
    (7, "lel", 100.0,  12.5,   125000, 100.0),  # 一氧化碳 LEL%=100
    # 额外测试：10% LEL
    (0, "lel", 10.0,   0.5,    5000,  10.0),    # 甲烷 10% LEL
    (0, "vol", 0.5,    0.5,    5000,  10.0),    # 甲烷 VOL%=0.5
    (0, "ppm", 5000,   0.5,    5000,  10.0),    # 甲烷 ppm=5000
]

TOLERANCE = 0.01  # 允许误差


def calculate(lel_limit, input_value, input_unit):
    """Python 版本的计算函数"""
    if input_unit == "ppm":
        ppm = input_value
        vol = ppm / 10000
        lel = vol / lel_limit * 100
    elif input_unit == "lel":
        lel = input_value
        vol = lel * lel_limit / 100
        ppm = vol * 10000
    else:  # vol
        vol = input_value
        ppm = vol * 10000
        lel = vol / lel_limit * 100
    return round(vol, 4), round(ppm, 2), round(lel, 4)


def approx_equal(a, b, tol=TOLERANCE):
    return abs(a - b) < tol


def run_tests():
    passed = 0
    failed = 0

    print("=" * 70)
    print("可燃气体 VOL% / ppm / LEL 换算工具 - 自动测试")
    print("=" * 70)

    for i, (gas_idx, unit, inp, exp_vol, exp_ppm, exp_lel) in enumerate(TEST_CASES):
        name, lel_limit = GASES[gas_idx]
        vol, ppm, lel = calculate(lel_limit, inp, unit)

        ok = (approx_equal(vol, exp_vol) and
              approx_equal(ppm, exp_ppm) and
              approx_equal(lel, exp_lel))

        status = "PASS" if ok else "FAIL"
        if ok:
            passed += 1
        else:
            failed += 1

        unit_label = {"vol": "VOL%", "ppm": "ppm", "lel": "LEL%"}[unit]
        print(f"  [{status}] {name} {unit_label}={inp}  ->  VOL%={vol}, ppm={ppm}, LEL%={lel}")
        if not ok:
            print(f"         期望: VOL%={exp_vol}, ppm={exp_ppm}, LEL%={exp_lel}")

    print("=" * 70)
    print(f"  结果: {passed} 通过, {failed} 失败, 共 {passed + failed} 项")
    print("=" * 70)

    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
