import argparse    # 1. argparseをインポート

parser = argparse.ArgumentParser(description='LAN Chat Server')    # 2. パーサを作る

# 3. parser.add_argumentで受け取る引数を追加していく
parser.add_argument('--host', type=str, default='127.0.0.1', required=True, help='サーバのホスト（IPアドレス） (default: 127.0.0.1)')
parser.add_argument('--port', type=int, default='9000', required=True, help='サーバのポート番号 (default: 9000)')
parser.add_argument('--name', type=str, required=True)
parser.add_argument('--mode', type=str, default='sync', choices=['sync', 'async'], help='同期(sync)／非同期(async)モード (default: sync)')

args = parser.parse_args()    # 4. 引数を解析

print(f'Client connecting to {args.host}:{args.port} as "{args.name}" (mode={args.mode})')
