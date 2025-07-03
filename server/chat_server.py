import argparse
import socket
import sys

def parse_args():
    parser = argparse.ArgumentParser(description='LAN Chat Server')
    parser.add_argument('--host', type=str, default='127.0.0.1', help='サーバのホスト（IPアドレス） (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=9000, help='サーバのポート番号 (default: 9000)')
    parser.add_argument('--mode', type=str, default='sync', choices=['sync', 'async'], help='同期(sync)／非同期(async)モード (default: sync)')

    return parser.parse_args()

def start_server(host, port):

    # ソケット作成（IPv4, TCP）
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:

        # ソケットをアドレスとポートに紐付け
        server.bind((host, port))

        # 接続待ち開始
        server.listen(1)
        print(f"Waiting for connection on {host}:{port}...")

        # 接続を受け付ける
        conn, addr = server.accept()
        print(f"Connection from ('{host}', {port})")

        with conn:

            # データ受信 → 返信（1回だけ）
            data = conn.recv(1024)
            print(f"Received: {data.decode()}")

            # エコー返信
            conn.sendall(data)

            # 終了処理
            print("Server done.")

def main():
    args = parse_args()
    start_server(args.host, args.port)

if __name__ == '__main__':
    main()