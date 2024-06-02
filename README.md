# scener dataset

A dataset of 10,000 unique 3D scenes, each containing rendered images and corresponding 3D models in various formats, derived from ShapeNet classes.

#### 3D model:
![3d_models](https://github.com/imangali01/scener-dataset/blob/main/images/3d_models.png)

#### Rendered images:
![rendered_images](https://github.com/imangali01/scener-dataset/blob/main/images/rendered_images.png)

<hr>

Link to [download](https://github.com/imangali01/scener-dataset/releases/tag/v1.0) dataset

To generate your own dataset download 
[Blender2.9.0](https://download.blender.org/release/Blender2.90/)

1. add [binvox_converter](https://www.patrickmin.com/binvox/) to path
2. `C:/Program Files/Blender Foundation/Blender 2.90/2.90/python/lib` by this path add [binvox_rw](https://dimatura.net/misc_projects/binvox_rw_py/) to blender python libraries
3. basic run command: `blender --background --python main.py > ./logs/output.txt`

!Note:
After generating for several hours, the program starts to work slowly, and it will need to be restarted, this is the code that will run the code on generation and runs it in the subprocess:
`python run.py > ./logs/output.txt`

### Metadata
- 10000 sample unique 3d scenes

Used classes from ShapeNet dataset:<br>
![metadata.png](https://github.com/imangali01/scener-dataset/blob/main/images/metadata.png)

Folder structure:
```
scener_dataset
├───1001104546554069805
│   ├───images
│   │       img_r_010.png
│   │       img_r_026.png
│   │       img_r_042.png
│   │       img_r_058.png
│   │       img_r_074.png
│   │
│   └───model
│           model.mtl
│           model.obj
│           model_32.binvox
│           model_32.npz
│           model_64.binvox
│           model_64.npz
│
├───1001319629564954782
│   ├───images
│   │       img_r_010.png
│   │       img_r_026.png
│   │       img_r_042.png
│   │       img_r_058.png
│   │       img_r_074.png
│   │
│   └───model
│           model.mtl
│           model.obj
│           model_32.binvox
│           model_32.npz
│           model_64.binvox
│           model_64.npz
...
```

### Algorithm of placing objects in scene
![locations.png](https://github.com/imangali01/scener-dataset/blob/main/images/locations.png)
There are 11 fixed locations on the scene where objects can be placed on the scene, as shown in the picture.<br>
At each location, objects can rotate only at specified angles.<br>
<i>Allowed Rotation Angles</i>
```
1 - [0°]
2 - [0°]
3 - [0°]
4 - [0°]
5 - [0°]
6 - [0° - 90°]
7 - [0°, 90°, 180°]
8 - [270° - 360°]
9 - [90° - 180°]
10 - [0°, 180°]
11 - [180° - 270°]
```
This setup ensures that each object is placed logically within the constraints of the scene's design.
```
{
    'bookshelf': {
        'locations': [1, 2, 3, 4, 5],
        'synsetId': '02871439',
    },
    'sofa': {
        'locations': [2, 3, 4, 6, 8, 10],
        'synsetId': '04256520',
    },
    'trash': {
        'locations': [1, 5, 9, 10, 11],
        'synsetId': '02747177',
    },
    'stove': {
        'locations': [1, 2, 3, 4, 5],
        'synsetId': '04330267',
    },
    'table': {
        'locations': [6, 7, 8, 10],
        'synsetId': '04379243',
    },
    'piano': {
        'locations': [2, 3, 4, 6, 7, 8],
        'synsetId': '03928116',
    },
    'chair': {
        'locations': [6, 7, 8, 9, 10, 11],
        'synsetId': '03001627',
    }
}
```

### Used sources:
1. [3D binary voxel converter](https://www.patrickmin.com/binvox/)
2. [Binvox to numpy array converter](https://dimatura.net/misc_projects/binvox_rw_py/)
3. [ShapeNet dataset](https://shapenet.org/)
4. [Blender](https://download.blender.org/release/Blender2.90/])
