# %%
# Librerías para manipulación y análisis de datos

import pandas as pd
import datetime
from datetime import datetime
import os
from dateutil.relativedelta import relativedelta    
from datetime import timedelta


import glob
import getpass


# %%
# Obtiene el nombre de usuario del sistema operativo actual
nombre_usuario = getpass.getuser()

# %%
# Obtiene la fecha actual
hoy = datetime.today()

# Obtiene el año actual
año = hoy.year

# Obtiene el año actual con dos dígitos
año_2 = año % 100

# Obtiene el número de mes actual
numero_mes = hoy.month

# Obtiene la fecha actual en formato YYYY-MM
fecha_n = hoy.strftime('%Y-%m')

# Obtiene la fecha actual en formato MM.YYYY
numero_mes_punto = hoy.strftime('%m.%Y')

# Obtiene la fecha de hace un mes
n_date = hoy - relativedelta(months=1)

# Obtiene la fecha de hace dos meses
n_1_date = hoy - relativedelta(months=2)

# Obtiene la fecha de hace cinco meses
n_4_date = hoy - relativedelta(months=5)

# Obtiene la fecha de hace dos meses en formato YYYY-MM
n_1 = n_1_date.strftime("%Y-%m")

# Obtiene la fecha de hace cinco meses en formato YYYY-MM
n_4 = n_4_date.strftime("%Y-%m")

# Obtiene la fecha de hace dos meses en formato MM.YYYY
n1_punto = n_1_date.strftime("%m.%Y")

# Obtiene la fecha de hace cinco meses en formato MM.YYYY
n4_punto = n_4_date.strftime("%m.%Y")

# Imprime las variables
print("n_1:", n_1)
print("n_4:", n_4)
print(n1_punto)
print(n4_punto)



# %%
# Crea una cadena con la fecha del primer día del mes anterior
n_b_fc = n_date.strftime('%Y-%m' + '-01')

# %%
#Funcion que entrega el nombre correspondiente al numero del mes
#input: numero de mes
#output: nombre de dicho mes
def obtener_nombre_mes(numero_mes):
    meses = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril",
        5: "Mayo",
        6: "Junio",
        7: "Julio",
        8: "Agosto",
        9: "Septiembre",
        10: "Octubre",
        11: "Noviembre",
        12: "Diciembre"
    }
    return meses.get(numero_mes, "Mes no válido")

# se crean variables de meses relativos a los peridos de medicion n-1 y n-4
mes_n1 = (hoy - relativedelta(months=2)).month
mes_n4 = (hoy - relativedelta(months=5)).month
ciclo_n1 = (hoy - relativedelta(months=1)).month
ciclo_n4 = (hoy - relativedelta(months=4)).month


#se obtienen nombres de dichos meses
nombre_mes_n1 = obtener_nombre_mes(mes_n1)
nombre_mes_n4 = obtener_nombre_mes(mes_n4)
nombre_ciclo_n1 = obtener_nombre_mes(ciclo_n1)
nombre_ciclo_n4 = obtener_nombre_mes(ciclo_n4)
nombre_numero_mes = obtener_nombre_mes(numero_mes)


# Imprimir el nombre del mes anterior
print(nombre_mes_n1)
print(nombre_mes_n4)


# %%
#Se especifican las rutas de los archivos de forecast para los ciclos n-1 y n-4
ruta_n1 = f'C:/Users/{nombre_usuario}/Inchcape/Planificación y Compras Chile - Documentos/Planificación y Compras OEM/Demanda/Forecast Inbound/{n_1[:4]}/{n_1} {nombre_mes_n1}/{n1_punto} S&OP Demanda Sin Restricciones OEM_Inbound.xlsx'
ruta_n4 = f'C:/Users/{nombre_usuario}/Inchcape/Planificación y Compras Chile - Documentos/Planificación y Compras OEM/Demanda/Forecast Inbound/{n_4[:4]}/{n_4} {nombre_mes_n4}/{n4_punto} S&OP Demanda Sin Restricciones OEM_Inbound.xlsx'
print(f'Archivo de FC n-1: {ruta_n1}'+ '\n' + f'Archivo de FC n-4: {ruta_n4}')
#se leen los archivos con pandas

df_n1 = pd.read_excel(ruta_n1, sheet_name= 'Base Forecast',header=2)
df_n4 = pd.read_excel(ruta_n4, sheet_name='Base Forecast', header=2)

# %%
df_n1['Input'].value_counts()

