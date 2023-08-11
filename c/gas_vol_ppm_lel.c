/*
 * @Author       : yzy
 * @Date         : 2023-02-20 15:55:43
 * @LastEditors: xt 1834031381@qq.com
 * @LastEditTime: 2023-08-11 14:45:41
 * @FilePath: \undefinedc:\Users\XT\Desktop\Gas_VOL_ppm_LEL\c\gas_vol_ppm_lel.c
 * @Description  :  VOL、ppm、LEL
 *
 * Copyright (c) 2023 by yzy, All Rights Reserved.
 */

#include <stdio.h>
#include <windows.h>

#define METHANE_LEL 0.05
#define ETHANCE_LEL 0.03
#define PROPANCE_LEL 0.021

typedef enum
{
    kMethane = 1,
    kEthance,
    kPropance
} TeGasNumber;

typedef enum
{
    kVol = 1,
    kLel,
    kPpm
} TeGasValue;

void UI_GasIntroduce(void);
int IsValid(int gas_num);
void GasChange(int number, double value);
double LEL_GasGet(int gas_name);
void GasChangeOtherValue(int change_num, double gas_lel, double value);

int main(void)
{
    int gas_change_number;
    double val;

    // "c": "cd $dir && gcc -fexec-charset=GBK $fileName -o $fileNameWithoutExt && $dir$fileNameWithoutExt",
    // SetConsoleOutputCP(65001);  //防止.exe中文乱码

    UI_GasIntroduce();

    while (1)
    {
        rewind(stdin);                                      // 清空缓冲区,防止输入字符出现死循环
        if (scanf("%d %lf", &gas_change_number, &val) == 2) // 正确读取数字
        {
            if (IsValid(gas_change_number) == 0) // 输入编号是否合理
            {
                continue;
            }
            else
            {
                GasChange(gas_change_number, val);
                printf("\r\n请输入气体编号和值,如\"11 6\"表示甲烷VOL=6,计算LEL值、PPM值\r\n");
            }
        }
        else
        {
            printf("\r\n输入有误,请重新输入气体编号和值,如\"11 6\"表示甲烷VOL=6,计算LEL值、PPM值\r\n");
        }
    }

    return 0;
}

/**
 * @description: 气体VOL、LEL、ppm转换对应编号
 * @return {*}
 */
void UI_GasIntroduce(void)
{
    printf("/******************************************************************************/\r\n");
    printf("              VOL、LEL、ppm转换表\r\n"
           "           1:甲烷      2:乙烷      3:丙烷\r\n"
           "1:VOL	    11          21	    31\r\n"
           "2:LEL	    12	        22	    32\r\n"
           "3:PPM       13	        23	    33\r\n"
           "Tip:编号11,表示对甲烷VOL的值进行换算,即输入甲烷VOL的值并将其转换成对应的LEL值、PPM值。\r\n");
    printf("/******************************************************************************/\r\n");
    printf("\r\n请输入气体编号和值,如\"11 6\"表示甲烷VOL=6,计算LEL值、PPM值\r\n");
}

/**
 * @description: 编号是否有效，参考转换表
 * @param {int}  gas_num 编号
 * @return {*} 0:无效;1:有效;
 */
int IsValid(int gas_num)
{
    int flag = 0;

    if (gas_num >= 11 && gas_num <= 13)
    {
        flag = 1;
    }
    else if (gas_num >= 21 && gas_num <= 23)
    {
        flag = 1;
    }
    else if (gas_num >= 31 && gas_num <= 33)
    {
        flag = 1;
    }

    if (flag == 0)
    {
        printf("\r\n输入有误,请输入气体编号和值,如\"11 6\"表示甲烷VOL=6,计算LEL值、PPM值\r\n");
    }

    return flag;
}

/**
 * @description: 根据气体获取气体默认系数LEL，参考转换表，如1表示甲烷
 * @param {int}  gas_name，气体名称
 * @return {*} lel
 */
double LEL_GasGet(int gas_name)
{
    double lel;
    switch (gas_name)
    {
    case kMethane:
        lel = METHANE_LEL;
        printf("甲烷\r\n");
        break;

    case kEthance:
        printf("乙烷\r\n");
        lel = ETHANCE_LEL;
        break;

    case kPropance:
        printf("丙烷\r\n");
        lel = PROPANCE_LEL;
        break;
    default:
        break;
    }

    return lel;
}

/**
 * @description: 参考转换表，如1表示输入气体VOL，计算LEL、PPM
 * @param {int} change_num  转换编号
 * @param {double} gas_lel 气体默认值LEL
 * @param {double} value  VOL、LEL、PPM输入值
 * @return {*}
 */
void GasChangeOtherValue(int change_num, double gas_lel, double value)
{

    double vol, lel, ppm;
    switch (change_num)
    {
    case kVol:
        vol = value;
        ppm = 10000 * vol;
        lel = vol / gas_lel;
        break;

    case kLel:
        lel = value;
        vol = lel * gas_lel;
        ppm = 10000 * vol;
        break;

    case kPpm:
        ppm = value;
        vol = ppm / 10000;
        lel = vol / gas_lel;
        break;

    default:
        break;
    }

    printf("VOL%% = %.4lf\r\n", vol);
    printf("LEL = %.4lf\r\n", lel);
    printf("PPM = %.4lf\r\n\r\n", ppm);
}

/**
 * @description: 参考转换表，如11表示通过甲烷输入VOL，获取LEL、PPM的值
 * @param {int} number 转换编号
 * @param {double} value VOL、LEL、PPM输入值，
 * @return {*}
 */
void GasChange(int number, double value)
{
    int gas_number;
    int change_number;
    double gas_lel;
    int a;

    gas_number = number / 10;
    change_number = number % 10;

    gas_lel = LEL_GasGet(gas_number);
    GasChangeOtherValue(change_number, gas_lel, value);
}
