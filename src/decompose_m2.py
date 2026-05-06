from typing import List
from bank import Bank
from banking_system import BankingSystem


def check_shares(checking_share: float, savings_share: float, time_share: float):
    total = checking_share + savings_share + time_share
    if abs(total - 1.0) > 1e-9:
        raise ValueError("checking_share + savings_share + time_share must be equal to 1")
    if checking_share < 0 or savings_share < 0 or time_share < 0:
        raise ValueError("Shares must be non-negative")


def normalize_weights(weights: List[float]) -> List[float]:
    if len(weights) == 0:
        raise ValueError("weights must not be empty")
    if any(w < 0 for w in weights):
        raise ValueError("weights must not be negative")
    total = sum(weights)
    return [w / total for w in weights]


def reconstruct_deposits_from_M2(M2: float, cash_outside: float, checking_share: float = 0.5, savings_share: float = 0.3, time_share: float = 0.2):
    check_shares(checking_share, savings_share, time_share)        # Проверяем, что доли складываются в 1
    total_deposits = M2 - cash_outside
    if total_deposits < 0:
        raise ValueError("M2 must be greater than or equal to cash_outside")
    deposits_checking = total_deposits * checking_share
    deposits_savings = total_deposits * savings_share
    deposits_time = total_deposits * time_share
    return deposits_checking, deposits_savings, deposits_time


def reconstruct_banks_from_M2(
    M2: float,
    cash_outside: float,
    bank_names: List[str],
    bank_weights: List[float] = None,
    checking_share: float = 0.5,
    savings_share: float = 0.3,
    time_share: float = 0.2,
    reserve_ratio: float = 0.1,
    securities_share: float = 0.0
) -> List[Bank]:
    
    check_shares(checking_share, savings_share, time_share)

    bank_weights = normalize_weights(bank_weights)

    total_deposits = M2 - cash_outside
    if total_deposits < 0:
        raise ValueError("M2 must be greater than or equal to cash_outside")

    banks = []

    for i, bank_name in enumerate(bank_names):
        bank_deposits_total = total_deposits * bank_weights[i]

        deposits_checking = bank_deposits_total * checking_share
        deposits_savings = bank_deposits_total * savings_share
        deposits_time = bank_deposits_total * time_share
        reserves = deposits_checking * reserve_ratio
        securities = bank_deposits_total * securities_share
        loans = bank_deposits_total - reserves - securities
        if loans < 0:
            raise ValueError(f"Cannot reconstruct bank '{bank_name}': loans became negative.")
        bank = Bank(
            name=bank_name,
            reserves=reserves,
            loans=loans,
            securities=securities,
            deposits_checking=deposits_checking,
            deposits_savings=deposits_savings,
            deposits_time=deposits_time
        )
        banks.append(bank)
    return banks


def reconstruct_system_from_M2(
    M2: float,
    cash_outside: float,
    bank_names: List[str],
    bank_weights: List[float] = None,
    checking_share: float = 0.5,
    savings_share: float = 0.3,
    time_share: float = 0.2,
    reserve_ratio: float = 0.1,
    securities_share: float = 0.0
) -> BankingSystem:
    banks = reconstruct_banks_from_M2(
        M2=M2,
        cash_outside=cash_outside,
        bank_names=bank_names,
        bank_weights=bank_weights,
        checking_share=checking_share,
        savings_share=savings_share,
        time_share=time_share,
        reserve_ratio=reserve_ratio,
        securities_share=securities_share
    )

    return BankingSystem(banks=banks, cash_outside=cash_outside)