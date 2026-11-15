"""读取资料并执行现有直接诊断。"""
import argparse
from .records import RecordBook,output
from .operations import describe

def main():
    parser=argparse.ArgumentParser(description='多层基金持仓的气候暴露穿透与覆盖诊断资料诊断')
    parser.add_argument('data')
    parser.add_argument('--as-of',required=True)
    args=parser.parse_args()
    print(output(describe(RecordBook.load(args.data),args.as_of)))

if __name__=='__main__':
    main()
