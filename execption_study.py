#!/usr/bin/env python
# - * - coding:utf-8 - * -
import sys

# list_a = []
# try:
#     list_a[0]
#     print(list_a)
# #except IndexError:
# except IndexError ,arg_value:
#     print("except:The list is None",arg_value)
# else:
#     print(list_a)

# try:
#     list_a[0]
# #except IndexError:
# finally:
#     print("finally:The list is None")
#     print(list_a)

def funName( level ):
    if level < 1:
        raise Exception("Invalid level!",level)
    #The code behind will not be executed
def main():
    if len(sys.argv) < 2:
        print("Please input argv:\n")
        print("Usage: %s xxxxx" %(sys.argv[0]))
        exit(1)
    in_values = sys.argv[1]
    funName(in_values)


if __name__ == '__main__':
    main()
