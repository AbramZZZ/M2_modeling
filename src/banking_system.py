from typing import List
from bank import Bank


class BankingSystem:
    def __init__(self, banks: List[Bank], cash_outside: float = 0.0, reserve_ratio: float = 0.1):
        self.banks = banks
        self.cash_outside = cash_outside
        self.reserve_ratio = reserve_ratio

    def total_loans(self) -> float:
        return sum(bank.loans for bank in self.banks)

    def total_reserves(self) -> float:
        return sum(bank.reserves for bank in self.banks)

    def total_checking_deposits(self) -> float:
        return sum(bank.deposits_checking for bank in self.banks)

    def total_savings_deposits(self) -> float:
        return sum(bank.deposits_savings for bank in self.banks)

    def total_time_deposits(self) -> float:
        return sum(bank.deposits_time for bank in self.banks)

    def total_deposits(self) -> float:
        return sum(bank.total_deposits for bank in self.banks)

    def compute_M0(self) -> float:
        return self.cash_outside

    def compute_M1(self) -> float:
        return self.compute_M0() + self.total_checking_deposits()

    def compute_M2(self) -> float:
        return self.compute_M1() + self.total_savings_deposits() + self.total_time_deposits()

    def issue_loan(self, bank_name: str, amount: float):        #При выдаче кредита растет loans и deposits, то есть растёт М1 и М2
        if amount <= 0:
            raise ValueError("amount must be positive")

        for bank in self.banks:
            if bank.name == bank_name:                
                max_checking = bank.reserves / self.reserve_ratio       # ограничение по резервам
                new_checking = bank.deposits_checking + amount
                if new_checking > max_checking:
                    raise ValueError("Not enough reserves to issue loan")
                bank.loans += amount
                bank.deposits_checking += amount
                assert abs(bank.check_balance()) < 1e-6, "Balance broken!"
                return

    def absorb_deposit(self, bank_name: str, amount: float):            #Погасили кредит = деньги уничтожились 
        if amount <= 0:
            raise ValueError("amount must be positive")

        for bank in self.banks:
            if bank.name == bank_name:
                if bank.loans < amount:
                    raise ValueError("Not enough loans to absorb")
                if bank.deposits_checking < amount:
                    raise ValueError("Not enough deposits to absorb")
                bank.loans -= amount
                bank.deposits_checking -= amount
                assert abs(bank.check_balance()) < 1e-6, "Balance broken!"
                return

    def check_system_balance(self) -> float:
        total_assets = sum(bank.total_assets for bank in self.banks)
        total_liabilities = self.total_deposits()
        return total_assets - total_liabilities

    def __repr__(self):
        return f"BankingSystem(" f"M0={self.compute_M0()}, " f"M1={self.compute_M1()}, " f"M2={self.compute_M2()})"