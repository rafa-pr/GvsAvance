import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib

#Condiciones de reacción
R = 8.314
T = 298.15
u_a = 0
u_b = 0
u_a_l = 0
u_b_l = 0
u_ab = 0
#Rango de avance de reacción
EPSILON = np.linspace(0.00001, 0.9999999999, 100)
fig = plt.figure(figsize=(10,7))
ax = fig.subplots()
plt.subplots_adjust(bottom=0.25)


def unimolecular(epsilon, u_a, u_b, P=1):
    """A ---> B"""
    G = (epsilon * (u_b - u_a) + R * T * np.log(P) + R * T * ((1 - epsilon) * np.log(1 - epsilon) +
                                                                            epsilon * np.log(epsilon))) + u_a
    return G


def line_uni(epsilon, u_a, u_b):
    """Permite visualizar la energía libre de Gibbs sin tener encuenta el efecto de mezcla"""
    line = (u_b - u_a) * epsilon + u_a
    return line


def bimolecular(epsilon,u_a, u_b, u_ab, P=1):
    """(1/2)A2 + (1/2)B2 ---> AB"""
    G = (0.5 * (1 - epsilon) * (u_a + u_b) + epsilon * u_ab +
        R * T * (epsilon * np.log(epsilon) + (1 - epsilon) * np.log(0.5 * (1 - epsilon))) +
        R * T * np.log(P))
    return G


def axis_uni_create():
    """Crea las barras de desplazamiento para los potenciales"""
    u_a_slider = plt.axes([0.15, 0.05, 0.7, 0.02])
    u_b_slider = plt.axes([0.15, 0.1, 0.7, 0.02])
    u_a_factor = Slider(u_a_slider,
                            "μ_A°",
                            valmin=-1000,
                            valmax=1000,
                            valinit=0,
                            valstep=20,
                            )
    u_b_factor = Slider(u_b_slider,
                            "μ_B°",
                            valmin=-1000,
                            valmax=1000,
                            valinit=0,
                            valstep=20,
                            )
    return u_a_factor, u_b_factor


def axis_bi_create():
    """Crea las barras de desplazamiento para los potenciales"""
    u_a_slider = plt.axes([0.15, 0.03, 0.7, 0.02])
    u_b_slider = plt.axes([0.15, 0.07, 0.7, 0.02])
    u_ab_slider = plt.axes([0.15, 0.12, 0.7, 0.02])

    u_a_factor = Slider(u_a_slider,
                        "μ_A°",
                        valmin=-1000,
                        valmax=1000,
                        valinit=0,
                        valstep=20,
                        )
    u_b_factor = Slider(u_b_slider,
                        "μ_B°",
                        valmin=-1000,
                        valmax=1000,
                        valinit=0,
                        valstep=20,
                        )
    u_ab_factor = Slider(u_ab_slider,
                        "μ_AB°",
                        valmin=-1000,
                        valmax=1000,
                        valinit=0,
                        valstep=20,
                        )
    return u_a_factor, u_b_factor, u_ab_factor


def potencial_quimico_uni1(val):
    """Actualizar u_A y u_B con los valores de la barra de desplazamiento"""
    global note
    current_u_A = u_a_factor.val
    current_u_B = u_b_factor.val
    gibbs_uni = unimolecular(EPSILON, current_u_A, current_u_B)
    gibbs_lin = line_uni(EPSILON, current_u_A, current_u_B)
    minGibbs = min(gibbs_uni)
    minPosGibss=  np.argmin(gibbs_uni)
    minEPSILON = EPSILON[minPosGibss]
    try:
        note.remove()
    except:
        pass
    
    note = matplotlib.text.Annotation('Gibs minimum at ξ = {0} \n and ΔGsist = {1}'.format(minEPSILON,minGibbs)\
                    ,xy=(minEPSILON, minGibbs), xytext=(minEPSILON+0.2, minGibbs-500),\
                    arrowprops=dict(facecolor='red', shrink=0.05))
    
    ax.add_artist(note) 
    plot_func.set_ydata(gibbs_uni)
    plot_func_2.set_ydata(gibbs_lin)
    fig.canvas.draw()

def  potencial_quimico_di(val):
    global note
    
    """Actualizar u_A, u_B y u_AB con los valores de la barra de desplazamiento"""
    current_u_A = u_a_factor.val
    current_u_B = u_b_factor.val
    current_u_AB = u_ab_factor.val
    gibbs_bi = bimolecular(EPSILON, current_u_A, current_u_B, current_u_AB )
    
    """Función para trazar el mínimo""" 
    
    minGibbs = min(gibbs_bi)
    minPosGibss=  np.argmin(gibbs_bi)
    
    minEPSILON = EPSILON[minPosGibss]
    
    try:
        note.remove()
    except:
        pass
    
    note = matplotlib.text.Annotation('Gibs minimum at ξ = {0} \n and ΔGsist = {1}'.format(minEPSILON,minGibbs)\
                    ,xy=(minEPSILON, minGibbs), xytext=(minEPSILON+0.2, minGibbs-500),\
                    arrowprops=dict(facecolor='red', shrink=0.05))
    
    ax.add_artist(note) 
    plot_func.set_ydata(gibbs_bi)
    fig.canvas.draw()


print("Seleccione el tipo de reacción con la que desea trabajar,"
      "escriba uni para trabajar con una reacción unimolecular o bi para trabajar con una bimolecular")
respuesta = input("\nReacción a trabajar: ")

if respuesta.lower() in {"uni"}:
    gibbs_uni = unimolecular(EPSILON, u_a, u_b)
    unit_line = line_uni(EPSILON, u_a_l, u_b_l)
    u_a_factor, u_b_factor = axis_uni_create()
    ax.grid()
    ax.set_ylim(-3300,1050)
    ax.set_xlim(0,1.5)
    ax.set_xlabel('ξ')
    ax.set_ylabel('ΔGsist')
    plot_func, = ax.plot(EPSILON, gibbs_uni, "g")
    plot_func_2, = ax.plot(EPSILON, unit_line, "r")
    u_a_factor.on_changed(potencial_quimico_uni1)
    u_b_factor.on_changed(potencial_quimico_uni1)
    plt.show()
elif respuesta.lower() in {"bi"}:
    gibbs_bi = bimolecular(EPSILON, u_a, u_b, u_ab)
    u_a_factor, u_b_factor, u_ab_factor = axis_bi_create()
    ax.grid()
    ax.set_ylim(-4000,1500)
    ax.set_xlim(0.0,1.3)
    ax.set_xlabel('ξ')
    ax.set_ylabel('ΔGsist')
    plot_func, = ax.plot(EPSILON, gibbs_bi, "g")
    u_a_factor.on_changed(potencial_quimico_di)
    u_b_factor.on_changed(potencial_quimico_di)
    u_ab_factor.on_changed(potencial_quimico_di)
    plt.show()
else:
    print("La opción ingresada no es válida")

















