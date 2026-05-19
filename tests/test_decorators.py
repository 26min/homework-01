"""Модуль тестирование декоратора логирования функций."""
import os

import pytest

from src.decorators import log


# Тестовые функции
@log()
def success_func(x, y):
    """Вспомогательная функция для проверки успешного выполнения."""
    return x + y


@log()
def error_func():
    """Вспомогательная функция для имитации падения с ошибкой деления на ноль."""
    return 1 / 0


def test_log_success_console(capsys):
    """Проверка успешного выполнения в консоль."""
    success_func(1, 2)
    captured = capsys.readouterr()
    assert captured.out.strip() == "success_func ok"


def test_log_error_console(capsys):
    """Проверка ошибки в консоль."""
    with pytest.raises(ZeroDivisionError):
        error_func()
    captured = capsys.readouterr()
    assert "error_func error: ZeroDivisionError. Inputs: (), {}" in captured.out


def test_log_to_file():
    """Проверка записи в файл."""
    filename = "test_log.txt"
    if os.path.exists(filename):
        os.remove(filename)

    @log(filename=filename)
    def file_func(x):
        return x

    file_func("test")

    with open(filename, "r") as f:
        lines = f.readlines()

    assert lines[0].strip() == "file_func ok"

    if os.path.exists(filename):
        os.remove(filename)
