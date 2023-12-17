### Reverse - hide and seek
![](./_/Screenshot%202023-12-16%20172823.png)

Sử dụng IDA để decompile chương trình, thấy đường dẫn chứa flag bị che bởi màu xanh. Từ đó mình patch lại màu chữ từ 0x11 thành 0x7 

![Alt text](./images/image-1.png)

Từ đó mình có biết được file chứa flag nằm tại `C:\Users\Pwn2Win\AppData\Local\Temp\.temp_html_file_428643812.html`

![Alt text](./images/image.png)

Flag là **KCSC{~(^._.)=^._.^=(._.^)~}** (Markdown render text bị lỗi)
