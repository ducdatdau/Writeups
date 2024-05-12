Đây là bài sử dụng bug FMT để đọc dữ liệu trên stack. Quan sát trên stack, ta thấy `flag` được chứa tại vị trí thứ 9, nghĩa là cần dùng fmt thứ 9 + 5 = 14 để đọc, do cần 5 fmt để đọc dữ liệu của 5 thanh ghi trước. 

Do chưa biết được kích thước của `flag` dài bao nhiêu, ta sẽ leak từ fmt thứ 14 - 20 cho chắc chắn. 