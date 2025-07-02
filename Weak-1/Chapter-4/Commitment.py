import random

# Tham số nhóm (nhỏ để dễ hiểu, thực tế dùng số lớn hàng trăm bit)
p = 2089             # số nguyên tố lớn
g = 2                # generator g
h = 7                # generator h, sao cho log_g(h) không biết

# Giá trị muốn cam kết
D1 = 10
D2 = 20
D3 = 30

# Các nonce ngẫu nhiên
r1 = random.randint(1, 100)
r2 = random.randint(1, 100)
r3 = random.randint(1, 100)

# Bước 1: Tính từng cam kết
C1 = (pow(g, D1, p) * pow(h, r1, p)) % p
C2 = (pow(g, D2, p) * pow(h, r2, p)) % p
C3 = (pow(g, D3, p) * pow(h, r3, p)) % p

# Bước 2: Tính cam kết tổng hợp
C123 = (C1 * C2 * C3) % p

# Tính tổng dữ liệu và tổng nonce
D123 = D1 + D2 + D3
r123 = r1 + r2 + r3

# Bước 3: Kiểm tra cam kết tổng có đúng không
C_check = (pow(g, D123, p) * pow(h, r123, p)) % p

# Kết quả
print(f"C1: {C1}")
print(f"C2: {C2}")
print(f"C3: {C3}")
print(f"\nTổng hợp C123: {C123}")
print(f"Kiểm tra lại với D123={D123}, r123={r123} → {C_check}")
print("\nCam kết đúng!" if C123 == C_check else "Sai lệch!")
