import pandas as pd

from plt_temp import build_dataframe


def test_build_dataframe_columns_rows_and_sorting():
    # Время намеренно перемешано, чтобы проверить сортировку.
    hours = [
        "2026-01-01T02:00",
        "2026-01-01T00:00",
        "2026-01-01T03:00",
        "2026-01-01T01:00",
    ]
    temps = [-3.0, -1.5, -4.5, -2.0]

    df = build_dataframe(hours, temps)

    # названия столбцов
    assert list(df.columns) == ["time", "temperature_c"]
    # количество строк
    assert len(df) == 4
    # сортировка по времени
    assert df["time"].is_monotonic_increasing
    assert df["time"].tolist() == [
        pd.Timestamp("2026-01-01T00:00"),
        pd.Timestamp("2026-01-01T01:00"),
        pd.Timestamp("2026-01-01T02:00"),
        pd.Timestamp("2026-01-01T03:00"),
    ]
    # температура соответствует своему времени после сортировки
    assert df["temperature_c"].tolist() == [-1.5, -2.0, -3.0, -4.5]
    # индекс сброшен
    assert df.index.tolist() == [0, 1, 2, 3]
