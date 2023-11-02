# Solve 

Bài này đơn giản hơn rất nhiều khi chúng ta đã có $q$ và $q$. Với $e$, chỉ cần thỏa mãn các điều kiện sau

```python
assert(isPrime(e))
assert(isPrime(e + 2))
assert(isPrime(e + 4))
```

Dễ dàng thấy $e = 3$ thỏa mãn những điều kiện phía trên. Câu hỏi đặt ra là, liệu có tồn tại số $e \neq 3$ thỏa mãn các điều kiện hay không? Để trả lời cho câu hỏi này, chúng ta có thể tham khảo câu trả lời tại đây [Show that we cannot have a prime triplet of the form $p, p+2, p+4$ for $p>3$](https://math.stackexchange.com/questions/1653536/show-that-we-cannot-have-a-prime-triplet-of-the-form-p-p-2-p-4-for).\
Từ $e$ có được phía trên, chúng ta sẽ có được $e_1, e_2$ và $e_3$. 

Tới đây, câu hỏi đặt ra là tại sao lại cho nhiều $e$ như vậy. Chúng ta có $p, q, n, \varphi(n), e$, từ đó tính ra được $d$. Khi có $c, d, n$, ta sẽ tính ra được $m$. Ở đây, tôi bị mắc một sai lầm đó là $gcd(e, \varphi(n)) \neq 1$, nghĩa là chúng ta không thể tính được $d$ theo suy luận trên. 

Quay lại với các giả thiết bài toán dã cho, ta có:
$$c_1 \equiv m^{e_1} \quad (\textrm{mod } n)$$
$$c_2 \equiv m^{e_2} \quad (\textrm{mod } n)$$

Suy ra: 

$$c_1^{k_1} \equiv m^{e_1k_1} \quad (\textrm{mod } n)$$
$$c_2^{k_2} \equiv m^{e_2k_2} \quad (\textrm{mod } n)$$
$$\to c_1^{k_1}c_2^{k_2} \equiv m^{e_1k_1 + e_2k_2} \quad (\textrm{mod } n)$$

Nếu $gcd(e_1, e_2) = 1$, theo thuật toán Euclid mở rộng, tồn tại cặp số $(x, y)$ thỏa mãn: $e_1x + e_2y = 1$. Từ đây, chúng ta dễ dàng có được $k_1, k_2$. 
