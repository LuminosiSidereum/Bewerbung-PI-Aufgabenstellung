import pandas as pd #type: ignore
import matplotlib.pyplot as plt #type: ignore
import numpy as np

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
    plt.tight_layout()
    #plt.show()
    plt.savefig(f"{title}.png", format='png', dpi=300)  # PNG speichern
    plt.close()

def plot_bar_stellweg():
    
    plt.figure(figsize=(10,6))
    
    groups = df["Group"].unique()
    x = np.arange(len(groups))  # Positionen für die Gruppen
    width = 0.2  # Balkenbreite
    
    # Alle L-Werte sortieren
    L_values = sorted(df["L"].unique())
    
    for i, L_val in enumerate(L_values):
        subset = df[df["L"] == L_val]
        # Werte für jede Gruppe passend anordnen
        heights = [subset[subset["Group"] == g]["Nominalstellweg [µm]"].values[0] 
                   if g in subset["Group"].values else 0 
                   for g in groups]
        
        errors = [subset[subset["Group"] == g]["Nominalstellweg [µm]"].values[0] * 
                  subset[subset["Group"] == g]["Nominalstellweg Abweichung [%]"].values[0] / 100
                  if g in subset["Group"].values else 0
                  for g in groups]
        
        plt.bar(x + i*width, heights, width, label=f"{L_val} mm", yerr=errors, capsize=4)
    
    plt.xticks(x + width*(len(L_values)-1)/2, groups)
    plt.ylabel("Stellweg [µm]")
    plt.xlabel("Abmessung A×B [mm]")
    #plt.title("Nominalstellweg gruppiert nach Abmessungen A×B und Länge L")
    plt.legend(loc= "upper left",title="Länge")
    plt.grid(True, linestyle="--", axis="y", alpha=0.6)
    plt.tight_layout()
    plt.savefig(f"Stellweg-Balkendiagramm.png", format='png', dpi=300)  # PNG speichern
    plt.close()
    #plt.show()

# a) Blockierkraft
plot_with_error("Blockierkraft [N]", "Blockierkraft Abweichung [%]", "Blockierkraft [N]", "Blockierkraft vs. L")

# b) Stellweg (Nominalstellweg als Basis)
plot_with_error("Nominalstellweg [µm]", "Nominalstellweg Abweichung [%]", "Stellweg [µm]", "Nominalstellweg vs. L")
plot_bar_stellweg()

# c) Kapazität
plot_with_error("elektrische Kapazität [µF]", "Kapazität Abweichung [%]", "elektrische Kapazität [µF]", "Kapazität vs. L")
