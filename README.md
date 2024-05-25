# scener dataset

Link to dataset [scener-dataset](https://github.com/imangali01/scener-dataset/releases/tag/v1.0)

To generate oun dataset run command:
`blender --background --python main.py > ./logs/output.txt`

After generating for several hours, the program starts to work slowly, and it will need to be restarted, this is the code that will run the code on generation and runs it in the subprocess:
`python run.py > ./logs/output.txt`
