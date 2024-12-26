import os
import shutil
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def backup_chromadb():
    try:
        source_dir = "./chroma_db"
        if not os.path.exists(source_dir):
            logger.error(f"Source directory {source_dir} does not exist")
            return False

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = f"./backups/chromadb_{timestamp}"
        
        os.makedirs(os.path.dirname(backup_dir), exist_ok=True)
        shutil.copytree(source_dir, backup_dir)
        
        logger.info(f"Successfully backed up ChromaDB to {backup_dir}")
        return True
    except Exception as e:
        logger.error(f"Error backing up ChromaDB: {str(e)}")
        return False

def cleanup_old_backups(max_backups=5):
    try:
        backup_dir = "./backups"
        if not os.path.exists(backup_dir):
            return
        
        backups = [os.path.join(backup_dir, d) for d in os.listdir(backup_dir)]
        backups.sort(key=lambda x: os.path.getctime(x), reverse=True)
        
        for backup in backups[max_backups:]:
            shutil.rmtree(backup)
            logger.info(f"Removed old backup: {backup}")
    except Exception as e:
        logger.error(f"Error cleaning up old backups: {str(e)}")

if __name__ == "__main__":
    if backup_chromadb():
        cleanup_old_backups()