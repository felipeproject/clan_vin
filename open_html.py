import os
import webview

html_file_path = 'index.html'

if not os.path.exists(html_file_path):
    raise FileNotFoundError(f"The file {html_file_path} does not exist.")

webview.create_window('Meu App Web', html_file_path)
webview.start()
