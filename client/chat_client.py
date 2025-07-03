import argparse
import socket
import sys

def parse_args():
    parser = argparse.ArgumentParser(description='LAN Chat Server')
    parser.add_argument('--host', type=str, required=True, help='サーバのホスト（IPアドレス） (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, required=True, help='サーバのポート番号 (default: 9000)')
    parser.add_argument('--name', type=str, required=True)
    parser.add_argument('--mode', type=str, default='sync', choices=['sync', 'async'], help='同期(sync)／非同期(async)モード (default: sync)')

    return parser.parse_args()

def start_client(host, port, name, mode):
    print(f'Client connecting to {host}:{port} as "{name}" (mode={mode})')

    try:
        # ソケット作成とサーバー接続
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((host, port))
            
            # メッセージを送信
            message = input(">>> ")
            if not message:
                print("空のメッセージは送信できません。")
                sys.exit(1)
            client.sendall(message.encode())

            # 返信を受信
            response = client.recv(1024)
            print(f"Echo: {response.decode()}")
    except ConnectionRefusedError:
        print("接続が拒否されました。サーバが起動しているか、アドレスとポートを確認してください。")
        sys.exit(1)

def main():
    args = parse_args()
    start_client(args.host, args.port, args.name, args.mode)

if __name__ == '__main__':
    main()