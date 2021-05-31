#!/usr/bin/python

import random, string
import argparse
from tqdm import tqdm
import time
import os


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--token_len', default=7, type=int, help="length of a token")
    parser.add_argument('--num', default=10000000, type=int, help="number of tokens")
    parser.add_argument('--file', '-f', default="tokens.txt", help="the storage file path")
    return parser.parse_args()


def generate_tokens(file_path: str, num: int, token_len: int) -> None:
    """generate a text file of tokens, each line contains one token

    Args:
        file_path (str): file path to write the token into
        num (int): number of tokens
        token_len (int): number of chars of the single token
    """
    with open(file_path, 'w') as f:
        for _ in tqdm(range(num), total=num):
            # SystemRandom makes the generator more cryptographically secure -- hard to predict!!
            _token = ''.join(random.SystemRandom().choices(string.ascii_lowercase, k=token_len))+"\n"
            f.write(_token)

if __name__=="__main__":
    args = parse_args()
    
    file_name = os.path.basename(args.file)
    current_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_dir, file_name)

    current_time = time.time()
    generate_tokens(file_path, num=args.num, token_len=args.token_len)
    end_time = time.time()
    print("elapsed time =", end_time-current_time)