import serial
import time

# 設定
COM_PORT = 'COM6'     # ご自身の環境に合わせて変更
BAUD_RATE = 38400      # 通信速度（製品に合わせて変更）
LOG_FILE = 'log.txt'  # 保存するファイル名

try:
    with serial.Serial(COM_PORT, BAUD_RATE, timeout=1) as ser:
        print(f"[INFO] ログ取得を開始します（{COM_PORT}, {BAUD_RATE}bps）")
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            while True:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line:
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                    log_entry = f"{timestamp} | {line}"
                    print(log_entry)
                    f.write(log_entry + '\n')
except serial.SerialException as e:
    print(f"[ERROR] シリアルポートに接続できません: {e}")
except KeyboardInterrupt:
    print("\n[INFO] ログ取得を中断しました")
