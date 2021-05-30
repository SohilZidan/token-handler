import random, string
import argparse
from tqdm import tqdm
import time


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--token_len', default=7, type=int, help="length of a token")
    parser.add_argument('--num', default=10000000, type=int, help="number of tokens")
    parser.add_argument('--file', '-f', default="tokens.txt", help="the storage file path")
    return parser.parse_args()


if __name__=="__main__":
    args = parse_args()

    # print("lowercase a-z:",string.ascii_lowercase)
    current_time = time.time()
    with open(args.file, 'w') as f:
        for _ in tqdm(range(args.num), total=args.num):
            # SystemRandom makes the generator more cryptographically secure -- hard to predict!!
            _token = ''.join(random.SystemRandom().choices(string.ascii_lowercase, k=7))+"\n"
            f.write(_token)
    
    end_time = time.time()
    print("elapsed time =", end_time-current_time)