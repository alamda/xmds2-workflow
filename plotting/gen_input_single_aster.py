import numpy as np 
import h5py 

bound=100
dim = 200
step=bound*2/dim

concentration = 10 #conc_scale/(dim)**2

CR= np.zeros((dim,dim))
CI = np.zeros((dim,dim))

#print(CR)

N1R = np.zeros((dim,dim))
#N1R = np.ones((dim,dim))
N1I = np.zeros((dim,dim))

N2R = np.zeros((dim,dim))
#N2R = np.zeros((dim,dim))
N2I = np.zeros((dim,dim))


x = np.linspace(-bound,bound-step,num=dim)
y = np.linspace(-bound,bound-step,num=dim)

for i in range(dim):
	for j in range(dim):

		# theta = np.arctan2(y[j],x[i])

		N1R[i,j] = x[j] #np.cos(theta)
		N2R[i,j] = y[i] #np.sin(theta)

		mag = np.sqrt(x[i]**2+y[j]**2)

		if mag > 0.0:
			N1R[i,j] /= mag
			N2R[i,j] /= mag

		CR[i,j] = (np.sqrt(bound**2+bound**2) - mag)**2


mean=CR.mean()

CR=CR*concentration/(mean*dim*dim)
print(CR.sum())

# for i in range (dim):
# 	for j in range (dim):
# 		nx = N1R[i,j]
# 		ny = N2R[i,j]

# 		print(np.sqrt(nx**2+ny**2))

# RR = -1*np.ones((dim,dim))
# RI = np.zeros((dim,dim))


with h5py.File("input.h5", "w") as data_file:
	data_file.create_dataset("CR", data=CR)
	data_file.create_dataset("CI", data=CI)
	data_file.create_dataset("N1R", data=N1R)
	data_file.create_dataset("N1I", data=N1I)
	data_file.create_dataset("N2R", data=N2R)
	data_file.create_dataset("N2I", data=N2I)
	# data_file.create_dataset("RR", data=RR)
	# data_file.create_dataset("RI", data=RI)
	data_file.create_dataset("x", data=x)
	data_file.create_dataset("y", data=y)
