import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# 下载密钥文件
with open("enc.key", "rb") as f:
    key = f.read()

# 下载TS片段
# def download_ts(i):
#     url = f"https://hnts.ymuuy.com:65/hls/27/20221013/17017/plist-0000{i}.ts"
#     r = requests.get(url)
#     with open(f"./ts片段/{i}.ts", "wb") as f:
#         aes = AES.new(key, AES.MODE_CBC, IV=b"\x00" * 16)
#         f.write(aes.decrypt(r.content))
#
# # 示例
# for i in range(16, 1038):
#     download_ts(i)
#     print("[INFO]:", i, "下载完成", sep="")
# print("[INFO]: 下载完成")

# 可以使用协程大大提升下载速度
import asyncio
import aiohttp

async def download_ts(i):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://hnts.ymuuy.com:65/hls/27/20221013/17017/plist-0000{i}.ts") as resp:
            with open(f"./ts片段/{i}.ts", "wb") as f:
                aes = AES.new(key, AES.MODE_CBC, IV=b"\x00" * 16)
                f.write(aes.decrypt(await resp.read()))
                print("[INFO]:", i, "下载完成", sep="")

async def main():
    tasks = []
    for i in range(1, 1038):
        tasks.append(asyncio.create_task(download_ts(i)))
    await asyncio.wait(tasks)

asyncio.run(main())

# 合并TS片段推荐使用第三方软件或者ffmpeg进行合并
