from dataclasses import dataclass, asdict
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE: str = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:

        self.action: int = action
        self.duration_hours: float = duration
        self.weight: float = weight
        self.time_in_mnts: float = duration * 60

    def get_distance(self) -> float:
        """Рассчет дистаниции за тренировку в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_hours

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration_hours,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    coeff_cal_run: float = 18
    coeff_cal_run_2: float = 20

    def get_spent_calories(self):
        return ((self.coeff_cal_run
                * self.get_mean_speed()
                - self.coeff_cal_run_2)
                * self.weight
                / self.M_IN_KM
                * self.time_in_mnts)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_cal_walk: float = 0.035
    coeff_cal_walk_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self):
        return ((self.coeff_cal_walk
                * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.coeff_cal_walk_2
                * self.weight) * self.time_in_mnts)


class Swimming(Training):
    """Тренировка: плавание."""
    coeff_cal_swm: float = 1.1
    coeff_cal_swm_2: float = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: int = count_pool

    def get_distance(self) -> float:
        return (self.action
                * self.LEN_STEP
                / self.M_IN_KM)

    def get_mean_speed(self) -> float:

        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration_hours)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                + self.coeff_cal_swm)
                * self.coeff_cal_swm_2
                * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in training_type:
        raise ValueError(
            f'Тип тренировки {workout_type} не найден! '
            f'Пожалуйста, выберите другой тип тренировки из представленных: '
            f'{training_type.keys()}'
        )
    return training_type[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
