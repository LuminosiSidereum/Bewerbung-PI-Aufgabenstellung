import pandas as pd #type: ignore
import matplotlib.pyplot as plt #type: ignore

# CSV einlesen
df = pd.read_csv("picma_linearaktoren.csv")

# Abmessung A×B als Gruppierung
df["Group"] = df["A"].astype(str) + "x" + df["B"].astype(str)

# Plot-Funktion für verschiedene Y-Werte
def plot_with_error(y_col, y_err_col, ylabel, title):
    plt.figure(figsize=(8,6))
    
    for key, group in df.groupby("Group"):
        plt.errorbar(
            group["L"], 
            group[y_col], 
            yerr=group[y_col] * group[y_err_col] / 100,
            fmt="o--", 
            label=f"{key} mm"
        )
    
    plt.xlabel("Länge L [mm]")
    plt.ylabel(ylabel)
    #plt.title(title)
    plt.legend(loc="upper left", title="Abmessung A×B")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.show()

# a) Blockierkraft
plot_with_error("Blockierkraft [N]", "Blockierkraft Abweichung [%]", "Blockierkraft [N]", "Blockierkraft vs. L")

# b) Stellweg (Nominalstellweg als Basis)
plot_with_error("Nominalstellweg [µm]", "Nominalstellweg Abweichung [%]", "Stellweg [µm]", "Nominalstellweg vs. L")

# c) Kapazität
plot_with_error("Kapazität [µF]", "Kapazität Abweichung [%]", "Kapazität [µF]", "Kapazität vs. L")
