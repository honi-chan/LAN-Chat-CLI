
# LANチャット CLI

ローカルネットワーク（LAN）上で動作する、シンプルなコマンドラインチャットアプリケーションです。 同期（スレッド）モードと非同期（asyncio）モードを選択可能。

## 機能

- **サーバ & クライアント**: `chat_server.py` と `chat_client.py` を別スクリプトで提供
- **モード切替**: `--mode sync`（threading） / `--mode async`（asyncio）
- **メッセージのブロードキャスト**: 送信メッセージを全クライアントへ配信
- **切断検知**: クライアント退出を検出して他ユーザーへ通知
- **外部依存なし**: Python 3.7+ の標準ライブラリのみで動作

## 動作要件

- Python 3.7 以上

## インストール

## 使い方

### サーバ起動

```bash
python3 chat_server.py --host 0.0.0.0 --port 9000 --mode sync
# 非同期モードの場合
python3 chat_server.py --host 0.0.0.0 --port 9000 --mode async
```

### クライアント接続

```bash
python3 chat_client.py --host 192.168.1.10 --port 9000 --name Alice
# 別の端末で起動
python3 chat_client.py --host 192.168.1.10 --port 9000 --name Bob
```

### チャット

- メッセージ入力後に Enter で送信
- すべてのクライアントにメッセージが表示される:
  ```
  [Alice] こんにちは！
  [Bob]   こんにちは、Aliceさん！
  ```
- `Ctrl+C` で終了すると、他クライアントに退出通知が表示
  ```
  [Server] Bob がチャットを退出しました。
  ```

## オプション

| オプション    | 説明                | デフォルト       |
| -------- | ----------------- | ----------- |
| `--host` | ホスト（IPアドレス）       | `127.0.0.1` |
| `--port` | ポート番号             | `9000`      |
| `--name` | クライアント名           | *必須*        |
| `--mode` | `sync` or `async` | `sync`      |

## 実装概要

- **サーバ (**``**)**

  - `socket` で bind／listen
  - `sync` モード: `threading.Thread` でクライアントごとにハンドラ起動
  - `async` モード: `asyncio.start_server` でコルーチン起動
  - 接続リストを管理し、ブロードキャストを実現

- **クライアント (**``**)**

  - `socket.connect`（sync）または `asyncio.open_connection`（async）
  - 標準入力読み取りとサーバ受信を並行実行

## 学べること

- TCP ソケットプログラミング
- スレッド並行処理 (`threading`)
- 非同期 I/O (`asyncio`)
- CLI 引数解析 (`argparse`)
- グレースフルなエラー・切断処理
