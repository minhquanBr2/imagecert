source /home/pc/miniconda3/etc/profile.d/conda.sh
conda activate imagecert-backend
conda env export > environment.yml
python3 -m uvicorn main:app --host 0.0.0.0 --port 8003 --reload