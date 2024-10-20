def real_to_float(real: str) -> float:
    real = real.replace('R$', '')
    real = real.replace('.', '')
    real = real.replace(' ', '')
    real = real.replace(',', '.')
    return float(real)
