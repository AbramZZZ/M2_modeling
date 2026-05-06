from decompose_m2 import reconstruct_system_from_M2

system = reconstruct_system_from_M2(
    M2=1000,
    cash_outside=120,
    bank_names=["Bank A", "Bank B"],
    bank_weights=[0.6, 0.4],
    checking_share=0.5,
    savings_share=0.3,
    time_share=0.2,
    reserve_ratio=0.1,
    securities_share=0.0
)

print(system)
print("M0:", system.compute_M0())
print("M1:", system.compute_M1())
print("M2:", system.compute_M2())

for bank in system.banks:
    print(bank.name, bank.check_balance())