import matplotlib.pyplot as plt
from sales_analytics import get_sales_by_year

# Récupération des ventes annuelles via le module analytics
df = get_sales_by_year()

plt.figure(figsize=(10,5))
plt.plot(df["Year"], df["sales"], marker="o")
plt.title("BrightBooks – Annual Sales")
plt.xlabel("Year")
plt.ylabel("Sales (USD)")
plt.grid(True)
plt.show()