# %%
#localizacion de el archivo de codigo actual para las cadenas de reemplazo
maestro = f"C:/Users/{nombre_usuario}/Inchcape/Planificación y Compras Chile - Documentos/Planificación y Compras Maestros"
dir_maestro = os.listdir(maestro)
for c_año in dir_maestro:
    if str(hoy.year) in c_año:
        c_carpeta = os.path.join(maestro, c_año)
        c_mes = os.listdir(c_carpeta)
        c_arch = os.path.join(c_carpeta, c_mes[-1])
        archivos = os.listdir(c_arch)
        print(archivos)
        for a in archivos:
            if 'COD_ACTUAL_R3' in a:
                ruta_cad = os.path.join(c_arch, a)
                cadena_de_remplazo = pd.read_excel(ruta_cad, usecols= ['Nro_pieza_fabricante_1',	'Cod_Actual_1'] )

# %%
#se genera ruta del archivo de ventas y se lee dicha ruta con pandas
ruta_ventas = f"C:/Users/{nombre_usuario}/Inchcape/Planificación y Compras Chile - Documentos/Planificación y Compras OEM/Demanda/S&OP/{fecha_n[:4]}/{fecha_n}/OEM/{numero_mes_punto} BaseVentaOEM Sell In PBI.xlsx"
df_ventas= pd.read_excel(ruta_ventas, sheet_name='Base Venta Sell In OEM', header=2)
print(f'Ruta archivo ventas: {ruta_ventas}')

# se lee una version auxiliar del archivo de ventas para obtener la 

df_ventas_p= pd.read_excel(ruta_ventas, sheet_name='TD BV', header=3)
df_ventas_p = df_ventas_p[['Último Eslabón', 'Prom.']]

# %%
ruta_ventas

# %%
df_n1['Material R3'] = df_n1['Material R3'].astype('str')
df_n1 = pd.merge(df_n1,cadena_de_remplazo, left_on='Material R3', right_on='Nro_pieza_fabricante_1', how='left')

# # #df_n1 = df_n1.drop(['Cod_Actual_1','Nro_pieza_fabricante_1','Cod_Actual_1_UE2','Nro_pieza_fabricante_1_UE2','Cod_Actual_1_Cod_Actual_1', 'Nro_pieza_fabricante_1_Cod_Actual_1'], axis=1)
# # #df_n4['Ult. Eslabón'] = df_n4['Ult. Eslabón'].astype('str')
#df_n4 = pd.merge(df_n4,cadena_de_remplazo, left_on='Material R3', right_on='Nro_pieza_fabricante_1', how='left')



# %%
df_n4['Material R3'] = df_n4['Material R3'].astype('str')
df_n4 = pd.merge(df_n4,cadena_de_remplazo, left_on='Material R3', right_on='Nro_pieza_fabricante_1', how='left')

# %%
df_n1['Cod_Actual_1'] = df_n1['Cod_Actual_1'].fillna(df_n1['Material R3'])

df_n4['Cod_Actual_1'] = df_n4['Cod_Actual_1'].fillna(df_n4['Material R3'])


# %%
df_n1 = df_n1.drop('Nro_pieza_fabricante_1', axis=1)

df_n4 = df_n4.drop('Nro_pieza_fabricante_1', axis=1)

# %%
df_n1 = df_n1.rename(columns = {'Cod_Actual_1': 'UE_2'})
df_n4 = df_n4.rename(columns = {'Cod_Actual_1': 'UE_2'})

# %%
df_n4

# %%
fecha_fc_n1 = datetime.strptime(n_1, '%Y-%m')
n_1_date = fecha_fc_n1 + relativedelta(months=1)
fecha_fc_n4 = datetime.strptime(n_4, '%Y-%m')
n_4_date = fecha_fc_n4 + relativedelta(months=4)

busqueda_fc_n1_anas =  f'{n_b_fc} 00:00:00.2'
busqueda_fc_n4_anas =  f'{n_b_fc} 00:00:00.1'





desired_column_index = 74  # El índice 57 corresponde a la columna número 58
desired_column_index_2 = 77  # El índice 57 corresponde a la columna número 58

# Accede a la columna por su índice
desired_column = df_n1.iloc[:, desired_column_index]
desired_column_n4 = df_n4.iloc[:, desired_column_index_2]


df_n1['fc_anas'] = desired_column
df_n4['fc_anas'] = desired_column_n4
df_n4['fc_anas'].sum()






# %%
busqueda_fc_n1 = f'{n_b_fc} 00:00:00.2'
busqueda_fc_n4 = f'{n_b_fc} 00:00:00.2' 




