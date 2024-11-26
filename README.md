# **Задание №4**

Разработать ассемблер и интерпретатор для учебной виртуальной машины (УВМ). Система команд УВМ представлена далее.

Для ассемблера необходимо разработать читаемое представление команд УВМ. Ассемблер принимает на вход файл с текстом 
исходной программы, путь к которой задается из командной строки. Результатом работы ассемблера является бинарный файл
в виде последовательности байт, путь к которому задается из командной строки. Дополнительный ключ командной строки 
задает путь к файлу-логу, в котором хранятся ассемблированные инструкции в духе списков “ключ=значение”, как 
в приведенных далее тестах.

Интерпретатор принимает на вход бинарный файл, выполняет команды УВМ и сохраняет в файле-результате значения
из диапазона памяти УВМ. Диапазон также указывается из командной строки.

Форматом для файла-лога и файла-результата является xml.

Необходимо реализовать приведенные тесты для всех команд, а также написать и отладить тестовую программу.

**Загрузка константы**

| A | B | C |
| - | - | - |
| Биты 0—6 | Биты 7—10 | Биты 11—37 |
| 2 | Адрес | Константа |

Размер команды: 5 байт. Операнд: поле C. Результат: регистр по адресу, которым является поле B.

Тест (A=2, B=4, C=995):

_0x02, 0x1A, 0x1F, 0x00, 0x00_

**Чтение значения из памяти**

| A | B | C | D |
| - | - | - | - |
| Биты 0—6 | Биты 7—21 | Биты 22—25 | Биты 26—29 |
| 109 | Смещение | Адрес | Адрес |

Размер команды: 4 байт. Операнд: значение в памяти по адресу, которым является сумма адреса (регистр по адресу, 
которым является поле C) и смещения (поле B). Результат: регистр по адресу, которым является поле D.

Тест (A=109, B=812, C=10, D=4):

_0x6D, 0x96, 0x81, 0x12_

**Запись значения в память**

| A | B | C |
| - | - | - |
| Биты 0—6 | Биты 7—10 | Биты 11—42 |
| 5 | Адрес | Адрес |

Размер команды: 6 байт. Операнд: регистр по адресу, которым является поле B. Результат: значение в памяти по адресу, 
которым является поле C.

Тест (A=5, B=8, C=799):

_0x05, 0xFC, 0x18, 0x00, 0x00, 0x00_

**Бинарная операция: pow()**

| A | B | C | D |
| - | - | - | - |
| Биты 0—6 | Биты 7—10 | Биты 11—14 | Биты 15—46 |
| 49 | Адрес | Адрес | Адрес |

Размер команды: 6 байт. Первый операнд: значение в памяти по адресу, которым является поле D. Второй операнд: регистр 
по адресу, которым является поле B. Результат: регистр по адресу, которым является поле C.

Тест (A=49, B=10, C=0, D=372):

_0x31, 0x05, 0xBA, 0x00, 0x00, 0x00_

**Тестовая программа**

Выполнить поэлементно операцию pow() над двумя векторами длины 6. Результат записать во второй вектор.

# Установка

Перед началом работы с программой требуется скачать репозиторий и необходимые библиотеки.

Клонирование репозитория:
```Bash
git clone https://github.com/DrTECHNIC/Assembler
```

