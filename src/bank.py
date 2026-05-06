class Bank:
    def __init__(
        self,
        name: str,
        reserves: float,        # Деньги банка в ЦБ и наличность в кассе 
        loans: float,       # Выданные кредиты
        securities: float,      # Ценные бумаги
        deposits_checking: float,       # Деньги на картах/счетах
        deposits_savings: float,        # Сберегательные счета
        deposits_time: float,       # Срочные вклады
    ):
        self.name = name
#Активы
        self.reserves = reserves
        self.loans = loans
        self.securities = securities
#Пассивы
        self.deposits_checking = deposits_checking
        self.deposits_savings = deposits_savings
        self.deposits_time = deposits_time

    @property
    def total_assets(self) -> float:
        return self.reserves + self.loans + self.securities

    @property
    def total_deposits(self) -> float:
        return self.deposits_checking + self.deposits_savings + self.deposits_time

    def m2_contribution(self) -> float:         # По сути это вклад банка в М2
        return self.total_deposits

    def check_balance(self) -> float:
        return self.total_assets - self.total_deposits

    def __repr__(self):
        return (f"Bank({self.name}, " f"Assets={self.total_assets}, " f"Deposits={self.total_deposits})")