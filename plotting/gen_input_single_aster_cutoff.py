import numpy as np 
import h5py 

bound=10
dim = 20
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

		N1R[i,j] = x[j] + np.random.uniform(-x[j],x[j])/5 #np.cos(theta)
		N2R[i,j] = y[i] + np.random.uniform(-y[i],y[i])/5 #np.sin(theta)

		mag = np.sqrt(x[j]**2+y[i]**2)

		if mag > 0.0:
			if mag > bound*0.9:
				N1R[i,j] = np.random.uniform(-x[j],x[j])/10
				N2R[i,j] = np.random.uniform(-y[i],y[i])/10
			
			N1R[i,j] /= mag
			N2R[i,j] /= mag

		if mag < bound/4:
			CR[i,j] = (np.sqrt(bound**2+bound**2) - mag)**2 + np.random.uniform(0, concentration**(-1))
		else: CR[i,j] = np.random.uniform(0, concentration**(-1))


mean=CR.mean()

CR=CR*concentration/(mean*dim*dim)
print(CR.sum())

N1R = N1R[:,::-1]
N2R = N2R[:,::-1]

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