Скачивание библиотеки [pytest](https://github.com/pytest-dev/pytest) путём запуска файла [script.sh](https://github.com/DrTECHNIC/Assembler/blob/main/script.sh):
```Bash
script.sh
```

# Запуск

Запуск [assembler.py](https://github.com/DrTECHNIC/Assembler/blob/main/assembler.py):
```Bash
py assembler.py <path/to/program.asm> <path/to/bin_file.bin> -l <path/to/log.xml>
```

Запуск [interpreter.py](https://github.com/DrTECHNIC/Assembler/blob/main/interpreter.py):
```Bash
py interpreter.py <path/to/bin_file.bin> <path/to/result.xml> <left_boundary:right_boundary>
```

Запуск [pytest_assembler.py](https://github.com/DrTECHNIC/Assembler/blob/main/pytest_assembler.py):
```Bash
pytest -v pytest_assembler.py
```

Запуск [pytest_interpreter.py](https://github.com/DrTECHNIC/Assembler/blob/main/pytest_interpreter.py):
```Bash
pytest -v pytest_interpreter.py
```

# Тесты

## Тесты тестовой программы

### [Тестовая программа](https://github.com/DrTECHNIC/Assembler/blob/main/program.asm)

**Входные данные:**

**A** = (2, 3, 4, 5, 6, 7)

**B** = (3, 2, 5, 3, 2, 1)

**Выходные данные:**

**A** = (2, 3, 4, 5, 6, 7)

**B** = (8, 9, 1024, 125, 36, 7)

```
LOAD 2 0 2
LOAD 2 1 3
LOAD 2 2 4
LOAD 2 3 5
LOAD 2 4 6
LOAD 2 5 7

LOAD 2 6 3
LOAD 2 7 2
LOAD 2 8 5
LOAD 2 9 3
LOAD 2 10 2
LOAD 2 11 1

POW 49 6 6 0
POW 49 7 7 1
POW 49 8 8 2
POW 49 9 9 3
POW 49 10 10 4
POW 49 11 11 5
```

### Файл-результат

```
<?xml version="1.0" encoding="utf-8"?>
<result>
	<register address="0">2</register>
	<register address="1">3</register>
	<register address="2">4</register>
	<register address="3">5</register>
	<register address="4">6</register>
	<register address="5">7</register>
	<register address="6">8</register>
	<register address="7">9</register>
	<register address="8">1024</register>
	<register address="9">125</register>
	<register address="10">36</register>
	<register address="11">7</register>
</result>
```

## [Ассемблер](https://github.com/DrTECHNIC/Assembler/blob/main/pytest_assembler.py)

### Тест операции "Загрузка константы"

```python
def test_load(setup_files):
    asm_file, bin_file, log_file = setup_files
    asm_file.write_text("LOAD 2 4 995\n")
    assembler = Assembler(str(asm_file), str(bin_file), str(log_file))
    assembler.assemble()
    with open(bin_file, "rb") as f:
        assert f.read() == bytes([0x02, 0x1A, 0x1F, 0x00, 0x00])
```

### Тест операции "Чтение значения из памяти"

```python
def test_read(setup_files):
    asm_file, bin_file, log_file = setup_files
    asm_file.write_text("READ 109 812 10 4\n")
    assembler = Assembler(str(asm_file), str(bin_file), str(log_file))
    assembler.assemble()
    with open(bin_file, "rb") as f:
        assert f.read() == bytes([0x6D, 0x96, 0x81, 0x12])
```

### Тест операции "Запись значения в память"

```python
def test_write(setup_files):
    asm_file, bin_file, log_file = setup_files
    asm_file.write_text("WRITE 5 8 799\n")
    assembler = Assembler(str(asm_file), str(bin_file), str(log_file))
    assembler.assemble()
    with open(bin_file, "rb") as f:
        assert f.read() == bytes([0x05, 0xFC, 0x18, 0x00, 0x00, 0x00])
```

### Тест операции "Бинарная операция: pow()"

```python
def test_pow(setup_files):
    asm_file, bin_file, log_file = setup_files
    asm_file.write_text("POW 49 10 0 372\n")
    assembler = Assembler(str(asm_file), str(bin_file), str(log_file))
    assembler.assemble()
    with open(bin_file, "rb") as f:
        assert f.read() == bytes([0x31, 0x05, 0xBA, 0x00, 0x00, 0x00])
```

### Результаты

![](https://github.com/DrTECHNIC/Assembler/blob/main/pytest_assembler.png)

## [Интерпретатор](https://github.com/DrTECHNIC/Assembler/blob/main/pytest_interpreter.py)

### Тест операции "Загрузка константы"

```python
def test_load(setup_binary_file):
    binary_file, result_file = setup_binary_file
    binary_file.write_bytes(bytes([0x02, 0x1A, 0x1F, 0x00, 0x00]))
    interpreter = Interpreter(str(binary_file), str(result_file), "0:25")
    interpreter.interpret()
    with open(result_file, "r", encoding="utf-8") as f:
        assert "<register address=\"4\">995</register>" in f.read()
```

### Тест операции "Чтение значения из памяти"

```python
def test_read(setup_binary_file):
    binary_file, result_file = setup_binary_file
    binary_file.write_bytes(bytes([0x6D, 0x96, 0x81, 0x12]))
    interpreter = Interpreter(str(binary_file), str(result_file), "0:850")
    interpreter.registers[10] = 1
    interpreter.registers[813] = 1000
    interpreter.interpret()
    with open(result_file, "r", encoding="utf-8") as f:
        assert "<register address=\"4\">1000</register>" in f.read()
```

### Тест операции "Запись значения в память"

```python
def test_write(setup_binary_file):
    binary_file, result_file = setup_binary_file
    binary_file.write_bytes(bytes([0x05, 0xFC, 0x18, 0x00, 0x00, 0x00]))
    interpreter = Interpreter(str(binary_file), str(result_file), "0:800")
    interpreter.registers[8] = 42
    interpreter.interpret()
    with open(result_file, "r", encoding="utf-8") as f:
        assert "<register address=\"799\">42</register>" in f.read()
```

### Тест операции "Бинарная операция: pow()"

```python
def test_pow(setup_binary_file):
    binary_file, result_file = setup_binary_file
    binary_file.write_bytes(bytes([0x31, 0x05, 0xBA, 0x00, 0x00, 0x00]))
    interpreter = Interpreter(str(binary_file), str(result_file), "0:400")
    interpreter.registers[10] = 2
    interpreter.registers[372] = 5
    interpreter.interpret()
    with open(result_file, "r", encoding="utf-8") as f:
        assert "<register address=\"0\">25</register>" in f.read()
```

### Результаты

![](https://github.com/DrTECHNIC/Assembler/blob/main/pytest_interpreter.png)
