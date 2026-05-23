import logging
import zipfile
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from kaggle.api.kaggle_api_extended import KaggleApi

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def download_kaggle_file(
    dataset_name: str,
    file_name: str,
    download_path: str,
    destination_dir: str = "data/raw"
) -> Optional[Path]:
    """
    Download a specific file from a Kaggle dataset.

    This function checks if the file already exists before attempting to
    download. If it does, the download is skipped. If the file is downloaded
    as a .zip archive, it is automatically extracted and the archive is deleted.

    Args:
        dataset_name (str): The Kaggle dataset identifier in format 'owner/dataset'.
                           Example: 'tahmidmir/credit-risk-dataset'
        file_name (str): The exact name of the file to download.
                        Example: 'train-FIN_ANA_DATA.xls'
        destination_dir (str): The destination directory for the downloaded file.
                              Defaults to 'data/raw'.

    Returns:
        Optional[Path]: The path to the downloaded/existing file if successful,
                       None if an error occurred.
    """

    try:
        # Convert to Path object for cross-platform compatibility
        dest_path = Path(destination_dir)
        target_file = dest_path / file_name
        target_zip = dest_path / f"{file_name}.zip"

        # Create destination directory if it doesn't exist
        dest_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Destination directory set to: {dest_path.resolve()}")

        # Check if file already exists
        if target_file.exists():
            logger.info(f"Data already exists, skipping download")
            return target_file

        # Check if .zip archive already exists
        if target_zip.exists():
            logger.info(f"Data archive already exists at {target_zip.resolve()}, skipping download")
            # If .zip exists but not extracted, extract it
            if not target_file.exists():
                logger.info(f"Extracting {target_zip.name}...")
                _extract_zip_file(target_zip, dest_path, file_name)
            return target_file

        # Initialize Kaggle API
        logger.info("Initializing Kaggle API...")
        api = KaggleApi()
        api.authenticate()
        logger.info("Kaggle API authentication successful")

        # Download the file
        logger.info(f"Downloading {download_path} from {dataset_name}...")
        api.dataset_download_file(dataset_name, download_path, path=str(dest_path))
        logger.info(f"Download completed for {download_path}")

        # Check if file was downloaded as .zip and extract if needed
        if target_zip.exists() and not target_file.exists():
            logger.info(f"File downloaded as .zip archive, extracting {target_zip.name}...")
            _extract_zip_file(target_zip, dest_path, download_path)

        # Verify the file exists after download
        if target_file.exists():
            logger.info(f"File successfully available at {target_file.resolve()}")
            return target_file
        else:
            logger.error(f"File {download_path} not found after download attempt")
            return None

    except FileNotFoundError as e:
        logger.error(f"Directory or file not found: {e}", exc_info=True)
        return None
    except PermissionError as e:
        logger.error(f"Permission denied while accessing files: {e}", exc_info=True)
        return None
    except zipfile.BadZipFile as e:
        logger.error(f"Downloaded file is not a valid zip archive: {e}", exc_info=True)
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred during download: {e}", exc_info=True)
        return None


def _extract_zip_file(zip_path: Path, destination_dir: Path, expected_file: str) -> None:
    """
    Extract a .zip file and clean up the archive.

    Args:
        zip_path (Path): Path to the .zip file to extract.
        destination_dir (Path): Directory where the file should be extracted.
        expected_file (str): The expected filename after extraction.

    Raises:
        Logs exceptions but does not raise them.
    """
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(path=str(destination_dir))
        logger.info(f"Successfully extracted {zip_path.name} to {destination_dir.resolve()}")

        # Delete the .zip file after extraction
        zip_path.unlink()
        logger.info(f"Deleted archive {zip_path.name} to keep directory clean")

    except zipfile.BadZipFile as e:
        logger.error(f"Failed to extract zip file {zip_path}: {e}", exc_info=True)
    except Exception as e:
        logger.error(f"An error occurred while extracting {zip_path}: {e}", exc_info=True)
