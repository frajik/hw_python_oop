class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        duration = self.duration
        distance = self.distance
        speed = self.speed
        calories = self.calories
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {duration:.3f} ч.; '
                f'Дистанция: {distance:.3f} км; '
                f'Ср. скорость: {speed:.3f} км/ч; '
                f'Потрачено ккал: {calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65  # расстояние в (м) за 1 шаг.
    M_IN_KM = 1000  # const для перевода (м) в (км).

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:

        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Рассчет дистаниции за тренировку в км."""
        result = self.action * self.LEN_STEP / self.M_IN_KM
        return result

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        avg_speed = self.get_distance() / self.duration
        return avg_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(training_type=self.__class__.__name__,
                           duration=self.duration,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self):  # рассчет калорий при беге.
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        time_in_mnts = self.duration * 60
        result = ((coeff_calorie_1
                  * self.get_mean_speed()
                  - coeff_calorie_2)
                  * self.weight
                  / self.M_IN_KM
                  * time_in_mnts)
        return result


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        coeff_calorie_1 = 0.035
        coeff_calorie_2 = 0.029
        time_in_mnts: float = self.duration * 60
        result = ((coeff_calorie_1
                   * self.weight
                   + (self.get_mean_speed()**2 // self.height)
                   * coeff_calorie_2
                   * self.weight) * time_in_mnts)
        return result


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38  # расcтояние в (м) за 1 гребок.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        result = (self.action
                  * self.LEN_STEP
                  / self.M_IN_KM)
        return result

    def get_mean_speed(self) -> float:

        result = (self.length_pool
                  * self.count_pool
                  / self.M_IN_KM
                  / self.duration)
        return result

    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 1.1
        coeff_calorie_2 = 2
        result = ((self.get_mean_speed()
                  + coeff_calorie_1)
                  * coeff_calorie_2
                  * self.weight)
        return result


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return training_type[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())
    return 0


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
