import multiprocessing
import random
import string
import argparse
import os
import time


def parse_args():
    """
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--token_len', default=7, type=int, help="length of a token")
    parser.add_argument('--num', default=10000000, type=int, help="number of tokens")
    parser.add_argument('--file', '-f', default="tokens.txt", help="the storage file path")
    parser.add_argument(
        '--method', default="parallel", 
        choices=['parallel', "sequential"], help="method of generating [parallel, sequential]")
    parser.add_argument('--secure', action="store_true", help="generate secure tokens")
    return parser.parse_args()


def generate_tokens_mul(file_path: str, num: int, token_len: int, secure: bool) -> None:
    """generate a text file of tokens in parallel, each line contains one token

    Args:
        file_path (str): file path to write the token into
        num (int): number of tokens
        token_len (int): number of chars of the single token
        secure (bool): whether to generate cryptographically secure token, 
        makes the procedure slower
    """
    # generate processes as much as half the cpu count
    # and make sure the tokens number is divisible by th processes number
    _pools = int(multiprocessing.cpu_count() / 2)
    while num % _pools > 0 and _pools > 1:
        _pools-=1

    _chunk = int(num / _pools)
    print("processes:",_pools)
    with multiprocessing.Pool(_pools) as p:
        _tokens = p.starmap(_generate_token, [[token_len, _chunk, secure]]*_pools)


    # flatten the result
    tokens = []
    for _token in _tokens:
        tokens += _token
    print(len(tokens))

    # write to the file
    with open(file_path, 'w', encoding="utf-8") as f:
        f.writelines(tokens)


def generate_tokens(file_path: str, num: int, token_len: int, secure: bool) -> None:
    """generate a text file of tokens, each line contains one token

    Args:
        file_path (str): file path to write the token into
        num (int): number of tokens
        token_len (int): number of chars of the single token
        secure (bool): whether to generate cryptographically secure token,
        makes the procedure slower
    """
    if secure: rand_gen = random.SystemRandom()
    else: rand_gen = random

    with open(file_path, 'w', encoding="utf-8") as f:
        for _ in range(num):
            # SystemRandom makes the generator more cryptographically secure -- hard to predict!!
            _token = ''.join(rand_gen.choices(string.ascii_lowercase, k=token_len))+"\n"
            f.write(_token)


def _generate_token(token_len: int, token_num: int, secure: bool=True) -> str:
    _tokens = []
    if secure: rand_gen = random.SystemRandom()
    else: rand_gen = random
    for _ in range(token_num):
        _token = ''.join(rand_gen.choices(string.ascii_lowercase, k=token_len))+"\n"
        _tokens.append(_token)
    return _tokens

if __name__=="__main__":
    args = parse_args()
    print(args)
    file_name = os.path.basename(args.file)
    current_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_dir, file_name)

    current_time = time.time()
    if args.method == "parallel":
        generate_tokens_mul(file_path, num=args.num, token_len=args.token_len, secure=args.secure)
    else:
        generate_tokens(file_path, num=args.num, token_len=args.token_len, secure=args.secure)

    end_time = time.time()

    print("elapsed time =", end_time-current_time)
