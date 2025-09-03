import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
import threading
import time
import datetime
import os
from colorama import init, Fore

# 初期化
init()

# GUIアプリケーションの作成
class SerialLoggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Serial Logger GUI")

        # ポート選択
        self.port_label = ttk.Label(root, text="シリアルポート選択:")
        self.port_label.pack(padx=10, pady=5)

        self.port_combo = ttk.Combobox(root, values=self.list_serial_ports())
        self.port_combo.pack(padx=10, pady=5)

        # ボーレート固定（必要なら Combobox に変更可能）
        self.baud_rate = 38400

        # 開始・停止ボタン
        self.start_button = ttk.Button(root, text="開始", command=self.start_logging)
        self.start_button.pack(padx=10, pady=5)

        self.stop_button = ttk.Button(root, text="停止", command=self.stop_logging, state="disabled")
        self.stop_button.pack(padx=10, pady=5)

        # ロギング関連
        self.ser = None
        self.running = False
        self.thread = None

    def list_serial_ports(self):
        return [port.device for port in serial.tools.list_ports.comports()]

    def start_logging(self):
        port = self.port_combo.get()
        if not port:
            messagebox.showwarning("警告", "シリアルポートを選択してください。")
            return

        try:
            self.ser = serial.Serial(port, self.baud_rate, timeout=1)
        except serial.SerialException as e:
            messagebox.showerror("エラー", f"ポートに接続できません: {e}")
            return

        # ログフォルダとファイルの準備
        os.makedirs("logs", exist_ok=True)
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.log_file_path = os.path.join("logs", f"log_{timestamp}.txt")

        self.running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

        self.thread = threading.Thread(target=self.read_serial, daemon=True)
        self.thread.start()

    def read_serial(self):
        with open(self.log_file_path, 'w', encoding='utf-8') as f:
            print(f"[INFO] ログ取得を開始します（{self.ser.port}, {self.baud_rate}bps）")
            while self.running:
                try:
                    line = self.ser.readline().decode('utf-8', errors='ignore').strip()
                    if line:
                        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                        log_entry = f"{timestamp} | {line}"
                        if 'ERROR' in line.upper():
                            print(Fore.RED + log_entry + Fore.RESET)
                        else:
                            print(log_entry)
                        f.write(log_entry + '\n')
                except serial.SerialException as e:
                    print(f"[ERROR] 読み取りエラー: {e}")
                    break

        self.ser.close()

    def stop_logging(self):
        self.running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        print("[INFO] ログ取得を停止しました")

# GUIを起動
if __name__ == "__main__":
    root = tk.Tk()
    app = SerialLoggerApp(root)
    root.mainloop()
