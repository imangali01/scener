import os
import time
import math
import random
import logging
import subprocess


import bpy
import numpy as np

import binvox_rw

# Настройка логгера
logging.basicConfig(filename='./logs/logs.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_blender_context():
    context = bpy.context
    scene = context.scene
    render = scene.render
    return context, scene, render


def clear_default_nodes(nodes):
    for n in nodes:
        nodes.remove(n)


def setup_scene(render, scene, engine='BLENDER_EEVEE', resolution=600, color_depth='8', format='PNG'):
    render.engine = engine
    render.image_settings.color_mode = 'RGBA'
    render.image_settings.color_depth = color_depth
    render.image_settings.file_format = format
    render.resolution_x = resolution
    render.resolution_y = resolution
    render.resolution_percentage = 100
    render.film_transparent = True

    scene.use_nodes = True
    scene.view_layers["View Layer"].use_pass_normal = True
    scene.view_layers["View Layer"].use_pass_diffuse_color = True
    scene.view_layers["View Layer"].use_pass_object_index = True


def setup_nodes(nodes, color_depth='8'):
    # Create normal output nodes
    scale_node = nodes.new(type="CompositorNodeMixRGB")
    scale_node.blend_type = 'MULTIPLY'
    scale_node.inputs[2].default_value = (0.5, 0.5, 0.5, 1)

    bias_node = nodes.new(type="CompositorNodeMixRGB")
    bias_node.blend_type = 'ADD'
    bias_node.inputs[2].default_value = (0.5, 0.5, 0.5, 0)

    # Create id map output nodes
    id_file_output = nodes.new(type="CompositorNodeOutputFile")
    id_file_output.label = 'ID Output'
    id_file_output.base_path = ''
    id_file_output.file_slots[0].use_node_format = True
    id_file_output.format.file_format = format
    id_file_output.format.color_depth = color_depth
    id_file_output.format.color_mode = 'BW'

    divide_node = nodes.new(type='CompositorNodeMath')
    divide_node.operation = 'DIVIDE'
    divide_node.use_clamp = False
    divide_node.inputs[1].default_value = 2**int(color_depth)

    return id_file_output


def delete_default_cube(context):
    # Delete default cube
    context.active_object.select_set(True)
    bpy.ops.object.delete()


def import_objects(obj_path, location, rotation):
    bpy.ops.import_scene.obj(filepath=obj_path)
    object = bpy.context.selected_objects[0]

    # Переводим координаты вершин на глобальную систему координат
    global_vertex = [object.matrix_world @ vertex.co for vertex in object.data.vertices]

    # Находим Z координату самой нижней точки объекта, Перемещаем объект так, чтобы его нижняя точка оказалась на уровне Z=0
    object.location.z -= min(global_vertex, key=lambda x: x.z).z - 0.001# min(vertex.co.y for vertex in object.data.vertices)

    if location[1] == -1:
        object.location.x = location[0]
        # Находим Y координату самой нижней точки объекта, Перемещаем объект так, чтобы его нижняя точка оказалась на уровне Y=0
        object.location.y = location[1] - min(global_vertex, key=lambda x: x.y).y + 0.001#min(vertex.co.z for vertex in object.data.vertices)
    else:
        object.location.x, object.location.y = location
    
    object.rotation_euler[2] = math.radians(rotation)


def add_plane_with_material(width, height, size, location, rotation, color, name):
    bpy.ops.mesh.primitive_plane_add(size=size, enter_editmode=False, location=location)
    plane = bpy.context.object

    plane.scale[0] = width  # X scale
    plane.scale[1] = height  # Y scale
    plane.name = name

    plane.rotation_euler = rotation
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = color
    plane.data.materials.append(material)


def setup_environment():
    # Add floor and background planes with materials
    add_plane_with_material(width=9, height=3, size=1, location=(0, 0.5, 0), rotation=(0,0,0), color=(0.45, 0.26, 0.07, 1), name="Plane-Floor")  # Floor
    add_plane_with_material(width=9, height=1.5, size=1, location=(0, -1, 0.75), rotation=(math.radians(90), 0, 0), color=(0.6, 0.26, 0.07, 1), name="Plane-Background")  # Background
    # add_plane_with_material(size=3, location=(-1.5, 0.5, 1.5), rotation=(math.radians(90), 0, math.radians(90)), color=(0.6, 0.26, 0.07, 1), name="BackgroundMaterial")  # Right plane


def adjust_planes_sides(width=None, height=None):
    for obj in bpy.data.objects:
        if "Plane" in obj.name:  # Adjust this condition based on your object naming
            if width is not None:
                obj.scale[0] = width
            if height is not None:
                obj.scale[1] = height


def setup_lights():
    # Lighting setup
    light = bpy.data.lights['Light']
    light.type = 'SUN'
    light.use_shadow = True
    light.specular_factor = 0.2
    light.energy = 10.0
    light_object = bpy.data.objects['Light']
    # light_object.rotation_euler[0] = math.radians(50)
    # light_object.rotation_euler[1] = math.radians(30)
    # light_object.rotation_euler[2] = math.radians(120)


def setup_camera():
    # Place and set up camera
    cam = scene.objects['Camera']
    x, y, z = 2, 2, 1.35
    cam.location = (x, y, z)
    cam.data.lens = 30
    cam.data.sensor_width = 30

    cam_constraint = cam.constraints.new(type='TRACK_TO')
    cam_constraint.track_axis = 'TRACK_NEGATIVE_Z'
    cam_constraint.up_axis = 'UP_Y'

    cam_empty = bpy.data.objects.new("Empty", None)
    cam_empty.location = (0, 0, 0)
    cam.parent = cam_empty

    scene.collection.objects.link(cam_empty)
    context.view_layer.objects.active = cam_empty
    cam_constraint.target = cam_empty

    return cam_empty


def remove_objects_with_substring(substring):
    # Собираем список объектов, которые нужно удалить
    to_remove = [obj for obj in bpy.context.scene.objects if substring in obj.name]
    
    # Удаляем каждый объект из списка
    for obj in to_remove:
        bpy.data.objects.remove(obj, do_unlink=True)


def save_obj_model(directory, filename):
    if not os.path.exists(directory):
        os.makedirs(directory)

    bpy.ops.export_scene.obj(filepath=f'{directory}/{filename}')


def clear_images(output_folder):
    files = os.listdir(output_folder)
    for i in files:
        os.remove(f'{output_folder}/{i}')


def convert_to_binvox(filepath, resolution=128, center_model=False):
    filename = os.path.basename(filepath).split('.')[0]
    binvox_file_path = f'{os.path.dirname(filepath)}/{filename}.binvox'
    new_binvox_file_path = f'{os.path.dirname(filepath)}/{filename}_{resolution}.binvox'

    if os.path.exists(binvox_file_path):
        os.remove(binvox_file_path)
    if os.path.exists(new_binvox_file_path):
        os.remove(new_binvox_file_path)

    command = ['binvox_converter', '-d', str(resolution), '-cb' if center_model else '', '-e', filepath]
    try:
        subprocess.run(command, check=True)
        os.rename(binvox_file_path, new_binvox_file_path)
    except subprocess.CalledProcessError as e:
        print("Error executing command:", e)


def convert_to_npz(filepath):
    filename = os.path.basename(filepath).split('.')[0]
    with open(filepath, 'rb') as f:
        model = binvox_rw.read_as_3d_array(f)
        np.savez(f'{os.path.dirname(filepath)}/{filename}.npz', data=model.data)



# Default values
views = 5
camera_start_angle = 10
camera_end_angle = 90
output_folder_path = './dataset'
dataset_path = './ShapeNet'
color_depth = '8'
format = 'PNG'
resolution = 600
engine = 'BLENDER_EEVEE'
DATASET_LENGTH = 100


# clear_images(f'{output_folder}/images')
context, scene, render = get_blender_context()
setup_scene(render=render, scene=scene, engine=engine, resolution=resolution, color_depth=color_depth, format=format)
nodes = scene.node_tree.nodes
clear_default_nodes(nodes=nodes)

# Create input render layer node
render_layers = nodes.new('CompositorNodeRLayers')
id_file_output = setup_nodes(nodes=nodes, color_depth=color_depth)
delete_default_cube(context=context)

setup_environment()
setup_lights()
cam_empty = setup_camera()
stepsize = (camera_end_angle - camera_start_angle) / views

# ----------------------------------------------------------------
# # Get the active camera
# cam = bpy.context.scene.camera.data

# # Camera parameters
# focal_length_mm = cam.lens                      # Focal length in millimeters
# sensor_width_mm = cam.sensor_width              # Sensor width in millimeters
# sensor_height_mm = cam.sensor_height            # Sensor height in millimeters
# image_width_px = bpy.context.scene.render.resolution_x  # Image width in pixels
# image_height_px = bpy.context.scene.render.resolution_y # Image height in pixels

# # Convert focal length from mm to pixels
# fx = (focal_length_mm / sensor_width_mm) * image_width_px
# fy = (focal_length_mm / sensor_height_mm) * image_height_px

# # Principal point (usually the center of the image)
# cx = image_width_px / 2
# cy = image_height_px / 2

# # Intrinsic matrix
# K = np.array([[fx,  0, cx],
#               [ 0, fy, cy],
#               [ 0,  0,  1]])

# print("Intrinsic Matrix:\n", K)
# ----------------------------------------------------------------


# Place objects
locations = {
    1: {'location': (2, -1), 'angle': 0},
    2: {'location': (1, -1), 'angle': 0},
    3: {'location': (0, -1), 'angle': 0},
    4: {'location': (-1, -1), 'angle': 0},
    5: {'location': (-2, -1), 'angle': 0},
    6: {'location': (1, 0), 'angle': random.randint(0, 90)},
    7: {'location': (0, 0), 'angle': random.choice([0, 90, 180])},
    8: {'location': (-1, 0), 'angle': random.randint(270, 360)},
    9: {'location': (1, 1), 'angle': random.randint(90, 180)},
    10: {'location': (0, 1), 'angle': random.choice([0, 180])},
    11: {'location': (-1, 1), 'angle': random.randint(180, 270)},
}

objects_class = {
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
    },
}


