import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from scipy.signal import savgol_filter
from scipy.fft import fft, fftfreq
from scipy.signal import hilbert


def test_fft(sig_1,sig_2,cas1): # (a, b, 350e-9)

    N = len(sig_1)
    yf1 = 2.0/N * np.abs(fft(sig_1)[0:N//2])
    xf1 = fftfreq(N, cas1)[:N//2]

    yf2 = 2.0/N * np.abs(fft(sig_2)[0:N//2])
    xf2 = fftfreq(N, cas1)[:N//2]

    return(xf1, yf1, xf2, yf2)


def test_amp(sig_1, sig_2,window_size,jmeno): # (a, b, 83,"ab")

    lim_min, lim_max = 0.75, 1.2
    rel_differences, match_conditions, con_v_1, con_v_2, vpp_l1, vpp_l2, X, q = [],[],[],[],[],[],[],0

    for i in range(0, len(sig_1), window_size):
        X.append(i)
        chunk_1 = sig_1[i:i+window_size]
        chunk_2 = sig_2[i:i+window_size]
        if len(chunk_1) < window_size: break # Konec dat
        
        vpp_1 = np.ptp(chunk_1)
        vpp_2 = np.ptp(chunk_2)

        vpp_l1.append(vpp_1)
        vpp_l2.append(vpp_2)
        
        cond_vpp_1 = lim_min <= vpp_1 <= lim_max
        cond_vpp_2 = lim_min <= vpp_2 <= lim_max
        
        relative_difference = abs(vpp_1 - vpp_2) / vpp_1
        cond_amplitude_match = relative_difference <= 0.10
        
        # 2. Uložení hodnot z aktuálního okna
        rel_differences.append(relative_difference)
        match_conditions.append(cond_amplitude_match)
        
        # Vypíšeme chyby průběžně, pokud signál nesplňuje normu Vpp
        if not cond_vpp_1 and q < 5:
            print(f"Vpp Signálu {jmeno[0]} mimo normu: {vpp_1:.3f} V")
            con_v_1.append(False)
            q+=1
        if not cond_vpp_2 and q < 5:
            print(f"Vpp Signálu {jmeno[1]} mimo normu: {vpp_2:.3f} V")
            con_v_2.append(False)
            q+=1
    if q == 5:
            print("...")
    if q == 0:
        print("Vpp OK")
    print()
    # 3. Převod na NumPy arrays
    arr_diff = np.array(rel_differences) * 100  # převod na procenta rovnou
    arr_match = np.array(match_conditions)

    # 4. Výpočet statistik
    mean_diff = np.mean(arr_diff)
    min_diff = np.min(arr_diff)
    max_diff = np.max(arr_diff)

    mean_vpp_l1 = np.mean(vpp_l1)
    min_vpp_l1 = np.min(vpp_l1)
    max_vpp_l1 = np.max(vpp_l1)
    
    mean_vpp_l2 = np.mean(vpp_l2)
    min_vpp_l2 = np.min(vpp_l2)
    max_vpp_l2 = np.max(vpp_l2)

    all_matched = "OK" if np.all(arr_match) and np.all(cond_vpp_1) and np.all(cond_vpp_2) else "NOK"

    # Definice šablony pro řádek: první sloupec 12 znaků, ostatní 15 znaků
    row_format = "{:<12} {:<15} {:<15} {:<15}"

    # Vypsání hlavičky
    print(row_format.format("Měření:", "Rel. rozdíl", f"Amp. sig_{jmeno[0]}", f"Amp. sig_{jmeno[1]}"))
    print("-" * 57) # Oddělovací čára

    # Vypsání dat
    print(row_format.format("Mean", f"{mean_diff:.2f} %", f"{mean_vpp_l1:.2f} V", f"{mean_vpp_l2:.2f} V"))
    print(row_format.format("Min", f"{min_diff:.2f} %", f"{min_vpp_l1:.2f} V", f"{min_vpp_l2:.2f} V"))
    print(row_format.format("Max", f"{max_diff:.2f} %", f"{max_vpp_l1:.2f} V", f"{max_vpp_l2:.2f} V"))
    print("=" * 57) # Oddělovací čára
    print(f"Vyhodnoceni: {all_matched}\n")

    polomer = np.sqrt(sig_1**2+sig_2**2)

    return(polomer)

def test_fi(sig_1,sig_2,velikost_okna): #(a ,b, 83)


    kolisavy_offset_1 = pd.Series(sig_1).rolling(window=velikost_okna, center=True, min_periods=1).mean().to_numpy()
    kolisavy_offset_2 = pd.Series(sig_2).rolling(window=velikost_okna, center=True, min_periods=1).mean().to_numpy()

    S1 = sig_1 - kolisavy_offset_1 
    S2 = sig_2 - kolisavy_offset_2

    S1_vyhl = savgol_filter(S1, window_length=15, polyorder=2)
    S2_vyhl = savgol_filter(S2, window_length=15, polyorder=2)

    trend1 = np.convolve(S1_vyhl, np.ones(velikost_okna)/velikost_okna, mode='same')
    signal_kolem_nuly1 = S1_vyhl - trend1

    analyticky_signal = hilbert(signal_kolem_nuly1)
    okamzita_obalka = np.abs(analyticky_signal)

    vyrovnany_signal_1 = signal_kolem_nuly1 / okamzita_obalka

    trend2 = np.convolve(S2_vyhl, np.ones(velikost_okna)/velikost_okna, mode='same')
    signal_kolem_nuly2 = S2_vyhl - trend2

    analyticky_signal2 = hilbert(signal_kolem_nuly2)
    okamzita_obalka2 = np.abs(analyticky_signal2)

    vyrovnany_signal_2 = signal_kolem_nuly2 / okamzita_obalka2

    pocet_oken = len(vyrovnany_signal_1) // velikost_okna

    vysledne_faze = np.zeros(pocet_oken)

    def spocitej_fazi_fft(signal, reference):
        fft_sig = np.fft.fft(signal)
        fft_ref = np.fft.fft(reference)

        # Najdeme index nejvyšší harmonické (vynecháme DC složku na indexu 0)
        idx = np.argmax(np.abs(fft_sig[1:])) + 1

        # Spočítáme fázi v radiánech
        faze_sig = np.angle(fft_sig[idx])
        faze_ref = np.angle(fft_ref[idx])

        # Rozdíl fází převedený na stupně
        rozdil_fazi_rad = faze_sig - faze_ref
        rozdil_fazi_deg = np.degrees(rozdil_fazi_rad)

        # Normalizace do rozsahu -180 až 180 stupňů
        return (rozdil_fazi_deg + 180) % 360 - 180

    # For loop procházející data po 83 vzorcích
    for i in range(pocet_oken):
        start = i * velikost_okna
        konec = start + velikost_okna
        # Výřez (okno) dat
        okno_sig = vyrovnany_signal_1[start:konec]
        okno_ref = vyrovnany_signal_2[start:konec]

        # Výpočet fáze (zvolte metodu 1 nebo 2)
        vysledne_faze[i] = spocitej_fazi_fft(okno_sig, okno_ref)

    print(f"{np.min(vysledne_faze[1:]):.2f} {np.mean(vysledne_faze[1:]):.2f} {np.max(vysledne_faze[1:]):.2f}")

    #print(f"plot(t[::{velikost_okna}],y)")

    return(vysledne_faze)