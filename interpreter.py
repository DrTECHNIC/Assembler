import argparse
import xml.etree.ElementTree as ET
import xml.dom.minidom

class Interpreter:
    def __init__(self, path_to_binary_file, path_to_result_file, boundaries):
        self.path_result = path_to_result_file
        self.boundaries = list(map(int, boundaries.split(':')))
        self.registers = [0] * (self.boundaries[1] - self.boundaries[0] + 1)
        with open(path_to_binary_file, 'rb') as binary_file:
            self.byte_code = int.from_bytes(binary_file.read(), byteorder="little")

    def interpret(self):
        while self.byte_code != 0:
            A = self.byte_code & ((1 << 7) - 1)
            self.byte_code >>= 7
            match A:
                case 2: self.load()
                case 109: self.read()
                case 5: self.write()
                case 49: self.pow()
                case _: raise ValueError("В бинарном файле содержатся невалидные данные: неверный байт-код")
        result_root = ET.Element("result")
        for pos, register in enumerate(self.registers, self.boundaries[0]):
            if register != 0:
                element = ET.SubElement(result_root, "register")
                element.attrib["address"] = str(pos)
                element.text = str(register)
        log_data = ET.tostring(result_root, encoding="unicode", method="xml").encode()
        dom = xml.dom.minidom.parseString(log_data)
        log = f"<?xml version=\"1.0\" encoding=\"utf-8\"?>\n" + dom.toprettyxml(newl="\n")[23:]
        with open(self.path_result, 'w', encoding="utf-8") as f:
            f.write(log)

    def load(self):
        B = self.byte_code & ((1 << 4) - 1); self.byte_code >>= 4
        C = self.byte_code & ((1 << 28) - 1); self.byte_code >>= 29
        if not (self.boundaries[0] <= B <= self.boundaries[1]):
            raise ValueError("В бинарном файле присутствуют невалидные данные: обращение к ячейки памяти по адресу вне диапазона")
        self.registers[B] = C

    def read(self):
        B = self.byte_code & ((1 << 15) - 1); self.byte_code >>= 15
        C = self.byte_code & ((1 << 4) - 1); self.byte_code >>= 4
        D = self.byte_code & ((1 << 4) - 1); self.byte_code >>= 9
        if not (self.boundaries[0] <= C <= self.boundaries[1]):
            raise ValueError("В бинарном файле присутствуют невалидные данные: обращение к ячейки памяти по адресу вне диапазона")
        if not (self.boundaries[0] <= D <= self.boundaries[1]):
            raise ValueError("В бинарном файле присутствуют невалидные данные: обращение к ячейки памяти по адресу вне диапазона")
        if not (self.boundaries[0] <= self.registers[C] + B <= self.boundaries[1]):
            raise ValueError("В бинарном файле присутствуют невалидные данные: обращение к ячейки памяти по адресу вне диапазона")
        self.registers[D] = self.registers[self.registers[C] + B]

    def write(self):
        B = self.byte_code & ((1 << 4) - 1); self.byte_code >>= 4
        C = self.byte_code & ((1 << 32) - 1); self.byte_code >>= 37
        if not (self.boundaries[0] <= B <= self.boundaries[1]):
            raise ValueError("В бинарном файле присутствуют невалидные данные: обращение к ячейки памяти по адресу вне диапазона")
        if not (self.boundaries[0] <= C <= self.boundaries[1]):
            raise ValueError("В бинарном файле присутствуют невалидные данные: обращение к ячейки памяти по адресу вне диапазона")
        self.registers[C] = self.registers[B]

    def pow(self):
        B = self.byte_code & ((1 << 4) - 1); self.byte_code >>= 4
        C = self.byte_code & ((1 << 4) - 1); self.byte_code >>= 4
        D = self.byte_code & ((1 << 32) - 1); self.byte_code >>= 33
        if not (self.boundaries[0] <= B <= self.boundaries[1]):
            raise ValueError("В бинарном файле присутствуют невалидные данные: обращение к ячейки памяти по адресу вне диапазона")
        if not (self.boundaries[0] <= C <= self.boundaries[1]):
            raise ValueError("В бинарном файле присутствуют невалидные данные: обращение к ячейки памяти по адресу вне диапазона")
        if not (self.boundaries[0] <= D <= self.boundaries[1]):
            raise ValueError("В бинарном файле присутствуют невалидные данные: обращение к ячейки памяти по адресу вне диапазона")
        self.registers[C] = self.registers[D] ** self.registers[B]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("bin_file", help="Входной файл (*.bin)")
    parser.add_argument("res_file", help="Выходной файл (*.xml)")
    parser.add_argument("boundaries", help="Границы памяти в формате: <левая>:<правая>")
    args = parser.parse_args()
    interpreter = Interpreter(args.bin_file, args.res_file, args.boundaries)
    try:
        interpreter.interpret()
        print(f"Интерпретация выполнена успешно. Результаты сохранены в {args.res_file}")
    except ValueError as error:
        print(f"Ошибка:\n{error}")
