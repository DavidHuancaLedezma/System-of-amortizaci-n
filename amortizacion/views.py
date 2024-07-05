from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def seleccion_problema(request):
    return render(request, "seleccion_problema.html")

def home (request):
    return render(request, "home.html")

def sac(request):
    return render(request,"sac.html")

def resultados_price(request):
    input_deuda = int(request.POST.get("input_deuda"))
    input_años = int(request.POST.get("input_años"))
    input_tasa_interes = int(request.POST.get("input_tasa_interes"))
    periodo = request.POST.get("opcion")
    numero_caso = request.POST.get("casos")
    opcion_a_pagar_caso_3 = request.POST.get("opcion_a_pagar_caso3")
    if numero_caso:
        pass
    else:
        numero_caso = ""
    tabla = sistema_cuota_fija(input_deuda, input_años, input_tasa_interes, periodo, numero_caso, opcion_a_pagar_caso_3)
    sumatoria_interes = tabla.pop(len(tabla)-1)
    return render(request,"resultados.html",{"datos":tabla, "interes_total":sumatoria_interes})


def resultados_sac(request):
    input_deuda = int(request.POST.get("input_deuda_sac"))
    input_años = int(request.POST.get("input_años_sac"))
    input_interes = int(request.POST.get("input_tasa_interes_sac"))
    input_capitalizar = request.POST.get("opcion_capitalizar_sac")
    input_periodo_de_pago = request.POST.get("opcion_periodo_sac")

    input_interes = input_interes/100

    tabla = sistema_amortizacion_constante(input_deuda, input_años, input_interes, input_capitalizar, input_periodo_de_pago)
    sumatoria_interes = tabla.pop(len(tabla) - 1)

    return render(request, "resultados.html", {"datos":tabla, "interes_total":sumatoria_interes})

    
    
    

    

def sistema_amortizacion_constante(deuda, años, interes, capitalizar, periodo_de_pago):
    sumatoria_interes_total = 0

    conversor_periodo_de_pago = {
        "anual" : 12,
        "semestral" : 6,
        "bimestral" : 2,
        "trimestral" : 3,
        "mensual": 1
    }

    conversor_capitalizacion = {
        "mensual" : 12,
        "bimestral": 6,
        "trimestral" : 4,
        "semestral" : 2,
        "anual" : 1 
    }
    
    k = round(deuda/años,2)
    numero_de_filas = int((años * 12) / conversor_periodo_de_pago[periodo_de_pago])
    tabla = []
    
    if capitalizar == "mensual":
        interes = round(((1 +(interes/conversor_capitalizacion[capitalizar]))**conversor_capitalizacion[capitalizar] - 1), 4)
        

    for i in range(numero_de_filas + 1):
        if i == 0:
            tabla.append([i,deuda,"----","----","----"])
        else:
            columna_interes = round((deuda * interes),2)
            sumatoria_interes_total += columna_interes
            columna_cuota = round((columna_interes + k),2)
            deuda = round((deuda - k),2)
            tabla.append([i, deuda, k, columna_interes, columna_cuota])
    
    tabla.append(round(sumatoria_interes_total,2))

    return tabla


def sistema_cuota_fija(deuda_ingresada,años_ingresados,interes_ingresado,periodo_a_pagar,numero_caso,opcion_a_pagar_caso3):
    deuda = deuda_ingresada  #Dato por consola
    años = años_ingresados * 12 #Años dato por consola
    cuotas = periodo_a_pagar #Dato por combo box
    valor_cuotas = 0 
    tasa_interes = interes_ingresado / 100 #Dato por consola 9% trimestral
    numero_filas = 0
    sumatoria_interes_total = 0

    tabla = []
    tiempo_de_pago = {"anual":12,
                      "trimestral":3,
                      "bimestral":2,
                      "semestral":6,
                      "mes":1
                      }
    valor_cuotas = tiempo_de_pago[cuotas]
    
    numero_filas = int(años / valor_cuotas)

    if numero_caso == "caso3":
        potencia_caso_3 = años / tiempo_de_pago[opcion_a_pagar_caso3]
        tasa_interes = (((1+(tasa_interes/numero_filas))**numero_filas)**(1/potencia_caso_3)) - 1
        tasa_interes = round(tasa_interes,4)
    elif numero_caso == "caso2":
        tasa_interes = ((1+(tasa_interes/numero_filas))**numero_filas) - 1


    #formula
    a = deuda * (tasa_interes/(1-((1+tasa_interes)**(-numero_filas))))
    a = round(a,2)

    # n | saldo deudor | Amortización | Interes | Cuota
    for i in range(numero_filas+1):
        if i == 0:
            tabla.append([i,deuda,"----","----","----"])
            
        else:
            interes = round((deuda * tasa_interes),2)
            amortizacion = round((a - interes),2)
            deuda = round((deuda - amortizacion),2)

            sumatoria_interes_total = sumatoria_interes_total + interes
            sumatoria_interes_total = round(sumatoria_interes_total,2)
            tabla.append([i,deuda,amortizacion,interes,a])

    tabla.append(sumatoria_interes_total)
    return tabla

def manual_de_uso(request):
    return render(request, "instrucciones_de_uso.html")
