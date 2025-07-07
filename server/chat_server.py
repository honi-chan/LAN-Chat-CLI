import socket
import threading
import argparse

class ChatServer:
    
    # サーバ起動処理
    def start(self):
        self._parse_args()
        self._init_server()
        self._bind_and_listen()
        self._accept_loop()

    # コマンドライン引数の解析を行う
    def _parse_args(self):
        parser = argparse.ArgumentParser(description='LAN Chat Server')
        parser.add_argument('--host', type=str, default='127.0.0.1', help='サーバのホスト（IPアドレス） (default: 127.0.0.1)')
        parser.add_argument('--port', type=int, default=9000, help='サーバのポート番号 (default: 9000)')
        parser.add_argument('--mode', type=str, default='sync', choices=['sync', 'async'], help='同期(sync)／非同期(async)モード (default: sync)')
        args = parser.parse_args()

        self.host = args.host
        self.port = args.port
        self.mode = args.mode

    # サーバーの初期化（ソケット作成など）
    def _init_server(self):
        self.backlog = 5  # 接続待ちの最大数を設定
        self.clients = []  # クライアント接続情報(conn, addr)のリストを初期化
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCPソケットを作成

    # ソケットをバインドし、接続待ち状態にする
    def _bind_and_listen(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(self.backlog)
        print(f"Server listening on {self.host}:{self.port}")

    # クライアントからの接続を受け付け続けるループ
    def _accept_loop(self):
        try:
            while True:
                conn, addr = self.sock.accept()
                self._handle_new_client(conn, addr)
        except KeyboardInterrupt:
            print("Server shutting down...")
        finally:
            self.sock.close()

    # 新しいクライアントの処理を開始
    def _handle_new_client(self, conn, addr):
        self.clients.append((conn, addr))  # クライアント情報をリストに追加
        thread = threading.Thread(target=self._client_handler, args=(conn, addr), daemon=True)  # クライアント処理用スレッド作成
        thread.start()  # スレッド開始

    def _client_handler(self, connection, address):
        while True:  # クライアントからのメッセージ受信ループ
            try:
                data = connection.recv(4096)  # データを受信（最大4096バイト）
                if not data:  # データが空なら切断されたと判断
                    self._remove_client(connection, address)
                    break
                self._broadcast_message(data, address)
            except Exception as e:
                print(f"Error with client {address}: {e}")
                self._remove_client(connection, address)
                break

    # 受信メッセージを他クライアントへ送信
    def _broadcast_message(self, data, sender_addr):
        message = f"{data.decode()}".encode("utf-8")
        for conn, addr in self.clients:
            if addr != sender_addr:  # 送信元以外に送信
                try:
                    conn.send(message)  # メッセージ送信
                except Exception as e:
                    print(f"送信エラー: {e}")  # 送信失敗時のエラーメッセージ

    # クライアント情報をリストから削除
    def _remove_client(self, connection, address):
        self.clients = [c for c in self.clients if c[0] != connection]  # 指定されたクライアントをリストから削除
        connection.close()

if __name__ == "__main__":
    server = ChatServer()  # ChatServerのインスタンス作成
    server.start()
