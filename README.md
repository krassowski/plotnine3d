# plotnine3d

3D geoms for [plotnine](https://github.com/has2k1/plotnine) (grammar of graphics in Python).

Status: experimental. Please leave feedback; pull requests welcome.


### Examples

Please refer to the [notebook with examples](https://github.com/krassowski/plotnine3d/blob/main/Examples.ipynb) for more details on data preparation.

#### Surface


```python
(
    ggplot_3d(mt_bruno_long)
    + geom_polygon_3d(size=0.01)
    + aes(x='x', y='y', z='height')
    + theme_minimal()
)
```

![surface](https://raw.githubusercontent.com/krassowski/plotnine3d/main/docs/images/surface.png)

#### Scatter

```python
(
    ggplot_3d(mtcars)
    + aes(
        x='hp', y='disp', z='mpg',
        shape='transmission',
        fill='transmission'
    )
    + theme_minimal()
    + scale_shape_manual(values={'automatic': 'o', 'manual': '^'})
    + geom_point_3d(stroke=0.25, size=3, color='black')
    + scale_fill_manual(values={'automatic': 'orange', 'manual': 'blue'})
)
```

![scatter](https://raw.githubusercontent.com/krassowski/plotnine3d/main/docs/images/scatter.png)

#### Voxels

```python
(
    ggplot_3d(voxels_long)
    + aes(x='x', y='y', z='z', fill='object')
    + geom_voxel_3d(size=0.01)
    + theme_minimal()
    + ylim(0, 8)
    + xlim(0, 8)
    + scale_fill_manual(values={
        'link': 'red',
        'cube1': 'blue',
        'cube2': 'green'
    })
)
```


![voxels](https://raw.githubusercontent.com/krassowski/plotnine3d/main/docs/images/voxels.png)

#### Line

```python
(
    ggplot_3d(data)
    + aes(x='x', y='y', z='z', color='z')
    + geom_line_3d(size=2)
    + theme_minimal()
)
```


![line](https://raw.githubusercontent.com/krassowski/plotnine3d/main/docs/images/line.png)


### Installation

Installation from PyPI:

```
pip install plotnine3d
```
