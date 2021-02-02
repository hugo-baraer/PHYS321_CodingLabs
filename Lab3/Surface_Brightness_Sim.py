import numpy as np
from matplotlib import pyplot as plt
import imageio
from IPython.display import Image

def create_pos(nb_pixels, nb_stars):
    """
    :param nb_pixels:
    :param nb_stars:
    :return:
    """

    return np.random.uniform(0,nb_pixels,(nb_stars,2))


def histogram_star_pix(star_pos, nb_pixels):
    """
    :param star_pos:
    :param nb_pixels:
    :return:
    """
    edges = np.arange(nb_pixels + 1)
    return np.histogram2d(star_pos[:,1], star_pos[:,0],edges)

def stdflux_distance(nb_stars,histogram):
    """

    :param nb_stars:
    :param histogram:
    :return:
    """
    return (sqrt(nb_stars),np.std(histogram[0]))



nb_pixels = 20
std_fluxes=[]
distances= []
name = 'test'
for nb_stars in range (100, 1000,50):
    star_pos = create_pos(nb_pixels,nb_stars)
    histogram = histogram_star_pix(star_pos, nb_pixels)
    std_fluxes.append(np.std(histogram[0]))
    distances.append(np.sqrt(nb_stars))
    plt.imsave('{}_{}.jpg'.format(name,nb_stars),histogram[0], cmap = 'gray')

#quick video
with imageio.get_writer('{}.gif'.format(name), mode='I') as writer:
    for nb_stars in range (100, 1000,5):
        filename = '{}_{}.jpg'.format(name,nb_stars)
        image = imageio.imread(filename)
        writer.append_data(image)





fig, ax = plt.subplots()
ax.scatter(distances,std_fluxes)
plt.xlabel("Relative distance ")
plt.ylabel(r"$\sigma$ flux")
plt.show()






#proof
#sigma_flux = np.std(histogram)


#assumptions that there is a constant distance between stars

#define the shortes distsnce between the stars,
#with the short angle approximation, assuming a constant distance between stars, find the distance ot each galaxies.



"""
#bonus part histogram
fig, ax = plt.subplots()
ax.imshow(histogram[0], cmap = 'gray')
plt.tick_params(axis = "both", bottom = False, left = False, labelbottom = False, labelleft = False)
ax.plot(star_pos[:,0]-0.5,star_pos[:,1]-0.5, '*', c = 'yellow', mec = 'red')
plt.show()
"""