start_time = time.time()
step = 1

while step <= DATASET_LENGTH:
    print(f'[+] STARTED_STEP={step}')
    iter_start_time = time.time()   # fixing iteration start time

    adjust_planes_sides(width=9)
    remove_objects_with_substring('model_normalized')

    object_places = {}
    output_folder = []

    # select random position for object
    for object, meta in objects_class.items():
        object_location_choice = random.choice(list(set(meta['locations']) - set(object_places.keys())))
        object_places[object_location_choice] = object

    object_places = dict(sorted(object_places.items()))

    # import object to scene
    for location_id, object in object_places.items():
        path_ = dataset_path + '/' + objects_class[object]['synsetId']
        model_id = random.choice(os.listdir(path_)) # selecting random object from class
        object_path = path_ + '/' + model_id + '/models/model_normalized.obj'
        import_objects(obj_path=object_path, location=locations[location_id]['location'], rotation=locations[location_id]['angle'])
        output_folder.append(objects_class[object]['synsetId'] + '_' + model_id)    # prepare output folder name

    output_folder = output_folder_path + '/' + str(abs(hash('-'.join(output_folder))))

    if os.path.exists(output_folder):
        logging.error('folder already exists')
        continue

    print(f'[+] OBJECT_ID={output_folder}, STEP={step}')
    os.mkdir(output_folder)

    fp = os.path.join(os.path.abspath(output_folder), 'images', 'img')

    for i in range(views):
        # calculate camera angle
        camera_angle = camera_start_angle + i * stepsize
        # Update the camera's rotation
        cam_empty.rotation_euler[2] = math.radians(camera_angle)

        render_file_path = fp + '_r_{0:03d}'.format(int(camera_angle))

        scene.render.filepath = render_file_path
        id_file_output.file_slots[0].path = render_file_path + "_id"

        bpy.ops.render.render(write_still=True)

    adjust_planes_sides(width=5)
    save_obj_model(directory=f'{output_folder}/model', filename='model.obj')
    convert_to_binvox(filepath=f'{output_folder}/model/model.obj', resolution=64, center_model=False)
    convert_to_npz(filepath=f'{output_folder}/model/model_64.binvox')
    convert_to_binvox(filepath=f'{output_folder}/model/model.obj', resolution=32, center_model=False)
    convert_to_npz(filepath=f'{output_folder}/model/model_32.binvox')

    # logging time
    current_iter = time.time() - iter_start_time
    avg_time_per_iteration = (time.time() - start_time) / step
    remaining_time = avg_time_per_iteration * (DATASET_LENGTH - step)

    logging.info(f'STEP={step}, avg_time={avg_time_per_iteration:.2f}s, current_iter={current_iter:.2f}s, spent_time={(avg_time_per_iteration*step/60):.2f}min, remain ~ {remaining_time/60:.2f}min')

    step += 1

end_time = time.time()

execution_time = end_time - start_time
logging.info(f'[+] Execution time: {execution_time} seconds')
