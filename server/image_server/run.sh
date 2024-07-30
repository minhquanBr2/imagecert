source /home/pc/miniconda3/etc/profile.d/conda.sh
conda activate imagecert-backend
conda env export > environment.yml
python3 main.py