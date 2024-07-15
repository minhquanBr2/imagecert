import os

SRC_DIR = "/home/pc/imagecert/backend/src"                                      
TEMP_IMAGE_DIR = "/home/pc/imagecert/backend/data/images/temp"    
PERM_IMAGE_DIR = "/home/pc/imagecert/backend/data/images/perm"                          
DATABASE_DIR = "/home/pc/imagecert/backend/data/database"                       
IMAGEDB_PATH = "/home/pc/imagecert/backend/data/database/imagedb.db"  

# Verification status
VERIFICATION_STATUS = {
    "ACCEPTED": 0,
    "PENDING": 1,
    "REJECTED": 2
}