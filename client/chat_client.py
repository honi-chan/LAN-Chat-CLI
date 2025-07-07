import socket
import threading
import argparse

class ChatClient:

    # クライアント処理開始
    def start(self):
        self._parse_args()
        self._init_client()
        self._connect()

        if not self.running:  # 接続失敗していたら終了
            return

        # 受信スレッド開始（非同期でメッセージを受信）
        receiver = threading.Thread(target=self._receive_loop, daemon=True)
        receiver.start()

        self._send_loop()

    # コマンドライン引数の解析
    def _parse_args(self):
        parser = argparse.ArgumentParser(description='LAN Chat Server')
        parser.add_argument('--host', type=str, required=True, help='サーバのホスト（IPアドレス） (default: 127.0.0.1)')
        parser.add_argument('--port', type=int, required=True, help='サーバのポート番号 (default: 9000)')
        parser.add_argument('--name', type=str, required=True)
        parser.add_argument('--mode', type=str, default='sync', choices=['sync', 'async'], help='同期(sync)／非同期(async)モード (default: sync)')

        args = parser.parse_args()

        self.host = args.host
        self.port = args.port
        self.name = args.name
        self.mode = args.mode

    # クライアントの初期化処理
    def _init_client(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP/IPソケットを作成
        self.running = False  # 接続状態を初期化

    # サーバに接続する処理
    def _connect(self):
        try:
            self.sock.connect((self.host, self.port))
            self.running = True  # 接続成功フラグを立てる
            print(f"Connected to {self.host}:{self.port} as {self.name}")
        except Exception as e:
            print(f"Connection failed: {e}")
            self.running = False  # 接続失敗フラグ

    # メッセージ受信ループ（スレッドで動作）
    def _receive_loop(self):
        while self.running:
            try:
                data = self.sock.recv(4096)  # データを受信
                if not data:  # 接続が切断された場合
                    print("接続が切断されました")
                    self.running = False  # ループを終了
                    break
                print(f"{data.decode()}")  # 受信データを表示
            except Exception as e:
                print(f"受信エラー: {e}")
                self.running = False
                break

    # メッセージ送信ループ（メインスレッドで動作）
    def _send_loop(self):
        while self.running:
            try:
                user_input = input("")
                if user_input.lower() in ['exit', 'quit']:  # 終了コマンドなら
                    print("切断します")
                    break
                
                message = f"[{self.name}] {user_input}"
                sent = self.sock.send(message.encode('utf-8'))
            except KeyboardInterrupt:
                print("切断します")
                break
            except Exception as e:
                print(f"送信エラー: {e}")
                break
        self.running = False
        self.sock.close()

if __name__ == "__main__":
    client = ChatClient()  # クライアントインスタンスを作成
    client.start()
