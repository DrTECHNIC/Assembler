import pytest
from interpreter import Interpreter


@pytest.fixture
def setup_binary_file(tmp_path):
    binary_file = tmp_path / "test.bin"
    result_file = tmp_path / "test_result.xml"
    return binary_file, result_file


def test_load(setup_binary_file):
    binary_file, result_file = setup_binary_file
    binary_file.write_bytes(bytes([0x02, 0x1A, 0x1F, 0x00, 0x00]))
    interpreter = Interpreter(str(binary_file), str(result_file), "0:25")
    interpreter.interpret()
    with open(result_file, "r", encoding="utf-8") as f:
        assert "<register address=\"4\">995</register>" in f.read()


def test_read(setup_binary_file):
    binary_file, result_file = setup_binary_file
    binary_file.write_bytes(bytes([0x6D, 0x96, 0x81, 0x12]))
    interpreter = Interpreter(str(binary_file), str(result_file), "0:850")
    interpreter.registers[10] = 1
    interpreter.registers[813] = 1000
    interpreter.interpret()
    with open(result_file, "r", encoding="utf-8") as f:
        assert "<register address=\"4\">1000</register>" in f.read()


def test_write(setup_binary_file):
    binary_file, result_file = setup_binary_file
    binary_file.write_bytes(bytes([0x05, 0xFC, 0x18, 0x00, 0x00, 0x00]))
    interpreter = Interpreter(str(binary_file), str(result_file), "0:800")
    interpreter.registers[8] = 42
    interpreter.interpret()
    with open(result_file, "r", encoding="utf-8") as f:
        assert "<register address=\"799\">42</register>" in f.read()


def test_pow(setup_binary_file):
    binary_file, result_file = setup_binary_file
    binary_file.write_bytes(bytes([0x31, 0x05, 0xBA, 0x00, 0x00, 0x00]))
    interpreter = Interpreter(str(binary_file), str(result_file), "0:400")
    interpreter.registers[10] = 2
    interpreter.registers[372] = 5
    interpreter.interpret()
    with open(result_file, "r", encoding="utf-8") as f:
        assert "<register address=\"0\">25</register>" in f.read()