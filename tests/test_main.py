import pytest

from conftest import StopInfiniteLoop


@pytest.mark.timeout(1, method='thread')
@pytest.mark.usefixtures('modified_clock')
def test_main_run_without_exceptions(_the_snake):
    try:
        _the_snake.main()
    except StopInfiniteLoop:
        pass
    except Exception as error:
        raise AssertionError(
            'При запуске функции `main` возникло исключение: '
            f'`{type(error).__name__}: {error}`\n\n'
            'Убедитесь, что функция работает корректно.'
        )
