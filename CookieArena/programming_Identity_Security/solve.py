def che_thong_tin(N, thong_tin):
    result = []
    for i in range(N):
        info = thong_tin[i]
        if '@' in info: 
            username, domain = info.split('@')
            if len(username) <= 7:
                che_username = username[0] + '*' * (len(username) - 2) + username[-1]
            else:
                che_username = username[:2] + '*' * (len(username) - 5) + username[-3:]
           
            result.append(che_username + '@' + domain)
        else:  
            result.append(info[:2] + '*' * (len(info) - 5) + info[-3:])
    return result

N = int(input())  
thong_tin = []
for _ in range(N):
    info = input()
    thong_tin.append(info)

ket_qua = che_thong_tin(N, thong_tin)

for info in ket_qua:
    print(info)