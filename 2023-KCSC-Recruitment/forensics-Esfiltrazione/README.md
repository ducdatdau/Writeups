Bài này khá giống với 1 bài mình từng làm trên Cookie Arena ([Trivial FTP](https://battle.cookiearena.org/challenges/digital-forensics/trivial-ftp)). Mình đọc lại blog giải của bạn @phgvee về cách giải, sau đó thay đổi đầu vào của code :

```python
from pyshark import FileCapture
from binascii import unhexlify

packets = FileCapture(".pcap", use_json=True, decode_as={"udp.port==50719": "tftp"})
res = ''
for pkt in packets:
if hasattr(pkt, 'tftp'):
    if hasattr(pkt, 'data'):
        res += pkt.data.data

res = unhexlify(res.replace(':', ''))

res = res.replace(b'\x0d\x0a', b'\x0a')
res = res.replace(b'\x0d\x00', b'\x0d')

with open('data_out', 'wb') as f:
  f.write(res)
```

Sau khi chạy ta nhận được 1 file zip hoàn chỉnh. Unzip để nhận được file pdf chứa cờ.

Flag là **KCSC{exfiltrate_important_data_using_tftp_351362a1}**
