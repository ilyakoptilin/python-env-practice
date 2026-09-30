import matplotlib.pyplot as plt
import pandas as pd
import requests

URL = "https://api.open-meteo.com/v1/forecast"
PARAMS = {"latitude": 55.75, "longitude": 37.61, "hourly": "temperature_2m"}
TIMEOUT_SECONDS = 10
HOURS_COUNT = 24
CSV_PATH = "temperature_24h.csv"
PNG_PATH = "temperature_24h.png"


def fetch_hourly_data() -> dict:
    """Запрашивает почасовой прогноз; ошибка HTTP не превращается в ошибку JSON."""
    response = requests.get(URL, params=PARAMS, timeout=TIMEOUT_SECONDS)
    response.raise_for_status()
    return response.json()


def build_dataframe(hours: list[str], temps: list[float]) -> pd.DataFrame:
    """Собирает DataFrame со столбцами time и temperature_c, отсортированный по времени.

    Сетевых запросов не выполняет: данные приходят только через аргументы.
    """
    df = pd.DataFrame({"time": pd.to_datetime(hours), "temperature_c": temps})
    return df.sort_values("time").reset_index(drop=True)


def plot_temperature(df: pd.DataFrame, path: str = PNG_PATH) -> None:
    plt.figure()
    plt.plot(df["time"], df["temperature_c"], marker="o")
    plt.xticks(rotation=45)
    plt.title("Температура в Москве (24 часа)")
    plt.xlabel("Время")
    plt.ylabel("°C")
    plt.tight_layout()
    plt.savefig(path)


def main() -> None:
    data = fetch_hourly_data()
    hours = data["hourly"]["time"][:HOURS_COUNT]
    temps = data["hourly"]["temperature_2m"][:HOURS_COUNT]

    df = build_dataframe(hours, temps)
    df.to_csv(CSV_PATH, index=False)
    print(f"Сохранено в {CSV_PATH}")

    plot_temperature(df)
    print(f"График сохранён в {PNG_PATH}")
    plt.show()


if __name__ == "__main__":
    main()