#COMPROBACION DE FECHAS
# df_n1[busqueda_fc_n1].sum()
df_n1['fc'] = df_n1[busqueda_fc_n1]
df_n4['fc'] = df_n4[busqueda_fc_n4]
df_n1['fc'].sum()



# %%
df_n4['fc'].sum()

# %%
df_n1['fc'].sum()

# %%
df_n1['ID2'] = df_n1['UE_2'] + df_n1['Canal']
df_n4['ID2'] = df_n4['UE_2'] + df_n4['Canal']

# %%
df_n1['fc'].sum()

# %%
df_n1['Periodo'] = 'N-1'
df_n4['Periodo'] = 'N-4'

# %%
df_n4.head()

# %%
df_consolidado = pd.concat([df_n1,df_n4], ignore_index=True)

# %%
df_consolidado

# %%
cols = ['ID2', 'UE_2', 'fc_anas','fc', 'Periodo','Costo Promedio Ponderado', 'Input']


# %%
df_consolidado_red = df_consolidado[cols]

# %%
df_consolidado_red['fc_anas'].sum()

# %%
df_consolidado_red = df_consolidado_red.sort_values(by='Input', ascending=True)

# %%
df_consolidado_red.shape

# %%
df_consolidado_red = df_consolidado_red.groupby(['ID2', 'Periodo']).agg({'UE_2':'first', 'fc': 'sum', 'fc_anas':'sum', 'Costo Promedio Ponderado': 'sum', 'Input':'first'}).reset_index()

# %%
indice_deseado = 24 # El índice 57 corresponde a la columna número 58


# Accede a la columna por su índice
col_deseada = df_ventas.iloc[:, indice_deseado]

# %%
df_ventas['Venta'] = col_deseada
df_ventas['Ventas UMB'] = df_ventas['Prom. VtaR']
red_columnas = ['ID V2','Último Eslabón', 'Venta', 'Ventas UMB']
df_ventas = df_ventas[red_columnas]

# %%
df_ventas['Venta'].sum()

# %%
#df_venta_prom = df_ventas[['Último Eslabón', 'Ventas UMB']].groupby('Último Eslabón')['Ventas UMB'].sum().reset_index()

# %%
#df_venta_prom['Venta'].sum()

# %%
df_ventas = df_ventas.groupby(['ID V2']).agg({'Venta': sum}).reset_index()

# %%
df_ventas['Venta'].sum()

# %%
df_ventas_p

# %%
df_ventas_p.columns

# %%
df_ventas

# %%
consolidado_cruce_ventas = pd.merge(df_consolidado_red, df_ventas, left_on='ID2', right_on='ID V2', how='left')
consolidado_cruce_ventas = consolidado_cruce_ventas.merge(df_ventas_p, left_on='UE_2', right_on='Último Eslabón', how='left')


# %%
consolidado_cruce_ventas['Venta'].sum()

# %%
consolidado_cruce_ventas = consolidado_cruce_ventas.drop(['Último Eslabón'], axis=1)
consolidado_cruce_ventas = consolidado_cruce_ventas.drop(['ID V2'], axis=1)

# %%


# %%
consolidado_cruce_ventas

# %%
columnas_eliminar = ['Último Eslabón_x','Ventas UMB_x','Último Eslabón_y']

# %%
consolidado_cruce_ventas

# %%
#consolidado_final_prom_ventas = pd.merge(consolidado_cruce_ventas, df_ventas, left_on='UE_2', right_on='Cod_Actual_1', how='left')

# %%
consolidado_cruce_ventas

# %%
#consolidado_cruce_ventas = consolidado_cruce_ventas.rename(columns={'Ventas UMB_y': 'Ventas UMB'})
#consolidado_cruce_ventas['Ventas UMB'] = consolidado_cruce_ventas['Ventas UMB']/4

# %%
fecha_n

# %%
ciclo_n1

# %%


# %%
carpeta_tubo = f"c:/Users/{nombre_usuario}/Inchcape/Planificación y Compras Chile - Documentos/Planificación y Compras KPI-Reportes/Tubo Semanal"
fecha_actual = datetime.today()

# Calcular la fecha del mes anterior
fecha_mes_anterior = fecha_actual - timedelta(days=fecha_actual.day)

# Formatear la fecha en "yyyy-mm"
fecha_formateada = fecha_mes_anterior.strftime('%Y-%m')
dtype_stock ={
    'Material SAP': str,
    'UE': str,
}


# Imprimir la fecha formateada
contador = 1  # Inicializa un contador para los nombres de los DataFrames


