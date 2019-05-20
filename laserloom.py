import svgwrite
from svgwrite import inch  


CSS_STYLES = """
    .background { fill: white; }
    .cut {stroke: red; stroke-width: .01; fill-opacity:0;}
    .vectorengrave { stroke: blue; stroke-width: .01; fill: blue; }
"""
TOOTH_DEPTH_DEFAULT = 3.0 / 16
TOOTH_MARGIN_DEFAULT = 0.25


TPI = {
    #    total width, gap  (difference is 'pin' width)
    4:  [1.0 / 4,  0.15],
    6:  [1.0 / 6,  0.10],
    8:  [1.0 / 8,  0.06],
    10: [1.0 / 10, 0.05]
} 

class Loom(object):
    def __init__(self, filename='output.svg'):
        self.filename = filename
        self.loom_type = ''   # OPEN, PLATE
        self.working_size_width = 0.0     # should divide evenly with TPI
        self.working_size_length = 0.0
        self.tpi = 0
        self.tooth_depth = TOOTH_DEPTH_DEFAULT 
        self.tooth_margin = TOOTH_MARGIN_DEFAULT
        self.side_margin = 0.0
        self.strip_margin = 0.0
        self.total_width = 0.0
        self.total_length = 0.0
        self.engrave_info = True
        self.include_background = True
    
    def generate(self):
        self.total_width = self.working_size_width + (2 * self.side_margin)
        self.total_length = self.working_size_length + (2 * self.tooth_depth) + (2 * self.tooth_margin) + (4 * self.strip_margin)
        if self.loom_type == 'PLATE' and not self.strip_margin:
            self.total_length += (2 * self.tooth_margin)
        self.dwg = svgwrite.Drawing(self.filename, 
                                    size=(self.total_width*inch, self.total_length*inch), 
                                    viewBox="0 0 {0} {1}".format(self.total_width, self.total_length)
        )
        self.dwg.defs.add(self.dwg.style(CSS_STYLES))
        if self.include_background:
            self.dwg.add(self.dwg.rect(size=('100%','100%'), class_='background'))
        
        tpi_width, tpi_gap = TPI.get(self.tpi, (None, None))
        if tpi_width is None:
            raise ValueError('TPI size must be one of (%s)' % ",".join(str(tpi) for tpi in sorted(TPI.keys())))
        tooth_count = int(self.working_size_width * self.tpi)
        if self.engrave_info:
            engrave_string = 'LaserLoom %sx%s (%i TPI)' % (str(self.working_size_width), str(self.working_size_length), self.tpi)
            engrave_x = self.working_size_length + self.tooth_depth + self.tooth_margin + (2 * self.strip_margin) - .20
            self.dwg.add(
                self.dwg.text(engrave_string,
                              insert=(0,0),
                              transform="rotate(-90 0,0) translate(-%s, .18)" % (engrave_x, ),
                              font_size=".12",
                              font_family="sans-serif",
                              class_="vectorengrave"
                             )
            )
        # top teeth
        start_xy = (self.side_margin + (tpi_width/4), 0.0)
        self.make_teeth(start_xy, self.tooth_depth, tpi_width, tpi_gap, tooth_count)
        # bottom teeth
        start_xy = (self.side_margin + (tpi_width/4), self.total_length - self.tooth_depth)
        self.make_teeth(start_xy, self.tooth_depth, tpi_width, tpi_gap, tooth_count)

        if self.loom_type == 'OPEN':
            # inside cutout
            start_x = self.side_margin
            start_y = self.tooth_depth + self.tooth_margin
            self.dwg.add(
                self.dwg.rect(insert=(start_x, start_y), size=(self.working_size_width, self.working_size_length), rx=0.1, ry=0.1, class_='cut')
            )
        elif self.loom_type == 'PLATE':
            # top strip
            start_x = 0
            start_y = self.tooth_depth + self.tooth_margin
            if self.strip_margin:
                self.dwg.add(
                    self.dwg.rect(insert=(start_x, start_y), size=(self.total_width, self.strip_margin), class_='cut')
                )
                start_y +=  2 * self.strip_margin
                self.dwg.add(
                    self.dwg.line(start=(start_x, start_y),  end=(self.total_width, start_y), class_='vectorengrave')
                )
            else:
                self.dwg.add(
                    self.dwg.line(start=(start_x, start_y),  end=(self.total_width, start_y), class_='cut')
                )
                start_y += self.tooth_margin
                self.dwg.add(
                    self.dwg.line(start=(start_x, start_y),  end=(self.total_width, start_y), class_='vectorengrave')
                )
            # bottom strip
            start_x = 0
            start_y = self.total_length - self.tooth_depth - self.tooth_margin - self.strip_margin
            if self.strip_margin:
                self.dwg.add(
                    self.dwg.rect(insert=(start_x, start_y), size=(self.total_width, self.strip_margin), class_='cut')
                )
                start_y -=  self.strip_margin
                self.dwg.add(
                    self.dwg.line(start=(start_x, start_y),  end=(self.total_width, start_y), class_='vectorengrave')
                )
            else:
                self.dwg.add(
                    self.dwg.line(start=(start_x, start_y),  end=(self.total_width, start_y), class_='cut')
                )
                start_y -=  self.tooth_margin
                self.dwg.add(
                    self.dwg.line(start=(start_x, start_y),  end=(self.total_width, start_y), class_='vectorengrave')
                )
        # outside cleanup
        self.dwg.add(self.dwg.rect(size=(self.total_width,self.total_length), rx=0.1, ry=0.1, class_='cut'))

    def make_teeth(self, start_xy, depth, width, gap, count):
        x,y = start_xy
        for i in range(count):
            self.dwg.add(
                self.dwg.rect(insert=(x,y), size=(gap, depth), class_='cut' )
            )
            x += width

    def save(self, filename=None):
        if filename:
            self.dwg.saveas(filename, pretty=True)
        else:
            self.dwg.save(pretty=True)
    
    def __str__(self):
        vals = (self.loom_type,
                self.tpi,
                self.working_size_width, 
                self.working_size_length, 
                self.total_width,
                self.total_length)
        return "Loom - %s with %i TPI, working size=(%f,%f) total_size=(%f, %f)" % vals

def main():
    l = Loom()
    l.loom_type = 'OPEN'
    l.side_margin= 1/4.0
    l.tooth_margin = 0.15
    
    #l.loom_type = 'PLATE'
    #l.side_margin= 1/8.0
    #l.tooth_margin = 1/4.0
    #l.strip_margin = 1/4.0

    l.tpi = 8
    l.working_size_length = 2.0
    l.working_size_width = 2.0
    l.generate()
    print(l)
    l.save()


if __name__== '__main__':
    main()