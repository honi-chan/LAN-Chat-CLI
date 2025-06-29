import argparse    # 1. argparseをインポート

parser = argparse.ArgumentParser(description='LAN Chat Server')    # 2. パーサを作る

# 3. parser.add_argumentで受け取る引数を追加していく
parser.add_argument('--host', type=str, default='127.0.0.1', help='サーバのホスト（IPアドレス） (default: 127.0.0.1)')    # 必須の引数を追加
parser.add_argument('--port', type=int, default='9000', help='サーバのポート番号 (default: 9000)')
parser.add_argument('--mode', type=str, default='sync', choices=['sync', 'async'], help='同期(sync)／非同期(async)モード (default: sync)')    # オプション引数（指定しなくても良い引数）を追加

args = parser.parse_args()    # 4. 引数を解析

print(f'Server starting on {args.host}:{args.port} (mode={args.mode})')
