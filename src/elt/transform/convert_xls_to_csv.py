import pandas as pd
from pathlib import Path
from src.utils.logger import get_logger

logger = get_logger(__name__)

def convert_xls_to_csv(input_path: str, output_path: str) -> bool:
    """
    Converts a legacy Excel file (.xls) to a clean CSV file.

    Args:
        input_path (str): Path to the source .xls file.
        output_path (str): Path where the .csv file will be saved.

    Returns:
        bool: True if conversion was successful, False otherwise.
    """
    try:
        input_file = Path(input_path)
        output_file = Path(output_path)

        # Check if output file already exists to save resources
        if output_file.exists():
            logger.info(f"Output file already exists: {output_path}. Skipping conversion.")
            return True

        if not input_file.exists():
            logger.error(f"Input file not found: {input_path}")
            return False

        logger.info(f"Reading Excel file: {input_path}")
         
        # Using dtype=str for all columns to preserve leading zeros as per requirement.
        df = pd.read_excel(input_file, engine='xlrd', dtype=str)

        # 1. Strip leading/trailing whitespaces from column headers
        df.columns = [str(col).strip() for col in df.columns]
        
        # 2. Strip leading/trailing whitespaces from cell values
        logger.info(f"Found {len(df)} rows and {len(df.columns)} columns.")
        logger.info(f"Columns: {df.columns.tolist()}")

        # Ensure the directory for output exists
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # 3. Export to CSV
        df.to_csv(output_file, index=False, encoding='utf-8', quoting=1)

        logger.info(f"Successfully converted {input_path} to {output_path}")
        return True

    except Exception as e:
        logger.error(f"Error during XLS to CSV conversion: {str(e)}", exc_info=True)
        return False
