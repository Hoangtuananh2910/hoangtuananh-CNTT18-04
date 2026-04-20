import socket
import tkinter as tk
from tkinter import messagebox
from Crypto.Random import get_random_bytes
import des_socket_utils as utils

class SenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DES Sender - Máy Gửi")
        self.root.geometry("400x300")

        tk.Label(root, text="ĐỊA CHỈ IP MÁY NHẬN:", font=("Arial", 10, "bold")).pack(pady=5)
        self.ip_ent = tk.Entry(root, width=25, justify='center', font=("Arial", 12))
        self.ip_ent.insert(0, "172.20.10.3") # Đã điền sẵn IP của bạn
        self.ip_ent.pack(pady=5)

        tk.Label(root, text="Cổng (Port):").pack()
        self.port_ent = tk.Entry(root, width=10, justify='center')
        self.port_ent.insert(0, "12345")
        self.port_ent.pack(pady=5)

        tk.Label(root, text="Nội dung tin nhắn:").pack(pady=5)
        self.msg_ent = tk.Entry(root, width=35)
        self.msg_ent.pack(pady=5)

        self.btn_send = tk.Button(root, text="MÃ HÓA & GỬI NGAY", command=self.send_payload, 
                                 bg="#2980b9", fg="white", font=("Arial", 10, "bold"), height=2)
        self.btn_send.pack(pady=20)

    def send_payload(self):
        ip = self.ip_ent.get()
        port = int(self.port_ent.get())
        msg = self.msg_ent.get()

        if not msg:
            messagebox.showwarning("Thiếu tin nhắn", "Bạn chưa nhập nội dung cần gửi!")
            return

        try:
            key = get_random_bytes(8)
            iv = get_random_bytes(8)
            ciphertext = utils.encrypt_data(msg.encode('utf-8'), key, iv)
            header = utils.format_header(len(ciphertext))

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5) 
                s.connect((ip, port))
                
                s.sendall(key)
                s.sendall(iv)
                s.sendall(header)
                s.sendall(ciphertext)

            messagebox.showinfo("Thành công", f"Đã gửi mật mã tới {ip} thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi kết nối", f"Không thể kết nối tới {ip}.\nLỗi: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SenderApp(root)
    root.mainloop()