tubo = os.listdir(carpeta_tubo)
for i in tubo:

    if i[5:7] == fecha_formateada[5:8] and i[0:4] == fecha_formateada[0:4]:
        
        
        carpeta = os.listdir(os.path.join(carpeta_tubo, i))
        for a in carpeta:
            if 'tock' in a and not 'iendas' in a and not 'añol' in a and not 'entros' in a and 'R3' in a:
               
                arch = os.path.join(carpeta_tubo, i, a)
                print(arch)
            

                df = pd.read_excel(arch, sheet_name='Sheet1', usecols=['Ult. Eslabon', 'Libre utilización','Ce.'], dtype = {'Ce.' : 'str'})
                df_suma = df.groupby('Ult. Eslabon', as_index=False).agg({'Libre utilización': 'sum'})

                df_ue = pd.merge(df_suma, cadena_de_remplazo, left_on='Ult. Eslabon', right_on='Nro_pieza_fabricante_1', how='left', suffixes=('Cod_Actual_1', '_Cad_reemplazo'))
                df_ue.drop('Nro_pieza_fabricante_1', axis=1, inplace=True)
                df_ue['Cod_Actual_1'].fillna(df_ue['Ult. Eslabon'], inplace=True)
                df_ue.drop('Ult. Eslabon', axis=1, inplace=True)
                df_suma = df_ue.groupby(['Cod_Actual_1']).agg({'Libre utilización': 'sum'}).reset_index()
                df_suma = df_suma.rename(columns = {'Libre utilización': f'Stock SEM {datetime.strptime(a[:10], '%Y-%m-%d').isocalendar()[1]}', 'Cod_Actual_1':f'Cod_Actual{a[:10]}'})

                suffix = f'_{i}' if i == (len(tubo) - 2) else f'_{i}a'  # Añadir sufijo para la primera fusión
                consolidado_cruce_ventas = consolidado_cruce_ventas.merge(df_suma, left_on='UE_2', right_on=f'Cod_Actual{a[:10]}', how='left')
               
#         



# %%
consolidado_cruce_ventas = consolidado_cruce_ventas.fillna(0)
columns_to_drop = consolidado_cruce_ventas.filter(like='Cod_Actual').columns
consolidado_cruce_ventas = consolidado_cruce_ventas.drop(columns=columns_to_drop)

# %%
semanas_habiles_por_mes = {
    '2023-10': 5,
    '2023-11': 4,
    '2023-12': 4,
    '2024-01': 5,
    '2024-02': 4,
    '2024-03': 4,
    '2024-04': 4,
    '2024-05': 5,
    '2024-06': 5,
    '2024-07': 5,
    '2024-08': 4,
    '2024-09': 4,
    '2024-10': 4,
    '2024-11': 4,
    '2024-12': 4,
    '2025-01': 4,
    '2025-02': 4,
    '2025-03': 4,
    '2025-04': 4,
    '2025-05': 4,
    '2025-06': 4,
    '2025-07': 5,
    '2025-08': 4,
    '2025-09': 4,
    '2025-10': 4,
    '2025-11': 4,
    '2025-12': 4
}

# %%
consolidado_cruce_ventas['Venta'] = consolidado_cruce_ventas['Venta'].apply(lambda x: x if x >= 0 else 0)


consolidado_cruce_ventas['Prom.'] = consolidado_cruce_ventas['Prom.'].apply(lambda x: x if x >= 0 else 0)
#consolidado_cruce_ventas['Prom.'] = consolidado_cruce_ventas['Prom.']/4
consolidado_cruce_ventas['Prom.'] = consolidado_cruce_ventas.apply(
    lambda row: row['Prom.'] / semanas_habiles_por_mes.get(fecha_formateada, 1),
    axis=1
)

# %%
for column in consolidado_cruce_ventas.columns:
    if 'Stock' in column:
        new_column_name = f'INSTOCK_{column[-2:]}'
        consolidado_cruce_ventas[new_column_name] = consolidado_cruce_ventas.apply(lambda row: 1 if row['Prom.'] < row[column] else 0, axis=1)


# %%
consolidado_cruce_ventas['Total instock'] = consolidado_cruce_ventas.filter(like='INSTOCK').sum(axis=1)


