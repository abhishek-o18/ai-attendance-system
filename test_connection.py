from zk import ZK

ip = "192.168.1.224"
port = 5005   # 👈 CHANGE HERE

zk = ZK(ip, port=port, timeout=5)

try:
    conn = zk.connect()
    print("✅ Connected to biometric device successfully!")
    conn.disconnect()
except Exception as e:
    print("❌ Connection failed:", e)