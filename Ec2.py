import cv2
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

def encrypt_image(image_path, key, output_path):
    # 加载图像
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 转换为灰度图像以简化处理
    image_data = image.flatten().tobytes()  # 将图像数据转换为字节流

    # 初始化AES加密器
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv  # 获取初始化向量
    ct_bytes = cipher.encrypt(pad(image_data, AES.block_size))  # 加密图像数据

    # 保存加密后的图像数据和初始化向量
    with open(output_path, 'wb') as f:
        f.write(iv)
        f.write(ct_bytes)

def decrypt_image(encrypted_path, key, output_path):
    # 读取加密后的图像数据和初始化向量
    with open(encrypted_path, 'rb') as f:
        iv = f.read(AES.block_size)
        ct = f.read()

    # 初始化AES解密器
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)  # 解密图像数据

    # 将字节流转换回图像格式
    image_data = np.frombuffer(pt, dtype=np.uint8)
    image = image_data.reshape((image_data.size // image.shape[1], image.shape[1]))

    # 保存解密后的图像
    cv2.imwrite(output_path, image)

# 示例使用
key = get_random_bytes(16)  # 生成一个随机的16字节密钥
encrypt_image('m.png', key, 'encrypted_image')
decrypt_image('encrypted_image', key, 'decrypted_image.png')