import os

print(len(set(os.listdir('scener_dataset_v1.1'))-set(os.listdir('scener_dataset_v1.2'))))
print(len(set(os.listdir('scener_dataset_v1.2'))-set(os.listdir('scener_dataset_v1.1'))))

f1 = sorted(os.listdir('scener_dataset_v1.1'))
f2 = sorted(os.listdir('scener_dataset_v1.2'))

print('--- scener_dataset_v1.1 ---')

for index, folder in enumerate(f1):
    folders = os.listdir(f'scener_dataset_v1.1/{folder}')

    if folders != ['images', 'model']:
        print(f'{index} - {folder} - error folder')

    if 'images' in folders:
        if os.listdir(f'scener_dataset_v1.1/{folder}/images') != ['img_r_010.png', 'img_r_026.png', 'img_r_042.png', 'img_r_058.png', 'img_r_074.png']:
            print(f'{index} - {folder} - error images')
    
    if 'model' in folders:
        if os.listdir(f'scener_dataset_v1.1/{folder}/model') != ['model.mtl', 'model.obj', 'model_32.binvox', 'model_32.npz', 'model_64.binvox', 'model_64.npz']:
            print(f'{index} - {folder} - error model')


print('\n\n\n--- scener_dataset_v1.2 ---')


for index, folder in enumerate(f2):
    folders = os.listdir(f'scener_dataset_v1.2/{folder}')

    if folders != ['images', 'model']:
        print(f'{index} - {folder} - error folder')

    if 'images' in folders:
        if os.listdir(f'scener_dataset_v1.2/{folder}/images') != ['img_r_010.png', 'img_r_026.png', 'img_r_042.png', 'img_r_058.png', 'img_r_074.png']:
            print(f'{index} - {folder} - error images')
    
    if 'model' in folders:
        if os.listdir(f'scener_dataset_v1.2/{folder}/model') != ['model.mtl', 'model.obj', 'model_32.binvox', 'model_32.npz', 'model_64.binvox', 'model_64.npz']:
            print(f'{index} - {folder} - error model')
