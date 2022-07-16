from plotnine import ggplot
import matplotlib.pyplot as plt


class ggplot_3d(ggplot):
    def _create_figure(self):
        figure = plt.figure()
        axs = [plt.axes(projection='3d')]

        figure._themeable = {}
        self.figure = figure
        self.axs = axs
        return figure, axs

    def _draw_labels(self):
        ax = self.axs[0]
        ax.set_xlabel(self.layout.xlabel(self.labels))
        ax.set_ylabel(self.layout.ylabel(self.labels))
        ax.set_zlabel(self.labels['z'])
