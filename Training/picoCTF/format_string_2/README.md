Ý tưởng bài này là dùng FMT bug để sửa đổi giá trị của global variable `sus`. Để ghi giá trị, chúng ta thường sử dụng những format string như "%n", "%hn", "%hhn" lần lượt để viết 1, 2, 4 bytes. 

Ta thấy `sus == 0x67616c66`, chúng ta sẽ đưa địa chỉ biến `sus` lên stack, rồi viết 0x67616c66 bytes bất kỳ và gán cho nó. Cách làm này tốn thời gian chạy cực kỳ lâu. Thay vào đó, ta sẽ ghi từng 2 bytes một. Nghĩa là: 
- sus[0] = 0x6c66
- sus[2] = 0x6761

Lưu ý rằng, do ban đầu đã viết 0x6761 bytes cho `sus[2]` rồi, vậy kế đến chỉ được viết (0x6c66-0x6761) bytes cho `sus[0]` mà thôi. Đây cũng chính là lý do tôi đã tạo ra dict để chứa 2 con số này và sort chúng. 