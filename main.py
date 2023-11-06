import numpy as np
import random
import matplotlib.pyplot as plt

import Huffman_encoding as Huffman_e
import Huffman_decoding as Huffman_d
import Hamming_encoding as Hamming

length = 1000

# Probabilities of A
P = 1 / 4 # 1이 나올 확률
Q = 1 - P

# Probabilities of B


# Calculate the steady state probabilities

# 전체 4비트 이진 숫자 리스트 생성
binary_numbers = [format(i, '04b') for i in range(16)]
array_A = np.random.choice([0, 1], size=length, p=[1 - P, P])
chunked_A = np.array([array_A[i:i+4] for i in range(0, len(array_A), 4)])
string_A = ''.join(map(str, array_A))

# array_A = np.random.choice([0, 1], size=length, p=[1-p_B, p_B])
chunked_B = np.array([array_A[i:i+4] for i in range(0, len(array_A), 4)])
string_B = ''.join(map(str, array_A))

# Probabilities of chunked_A
probabilities_A = {}
for binary_number in binary_numbers:
    # 확률을 계산하고 딕셔너리에 추가
    if binary_number.count('1') == 0:
        probabilities_A[binary_number] = (Q ** 4)
    if binary_number.count('1') == 1:
        probabilities_A[binary_number] = (P) * (Q ** 3)
    if binary_number.count('1') == 2:
        probabilities_A[binary_number] = ((P) ** 2) * ((Q) ** 2)
    if binary_number.count('1') == 3:
        probabilities_A[binary_number] = ((P) ** 3) * ((Q) ** 1)
    if binary_number.count('1') == 4:
        probabilities_A[binary_number] = ((P) ** 4)

# Probabilities of chunked_B
probabilities_B = {}
for binary_number in binary_numbers:
    if int(binary_number[0])^int(binary_number[1]) == 1 : # 0번째와 1번째 비트의 xor 연산
        i = P # 다르면 확률 1/4
    else :
        i = Q # 같면 확률 3/4
    if int(binary_number[1])^int(binary_number[2]) == 1 : # 1번째와 2번째 비트의 xor 연산
        j = P
    else :
        j = Q
    if int(binary_number[2])^int(binary_number[3]) == 1 : # 2번째와 3번째 비트의 xor 연산
        k = P
    else :
        k = Q
    probabilities_B[binary_number] = (1/2)*i*j*k

#
#Huffman 트리 및 코드 테이블 생성 A
huffman_tree_A = Huffman_e.build_huffman_tree(probabilities_A)
huffman_codes_A = Huffman_e.build_huffman_codes(huffman_tree_A)

Entropy_A = Huffman_e.cal_Entropy((probabilities_A))
avg_A = Huffman_e.avg_bitpersym(huffman_codes_A, probabilities_A)

# Hamming 코드 직접 에러 계산
p_array= np.arange(0, 0.52, 0.02)
step_size = 0.5/0.02
P_e = np.zeros(int(step_size+1))

repeat = 10000


for i in range(int(step_size+1)):
    error_count = 0
    print('P=',p_array[i])
    for n in range(repeat):

        binary_string = ''.join(random.choice('01') for _ in range(4))

        encoded_binary = Hamming.hamming_code_encoder(binary_string)
        BSC_binary = Hamming.BSC(encoded_binary,p_array[i])
        decoded_binary =Hamming.hamming_code_decoder(BSC_binary)


        decoded_binary = ''.join(map(str, decoded_binary))
        print(binary_string, "__", encoded_binary, "__", BSC_binary, "__", decoded_binary)
        #print(type(decoded_binary), type(binary_string))
        #print(binary_string, "__",decoded_binary)
        if binary_string != decoded_binary:
            error_count = error_count + 1
            #print(binary_string, "__",decoded_binary)

    P_e[i] = error_count/repeat

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
    print("no perfect reconstruction\n")

# Huffman_e.visualize_huffman_tree(huffman_tree_A)

### Hamming ###



# 데이터를 생성합니다. 예를 들어, x와 y 값의 리스트를 생성합니다.
x = np.arange(0, 0.52, 0.02)
y = 1-(7*x*((1-x)**6)+(1-x)**7)
# 그래프를 생성하고 데이터를 플롯합니다.

plt.plot(p_array, y, label='analytic')

plt.plot(p_array,P_e, label='numerical')
# 그래프에 제목과 라벨을 추가합니다.
plt.title('FER curve')
plt.xlabel('P')
plt.ylabel('P_E')

# 그래프를 표시합니다.
plt.legend()
plt.grid()
plt.show()



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
