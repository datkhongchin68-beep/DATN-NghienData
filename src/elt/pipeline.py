from pathlib import Path
from typing import Optional

from .extract import download_kaggle_file
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ELTPipeline:
    """
    Manages the Extract-Load-Transform pipeline.

    This class orchestrates the complete data processing workflow, starting
    with Kaggle dataset extraction.
    """

    KAGGLE_DATASET = "tahmidmir/credit-risk-dataset"
    TARGET_FILE = "train-FIN_ANA_DATA%20.xls"
    DOWNLOAD_PATH = f"Credit_Risk_Data_Set/{TARGET_FILE}"
    RAW_DATA_DIR = "data/raw"

    def __init__(self, raw_data_dir: str = RAW_DATA_DIR) -> None:
        """
        Initialize the ELT pipeline.

        Args:
            raw_data_dir (str): Directory for storing raw data.
                               Defaults to 'data/raw'.
        """
        self.raw_data_dir = raw_data_dir
        self.raw_data_path: Optional[Path] = None

    def extract(self) -> bool:
        """
        Execute the Extract phase of the pipeline.

        Downloads the required dataset from Kaggle if it doesn't already exist.

        Returns:
            bool: True if extraction was successful, False otherwise.
        """
        logger.info("=" * 60)
        logger.info("Starting ELT Pipeline - Extract Phase")
        logger.info("=" * 60)

        try:
            logger.info(
                f"Attempting to download '{self.TARGET_FILE}' from "
                f"'{self.KAGGLE_DATASET}' to '{self.raw_data_dir}'"
            )

            # Call the download function from extract module
            self.raw_data_path = download_kaggle_file(
                dataset_name=self.KAGGLE_DATASET,
                file_name=self.TARGET_FILE,
                download_path=self.DOWNLOAD_PATH,
                destination_dir=self.raw_data_dir
            )

            if self.raw_data_path:
                logger.info(
                    f"Extract phase completed successfully. "
                    f"Data available at: {self.raw_data_path.resolve()}"
                )
                return True
            else:
                logger.error("Extract phase failed - file could not be obtained")
                return False

        except Exception as e:
            logger.error(f"Unexpected error during extract phase: {e}", exc_info=True)
            return False

    def run(self) -> bool:
        """
        Execute the complete ELT pipeline.

        Currently implements the Extract phase. Can be extended to include
        Load and Transform phases.

        Returns:
            bool: True if the entire pipeline succeeds, False otherwise.
        """
        logger.info("Initializing ELT Pipeline")

        # Execute Extract phase
        if not self.extract():
            logger.error("Pipeline failed during Extract phase")
            return False

        logger.info("=" * 60)
        logger.info("ELT Pipeline completed successfully!")
        logger.info("=" * 60)
        return True
