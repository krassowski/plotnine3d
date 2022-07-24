from plotnine import geom_polygon, geom_point, geom_path, geom_text, geom_label
from plotnine.utils import to_rgba, SIZE_FACTOR
from plotnine.geoms.geom_path import _get_joinstyle
import numpy as np
from warnings import warn


class geom_line_3d(geom_path):
    REQUIRED_AES = {
        'x', 'y', 'z'
    }

    @staticmethod
    def draw_group(data, panel_params, coord, ax, **params):
        data = coord.transform(data, panel_params, munch=True)
        data['size'] *= SIZE_FACTOR
        constant = params.pop('constant', data['group'].nunique() == 1)
        join_style = _get_joinstyle(data, params)

        if constant:
            color = to_rgba(data['color'].iloc[0], data['alpha'].iloc[0])

            ax.plot(
                xs=data['x'].values,
                ys=data['y'].values,
                zs=data['z'].values,
                color=color,
                linewidth=data['size'].iloc[0],
                linestyle=data['linetype'].iloc[0],
                zorder=params['zorder'],
                rasterized=params['raster'],
                **join_style
            )
        else:
            # TODO: this is rather inefficient, geom_path has a better
            # segmentation implementation (rather than point-by-point)
            color = to_rgba(data['color'], data['alpha'])

            x = data['x'].values
            y = data['y'].values
            z = data['z'].values

            for i in range(len(data) - 1):
                ax.plot(
                    x[i:i + 2],
                    y[i:i + 2],
                    z[i:i + 2],
                    color=color[i],
                    linewidth=data['size'].iloc[i],
                    linestyle=data['linetype'].iloc[i],
                    zorder=params['zorder'],
                    rasterized=params['raster'],
                    **join_style
                )


class geom_polygon_3d(geom_polygon):
    REQUIRED_AES = {'x', 'y', 'z'}
    DEFAULT_PARAMS = {
        'lightsource': None,
        'antialiased': True,
        'shade': True,
        **geom_polygon.DEFAULT_PARAMS
    }

    @staticmethod
    def draw_group(data, panel_params, coord, ax, **params):
        data = coord.transform(data, panel_params, munch=True)
        data['size'] *= SIZE_FACTOR

        grouper = data.groupby('group', sort=False)
        for i, (group, df) in enumerate(grouper):
            fill = to_rgba(df['fill'], df['alpha'])

            ax.plot_trisurf(
                df['x'].values,
                df['y'].values,
                df['z'].values,
                facecolors=fill if any(fill) else 'none',
                edgecolors=df['color'] if any(df['color']) else 'none',
                linestyles=df['linetype'],
                linewidths=df['size'],
                zorder=params['zorder'],
                rasterized=params['raster'],
                antialiased=params['antialiased'],
                lightsource=params['lightsource'],
                shade=params['shade'],
            )


class geom_voxel_3d(geom_point):
    REQUIRED_AES = {'x', 'y', 'z'}
    DEFAULT_AES = {
        **geom_point.DEFAULT_AES,
        'fill': 'blue',
        'shape': 's'
    }

    @staticmethod
    def draw_group(data, panel_params, coord, ax, **params):
        data = coord.transform(data, panel_params, munch=True)
        data['size'] *= SIZE_FACTOR
        grouper = data.groupby('group', sort=False)
        for i, (group, df) in enumerate(grouper):
            fill = to_rgba(df['fill'], df['alpha'])

            voxel_grid = np.zeros((
                df['x'].max() + 1,
                df['y'].max() + 1,
                df['z'].max() + 1
            ))
            voxel_grid[df['x'], df['y'], df['z']] = 1
            fills = np.empty(voxel_grid.shape, dtype=object)
            fills[df['x'], df['y'], df['z']] = fill

            colors = np.empty(voxel_grid.shape, dtype=object)
            colors[df['x'], df['y'], df['z']] = df['color']

            ax.voxels(
                filled=voxel_grid,
                facecolors=fills,
                edgecolors=colors,
                zorder=params['zorder'],
            )


