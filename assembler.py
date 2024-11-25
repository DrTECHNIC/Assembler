import argparse
import xml.etree.ElementTree as ET
import xml.dom.minidom

class Assembler:
    def __init__(self, path_to_code_file, path_to_binary_file, path_to_log_file):
        self.path_binary = path_to_binary_file
        self.path_code = path_to_code_file
        self.path_log = path_to_log_file
        self.bytes = []
        self.log_root = ET.Element("log")

    def assemble(self):
        with open(self.path_code, 'rt') as code:
            for line in code:
                line = line.split('\n')[0].strip()
                if not line: continue
                command, *args = line.split()
                match command:
                    case "LOAD":
                        if len(args) != 3:
                            raise SyntaxError(f"{line}\nУ операции \"Загрузка константы\" должно быть 3 аргумента")
                        self.bytes.append(self.load(int(args[0]), int(args[1]), int(args[2])))
                    case "READ":
                        if len(args) != 4:
                            raise SyntaxError(f"{line}\nУ операции \"Чтение значения из памяти\" должно быть 4 аргумента")
                        self.bytes.append(self.read(int(args[0]), int(args[1]), int(args[2]), int(args[3])))
                    case "WRITE":
                        if len(args) != 3:
                            raise SyntaxError(f"{line}\nУ операции \"Запись значения в память\" должно быть 3 аргумента")
                        self.bytes.append(self.write(int(args[0]), int(args[1]), int(args[2])))
                    case "POW":
                        if len(args) != 4:
                            raise SyntaxError(f"{line}\nУ операции \"Бинарная операция: pow()\" должно быть 4 аргумента")
                        self.bytes.append(self.pow(int(args[0]), int(args[1]), int(args[2]), int(args[3])))
                    case _:
                        raise SyntaxError(f"{line}\nНеизвестная операция")
        with open(self.path_binary, 'wb') as binary:
            for byte in self.bytes:
                binary.write(byte)
        log_data = ET.tostring(self.log_root, encoding="unicode", method="xml").encode()
        dom = xml.dom.minidom.parseString(log_data)
        log = f"<?xml version=\"1.0\" encoding=\"utf-8\"?>\n" + dom.toprettyxml(newl="\n")[23:]
        with open(self.path_log, 'w', encoding="utf-8") as f: f.write(log)

    def load(self, A, B, C):
        if A != 2: raise ValueError("Параметр А должен быть равен 2")
        if not (0 <= B < (1 << 4)): raise ValueError("Адрес B должен быть в пределах от 0 до 15 (2^4-1)")
        if not (0 <= C < (1 << 27)): raise ValueError("Константа C должна быть в пределах от 0 до 134217727 (2^27-1)")
        bits = (C << 11) | (B << 7) | A
        bits = bits.to_bytes(5, byteorder="little")
        element = ET.SubElement(self.log_root, "LOAD")
        element.attrib["A"] = str(A)
        element.attrib["B"] = str(B)
        element.attrib["C"] = str(C)
        element.text = bits.hex()
        return bits

    def read(self, A, B, C, D):
        if A != 109: raise ValueError("Параметр А должен быть равен 109")
        if not (0 <= B < (1 << 15)): raise ValueError("Адрес B должен быть в пределах от 0 до 32767 (2^15-1)")
        if not (0 <= C < (1 << 4)): raise ValueError("Адрес C должен быть в пределах от 0 до 15 (2^4-1)")
        if not (0 <= D < (1 << 4)): raise ValueError("Адрес D должен быть в пределах от 0 до 15 (2^4-1)")
        bits = (D << 26) | (C << 22) | (B << 7) | A
        bits = bits.to_bytes(4, byteorder="little")
        element = ET.SubElement(self.log_root, "READ")
        element.attrib["A"] = str(A)
        element.attrib["B"] = str(B)
        element.attrib["C"] = str(C)
        element.attrib["D"] = str(D)
        element.text = bits.hex()
        return bits

    def write(self, A, B, C):
        if A != 5: raise ValueError("Параметр А должен быть равен 5")
        if not (0 <= B < (1 << 7)): raise ValueError("Адрес B должен быть в пределах от 0 до 127 (2^7-1)")
        if not (0 <= C < (1 << 32)): raise ValueError("Адрес C должен быть в пределах от 0 до 4294967295 (2^32-1)")
        bits = (C << 11) | (B << 7) | A
        bits = bits.to_bytes(6, byteorder="little")
        element = ET.SubElement(self.log_root, "WRITE")
        element.attrib["A"] = str(A)
        element.attrib["B"] = str(B)
        element.attrib["C"] = str(C)
        element.text = bits.hex()
        return bits

    def pow(self, A, B, C, D):
        if A != 49: raise ValueError("Параметр А должен быть равен 49")
        if not (0 <= B < (1 << 4)): raise ValueError("Адрес B должен быть в пределах от 0 до 15 (2^4-1)")
        if not (0 <= C < (1 << 4)): raise ValueError("Адрес C должен быть в пределах от 0 до 15 (2^4-1)")
        if not (0 <= D < (1 << 32)): raise ValueError("Адрес D должен быть в пределах от 0 до 4294967295 (2^32-1)")
        bits = (D << 15) | (C << 11) | (B << 7) | A
        bits = bits.to_bytes(6, byteorder="little")
        element = ET.SubElement(self.log_root, "POW")
        element.attrib["A"] = str(A)
        element.attrib["B"] = str(B)
        element.attrib["C"] = str(C)
        element.attrib["D"] = str(D)
        element.text = bits.hex()
        return bits


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("asm_file", help="Входной файл (*.asm)")
    parser.add_argument("bin_file", help="Выходной файл (*.bin)")
    parser.add_argument("-l", "--log_file", help="Лог файл (*.xml)")
    args = parser.parse_args()
    assembler = Assembler(args.asm_file, args.bin_file, args.log_file)
    try:
        assembler.assemble()
        print(f"Ассемблирование выполнено успешно. Выходной файл: {args.bin_file}")
    except ValueError as error:
        print(f"Ошибка:\n{error}")
