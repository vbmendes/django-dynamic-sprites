# coding: utf8


class OutputCss(str):

    def save(self, file_path):
        with open(file_path, 'w') as f:
            f.write(self + '\n')