class geom_point_3d(geom_point):
    REQUIRED_AES = {'x', 'y', 'z'}
    DEFAULT_PARAMS = {
        'depthshade': True,
        **geom_point.DEFAULT_PARAMS
    }

    @staticmethod
    def draw_unit(data, panel_params, coord, ax, **params):
        size = ((data['size'] + data['stroke'])**2) * np.pi
        stroke = data['stroke'] * SIZE_FACTOR
        color = to_rgba(data['color'], data['alpha'])

        if all(c is None for c in data['fill']):
            fill = color
        else:
            fill = to_rgba(data['fill'], data['alpha'])

        # https://github.com/matplotlib/matplotlib/issues/23433
        stroke = set(stroke)

        if len(stroke) > 1:
            warn(
                'Variable stroke values not supported for `geom_point_3d` see'
                ' https://github.com/matplotlib/matplotlib/issues/23433'
            )
        stroke = next(iter(stroke))

        ax.scatter3D(
            data['x'],
            data['y'],
            data['z'],
            s=size,
            facecolor=fill,
            edgecolor=color,
            marker=data.loc[0, 'shape'],
            linewidths=stroke,
            depthshade=params['depthshade']
        )

    @staticmethod
    def draw_group(data, panel_params, coord, ax, **params):
        data = coord.transform(data, panel_params)
        units = 'shape'
        for _, udata in data.groupby(units, dropna=False):
            udata.reset_index(inplace=True, drop=True)
            geom_point_3d.draw_unit(udata, panel_params, coord, ax, **params)


class geom_text_3d(geom_text):
    """
    This class is reusing the code of `plotnine.geom_text` which is licensed under:

    The MIT License (MIT)

    Copyright (c) 2022 Hassan Kibirige

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
    """

    REQUIRED_AES = {
        'x', 'y', 'z',
        'label'
    }
    DEFAULT_AES = {
        'zdir': None,
        **geom_text.DEFAULT_AES
    }

    @staticmethod
    def draw_group(data, panel_params, coord, ax, **params):
        data = coord.transform(data, panel_params)

        # Bind color and alpha
        color = to_rgba(data['color'], data['alpha'])

        # Create a dataframe for the plotting data required
        # adding custom "params" mappings

        df = data[['x', 'y', 'z', 'size']].copy()
        df['zdir'] = data['zdir']
        df['s'] = data['label']
        df['rotation'] = data['angle']
        df['linespacing'] = data['lineheight']
        df['color'] = color
        df['ha'] = data['ha']
        df['va'] = data['va']
        df['family'] = params['family']
        df['fontweight'] = params['fontweight']
        df['fontstyle'] = params['fontstyle']
        df['zorder'] = params['zorder']
        df['rasterized'] = params['raster']
        df['clip_on'] = True

        # 'boxstyle' indicates geom_label so we need an MPL bbox
        draw_label = 'boxstyle' in params
        if draw_label:
            fill = to_rgba(data.pop('fill'), data['alpha'])
            if isinstance(fill, tuple):
                fill = [list(fill)] * len(data['x'])
            df['facecolor'] = fill

            if params['boxstyle'] in ('round', 'round4'):
                boxstyle = '{},pad={},rounding_size={}'.format(
                    params['boxstyle'],
                    params['label_padding'],
                    params['label_r'])
            elif params['boxstyle'] in ('roundtooth', 'sawtooth'):
                boxstyle = '{},pad={},tooth_size={}'.format(
                    params['boxstyle'],
                    params['label_padding'],
                    params['tooth_size'])
            else:
                boxstyle = '{},pad={}'.format(
                    params['boxstyle'],
                    params['label_padding'])
            bbox = {'linewidth': params['label_size'],
                    'boxstyle': boxstyle}
        else:
            bbox = {}

        texts = []

        # For labels add a bbox
        for i in range(len(data)):
            kw = df.iloc[i].to_dict()
            if draw_label:
                kw['bbox'] = bbox
                kw['bbox']['edgecolor'] = params['boxcolor'] or kw['color']
                kw['bbox']['facecolor'] = kw.pop('facecolor')

            text_elem = ax.text(**kw)
            texts.append(text_elem)
            if params['path_effects']:
                text_elem.set_path_effects(params['path_effects'])


class geom_label_3d(geom_text_3d):
    DEFAULT_AES = {
        **geom_text_3d.DEFAULT_AES,
        **geom_label.DEFAULT_AES
    }
    DEFAULT_PARAMS = {
        **geom_text_3d.DEFAULT_PARAMS,
        **geom_label.DEFAULT_PARAMS
    }

    @staticmethod
    def draw_legend(data, da, lyr):
        geom_label.draw_legend(data, da, lyr)
