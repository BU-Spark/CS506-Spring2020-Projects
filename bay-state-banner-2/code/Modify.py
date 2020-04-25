import os
PROJECT_DIR_PATH = os.path.dirname(os.path.abspath(os.path.abspath(__file__)))
DIR_PATH = os.path.join(PROJECT_DIR_PATH, '/Users/ymy/Downloads')
files = os.listdir(DIR_PATH)
def is_suffix_txt(suffix: str):
    if suffix == '.aspx':
        return True
    return False
for filename in files:
    name, suffix = os.path.splitext(filename)
    if is_suffix_txt(suffix):
        new_name = os.path.join(DIR_PATH, name) + '.pdf'
        old_name = os.path.join(DIR_PATH, filename)
        os.rename(old_name, new_name)