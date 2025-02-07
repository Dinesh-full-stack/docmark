import pandas as pd
import io


def convert_file_to_markdown(content: bytes, filename: str) -> str:
    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(content))
        else:
            df = pd.read_excel(io.BytesIO(content))

        df = df.fillna("")
        df.columns = [str(col).strip() for col in df.columns]

        return df.to_markdown(index=False)
    except Exception as e:
        raise ValueError(f"Failed to parse file: {str(e)}")
