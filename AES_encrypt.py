import cv2
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

def encrypt_image(image_path, key, output_path,iv):
    # 加载图像
    cvimage = cv2.imread(image_path)
    #获取图像宽高
    img_height=cvimage.shape[0]
    img_width=cvimage.shape[1]
    #将图像数据转换为字节流
    image_data=cvimage.flatten().tobytes()
    # 初始化AES加密器
    cipher = AES.new(key, AES.MODE_CBC,iv)
    # 加密图像数据
    encrypt=cipher.encrypt(pad(image_data,AES.block_size))
    #得出原始图像大小并记录存入加密后的字节流中
    image_size=len(encrypt).to_bytes(6,byteorder='little')
    encrypted=image_size+encrypt
    #将原始图像的宽高信息和初始化向量存入加密后的字节流中
    encrypted = img_height.to_bytes(3,'little')+img_width.to_bytes(3,'little')+iv+encrypted
    # 计算填充数据块
    length=len(encrypted)
    num_pixels=(length+2)//3
    encrypted_width=img_width
    encrypted_height=(num_pixels+encrypted_width-1)//encrypted_width
    pad1=b'\x00'
    padded=encrypted+(encrypted_width*encrypted_height*3-length)*pad1
    #将字节流重塑为图像矩阵
    arr=np.frombuffer(padded, dtype=np.uint8).reshape(encrypted_height, encrypted_width, 3)
    #输出图像
    cv2.imwrite(output_path,arr)
        
def decrypt_image(encrypted_path, key, output_path):
    # 读取加密后的图像数据和初始化向量
    image_encrypted=cv2.imread(encrypted_path)
    image_depth = image_encrypted.shape[2]
    encrypted=image_encrypted.tobytes()
    image_height=int.from_bytes(encrypted[:3],byteorder='little')
    image_width=int.from_bytes(encrypted[3:6],byteorder='little')
    iv=encrypted[6:22]
    length = int.from_bytes(encrypted[22:28],byteorder='little')
    image_data=encrypted[28:28+length]
    # 初始化AES解密器
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 解密图像数据
    pt = unpad(cipher.decrypt(image_data),AES.block_size)  
    # 将字节流转换回图像格式
    arr = np.frombuffer(pt, dtype=np.uint8)
    image = arr.reshape(image_height, image_width,3)
    # 保存解密后的图像
    cv2.imwrite(output_path, image)

key = get_random_bytes(16)  # 生成一个随机的16字节密钥
iv =get_random_bytes(16)    # 生成一个随机的16字节初始化向量
encrypt_image('m.png', key, 'T1.png',iv)
decrypt_image('T1.png', key, 'T2.png')