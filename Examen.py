
import math
import numpy as np

depreciacion_anios = {}

def obtener_valores():
    
    empresas = {}
    print('Empieze introduciendo el nombre de las propuestas')
    print('cuando termine introdusca la palabra listo')

    while True:

        empresa = input('Dame el nombre de la empresa ')

        if empresa == 'listo':
            break

        empresas[empresa] = {}

    obtener_numeros(empresas)



def obtener_numeros(empresas):

    for empresa in empresas:
        
        valor = float(input(f'Dame el valor de la empresa {empresa}'))
        gastos_instalacion = float(input(f'Dame los gastos de instalacion de la {empresa}'))
        valor_residual = float(input(f'Dame el valor residual de la {empresa}'))
        vida_util = float(input(f'Dame la vida util de la {empresa}'))
        anios_depreciacion = float(input(f'Dame los aanios de depreciacion de la {empresa}'))
       
        empresas[empresa]['valor'] = valor
        empresas[empresa]['gastos_instalacion'] = gastos_instalacion  
        empresas[empresa]['valor_residual'] = valor_residual
        empresas[empresa]['vida_util'] = vida_util
        empresas[empresa]['anios_depreciacion'] = anios_depreciacion
        
    primeros_calculos(empresas)
    

def primeros_calculos(empresas):

    valor_libros = 0

    for empresa in empresas:
        
        total = empresas[empresa]['valor'] + empresas[empresa]['gastos_instalacion']
        total_total = total - empresas[empresa]['valor_residual']
        depreciacion_anio = total_total / empresas[empresa]['vida_util']


        if empresas[empresa]['anios_depreciacion'] > 0:
            
            depreciacion_acumulada = empresas[empresa]['anios_depreciacion']*depreciacion_anio
            valor_libros = empresas[empresa]['valor'] - depreciacion_acumulada
            valor_libros = valor_libros
            empresas[empresa]['depreciacion_acumulada'] = depreciacion_acumulada
            empresas[empresa]['valor_libros'] = valor_libros
            depreciacion_anios['depreciacion_base'] = depreciacion_anio
        else:
            depreciacion_anios[empresa] = depreciacion_anio

        empresas[empresa]['total'] = total
        empresas[empresa]['total_total'] = total_total
        empresas[empresa]['depreciacion_anio'] = depreciacion_anio
    #imprimir_primeros_calculos(empresas)
    inversion_inicial(empresas, valor_libros, depreciacion_anios)


def inversion_inicial(empresas, valor_libros, depreciacion_anios):
    tabla_inversion_inicial = {}
    tasa_impuestos = 0

    for empresa in empresas:
        if 'valor_libros' not in empresas[empresa]:

            tabla_inversion_inicial[empresa] = {}
            
            venta = float(input(f'Dame el valor de venta [empresa]'))
            tasa_impuestos = float(input(f'Dame la tasa de impuestos de la empresa {empresa}'))

            tasa_impuestos = tasa_impuestos / 100

            utilidad = valor_libros - venta
            utilidad_utilidad = utilidad * tasa_impuestos
            inversion_inicial = empresas[empresa]['total'] - venta - utilidad_utilidad

            tabla_inversion_inicial[empresa]['venta'] = venta
            tabla_inversion_inicial[empresa]['inversion_inicial'] = inversion_inicial
            tabla_inversion_inicial[empresa]['utilidad'] = utilidad
            tabla_inversion_inicial[empresa]['utilidad utilidad'] = utilidad_utilidad
    #imprimir_inversion_inicial(tabla_inversion_inicial)
    flujos_efectivo(empresas, tasa_impuestos, tabla_inversion_inicial, depreciacion_anios)
            
