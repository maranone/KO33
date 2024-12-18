from file_to_variable import file_to_variable
import datetime
from collections import defaultdict
import pandas as pd
# Variables for storing data and totals
TotalArticulos = [0]
Articulos = []
TotalVentas = [0]
Ventas = []
TotalClientes = [0]
Clientes = []

# File paths
curyearmonth = input("Please enter the year and month in 'YYMM' format (e.g., '2411' for November 2024): ")


# Call the function to load data from files
file_base = f"c:\\Estancos\\csv\\49"
file_to_variable(f"{file_base}_articulos.csv", TotalArticulos, Articulos)
file_to_variable(f"{file_base}_ventas.csv", TotalVentas, Ventas)
file_to_variable(f"{file_base}_clientes.csv", TotalClientes, Clientes)

file_base = f"c:\\Estancos\\csv\\53"
file_to_variable(f"{file_base}_articulos.csv", TotalArticulos, Articulos)
file_to_variable(f"{file_base}_ventas.csv", TotalVentas, Ventas)
file_to_variable(f"{file_base}_clientes.csv", TotalClientes, Clientes)


# Print out the results to check
print(f"Articulos: {TotalArticulos[0]} items loaded")
print(f"Ventas: {TotalVentas[0]} items loaded")
print(f"Clientes: {TotalClientes[0]} items loaded")

# Assuming `Ventas` and `Articulos` are lists already loaded with data
Ventas2 = []
Articulos2 = []
from tqdm import tqdm
current_year = datetime.datetime.now().year
current_year_last_two_digits = int(str(current_year)[2:])-1
counter = 0

with tqdm(Ventas, desc="Processing Ventas") as pbar:
    for venta in pbar:
        b = venta.split(";")  # Split the Venta string into a list by ';'
        b = [x.replace('"', '') for x in b]  
        if f"{b[3][6:8]}{b[3][0:2]}" == curyearmonth:
            if b[8] != "":
                if b[23].strip()[:3].upper() == 'TA1':
                    Ventas2.append(f'{b[3][6:8]}{b[3][0:2]};{b[8]};{b[15]};{b[17]}')
                    counter += 1
                    pbar.set_postfix({"Appended": counter})


counter = 0

with tqdm(Articulos, desc="Processing Articulos") as pbar:               
    for articulo in pbar:
        b = articulo.split(";")
        b = [x.replace('"', '') for x in b]
        if b[3][:3].strip().upper() == 'TA1':
            Articulos2.append(f"{b[0]};{b[3]};{b[4]};{b[6]}")
            counter += 1
            pbar.set_postfix({"Appended": counter})
        elif b[2][:3].strip().upper() == 'TA1':
            Articulos2.append(f"{b[0]};{b[2]};{b[3]};{b[59]}")
            counter += 1
            pbar.set_postfix({"Appended": counter})


Articulos2.sort()
Ventas2.sort()
Ventas3 = []

counter = 0
with tqdm(Ventas2, desc="Processing Ventas2 with Articulos") as pbar:
    for venta in pbar:
        a = venta.split(";")
        for articulo in Articulos2:
            b = articulo.split(";")
            if a[2] == b[0]:
                if b[3].upper() == "ALTADIS" or b[3].upper() == "IMPERIAL":
                    Ventas3.append(f'{a[0]};{a[1]};{b[1]};{b[2]};{a[3]}')
                    counter += 1
                    pbar.set_postfix({"Appended": counter})
                else:
                    Ventas3.append(f'{a[0]};{a[1]};{b[1]};-;{a[3]}')

Bares = []
counter = 0
with tqdm(Clientes, desc="Processing Clientes") as pbar:
    for client in pbar:
        a = client.split(";")
        a = [x.replace('"', '') for x in a]
        Bares.append(f'{a[0]};{a[1]}')



Ventas4 = []
Ventas4.append(f'Mes;Bar;Descripcion;TRubio;TNegro;Tliar')
counter = 0


totals_prod = defaultdict(int)
totals = defaultdict(int)
totals_by_bar = defaultdict(lambda: defaultdict(int))  # Nested defaultdict to hold totals for each bar
Ventas4 = []
totals_ventas = 0
counter = 0
bar_mapping = {bare.split(";")[0]: bare.split(";")[1] for bare in Bares}

Ventas4.append(f"Mes;Bar;Producto;Cdad;TRubio;TNegro;TLiar")

with tqdm(Ventas3, desc="Processing Ventas3 with Bares") as pbar:
    for venta in pbar:
        a = venta.split(";")
        a = [x.replace('"', '') for x in a]  # Clean up quotes
        curmonth, bar, curprod, curtype, amount = a[0], a[1], a[3], a[2], int(a[4])
        bar2 = bar_mapping.get(bar, "")  # Get the bar2 value from the bar_mapping
        
        # Accumulate totals for the product (per bar)
        totals_prod[(bar, curprod)] += amount
        
        # Update the totals for the current type
        if curtype.upper() == "TA1CR1":
            totals_by_bar[bar]["TA1CR1"] += amount
        elif curtype.upper() == "TA1CN1":
            totals_by_bar[bar]["TA1CN1"] += amount
        elif curtype.upper() == "TA1TL1":
            totals_by_bar[bar]["TA1TL1"] += amount
        
        totals_ventas += amount  # Total sales across all entries
        
        # Update progress bar
        counter += 1
        pbar.set_postfix({"Appended": counter})

    # After processing all ventas, append totals for each product and bar combination
    for (bar, curprod), prod_total in totals_prod.items():
        if prod_total != 0:
            # Append the total for the product per bar
            bar2 = bar_mapping.get(bar, "")
            Ventas4.append(f'{curmonth};{bar2};{curprod};{prod_total}')
    
    # After processing all ventas, append totals for each bar and its types
    for bar, bar_totals in totals_by_bar.items():
        if bar:  # Ensure the bar is not empty
            bar2 = bar_mapping.get(bar, "")
            Ventas4.append(f'{curmonth};{bar2};Totales;{bar_totals["TA1CR1"]};{bar_totals["TA1CN1"]};{bar_totals["TA1TL1"]}')

data = [row.split(';') for row in Ventas4]

# Create a DataFrame from the list of data
df = pd.DataFrame(data)

# Define the path where the file will be saved
file_path = r"C:\stock\altadis.xlsx"

# Save the DataFrame to an Excel file
df.to_excel(file_path, index=False, header=False)