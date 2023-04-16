import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

#Variaveis de Entrada (Antecedent)
comer = ctrl.Antecedent(np.arange(0, 10000, 2000), 'comer')
treina = ctrl.Antecedent(np.arange(0, 16, 2), 'treina(horas)')

#Variaveis de saída (Consequent)
peso = ctrl.Consequent(np.arange(0, 120, 20), 'peso')

# automf -> Atribuição de categorias automaticamente
comer['Pouco'] = fuzz.trapmf(comer.universe, [-1000,0,2000,4000])
comer['Razoável'] = fuzz.trapmf(comer.universe, [2000,4000,6000,8000])
comer['Bastante'] = fuzz.trapmf(comer.universe, [4000,6000,8000,10000])

treina['Pouco'] = fuzz.trapmf(treina.universe, [-1,0,3,5])
treina['Razoável'] = fuzz.trapmf(treina.universe, [4,6, 10,12])
treina['Bastante'] = fuzz.trapmf(treina.universe, [8, 12,14,16])


# atribuicao sem o automf
peso['Leve'] = fuzz.trapmf(peso.universe, [-20,0,40,60])
peso['Medio'] = fuzz.trapmf(peso.universe, [40,60,80,100])
peso['Pesado'] = fuzz.trapmf(peso.universe, [80,100,120,140])


#Visualizando as variáveis
comer.view()
treina.view()
peso.view()

#Criando as regras
regra_1 = ctrl.Rule(comer['Pouco'], peso['Leve'])
regra_2 = ctrl.Rule(comer['Razoável'] & treina['Bastante'], peso['Leve'])
regra_3 = ctrl.Rule(comer['Razoável'] & treina['Razoável'], peso['Medio'])
regra_4 = ctrl.Rule(comer['Bastante'] & treina['Bastante'], peso['Medio'])
regra_5 = ctrl.Rule(comer['Bastante'] & treina['Pouco'], peso['Pesado'])

controlador = ctrl.ControlSystem([regra_1, regra_2, regra_3, regra_4, regra_5])


#Simulando
CalculoPeso = ctrl.ControlSystemSimulation(controlador)

notaComer = int(input('Comer: '))
notaTreina = int(input('Treina: '))
CalculoPeso.input['comer'] = notaComer
CalculoPeso.input['treina(horas)'] = notaTreina
CalculoPeso.compute()

valorPeso = CalculoPeso.output['peso']

print("\Comer %d  \Treina %d \Peso %5.2f" %(
        notaComer,
        notaTreina,
        valorPeso))


comer.view(sim=CalculoPeso)
treina.view(sim=CalculoPeso)
peso.view(sim=CalculoPeso)

plt.show()