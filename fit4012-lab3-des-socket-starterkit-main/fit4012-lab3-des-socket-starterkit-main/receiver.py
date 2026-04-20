import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
import des_socket_utils as utils

class ReceiverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DES Receiver - Máy Nhận (172.20.10.3)")
        self.root.geometry("500x450")

        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Label(frame, text="IP của tôi: 172.20.10.3").pack(side=tk.LEFT, padx=10)
        tk.Label(frame, text="Port:").pack(side=tk.LEFT)
        self.port_ent = tk.Entry(frame, width=8)
        self.port_ent.insert(0, "12345")
        self.port_ent.pack(side=tk.LEFT, padx=5)

        self.btn_start = tk.Button(frame, text="MỞ CỔNG NHẬN", command=self.start_server, bg="#27ae60", fg="white")
        self.btn_start.pack(side=tk.LEFT, padx=5)

        self.log_area = scrolledtext.ScrolledText(root, width=60, height=20, state='disabled', bg="#f0f0f0")
        self.log_area.pack(padx=10, pady=10)

    def write_log(self, msg):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, msg + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def start_server(self):
        port = int(self.port_ent.get())
        self.btn_start.config(state='disabled', text="ĐANG ĐỢI...")
        threading.Thread(target=self.run_socket, args=(port,), daemon=True).start()
        self.write_log(f"[*] Server đã mở cổng {port}. Đang đợi Sender kết nối...")

    def run_socket(self, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('0.0.0.0', port)) # Lắng nghe trên tất cả card mạng
            s.listen(5)
            while True:
                conn, addr = s.accept()
                with conn:
                    self.write_log(f"\n[+] Thiết bị kết nối: {addr}")
                    try:
                        key = conn.recv(8)
                        iv = conn.recv(8)
                        header = conn.recv(4)
                        if not header: continue
                        length = utils.parse_header(header)
                        
                        ciphertext = b""
                        while len(ciphertext) < length:
                            chunk = conn.recv(length - len(ciphertext))
                            if not chunk: break
                            ciphertext += chunk

                        plaintext, err = utils.decrypt_data(ciphertext, key, iv)
                        if err:
                            self.write_log(f"[!] {err}")
                        else:
                            self.write_log(f"[BẢN RÕ]: {plaintext.decode('utf-8')}")
                            self.write_log("-" * 30)
                    except Exception as e:
                        self.write_log(f"[!] Lỗi: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ReceiverApp(root)
    root.mainloop()