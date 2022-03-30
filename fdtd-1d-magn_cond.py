import numpy as np
import math
import matplotlib.pyplot as plt
import numpy.fft as npf
import matplotlib.animation as animation



pi = math.pi
#mu = 4*pi*1e-7
#eps0 = 8.8541878128e-12
# Voy a trabajar en unidades naturales
mu = 1.0
eps = 1.0
c0 = 1.0

## -- Grid
tEnd = 5

xIni = 0
xEnd = 10
N = int(101)

grid = np.linspace(xIni,xEnd,N)
dualGrid = (grid[:-1] + grid[1:])/2.0 # Tiene un punto menos que el primal

## -- Espaciados
Dx = grid[1] - grid[0]
Dt = 0.8*Dx/c0 # Para que sea dimensionalmente correcto

## - Condicion inicial (gaussiana)
media = (xIni + xEnd)/3.0
sigma= (xIni-xEnd)/10.0

# Dos gaussianas que empiezan a la vez
Eini = np.exp( - np.power(grid - media,2) / (2.0*sigma**2))
Hini = np.exp( - np.power(dualGrid - media-c0*Dt*0.5,2) / (2.0*sigma**2))
# Es que si no traslado el centro de la gaussiana de ese modo,
# como los campos se calculan en instantes diferentes no tengo la misma
# condicion inicial


# Condiciones dielectricas
epsV = np.zeros(N)
epsV[0:81]= 1.0
epsV[81:] = 3.0



## -- Algoritmo
# Primero inicializamos
Eold = Eini
Hold = Hini

Enew = Eold*0.0
Hnew = Hold*0.0

t=0.0

fig = plt.figure(figsize = (15,15))
ax = fig.add_subplot(111)

Edata, Hdata = [],[]





while t < tEnd:
    Enew[1:-1] = -(Dt/(epsV[1:-1]*Dx)) * (Hold[1:] - Hold[:-1]) + Eold[1:-1]
    Enew[-1] = (Dt/(epsV[-1]*Dx)) * (2*Hold[-1]) + Eold[-1]
    Enew[0] = -(Dt/(epsV[0]*Dx)) * (2*Hold[0]) + Eold[0]

    Hnew[:] = -(Dt/(mu*Dx)) * (Enew[1:] - Enew[:-1]) + Hold[:]

    Eold[:] = Enew[:]
    Hold[:] = Hnew[:]
    Edata.append(Enew)
    Hdata.append(Hnew)

    t+=Dt

    # plt.plot(grid,Enew)
    # plt.plot(dualGrid,Hnew)
    # plt.grid()
    # plt.xlim(0,11)
    # plt.ylim(-3,3)
    # plt.legend(['Electrico','Magnetico'])
    # rectangle = plt.Rectangle((0,8.0),2,6,fc='blue',ec="blue")
    # plt.gca().add_patch(rectangle)
    # plt.show()


print('End')

def animate(i):
    ax.clear()
    ax.plot(grid,Edata[i],color = 'darkblue')
    ax.plot(dualGrid,Hdata[i],color = 'red')
    rectangle = plt.Rectangle((8,0), 2, 20, fc='blue',ec="blue")
    plt.gca().add_patch(rectangle)
    plt.grid()



anim = animation.FuncAnimation(fig, animate,frames=63)

#anim.save('basic_animation.gif', fps=30, extra_args=['-vcodec', 'libx264'])
#anim.save('caca.gif')
                            
plt.show()

# grid[a:b] coge el intervalo [a,b). El -1 es el ultimo (empiezo en 0)
# Luego grid[:-1] coge desde el primero hasta el penultimo y
# grid[1:] coge desde el segundo hasta el ultimo

