import matplotlib.pyplot as plt
import pandas as pd
tabla = pd.read_csv('test.csv')
xidas = tabla['dias']
ydescuento  = tabla['descuento']
plt.plot(xidas,ydescuento,)
plt.title('predicciones')
plt.show()