import hashlib

def hash_data(data: str) -> str:     # Nhận vào một chuỗi (data)
    return hashlib.sha256(data.encode()).hexdigest()    # Mã hóa bằng SHA-256 để tạo một chuỗi hex 64 ký tự

# Dùng làm hash cho các node trong cây Merkle
# .encode() để chuyển từ str → bytes (bắt buộc cho SHA-256)
# .hexdigest() trả ra chuỗi dạng hexa (dễ đọc, in ra)

def merkle_parent(h1: str, h2: str) -> str:     # Nhận vào 2 hash của các node con
    return hash_data(h1 + h2)     # Trả về hash của node cha bằng cách nối 2 hash con và mã hóa lại

def build_merkle_tree(leaves: list[str]) -> tuple[str, list[str]]:  # Nhận vào danh sách các lá (leaves) của cây Merkle
    leaf_hashes = [hash_data(x) for x in leaves]        # Mã hóa từng lá thành hash
    tree_levels = [leaf_hashes]   # Khởi tạo danh sách các cấp của cây Merkle, bắt đầu với lá
    
    while len(tree_levels[-1]) > 1:     # Trong khi còn nhiều hơn 1 lá
        current = tree_levels[-1]       # Lấy cấp hiện tại (cấp cuối cùng trong danh sách)
        next_level = []
        for i in range(0, len(current), 2):
            left = current[i]
            right = current[i+1] if i+1 < len(current) else current[i]
            next_level.append(merkle_parent(left, right))
        tree_levels.append(next_level)
    
    root = tree_levels[-1][0]
    return root, tree_levels[0]  # return root and leaves

def generate_merkle_proof(index: int, leaves: list[str]) -> tuple[list[tuple[str, str]], str]:
    """
    Trả về: [(sibling_hash, direction)], leaf_hash
    direction = 'L' hoặc 'R' (trái hay phải)
    """
    hash_list = [hash_data(x) for x in leaves]
    proof = []
    leaf_hash = hash_list[index]
    
    current = hash_list
    pos = index

    while len(current) > 1:
        next_level = []
        for i in range(0, len(current), 2):
            left = current[i]
            right = current[i+1] if i+1 < len(current) else current[i]
            parent = merkle_parent(left, right)
            next_level.append(parent)
        
        sibling_index = pos ^ 1  # 0->1, 1->0
        if sibling_index < len(current):
            sibling_hash = current[sibling_index]
            direction = 'L' if sibling_index < pos else 'R'
            proof.append((sibling_hash, direction))
        pos = pos // 2
        current = next_level

    return proof, leaf_hash

def verify_merkle_proof(leaf_hash: str, proof: list[tuple[str, str]], root: str) -> bool:
    computed_hash = leaf_hash
    for sibling_hash, direction in proof:
        if direction == 'L':
            computed_hash = merkle_parent(sibling_hash, computed_hash)
        else:
            computed_hash = merkle_parent(computed_hash, sibling_hash)
    return computed_hash == root

gifts = ["Bear", "Bike", "Doll", "Train"]
target = "Train"
index = gifts.index(target)

# Bước 1: Xây cây Merkle
root, leaf_hashes = build_merkle_tree(gifts)
print("🎄 Merkle Root:", root)

# Bước 2: Sinh proof
proof, leaf_hash = generate_merkle_proof(index, gifts)
print(f"\n🧾 Merkle Proof for '{target}':")
for i, (h, d) in enumerate(proof):
    print(f"  Step {i+1}: sibling = {h[:10]}..., direction = {d}")

# Bước 3: Xác minh
verified = verify_merkle_proof(leaf_hash, proof, root)
print(f"\n✅ Món quà '{target}' có trong danh sách hợp lệ không?:", verified)
