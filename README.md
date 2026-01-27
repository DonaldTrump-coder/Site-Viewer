# Site Viewer
A scene render for buildings or sites (surveying data) with GUI, displaying RGB rendering and depth rendering, supporting Point Cloud, Mesh, 2DGS, 3DGS.

## Environment
OS: Windows 10, Ubuntu<br>
CUDA: 12.4<br>
#### build the project
```
conda create -n meshrendering python=3.11
conda activate meshrendering
pip install torch==2.5.0 torchvision==0.20.0 torchaudio==2.5.0 --index-url https://download.pytorch.org/whl/cu124
pip install -r requirements.txt
pip install --no-build-isolation ./submodules/meshing_surfel_rasterization
```
#### run the GUI
```
python main.py
```