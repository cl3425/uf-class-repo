########################################################################
# 
# hw2.py
#
# This is my attempt at #3 on HW 2
#
########################################################################

# Import the despotic library
from despotic import cloud

# Import standard python libraries
from numpy import *
import scipy.constants
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
from datetime import datetime
from datetime import timedelta

mycloud = cloud()
mycloud.nH = 1.0e2
mycloud.colDen = 1.0e22
mycloud.sigmaNT = 2.0e5
mycloud.Tg = 10.0
mycloud.comp.xoH2 = 0.1
mycloud.comp.xpH2 = 0.4
mycloud.comp.xHe = 0.1
mycloud.addEmitter("CO", 1.0e-4)
lines = mycloud.lineLum("CO")
inttb = lines[0]['intTB']
xco = mycloud.colDen/inttb 

tgs = np.logspace(0, 2, 100)
sigmaNTs = np.logspace(0, 6, 100)
sigmaNTs = np.logspace(0, 7, 100) # max of max(sigmaNT) among the cloudfiles
xcos = []

########################################################################
### Relation between Tg and XCO
########################################################################
"""
for tg in tgs:
  mycloud.Tg = tg
  #mycloud.addEmitter("CO", 1.0e-4)
  lines = mycloud.lineLum("CO")
  inttb = lines[0]['intTB']
  print(mycloud.colDen, inttb)
  xcos.append(mycloud.colDen/inttb)

fig = figure(1)
ax = fig.add_subplot(111)
ax.scatter(tgs, xcos)
ax.set_ylabel('X_CO')
ax.set_xlabel('T_g')
ax.set_title('X_CO vs T_g')
savefig('xco_vs_tg_zoomout.eps')
plt.show()
"""

########################################################################
### Relation between sigmaNT and XCO
########################################################################
"""
for sigmaNT in sigmaNTs:
  mycloud.sigmaNT = sigmaNT
  #mycloud.addEmitter("CO", 1.0e-4)
  lines = mycloud.lineLum("CO")
  inttb = lines[0]['intTB']
  #print(mycloud.colDen, inttb)
  xcos.append(mycloud.colDen/inttb)

fig = figure(2)
ax = fig.add_subplot(111)
ax.set_yscale('log')
ax.set_xscale('log')
ax.scatter(sigmaNTs, xcos)
ax.set_ylabel('X_CO')
ax.set_xlabel('sigmaNT')
ax.set_title('X_CO vs sigmaNT')
savefig('xco_vs_sigmaNT.eps')
plt.show()
"""

########################################################################
### Relation between surface density and XCO
### From class notes, Sigma_mol = Alpha_CO * W_CO
### Alpha_CO is the virial parameter, alpha = 5*sigmaNT**2/(G*M)
### So for linear increase in alphaCO, sigmaNT increases by sqrt
### Holding mass constant, this would be a relation of sqrt(sigmaNT)*intTB to XCO (???)
########################################################################

G = scipy.constants.G*1e3
M = 2e39 # assuming 1 million solar mass cloud, in grams
#alpha_COs = np.logspace(0, 10, 100)

def sigmant_from_sigmamol(alpha, inttb):
  return np.sqrt(alpha*G*M/(5*inttb))

def sigma_mol(sigmaNT, inttb):
  alpha = 5*sigmaNT**2/(G*M)
  return alpha * inttb 

surf_dens = []
for sigmaNT in sigmaNTs:
  #mycloud.sigmaNT = sigma_from_alpha(alpha_CO)
  mycloud.sigmaNT = sigmaNT
  mycloud.addEmitter("CO", 1.0e-4)
  lines = mycloud.lineLum("CO")
  inttb = lines[0]['intTB']
  surf_den = sigma_mol(mycloud.sigmaNT, inttb)
  surf_dens.append(surf_den)
  #print(surf_den)
  xcos.append(mycloud.colDen/inttb)

fig = figure(3)
ax = fig.add_subplot(111)
ax.set_yscale('log')
ax.set_xscale('log')
ax.scatter(surf_dens, xcos)
ax.set_ylabel('X_CO')
ax.set_xlabel('Sigma_mol')
ax.set_title('X_CO vs Sigma_mol')
savefig('xco_vs_sigmamol.eps')
plt.show()

quit()

########################################################################
### Get relations using what little cloudfiles data we have
########################################################################

