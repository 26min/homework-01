"""Модуль, содержащий декораторы для логирования работы функций."""
import functools
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """Декоратор, логирующий детали выполнения функции."""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                # Выполняем функцию
                result = func(*args, **kwargs)
                log_message = f"{func.__name__} ok"

                # Запись лога
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(log_message + "\n")
                else:
                    print(log_message)

                return result

            except Exception as e:
                # Если ошибка — формируем сообщение по шаблону
                error_type = type(e).__name__
                log_message = f"{func.__name__} error: {error_type}. Inputs: {args}, {kwargs}"

                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(log_message + "\n")
                else:
                    print(log_message)

                # Пробрасываем ошибку дальше
                raise e

        return wrapper

    return decorator