# %%
consolidado_cruce_ventas['MAPE_AJUSTADO'] = abs(consolidado_cruce_ventas['Venta'] - consolidado_cruce_ventas['fc'])
consolidado_cruce_ventas['ERP'] = consolidado_cruce_ventas.apply(lambda row: row['fc'] - row['Venta'] if row['fc'] > row['Venta'] else 0, axis=1)
consolidado_cruce_ventas['ERN'] = consolidado_cruce_ventas.apply(lambda row: row['Venta'] - row['fc'] if row['Venta'] > row['fc'] else 0, axis=1)
consolidado_cruce_ventas['MAPE_ANASTASIA'] = abs(consolidado_cruce_ventas['Venta'] - consolidado_cruce_ventas['fc_anas'])
consolidado_cruce_ventas['ERP_ANASTASIA'] = consolidado_cruce_ventas.apply(lambda row: row['fc_anas'] - row['Venta'] if row['fc_anas'] > row['Venta'] else 0, axis=1)
consolidado_cruce_ventas['ERN_ANASTASIA'] = consolidado_cruce_ventas.apply(lambda row: row['Venta'] - row['fc_anas'] if row['Venta'] > row['fc_anas'] else 0, axis=1)


# %%


# %%


# %%
consolidado_cruce_ventas['WMAPE'] = consolidado_cruce_ventas['MAPE_AJUSTADO'] / consolidado_cruce_ventas['Venta']
consolidado_cruce_ventas['WMAPE.1'] = consolidado_cruce_ventas['MAPE_ANASTASIA'] / consolidado_cruce_ventas['Venta']
consolidado_cruce_ventas['Mes'] = hoy.strftime('%Y-%m-%d')
consolidado_cruce_ventas['Costo de Venta'] = consolidado_cruce_ventas['Costo Promedio Ponderado'] * consolidado_cruce_ventas['Venta']
consolidado_cruce_ventas['Forecast en Costo'] = consolidado_cruce_ventas['Costo Promedio Ponderado'] * consolidado_cruce_ventas['fc']
consolidado_cruce_ventas['MAPE Costo']  = abs(consolidado_cruce_ventas['Costo de Venta'] - consolidado_cruce_ventas['Forecast en Costo'])
consolidado_cruce_ventas['ERP Costo'] = consolidado_cruce_ventas.apply(lambda row: row['Forecast en Costo'] - row['Costo de Venta'] if row['Forecast en Costo'] > row['Costo de Venta'] else 0, axis=1)
consolidado_cruce_ventas['ERN Costo'] = consolidado_cruce_ventas.apply(lambda row: row['Costo de Venta'] - row['Forecast en Costo'] if row['Costo de Venta'] > row['Forecast en Costo'] else 0, axis=1)
consolidado_cruce_ventas['WMAPE Costo'] = consolidado_cruce_ventas['MAPE Costo'] / consolidado_cruce_ventas['Costo de Venta']

# %%
consolidado_cruce_ventas = consolidado_cruce_ventas[['ID2', 'Periodo', 'UE_2', 'fc', 'fc_anas',
       'Venta', 'Prom.', 'Total instock', 'MAPE_AJUSTADO', 'ERP',
       'ERN', 'MAPE_ANASTASIA', 'ERP_ANASTASIA', 'ERN_ANASTASIA', 'WMAPE',
       'WMAPE.1', 'Mes', 'Costo Promedio Ponderado', 'Costo de Venta', 'Forecast en Costo', 'MAPE Costo',
       'ERP Costo', 'ERN Costo', 'WMAPE Costo', 'Input']]

# %%
consolidado_cruce_ventas.to_excel(f'C:/Users/{nombre_usuario}/Inchcape/Planificación y Compras Chile - Documentos/Planificación y Compras KPI-Reportes/Forecast Error (Python)/OEM/Base Forecast Error/Forecast Error OEM {nombre_numero_mes} {año}.xlsx', index=False)


# %%
f'C:/Users/{nombre_usuario}/Inchcape/Planificación y Compras Chile - Documentos/Planificación y Compras KPI-Reportes/Forecast Error (Python)/OEM/Base Forecast Error/Forecast Error OEM {nombre_numero_mes} {año}'

# %%
import easygui as eg
print(f'Total fc n_1: {df_n1['fc'].sum()}' + '\n' + 
f'Total fc IA n_1: {df_n1['fc_anas'].sum()}' + '\n' + 
f'Total fc n_4: {df_n4['fc'].sum()}' + '\n' + 
f'Total fc IA n_4: {df_n4['fc_anas'].sum()}' + '\n' + 
f'Total Venta: {df_ventas['Venta'].sum()}')

# %%
eg.msgbox('Base de Forecast Error OEM Construida', 'TAREA FINALIZADA!', 'OK')

# %%
df_n4['fc_anas'].sum()

# %%
df_n4['fc'].sum()

# %%


# %%



