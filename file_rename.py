# @since Python 3.7
# 批量修改文件名
import os
import re
import argparse
import random

VERSION = "1.0"
RECURSION = False


def rename_all(dest_dir, regex, replace_str):
    current_path = os.getcwd()  # 后续改回当前工作目录，方便递归
    os.chdir(dest_dir)  # 将当前工作目录修改为待修改文件夹的位置
    work_dir = os.listdir(dest_dir)  # 待修改文件夹
    pattern = re.compile(regex)
    for file_name in work_dir:  # 遍历文件夹中所有文件
        if os.path.isdir(file_name):
            if RECURSION:
                rename_all(rf"{dest_dir}\{file_name}", regex, replace_str)  # 递归
        else:
            new_file_name = pattern.sub(replace_str, file_name)  # 进行匹配
            if new_file_name != file_name:
                os.rename(file_name, new_file_name)  # 文件重新命名
    print(f"已完成{dest_dir}文件夹下所有文件的重命名")
    os.chdir(current_path)


def auto_rename(dest_dir):
    os.chdir(dest_dir)
    work_dir = os.listdir(dest_dir)
    work_dir = sorted(work_dir, key=lambda x: os.path.getmtime(rf"{dest_dir}\{x}"))
    n = 1
    nstr = ""
    pattern = re.compile(r"^[^\.]*")
    for file_name in work_dir:
        if os.path.isdir(file_name):
            continue
        if n < 10:
            nstr = "000" + str(n)
        if 9 < n < 100:
            nstr = "00" + str(n)
        if 99 < n < 1000:
            nstr = "0" + str(n)
        new_file_name = pattern.sub(nstr, file_name)
        if new_file_name == file_name:
            n = n + 1
            continue
        if os.path.exists(new_file_name):
            os.rename(new_file_name, str(random.randint(0, 100)) + new_file_name)
        os.rename(file_name, new_file_name)
        n = n + 1
    print("done")


if __name__ == '__main__':
    # 迂回实现下列功能：正常情况下，需要三个参数args.dest_dir, args.regex, args.replace_str
    # 当--auto时，只需目录即可
    # 矛盾在于，可选参数不能单独使用，一定要填入必选参数
    # 只有默认的 -h，以及 action="version" 时，才能忽略必选参数单独使用可选参数
    parser = argparse.ArgumentParser(description="重命名目标目录下的文件，根据正则匹配将替换的内容。"
                                                 "字符串参数不要使用单引号包裹，可以使用双引号或不使用引号。",
                                     usage="%(prog)s [-h] [-v] [-r] [--auto] 目标文件夹 正则表达式 用于替换的字符串",
                                     epilog='用法示例: python %(prog)s -r D:\\test \\.jfif .jpg')
    # metavar伪装 help文档
    parser.add_argument("default_usage", nargs='*', metavar="目标文件夹\t\t建议使用绝对路径，必选参数"
                                                            "\n  正则表达式\t\t被匹配上的位置将被替换，与--auto互斥"
                                                            "\n  用于替换的字符串\t与--auto互斥，使用--auto则无需此参数")

    parser.add_argument("-v", "--version", help=r"显示程序版本", action="version", version=VERSION)
    # -r --auto互斥
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-r", "--recursion", help=r"递归运行，子文件夹中的文件也进行替换。与--auto互斥", action="store_true")
    group.add_argument("--auto", help=r"自动根据文件修改时间来用递增数列命名，如 0001.png 0002.png...0001.png为最早创建(修改)的文件，"
                                      r"此模式会重命名文件夹下所有文件，文件夹不会被命名",
                       action="store_true")
    args = parser.parse_args()
    if args.auto:
        if len(args.default_usage) != 1:
            print("有且需要一个参数：目标文件夹，详情使用 -h 查看")
            exit(-1)
    else:
        if len(args.default_usage) != 3:
            print("缺少必选参数，详情使用 -h 查看")
            exit(-1)
        if args.default_usage[1] == "'" and args.default_usage[1] == "'":
            print("提示，字符串参数不要使用单引号包裹，可以使用双引号或不使用引号：" + args.regex)
        RECURSION = args.recursion
        if RECURSION:
            print("已开启递归选项")
        else:
            print("未开启递归选项")

    if not os.path.exists(args.default_usage[0]):
        print("目标文件夹不存在，详情使用 -h 查看")
        exit(-1)

    if args.auto:
        auto_rename(args.default_usage[0])
    else:
        rename_all(args.default_usage[0], args.default_usage[1], args.default_usage[2])
