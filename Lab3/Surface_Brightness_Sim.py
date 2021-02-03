import numpy as np
from matplotlib import pyplot as plt
import imageio
# from IPython.display import Image

def create_pos(nb_pixels, nb_stars):
    """
    Generate random star positions within a square window
    :param nb_pixels: [int] number of squares in one row/column of the square window
    :param nb_stars: [int] number of stars to generate
    :return: [array] an array of x and y coordinates of the stars
    """

    return np.random.uniform(0,nb_pixels,(nb_stars,2))


def histogram_star_pix(star_pos, nb_pixels, weighted=False):
    """
    Bin the star positions into square "pixels" within the square window
    :param star_pos: [array] an array of star postions with x and y coordinates
    :param nb_pixels: [int] number of squares in one row/column of the square window
    :return: [np.histogram] a histogram object containing the bin information
    """
    edges = np.arange(nb_pixels + 1)
    if weighted:
        weights = np.random.normal(3,1,len(star_pos))
        return np.histogram2d(star_pos[:,1], star_pos[:,0],edges, weights=weights), weights
    else:
        return np.histogram2d(star_pos[:,1], star_pos[:,0],edges)

def stdflux_distance(nb_stars,histogram):
    """

    :param nb_stars:
    :param histogram:
    :return:
    """
    return np.sqrt(nb_stars),np.std(histogram[0])



nb_pixels = 10
std_fluxes=[]
distances= []
name = 'test'
# for nb_stars in np.linspace(100, 100000, 100, dtype=int):
#     star_pos = create_pos(nb_pixels,nb_stars)
#     histogram = histogram_star_pix(star_pos, nb_pixels)
#     std_fluxes.append(np.std(histogram[0]))
#     distances.append(np.sqrt(nb_stars))
#     plt.imsave('./tmp/{}_{}.jpg'.format(name,nb_stars),np.kron(histogram[0],np.ones((50,50))), cmap = 'gray')
#


#bonus part histogram
for nb_stars in np.exp(np.linspace(1, 16, 100)).astype(int):
    fig, ax = plt.subplots(figsize=(5,5))
    star_pos = create_pos(nb_pixels, nb_stars)
    histogram, weights= histogram_star_pix(star_pos, nb_pixels, weighted=True)
    std_fluxes.append(np.std(histogram[0]/nb_stars))
    distances.append(np.sqrt(nb_stars))
    image = ax.imshow(histogram[0])
    image.set_clim(0,np.max(histogram[0]))
    ax.text(1,1,"stars: {}".format(nb_stars), fontsize=15,bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10} )
    plt.tick_params(axis = "both", bottom = False, left = False, labelbottom = False, labelleft = False)
    # plt.show()
    # plt.savefig('./tmp/{}_{}.jpg'.format(name,nb_stars))
    plt.close()
# for i in range(len(star_pos)):
#     ax.plot(star_pos[:,0][i]-0.5,star_pos[:,1][i]-0.5, '*', c = 'yellow', mec='red',ms=weights[i]*2)
# #quick video
with imageio.get_writer('{}.gif'.format(name), mode='I') as writer:
    for nb_stars in np.exp(np.linspace(1, 16, 100)).astype(int):
        filename = './tmp/{}_{}.jpg'.format(name,nb_stars)
        image = imageio.imread(filename)
        writer.append_data(image)



fig, ax = plt.subplots()
ax.scatter(np.power(distances,-1),std_fluxes)
plt.xlabel("1/distance ")
plt.ylabel(r"$\sigma$ flux")
plt.show()






#proof
#sigma_flux = np.std(histogram)


#assumptions that there is a constant distance between stars

#define the shortes distsnce between the stars,
#with the short angle approximation, assuming a constant distance between stars, find the distance ot each galaxies.




