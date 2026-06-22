/*
 * @Description  : 可燃气体 VOL%、ppm、LEL 换算工具（支持 8 种常见可燃气体）
 * @Date         : 2023-02-20
 * @Author       : yzy
 *
 * Copyright (c) 2023 by yzy, All Rights Reserved.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define GAS_COUNT 8

/* 气体数据结构 */
typedef struct
{
    const char *name;    /* 中文名 */
    const char *formula; /* 分子式 */
    double lel;          /* 爆炸下限 VOL% */
    double uel;          /* 爆炸上限 VOL% */
} GasInfo;

/* 8 种常见可燃气体数据 */
static const GasInfo gas_table[GAS_COUNT] = {
    {"甲烷",     "CH4",  5.0,  15.0},
    {"乙烷",     "C2H6", 3.0,  15.5},
    {"丙烷",     "C3H8", 2.1,  9.5},
    {"丁烷",     "C4H10",1.8,  8.4},
    {"氢气",     "H2",   4.0,  75.0},
    {"乙烯",     "C2H4", 2.7,  36.0},
    {"乙炔",     "C2H2", 2.5,  81.0},
    {"一氧化碳", "CO",   12.5, 74.2},
};

/* 打印气体列表 */
void print_gas_list(void)
{
    printf("\n");
    printf("================================================================\n");
    printf("             可燃气体 VOL%% / ppm / LEL 换算工具\n");
    printf("================================================================\n");
    printf("  编号  气体名称      分子式    LEL(VOL%%)  UEL(VOL%%)\n");
    printf("----------------------------------------------------------------\n");
    for (int i = 0; i < GAS_COUNT; i++)
    {
        printf("  %-4d  %-10s  %-6s    %-8.1f    %-8.1f\n",
               i + 1, gas_table[i].name, gas_table[i].formula,
               gas_table[i].lel, gas_table[i].uel);
    }
    printf("================================================================\n");
    printf("  单位编号: 1=VOL%%   2=ppm   3=LEL%%\n");
    printf("  输入格式: <气体编号> <单位编号> <值>\n");
    printf("  示例: 1 1 5.0  →  甲烷 VOL%%=5.0, 计算 ppm 和 LEL%%\n");
    printf("================================================================\n\n");
}

/* 从任意一种单位计算另外两种 */
void convert(int gas_idx, int unit_idx, double value)
{
    if (gas_idx < 0 || gas_idx >= GAS_COUNT)
    {
        printf("  错误: 气体编号无效 (1-%d)\n", GAS_COUNT);
        return;
    }
    if (unit_idx < 1 || unit_idx > 3)
    {
        printf("  错误: 单位编号无效 (1-3)\n");
        return;
    }

    const GasInfo *gas = &gas_table[gas_idx];
    double vol, ppm, lel;

    switch (unit_idx)
    {
    case 1: /* 输入 VOL% */
        vol = value;
        ppm = vol * 10000;
        lel = (gas->lel > 0) ? (vol / gas->lel * 100) : 0;
        break;
    case 2: /* 输入 ppm */
        ppm = value;
        vol = ppm / 10000;
        lel = (gas->lel > 0) ? (vol / gas->lel * 100) : 0;
        break;
    case 3: /* 输入 LEL% */
        lel = value;
        vol = lel * gas->lel / 100;
        ppm = vol * 10000;
        break;
    default:
        return;
    }

    printf("\n  [%s (%s)]\n", gas->name, gas->formula);
    printf("  VOL%% = %.4f\n", vol);
    printf("  ppm   = %.2f\n", ppm);
    printf("  LEL%%  = %.4f\n\n", lel);
}

int main(void)
{
    int gas_idx, unit_idx;
    double value;

    print_gas_list();

    while (1)
    {
        printf("请输入 (气体编号 单位编号 值): ");
        rewind(stdin);

        if (scanf("%d %d %lf", &gas_idx, &unit_idx, &value) == 3)
        {
            if (gas_idx < 1 || gas_idx > GAS_COUNT)
            {
                printf("  气体编号无效，请输入 1-%d\n", GAS_COUNT);
                continue;
            }
            if (unit_idx < 1 || unit_idx > 3)
            {
                printf("  单位编号无效，请输入 1-3\n");
                continue;
            }
            convert(gas_idx - 1, unit_idx, value);
        }
        else
        {
            printf("  输入格式错误，请按: 气体编号 单位编号 值\n");
        }
    }

    return 0;
}
