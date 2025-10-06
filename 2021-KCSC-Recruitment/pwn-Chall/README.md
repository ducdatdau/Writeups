# 0x00 Vulnerability 
Quan sát mã giả của file binary, chúng ta thấy có bug FMT ngay tại `printf(s)`

Debug chương trình, chúng ta thấy được `flag` nằm ở vị trí cách `$rsp` 0x10 bytes. Đối với binary 64 bits, chúng ta cần thêm 5 format string để đọc giá trị của 5 thanh ghi trước rồi mới có thể đọc các giá trị trên stack. 

```
gef➤  telescope
0x00007fffffffdc10│+0x0000: 0x00007fffffffddd8  →  0x00007fffffffe05e  →  "/home/georgedo/CTF/KMACTF/2022-ExtranceTest/pwn-Ch[...]"      ← $rsp
0x00007fffffffdc18│+0x0008: 0x0000000100000000
0x00007fffffffdc20│+0x0010: 0x00007fffffffdc70  →  "KCSC{17888f2f-a1fd-40cd-9af1-86def4c3be7e}\n"
0x00007fffffffdc28│+0x0018: 0x00005555555592a0  →  0x00000000fbad2488
0x00007fffffffdc30│+0x0020: 0x0000000000000000   ← $rax, $rdi
0x00007fffffffdc38│+0x0028: 0x0000000000000000
0x00007fffffffdc40│+0x0030: 0x0000000000000000
0x00007fffffffdc48│+0x0038: 0x0000000000000000
0x00007fffffffdc50│+0x0040: 0x0000000000000000
0x00007fffffffdc58│+0x0048: 0x0000000000000000
```

