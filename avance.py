import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


R = 8.314
T = 298.15
u_a = 0
u_b = 0
u_ab = 0
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
    """"""
    u_a_slider = plt.axes([0.15, 0.05, 0.7, 0.02])
    u_b_slider = plt.axes([0.15, 0.1, 0.7, 0.02])
    u_a_factor = Slider(u_a_slider,
                            "u_A°",
                            valmin=-1000,
                            valmax=1000,
                            valinit=0,
                            valstep=20,
                            )
    u_b_factor = Slider(u_b_slider,
                            "u_B°",
                            valmin=-1000,
                            valmax=1000,
                            valinit=0,
                            valstep=20,
                            )
    return u_a_factor, u_b_factor


def axis_bi_create():
    """"""
    u_a_slider = plt.axes([0.15, 0.03, 0.7, 0.02])
    u_b_slider = plt.axes([0.15, 0.07, 0.7, 0.02])
    u_ab_slider = plt.axes([0.15, 0.12, 0.7, 0.02])

    u_a_factor = Slider(u_a_slider,
                        "u_A°",
                        valmin=-1000,
                        valmax=1000,
                        valinit=0,
                        valstep=20,
                        )
    u_b_factor = Slider(u_b_slider,
                        "u_B°",
                        valmin=-1000,
                        valmax=1000,
                        valinit=0,
                        valstep=20,
                        )
    u_ab_factor = Slider(u_ab_slider,
                        "u_AB°",
                        valmin=-1000,
                        valmax=1000,
                        valinit=0,
                        valstep=20,
                        )
    return u_a_factor, u_b_factor, u_ab_factor


def potencial_quimico_uni(val):
    """Actualizar u_A y u_B con los valores de la barra de desplazamiento"""
    current_u_A = u_a_factor.val
    current_u_B = u_b_factor.val
    gibbs_uni = unimolecular(EPSILON, current_u_A, current_u_B)
    unit_line = line_uni(EPSILON, current_u_A, current_u_B)
    plot_func.set_ydata(gibbs_uni)
    plot_func_2.set_ydata(unit_line)
    fig.canvas.draw()


def  potencial_quimico_di(val):
    """Actualizar u_A, u_B y u_AB con los valores de la barra de desplazamiento"""
    current_u_A = u_a_factor.val
    current_u_B = u_b_factor.val
    current_u_AB = u_ab_factor.val
    gibbs_uni = bimolecular(EPSILON, current_u_A, current_u_B, current_u_AB )
    plot_func.set_ydata(gibbs_uni)
    fig.canvas.draw()


print("Seleccione el tipo de reacción con la que desea trabajar,"
      "escriba uni para trabajar con una reacción unimolecular o bi para trabajar con una bimolecular")
respuesta = input("\nReacción a trabajar: ")

if respuesta.lower() == "uni":
    gibbs_uni = unimolecular(EPSILON, u_a, u_b)
    unit_line = line_uni(EPSILON, u_a, u_b)
    u_a_factor, u_b_factor = axis_uni_create()
    ax.grid()
    ax.set_ylim(-2800,1050)
    ax.set_xlim(0,1)
    ax.set_ylim(-4000,1500)
    ax.set_xlim(0.0,1.0001)
    plot_func, = ax.plot(EPSILON, gibbs_uni, "g")
    plot_func_2, = ax.plot(EPSILON, unit_line, "r")
    u_a_factor.on_changed(potencial_quimico_uni)
    u_b_factor.on_changed(potencial_quimico_uni)
    plt.show()
elif respuesta.lower() == "bi":
    gibbs_bi = bimolecular(EPSILON, u_a, u_b, u_ab)
    u_a_factor, u_b_factor, u_ab_factor = axis_bi_create()
    ax.grid()
    ax.set_ylim(-4000,1500)
    ax.set_xlim(0.0,1.0001)
    ax.set_xlabel('E')
    ax.set_ylabel('Gsist')
    plot_func, = ax.plot(EPSILON, gibbs_uni, "g")
    u_a_factor.on_changed(potencial_quimico_di)
    u_b_factor.on_changed(potencial_quimico_di)
    u_ab_factor.on_changed(potencial_quimico_di)
    plt.show()
else:
    print("La opción ingresada no es válida")

















