import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import scipy
nx = 100
xmax = 1
x = np.linspace(0,xmax,nx)
y = np.cos(2*np.pi*x)
fig = plt.subplots(figsize=(10, 10), tight_layout=True)
plt.rcParams["font.family"] = 'serif'
plt.rcParams.update({'font.size': 24})
plt.rcParams['text.usetex'] = True
plt.plot(x,y, lw = 1.5)
plt.xlim(x[0],x[-1])
plt.ylim(-1,1)
plt.xlabel("$\Omega$")
plt.ylabel("$y = f(x) 1/2$")
plt.grid()
plt.show()
x = np.linspace(0,1,100)
y = np.sin(2*np.pi*x)

fig = plt.subplots(figsize=(13,7), layout='constrained')
ax = plt.gca()
ax.xaxis.set_major_locator(ticker.MultipleLocator(1/12))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(1/36))
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.25))
ax.yaxis.set_ticks_position('left')
ax.tick_params(which='major', width=1, length=5)
ax.tick_params(which='minor', width=1, length=5)
ax.tick_params(axis='x', color='m', length=10, direction='out', width=2, labelcolor='g', grid_color='b')
ax.tick_params(axis='y', color='k', length=10, direction='out', width=2, labelcolor='k', grid_color='gray')
ax.set_xticks([0,0.083,0.167,0.25,1/3,0.417,0.5,0.583,2/3,0.75,0.833,0.917,1]) 
ax.set_xticklabels(["",r'$\frac{\pi}{6}$',r'$\frac{\pi}{3}$',r'$\frac{\pi}{2}$',r'$\frac{2\pi}{3}$',r'$\frac{5\pi}{6}$', '$\pi$',r'$\frac{7\pi}{6}$',r'$\frac{4\pi}{3}$', r'$\frac{3}{2}\pi$',r'$\frac{5\pi}{3}$',r'$\frac{11\pi}{6}$',r'$2\pi$'])
# ax.spines['left'].set_position('center')
ax.spines['bottom'].set_position('center')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
# ax.spines['bottom'].set_visible(False)
# ax.spines['left'].set_visible(False)
plt.plot(x,y)
# plt.hlines(0, 0, x[-1], colors="k", linestyles='solid', label='-')
plt.xlim(0,1)
# plt.grid()
plt.show()
