import os
import shutil

def listdir_recursive(root):
    depth_one = os.listdir(root)
    result = []
    for item in depth_one:
        full_path = os.path.join(root, item)
        if (os.path.isdir(full_path)):
            result += listdir_recursive(full_path)
        else:
            result += [full_path]
    return result

def read_file(filename, encoding="UTF-8"):
    f = open(filename, encoding=encoding)
    result = f.read()
    f.close()
    return result

class HtmlPostProcessor:
    def __init__(self, footer_template, encoding="UTF-8"):
        self.FOOTER = read_file(footer_template)
        self.encoding = encoding

    def postprocess_file(self, input_path, output_path):
        input_text = read_file(input_path, self.encoding)
        output_text = input_text.replace("<auto-footer></auto-footer>", self.FOOTER)
        output_file = open(output_path, "w", encoding=self.encoding)
        output_file.write(output_text)
        output_file.close()

if __name__ == "__main__":
    proc = HtmlPostProcessor(os.path.join("randallscharpf.com", "FOOTER"))
    output_path = os.path.join("build", "website")
    shutil.copytree("randallscharpf.com", output_path, dirs_exist_ok=True)
    os.remove(os.path.join(output_path, "FOOTER"))
    website_files = listdir_recursive(output_path)

    for html_file in filter((lambda website_file: os.path.splitext(website_file)[1] == ".html"), website_files):
        proc.postprocess_file(html_file, html_file)
