import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.tri as tri
import matplotlib as mpl
from matplotlib import cm
from mpl_toolkits.axes_grid1 import make_axes_locatable
from cycler import cycler
import numpy as np
import scipy


def use_plotting_defaults():
    plt.style.use('dark_background')

    plt.rc('figure', figsize=(9, 5))
    plt.rc('figure', dpi=250)

    # rcParams['figure.figsize'] = (9, 5)
    # rcParams['figure.dpi'] = 250

    modified_c_cycle = rcParams["axes.prop_cycle"].by_key()['color']
    modified_c_cycle[0] = 'orange'
    modified_c_cycle[1] = 'red'
    modified_c_cycle[2] = 'darkviolet'
    rcParams['axes.prop_cycle'] = cycler(color=modified_c_cycle)


def use_printplot_defaults():
    plt.rc('figure', figsize=(10, 5))
    plt.rc('figure', dpi=250)
    plt.rc('font', size=15)

    plt.rc('axes', labelpad=10)

    plt.rc('figure.subplot', top=0.95, bottom=0.15,
           left=0.08, right=0.92)

    # rcParams['figure.figsize'] = (10, 5)
    # rcParams['figure.dpi'] = 250
    # rcParams['font.size'] = 15

    # rcParams['axes.labelpad'] = 10

    # rcParams['figure.subplot.top'] = 0.95
    # rcParams['figure.subplot.bottom'] = 0.15
    #
    # rcParams['figure.subplot.left'] = 0.08
    # rcParams['figure.subplot.right'] = 0.92

    modified_c_cycle = rcParams["axes.prop_cycle"].by_key()['color']
    modified_c_cycle.pop(0)
    rcParams['axes.prop_cycle'] = cycler(color=modified_c_cycle)


def custom_cmap(n: int, name: str = 'hsv'):
    return plt.cm.get_cmap(name, n)


class GetCmapColor:
    def __init__(self, cmap_name, start_val, stop_val):
        self.cmap_name = cmap_name
        self.cmap = plt.get_cmap(cmap_name)
        self.norm = mpl.colors.Normalize(vmin=start_val, vmax=stop_val)
        self.scalarMap = cm.ScalarMappable(norm=self.norm, cmap=self.cmap)

    def get_rgb(self, val):
        rgb = np.array(self.scalarMap.to_rgba(val))[:-1] * 255
        return rgb.astype(np.uint8)


def irregular_2d_plot(x, y, z,
                      x_label=None, y_label=None, title=None,
                      interpolation=True, smooth=False,
                      n_x_intervals=35, n_y_intervals=20):
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)

    x_range, x_step = np.linspace(np.min(x), np.max(x), n_x_intervals, retstep=True)
    y_range, y_step = np.linspace(np.min(y), np.max(y), n_y_intervals, retstep=True)

    if interpolation:
        triang = tri.Triangulation(x, y)
        interpolator = tri.LinearTriInterpolator(triang, z)
        X, Y = np.meshgrid(x_range, y_range)
        array_2d = interpolator(X, Y)

    else:
        array_2d = np.zeros((n_x_intervals, n_y_intervals))

        for _x, row in enumerate(array_2d):
            for _y, elem in enumerate(row):
                measures_values_ids = np.where( (np.abs(x - x_range[_x]) < x_step / 2) &
                                                (np.abs(y - y_range[_y]) < y_step / 2) )[0]

                if len(measures_values_ids) == 0:
                    array_2d[_x, _y] = np.nan
                elif len(measures_values_ids) == 1:
                    array_2d[_x, _y] = z[measures_values_ids[0]]
                else:
                    array_2d[_x, _y] = np.mean(z[measures_values_ids])

        array_2d = array_2d.T

    if smooth:
        V = array_2d.copy()
        V[np.isnan(array_2d)] = 0
        VV = scipy.ndimage.gaussian_filter(V, sigma=smooth)

        W = np.ones(array_2d.shape)
        W[np.isnan(array_2d)] = 0
        WW = scipy.ndimage.gaussian_filter(W, sigma=smooth)

        WW[WW == 0] = np.nan
        array_2d = VV / WW

    scatter_x = np.interp(x, (np.min(x), np.max(x)), (0, len(x_range) - 1))
    scatter_y = np.interp(y, (np.min(y), np.max(y)), (0, len(y_range) - 1))

    fig, ax = plt.subplots()

    im_plot = ax.imshow(array_2d, origin='lower', aspect='auto')
    plt.title(title)

    ax.scatter(scatter_x, scatter_y, marker='x', color='red', s=1)

    for _x, _y in zip(scatter_x, scatter_y):
        occurrences = list(zip(scatter_x, scatter_y)).count((_x, _y))
        ax.annotate(occurrences, (_x, _y), color='white')

    x_decimal_places = max([len(str(_x).split('.')[-1]) for _x in x])
    y_decimal_places = max([len(str(_y).split('.')[-1]) for _y in y])

    nx = max(1, n_x_intervals//20)
    ny = max(1, n_y_intervals//15)
    plt.xticks(range(len(x_range))[::nx], [round(_x, x_decimal_places) for _x in x_range[::nx]], rotation=90)
    plt.yticks(range(len(y_range))[::ny], [round(_y, y_decimal_places) for _y in y_range[::ny]])
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(im_plot, cax=cax)

    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    use_plotting_defaults()

    x = np.linspace(0, 10, 100)
    y = np.linspace(0, 10, 100)

    #cmap = plt.cm.get_cmap('hsv', len(x))

    #cmap = plt.cm.get_cmap('hsv', len(x))

    cmap = mpl.colormaps.get_cmap('hsv', lut=len(x))

    for idx, (_x, _y) in enumerate(zip(x, y)):
        plt.scatter([_x], [_y], color=cmap(idx))

    plt.show()