# Read the Milky Way GMC cloud file
gmc = cloud(fileName='cloudfiles/MilkyWayGMC.desp')
print(gmc.emitters)

# Read the ULIRG cloud file
ulirg = cloud(fileName='cloudfiles/ULIRG.desp')

# Read the other two clouds bc I want more than just two data points
postshock = cloud(fileName='cloudfiles/postShockSlab.desp')
protostellar = cloud(fileName='cloudfiles/protostellarCore.desp')

# Compute the luminosity of the CO lines in all four clouds
# Decide to use one kind of emitter
t1=datetime.now()
gmclines = gmc.lineLum('co')
ulirglines = ulirg.lineLum('co')
gmclines13 = gmc.lineLum('13co')
ulirglines13 = ulirg.lineLum('13co')
postshocklines = postshock.lineLum('co')
protostellarlines = protostellar.lineLum('co')
postshocklines13 = postshock.lineLum('13co')
protostellarlines13 = protostellar.lineLum('13co')
t2=datetime.now()
print('Execution time = '+str(t2-t1))

#print(postshock.colDen, protostellar.colDen)
#print(postshocklines[0], protostellarlines[0])
#print(postshock.colDen/postshocklines[0]['intTB'], protostellar.colDen/protostellarlines[0]['intTB'])
#print(gmclines[0:5])

# Print out the CO X factor for both clouds. This is column density
# divided by velocity-integrated brightness temperature.
# Why use only the intTB for the 1->0 transition? Why not the other ones? 
print("GMC X_CO = "+str(gmc.colDen/gmclines[0]['intTB']) + 
      " cm^-2 / (K km s^-1)")
print("ULIRG X_CO = "+str(ulirg.colDen/ulirglines[0]['intTB']) + 
      " cm^-2 / (K km s^-1)")

#postShockSlab.desp
print(gmclines[0])
print(ulirglines[0])
print(gmclines13[0])
print(ulirglines13[0])
print(postshocklines[0])
print(protostellarlines[0])
print(postshocklines13[0])
print(protostellarlines13[0])

tgs = [gmc.Tg, ulirg.Tg, postshock.Tg, protostellar.Tg]
#tgs = [gmc.Tg, ulirg.Tg, postshock.Tg]
tgs = [gmc.Tg, ulirg.Tg, postshock.Tg, protostellar.Tg, 
  gmc.Tg, ulirg.Tg, postshock.Tg, protostellar.Tg]
print(tgs)

velocity_dispersion = [gmc.sigmaNT, ulirg.sigmaNT, postshock.sigmaNT, protostellar.sigmaNT,
  gmc.sigmaNT, ulirg.sigmaNT, postshock.sigmaNT, protostellar.sigmaNT]
#velocity_dispersion = [gmc.sigmaNT, ulirg.sigmaNT, postshock.sigmaNT]
print(velocity_dispersion)

xcos = [gmc.colDen/gmclines[0]['intTB'], ulirg.colDen/ulirglines[0]['intTB'], 
  postshock.colDen/postshocklines[0]['intTB'], protostellar.colDen/protostellarlines[0]['intTB']]
#xcos = [gmc.colDen/gmclines[0]['intTB'], ulirg.colDen/ulirglines[0]['intTB'], 
#  postshock.colDen/postshocklines[0]['intTB']]
xcos = [gmc.colDen/gmclines[0]['intTB'], ulirg.colDen/ulirglines[0]['intTB'], 
  postshock.colDen/postshocklines[0]['intTB'], protostellar.colDen/protostellarlines[0]['intTB'],
  gmc.colDen/gmclines13[0]['intTB'], ulirg.colDen/ulirglines13[0]['intTB'], 
  postshock.colDen/postshocklines13[0]['intTB'], protostellar.colDen/protostellarlines13[0]['intTB']]
print(xcos)

fig = figure(1)
ax = fig.add_subplot(111)
ax.scatter(velocity_dispersion, xcos)
ax.set_ylabel('X_CO')
ax.set_xlabel('sigmaNT')
ax.set_title('X_CO vs sigmaNT')
savefig('xco_vs_sigmaNT_cloudfiles.eps')
#plt.show()

fig = figure(2)
ax = fig.add_subplot(111)
ax.scatter(tgs, xcos)
ax.set_ylabel('X_CO')
ax.set_xlabel('T_gs')
ax.set_title('X_CO vs T_gs')
savefig('xco_vs_tg_cloudfiles.eps')
plt.show()