import os


def save_to_csv(df, file_name="option_chain.csv"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, file_name)
    df.to_csv(file_path, index=False)
