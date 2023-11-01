import numpy as np
import Huffman_encoding as Huffman_e
import Huffman_decoding as Huffman_d

length = 1000

# Probabilities of A
p_A = 1/4 # 1이 나올 확률
q_A = 1 - p_A

# Probabilities of B
P = np.array([[3/4, 1/4], [1/4, 3/4]])

# Calculate the steady state probabilities
eigenvalues, eigenvectors = np.linalg.eig(P.T)  # Transpose P for left eigenvector
steady_state_probabilities = eigenvectors[:, 0] / np.sum(eigenvectors[:, 0])

p_B, q_B = steady_state_probabilities

# 전체 4비트 이진 숫자 리스트 생성
binary_numbers = [format(i, '04b') for i in range(16)]
array_A = np.random.choice([0, 1], size=length, p=[1-p_A, p_A])
chunked_A = np.array([array_A[i:i+4] for i in range(0, len(array_A), 4)])
string_A = ''.join(map(str, array_A))

array_A = np.random.choice([0, 1], size=length, p=[1-p_B, p_B])
chunked_B = np.array([array_A[i:i+4] for i in range(0, len(array_A), 4)])
string_B = ''.join(map(str, array_A))

# Probabilities of chunked_A
probabilities_A = {}
for binary_number in binary_numbers:
    # 확률을 계산하고 딕셔너리에 추가
    if binary_number.count('1') == 0:
        probabilities_A[binary_number] = (q_A ** 4)
    if binary_number.count('1') == 1:
        probabilities_A[binary_number] = (p_A) * (q_A ** 3)
    if binary_number.count('1') == 2:
        probabilities_A[binary_number] = ((p_A) ** 2) * ((q_A) ** 2)
    if binary_number.count('1') == 3:
        probabilities_A[binary_number] = ((p_A) ** 3) * ((q_A) ** 1)
    if binary_number.count('1') == 4:
        probabilities_A[binary_number] = ((p_A) ** 4)

probabilities_B = {}
for binary_number in binary_numbers:
    probabilities_B[binary_number] = (p_B)**4

#Huffman 트리 및 코드 테이블 생성 A
huffman_tree_A = Huffman_e.build_huffman_tree(probabilities_A)
huffman_codes_A = Huffman_e.build_huffman_codes(huffman_tree_A)

Entropy_A = Huffman_e.cal_Entropy((probabilities_A))
avg_A = Huffman_e.avg_bitpersym(huffman_codes_A, probabilities_A)

###code book##
# for symbol, code in huffman_codes.items():
#     print(f"Symbol: {symbol}, Huffman Code: {code}")

enocoded_Huffman_A = Huffman_e.huffman_encode(string_A, huffman_codes_A)

###decoding##
decoded_Huffman_A = Huffman_d.huffman_decode(enocoded_Huffman_A, huffman_tree_A)

###ratio###
comp_ratio_A = (len(string_A) - len(enocoded_Huffman_A)) / len(string_A) * 100


#Huffman 트리 및 코드 테이블 생성 B
huffman_tree_B = Huffman_e.build_huffman_tree(probabilities_B)
huffman_codes_B = Huffman_e.build_huffman_codes(huffman_tree_B)

Entropy_B = Huffman_e.cal_Entropy((probabilities_B))
avg_B = Huffman_e.avg_bitpersym(huffman_codes_B, probabilities_B)

enocoded_Huffman_B = Huffman_e.huffman_encode(string_B, huffman_codes_B)

###decoding##
decoded_Huffman_B = Huffman_d.huffman_decode(enocoded_Huffman_B, huffman_tree_B)

###ratio###
comp_ratio_B = (len(string_B) - len(enocoded_Huffman_B)) / len(string_B) * 100


###results of A##
print('Entropy of A=', Entropy_A)
print('compression ratio=', avg_A)

print("Origin data :","length = ", len(string_A) ,"\n", string_A)
print("Encoded data :","length = ", len(enocoded_Huffman_A), "\n", enocoded_Huffman_A)
print("Decoded code :","length = ", len(decoded_Huffman_A), "\n", decoded_Huffman_A)

print("Compresstion ratio =", comp_ratio_A, "%")

if string_A == decoded_Huffman_A:
    print("Perfect reconstruction")
else :
    print("no perfect reconstruction")

# Huffman_e.visualize_huffman_tree(huffman_tree_A)

###results of B##
print('Entropy of B=', Entropy_B)
print('compression ratio=', avg_B)

print("Origin data :","length = ", len(string_B) ,"\n", string_B)
print("Encoded data :","length = ", len(enocoded_Huffman_B), "\n", enocoded_Huffman_B)
print("Decoded code :","length = ", len(decoded_Huffman_B), "\n", decoded_Huffman_B)

print("Compresstion ratio =", comp_ratio_B, "%")

if string_A == decoded_Huffman_B:
    print("Perfect reconstruction")
else :
    print("no perfect reconstruction")

for symbol, code in huffman_codes_B.items():
    print(f"Symbol: {symbol}, Huffman Code: {code}")
