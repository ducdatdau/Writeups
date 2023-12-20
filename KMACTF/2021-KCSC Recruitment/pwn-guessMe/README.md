# 0x00 Plan 

Load file binary vào IDA, chúng ta cùng nhìn qua mã giả của chương trình 
```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int v4; // [rsp+8h] [rbp-18h] BYREF
  int v5; // [rsp+Ch] [rbp-14h]
  unsigned int seed[2]; // [rsp+10h] [rbp-10h]
  unsigned __int64 v7; // [rsp+18h] [rbp-8h]

  v7 = __readfsqword(0x28u);
  *(_QWORD *)seed = time(0LL);
  srand(seed[0]);
  v5 = rand() % 1337;
  __isoc99_scanf("%d", &v4);
  if ( v5 == v4 )
    print_flag();
  else
    puts("Wrong!");
  return 0;
}
```

Ý tưởng của bài toán này rất rõ ràng
- Tạo số random với seed là `time(0)` rồi chia lấy dư cho 1337 
- Nhập một số bất kỳ vào chương trình, nếu số đó bằng số random sẽ gọi hàm in ra flag `print_flag()`

Với seed là `time(0)`, số random không thực sự random trong 1s. Hiểu đơn giản, nếu mình chạy song song cùng một chương trình, mình sẽ biết được số random kia là bao nhiêu. 

Để giải quyết bài toán này, chúng ta có 2 phương pháp giải
- Phương pháp 1: Viết một chương trình C để tạo ra số random với `seed` bằng `time(0)`. Tiếp đến sử dụng `subprocess` trong Python để sử dụng số random đó. 
- Phương pháp 2: Sử dụng glibc trong Python để gọi `srand()` trong C. 

# 0x01 Exploit 

## Phương pháp 1. C + subprocess

Chương trình lấy số random `getrand`
```c
#include <stdio.h>
#include <time.h>
#include <stdlib.h>

int main() {
  unsigned int r; 
  srand(time(0));
  r = rand();

  printf("%x\n", r);
  return 0;
}
```

```sh
gcc getrand.c -o getrand
```

Chương trình sử dụng `subprocess` 
```python
proc = subprocess.Popen(['./getrand'], stdout = subprocess.PIPE)
line = proc.stdout.readline().strip()
line = int(line, 16) % 1337
```

## Phương pháp 2. Glibc

Với phương pháp này, chúng ta cần phải patch file binary với libc cho trước. 
```sh
$pwn-guessMe pwninit
bin: ./guessMe
libc: ./libc6_2.27-3ubuntu1.4_amd64.so

fetching linker
https://launchpad.net/ubuntu/+archive/primary/+files//libc6_2.27-3ubuntu1.4_amd64.deb
setting ./ld-2.27.so executable
symlinking ./libc.so.6 -> libc6_2.27-3ubuntu1.4_amd64.so
copying ./guessMe to ./guessMe_patched
running patchelf on ./guessMe_patched
writing solve.py stub
```

Đoạn mã load glibc chạy chung với chương trình 

```python
from ctypes import *

p = process('./guessMe_patched')
glibc = cdll.LoadLibrary('./libc6_2.27-3ubuntu1.4_amd64.so')
glibc.srand(glibc.time(0))

val = glibc.rand() % 1337 
```
# 0x02 Reference
- https://github.com/nhtri2003gmail/CTFWriteup/blob/master/2022/KCSC-CTF-entrance-test/guessMe/README.md
