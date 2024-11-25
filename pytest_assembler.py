import pytest
from assembler import Assembler


@pytest.fixture
def setup_files(tmp_path):
    asm_file = tmp_path / "test.asm"
    bin_file = tmp_path / "test.bin"
    log_file = tmp_path / "test_log.xml"
    return asm_file, bin_file, log_file


def test_load(setup_files):
    asm_file, bin_file, log_file = setup_files
    asm_file.write_text("LOAD 2 4 995\n")
    assembler = Assembler(str(asm_file), str(bin_file), str(log_file))
    assembler.assemble()
    with open(bin_file, "rb") as f:
        assert f.read() == bytes([0x02, 0x1A, 0x1F, 0x00, 0x00])


def test_read(setup_files):
    asm_file, bin_file, log_file = setup_files
    asm_file.write_text("READ 109 812 10 4\n")
    assembler = Assembler(str(asm_file), str(bin_file), str(log_file))
    assembler.assemble()
    with open(bin_file, "rb") as f:
        assert f.read() == bytes([0x6D, 0x96, 0x81, 0x12])


def test_write(setup_files):
    asm_file, bin_file, log_file = setup_files
    asm_file.write_text("WRITE 5 8 799\n")
    assembler = Assembler(str(asm_file), str(bin_file), str(log_file))
    assembler.assemble()
    with open(bin_file, "rb") as f:
        assert f.read() == bytes([0x05, 0xFC, 0x18, 0x00, 0x00, 0x00])


def test_pow(setup_files):
    asm_file, bin_file, log_file = setup_files
    asm_file.write_text("POW 49 10 0 372\n")
    assembler = Assembler(str(asm_file), str(bin_file), str(log_file))
    assembler.assemble()
    with open(bin_file, "rb") as f:
        assert f.read() == bytes([0x31, 0x05, 0xBA, 0x00, 0x00, 0x00])