import subprocess
from version import __version__ as v


def create_dist():
    newfile = f'pdf_chainsaw_v.{v}'
    cmd = f"pyinstaller split_pdf.py --onefile --name {newfile}".split()
    subprocess.run(cmd)
    return newfile


if __name__ == '__main__':
    filename = create_dist()
