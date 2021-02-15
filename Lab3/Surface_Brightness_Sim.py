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
    :param weighted: [bool] give the stars random gaussian distributed brightnesses if True
    :return: [np.histogram] a histogram object containing the bin information
    """
    edges = np.arange(nb_pixels + 1)

    if weighted:
        # give the stars random gaussian distributed brightnesses
        weights = np.abs(np.random.normal(10,5,len(star_pos)))
        return np.histogram2d(star_pos[:,1], star_pos[:,0],edges, weights=weights), weights
    else:
        return np.histogram2d(star_pos[:,1], star_pos[:,0],edges), None

def std_flux(nb_stars,histogram):
    """
    compute the standard deviation of the flux
    :param nb_stars: [int] number of stars that were used in the histogram
    :param histogram: [np.histogram] the histogram of the stars in the pixels
    :return: [float] the standard deviation of the flux
    """
    # note, we divide by the distance squared to account for the inverse square law of the flux
    # The distance squared is the same as the number of stars (see txt file)
    return np.std(histogram[0]/nb_stars)

########################################################################################################################
# create a figure of the stars and the pixels they fall into
fig, ax = plt.subplots(figsize=(5,5))
# create random star positions
star_pos = create_pos(10, 100)
# fit star positions into a grid of pixels
histogram, weights= histogram_star_pix(star_pos, 10, weighted=True)
image = ax.imshow(histogram[0],cmap="inferno")
# anchor the color map minimum value to 0
image.set_clim(0, np.max(histogram[0]))
for i in range(len(star_pos)):
    # show brightness as size
    ax.plot(star_pos[:,0][i]-0.5,star_pos[:,1][i]-0.5, '*', c = 'yellow', mec='red',ms=weights[i],alpha=0.8)
plt.show()

########################################################################################################################
# create an animated gif of the variation of the flux with increasing distance/number of stars
# set the number of pixels for the animation
nb_pixels = 10

std_fluxes=[]
distances= []
name = 'animation'
# iteratively create and save figures with fluxes generated by an increasing amount of stars
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
    plt.savefig('./tmp/{}_{}.jpg'.format(name,nb_stars))
    plt.close()

# add figures together to create a gif
with imageio.get_writer('{}.gif'.format(name), mode='I') as writer:
    for nb_stars in np.exp(np.linspace(1, 16, 100)).astype(int):
        filename = './tmp/{}_{}.jpg'.format(name,nb_stars)
        image = imageio.imread(filename)
        writer.append_data(image)


########################################################################################################################
# plot the standard deviation of the fluxes as a function of the inverse of the distance
nb_stars = np.exp(np.linspace(1, 16, 100)).astype(int)
# nb_stars = np.linspace(1, 100, 100).astype(int)
fig, ax = plt.subplots()
std_fluxes=[]
inv_distances= []
for number in nb_stars:
    hist, w = histogram_star_pix(create_pos(nb_pixels, number), nb_pixels, True)
    # recall the distance is proportional to the sqrt of the number of stars (see txt document)
    inv_distances.append(np.power(number,-0.5))
    std_fluxes.append(std_flux(number,hist))

# do a linear fit on the data
fit = np.polyfit(inv_distances,std_fluxes,1)
ax.scatter(inv_distances,std_fluxes)
ax.plot(inv_distances, fit[0]*np.array(inv_distances)+fit[1], '--', c="r", label="linear fit")
plt.xlabel("1/distance ")
plt.ylabel(r"$\sigma$ flux")
plt.legend()
plt.show()





"""
Marion bar chart code 

x = np.linspace(1,6,6)
heights = [720, 670, 670, 720, 695, 695]
labels = ['Accelerating upwards ',
'Slowing down upwards ',
'Accelerating downwards ',
'Slowing down downwards ',
'Moving at constant speed ',
'At rest'
]
fig, ax = plt.subplots(figsize=(25, 10))
ax.bar(x,heights)
ax.set_ylabel('Normal force recorded on the scale [N]',fontsize  = 20)
ax.set_title('Normal forces recorded on a scale in an elevator based on the motion of the elevator', fontsize  = 20)
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_xlabel('Motion of the elevator', fontsize  = 20)
ax.legend()

plt.show()
"""





