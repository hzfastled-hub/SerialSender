import serial
import time
import random
import platform


def calculate_xor(data):
    result = 0
    for byte in data:
        result ^= byte
    return result


def generate_packet(prefix, value):
    data = list(prefix)
    data.append(value)
    checksum = calculate_xor(data)
    data.append(checksum)
    return bytes(data)


def send_to_serial(port, baudrate=9600, interval=10.0):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        print(f"串口已打开: {port}, 波特率: {baudrate}")
        print(f"发送间隔: {interval}秒")

        prefix1 = [0x57, 0x4B, 0x4C, 0x59, 0x09, 0x01, 0x88]
        values1 = list(range(1, 128))
        random.shuffle(values1)

        print("\n=== 第一组数据发送 ===")
        for i, value in enumerate(values1, 1):
            packet = generate_packet(prefix1, value)
            ser.write(packet)
            hex_str = " ".join(f"{byte:02X}" for byte in packet)
            print(f"[{time.strftime('%H:%M:%S')}] 第{i}/127组: {hex_str}")
            time.sleep(interval)

        print("\n第一组数据发送完成！")

        prefix2 = [0x57, 0x4B, 0x4C, 0x59, 0x09, 0x01, 0x89]
        values2 = list(range(1, 128))

        print("\n=== 第二组数据发送 ===")
        for i, value in enumerate(values2, 1):
            packet = generate_packet(prefix2, value)
            ser.write(packet)
            hex_str = " ".join(f"{byte:02X}" for byte in packet)
            print(f"[{time.strftime('%H:%M:%S')}] 第{i}/127组: {hex_str}")
            time.sleep(interval)

        print("\n第二组数据发送完成！")

    except serial.SerialException as e:
        print(f"串口错误: {e}")
        print("请检查串口是否存在或被其他程序占用")
    except KeyboardInterrupt:
        print("\n程序已停止")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("串口已关闭")


def get_default_port():
    if platform.system() == 'Windows':
        return 'COM2'
    elif platform.system() == 'Darwin':
        return '/dev/tty.usbserial-2'
    else:
        return '/dev/ttyUSB0'


if __name__ == "__main__":
    send_to_serial(get_default_port(), baudrate=9600, interval=10.0)