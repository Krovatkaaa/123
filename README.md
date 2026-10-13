# Калькулятор на Python

Удобный оконный калькулятор для Windows с операциями сложения, вычитания,
умножения и деления. Поддерживает ввод с клавиатуры, проценты, смену знака,
удаление последнего символа и последовательные вычисления.

## Запуск

```powershell
python calculator.py
```

Также можно запустить готовый файл `dist/Calculator.exe` — установка Python для
этого не требуется.

## Тесты

```powershell
python -m unittest -v
```

## Сборка EXE

```powershell
python -m pip install pyinstaller
python -m PyInstaller --noconfirm --clean --onefile --windowed --name Calculator calculator.py
```
