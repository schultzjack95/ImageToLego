import tkinter as tk
from tkinter import filedialog


def acquireImage():
    """
    User selects an image file.
    :return: the selected image filename
    :rtype: String
    """
    root = tk.Tk()
    root.withdraw()

    print("Please select an image file.")
    
    file_path = filedialog.askopenfilename()
    return file_path

