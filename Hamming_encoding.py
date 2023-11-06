import random

def hamming_code_encoder(data):
    # 데이터 비트의 위치를 계산하기 위해 패리티 비트를 채울 위치를 결정합니다.
    # 1, 2, 4 비트는 패리티 비트의 위치입니다. 0-based 인덱스로 계산합니다.


    encoded_data = [0, 0, int(data[0]), 0, int(data[1]), int(data[2]), int(data[3])]

    # 패리티 비트를 계산하여 설정합니다.
    encoded_data[0] = encoded_data[2] ^ encoded_data[4] ^ encoded_data[6]
    encoded_data[1] = encoded_data[2] ^ encoded_data[5] ^ encoded_data[6]
    encoded_data[3] = encoded_data[4] ^ encoded_data[5] ^ encoded_data[6]

    return encoded_data


# 4비트 데이터 비트를 입력으로 넣습니다.
data_bits = [format(i, '04b') for i in range(16)]

print(type(int(data_bits[0])))
# 해밍 코드 인코딩
for i in range(16):
    encoded_bits = hamming_code_encoder(data_bits[i])

    print(data_bits[i], "->", encoded_bits)

def BSC(data,p):
    for i in range(len(data)):
        if random.random() < p:
            if data[i] == 0:
                data[i] = 1
            else:
                data[i] = 0
    return data

def hamming_code_decoder(encoded_data):
    for i in range(7):
        encoded_data[i] = int(encoded_data[i])
    # 패리티 비트의 위치를 계산하기 위해 각 비트의 값을 검사합니다.
    p1 = encoded_data[0] ^ encoded_data[2] ^ encoded_data[4] ^ encoded_data[6]
    p2 = encoded_data[1] ^ encoded_data[2] ^ encoded_data[5] ^ encoded_data[6]
    p4 = encoded_data[3] ^ encoded_data[4] ^ encoded_data[5] ^ encoded_data[6]

    # 오류 위치를 계산합니다.
    error_position = p1 + 2 * p2 + 4 * p4

    # 오류 위치에 따라 오류 비트를 수정합니다.
    if error_position != 0:
        # print("오류 발견 및 수정 시도 중...")
        # print("오류 발생 위치:", error_position)
        # 오류 비트를 토글합니다.
        encoded_data[error_position - 1] = 1 - encoded_data[error_position - 1]

    # 수정된 데이터를 추출합니다.
    decoded_data = [encoded_data[2], encoded_data[4], encoded_data[5], encoded_data[6]]

    return decoded_data