def flujos_efectivo(empresas, tasa_impuestos, tabla_inversion_inicial, depreciacion_anios):

    tabla_flujos_efectivo = {}
    sumatoria = 0

    for empresa in empresas:
        tabla_flujos_efectivo[empresa] = {}
        
        if empresas[empresa]['anios_depreciacion'] == 0:
            for i in range(int(empresas[empresa]['vida_util'])):
                tabla_flujos_efectivo[empresa][i] = {}
                venta = float(input(f'Dame el incremento en las ventas de la empresa {empresa} para el anio {i}'))
                costo = float(input(f'Dame la reduccion en costos de trabajo  de la emoresa {empresa} para el anio {i}'))
                
                utilidad_antes_impuestos = venta + costo
                diferencia_depreciacion = empresas[empresa]['depreciacion_anio'] - depreciacion_anios['depreciacion_base'] 
                utilidad_depreciacion = utilidad_antes_impuestos - diferencia_depreciacion
                impuestos = utilidad_depreciacion * tasa_impuestos
                utilidad_despues_impuesto = utilidad_depreciacion - impuestos
                flujos_efectivo = diferencia_depreciacion + utilidad_despues_impuesto

                tabla_flujos_efectivo[empresa][i]['ventas'] = (venta)
                tabla_flujos_efectivo[empresa][i]['costo'] = costo
                tabla_flujos_efectivo[empresa][i]['utilidad_antes_impuestos'] = utilidad_antes_impuestos
                tabla_flujos_efectivo[empresa][i]['diferencia_depreciacion'] = diferencia_depreciacion
                tabla_flujos_efectivo[empresa][i]['utilidad_depreciacion'] = utilidad_depreciacion
                tabla_flujos_efectivo[empresa][i]['impuestos'] = impuestos
                tabla_flujos_efectivo[empresa][i]['utilidad_despues_impuestos'] = utilidad_despues_impuesto
                tabla_flujos_efectivo[empresa][i]['flujos_efectivo'] = flujos_efectivo
                sumatoria += flujos_efectivo
            tabla_flujos_efectivo[empresa]['sumatoria'] = sumatoria

    presupuesto_recuperacion(empresas, tabla_flujos_efectivo, tabla_inversion_inicial)                

        
    
def presupuesto_recuperacion(empresas, tabla_flujos_efectivo, tabla_inversion_inicial):
    
    flujos = 0
    tiempos = [30.5, 8, 60]
    tiempo_recuperacion = []

    for empresa in tabla_inversion_inicial:
        print(tabla_inversion_inicial[empresa]['inversion_inicial'])
        
        for i in range(len(tabla_flujos_efectivo[empresa])):
            flujos += tabla_flujos_efectivo[empresa][i]['flujos_efectivo']
        
            if flujos > tabla_inversion_inicial[empresa]['inversion_inicial']:
                flujos -= tabla_flujos_efectivo[empresa][i]['flujos_efectivo']
                
                resta = tabla_inversion_inicial[empresa]['inversion_inicial'] - flujos
                k = i -1
                multiplicaodr = tabla_flujos_efectivo[empresa][k]['flujos_efectivo'] / 12
                anios = resta / multiplicaodr
                redondeo = math.floor(anios)
                tiempo_recuperacion.append(redondeo)
                inve = multiplicaodr * redondeo
                
                for j in range(3):
                    
                    resta = resta - inve
                    
                    multiplicaodr = multiplicaodr / tiempos[j]
                    redondeo = math.floor(resta / multiplicaodr)
                    inve = multiplicaodr * redondeo
                    tiempo_recuperacion.append(redondeo)
                    
                break
    

def VAN(empresas, tabla_flujos_efectivo, tabla_inversion_inicial):
    
    tablas_VAN = {}
    
    for empresa in tabla_flujos_efectivo:
        
        tablas_VAN[empresa] = {}
        
        costo_capital = input(f'Dame el porcentaje de costo de capital de la empresa {empresa}')   
        costo_capital = costo_capital / 100
        costo_capital += 1
        
        for i in range(empresas[empresa]['vida_util']):
            factor = costo_capital ^ empresas[empresa]['vida_util'] 
            van = factor * tabla_flujos_efectivo[empresa][i]['flujos_efectivo']
            van_total += van
            
        utilidad = van_total - tabla_inversion_inicial[empresa]['inversion_inicial']
        
            
def TIR(empresas, tabla_flujos_efectivo, tabla_inversion_inicial):
    
    for empresa in tabla_flujos_efectivo:
        
        flujos = []
        
        for i in range(empresas[empresa]['vida_util']):
            
            flujos.append(tabla_flujos_efectivo[empresa][i]['flujos_efectivo'])
            tir = np.irr(flujos)
            
            print(tir)
            
            
        
        
        
        
    
def imprimir_primeros_calculos(empresas):

    for empresa in empresas:
        print(empresas[empresa])
                    
def imprimir_inversion_inicial(tablas):

    for tabla in tablas: 
        print(tablas[tabla])

def imprimir_flujos_efectivo(tablas):

    for tabla in tablas:
        print(tablas[tabla])



obtener_valores()
