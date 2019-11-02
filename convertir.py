import os
from reportlab.pdfgen import canvas


class LineWriter:
    def __init__(self, output_file="sample.pdf"):
        self.c = canvas.Canvas(output_file)

        self.width = 595
        self.height = 842
        self.font_size = 12
        self.font_distance = 5
        self.margin = 50

        self.normal_font = 'Helvetica'
        self.title_font = 'Helvetica-Bold'
        self.c.setPageSize((self.width, self.height))
        self.c.setFont(self.title_font, self.font_size)

        self.initial_line = self.height - self.margin
        self.curr_line = self.initial_line

    def add_line(self, text, font_name='Helvetica', i=0):
        if self.last_line():
            self.new_page()
            self.curr_line = self.initial_line
        line_decrease = self.font_size + self.font_distance
        self.c.setFont(font_name, self.font_size)
        text_exceeds_width = False
        max_chars = (self.width - 2 * self.margin) // (self.font_size//2) # 83
        if len(text) > max_chars:
            text_exceeds_width = True
            new_line_text = text[max_chars:]
            text = text[:max_chars]
        self.c.drawString(self.margin, self.curr_line, text)
        self.curr_line -= line_decrease
        if text_exceeds_width and i < 800:
            self.add_line(new_line_text, font_name, i+1)

    def new_page(self):
        self.c.showPage()  # ends current page
        self.curr_line = self.initial_line

    def last_line(self):
        if self.curr_line <= self.margin:
            return True
        else:
            return False

    def save(self):
        self.c.save()


folder = r"C:\Users\Ivan's PC\PycharmProjects\SistemaCitaMedico\SistemaCitaMedicoSite"
outputFile = "simefar.pdf"


def get_file_list(folder, ignore_folder=('media', 'photos', '__pycache__', 'migrations', 'fixtures')):
    files = os.listdir(folder)
    files = list(map(lambda file: os.path.join(folder, file), files))
    res = []
    for f in files:
        if os.path.isdir(f) and os.path.basename(f) not in ignore_folder:
            res += get_file_list(f)
        elif os.path.isfile(f):
            res.append(f)
    res.sort()
    return res


if __name__ == '__main__':
    files = get_file_list(folder)
    # for i in files:
    #     print(i)
    lw = LineWriter(outputFile)
    for fp in files:
        print(f"writing file {fp}")
        lw.add_line(fp.replace(folder, ""), font_name=lw.title_font)
        lw.add_line("")
        with open(fp, errors='ignore') as f:
            for l in f.readlines():
                lw.add_line(l[:-1])
        lw.new_page()
    # for i in range(0,20000):
    #     lw.add_line(f"{i}")
    lw.save()
