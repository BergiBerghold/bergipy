import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.tri as tri
from mpl_toolkits.axes_grid1 import make_axes_locatable
from cycler import cycler
import numpy as np

plt.style.use('dark_background')
rcParams['figure.figsize'] = (9, 5)
rcParams['figure.dpi'] = 250

modified_c_cycle = rcParams["axes.prop_cycle"].by_key()['color']
modified_c_cycle[0] = 'orange'
rcParams['axes.prop_cycle'] = cycler(color=modified_c_cycle)


def custom_cmap(n: int, name: str = 'hsv'):
    return plt.cm.get_cmap(name, n)


# TODO: Improve!!!
def irregular_2d_plot(x, y, z, x_label='', y_label='', title=None, interpolation=True):
    x = np.array(x)
    y = np.array(y)
    sorted_x = np.unique(x)
    sorted_y = np.unique(y)

    dx = np.min(np.diff(sorted_x))
    x_range = np.arange(sorted_x[0], sorted_x[-1] + dx, dx)

    dy = np.min(np.diff(sorted_y))
    y_range = np.arange(sorted_y[0], sorted_y[-1] + dy, dy)

    x_range = sorted_x
    y_range = sorted_y

    if interpolation:
        triang = tri.Triangulation(x, y)
        interpolator = tri.LinearTriInterpolator(triang, z)
        X, Y = np.meshgrid(x_range, y_range)
        array_2d = interpolator(X, Y)

    else:
        array_2d = np.zeros((len(x_range), len(y_range)))
        print(array_2d.shape)

        for _x, row in enumerate(array_2d):
            for _y, elem in enumerate(row):
                #measures_values_ids = np.where( (np.abs(x - x_range[_x]) < 1e-12) & (np.abs(y - y_range[_y]) < 1e-12) )[0]
                measures_values_ids = np.where((x == x_range[_x]) & (y == y_range[_y]))[0]

                if len(measures_values_ids) == 0:
                    array_2d[_x, _y] = np.nan
                elif len(measures_values_ids) == 1:
                    array_2d[_x, _y] = z[measures_values_ids[0]]
                else:
                    array_2d[_x, _y] = np.mean(np.array(z)[measures_values_ids])

        array_2d = array_2d.T

    # array_2d = scipy.ndimage.gaussian_filter(array_2d, sigma=2, radius=1)

    scatter_x = np.interp(x, (min(x), max(x)), (0, len(x_range) - 1))
    scatter_y = np.interp(y, (min(y), max(y)), (0, len(y_range) - 1))

    fig, ax = plt.subplots()

    im_plot = ax.imshow(array_2d, origin='lower')
    plt.title(title)

    ax.scatter(scatter_x, scatter_y, marker='x', color='red', s=1)

    for x, y in zip(scatter_x, scatter_y):
        occurrences = list(zip(scatter_x, scatter_y)).count((x, y))
        ax.annotate(occurrences, (x, y), color='white')

    # nx = max(1, len(x_range)//6)
    # ny = max(1, len(y_range)//6)
    nx = None
    ny = None
    plt.xticks(range(len(x_range))[::nx], x_range[::nx], rotation=90)
    plt.yticks(range(len(y_range))[::ny], y_range[::ny])
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(im_plot, cax=cax)

    fig.tight_layout()
    plt.show()
