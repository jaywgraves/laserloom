from laserloom import Loom

l = Loom()
l.loom_type = 'OPEN'
l.side_margin= 1/4.0
l.tooth_margin = 0.15
l.tpi = 10
l.working_size_length = 0.5
l.working_size_width = 2.0
l.include_background = True 
l.generate()
print(l)
l.save('tpi_10.svg')

l.tpi = 8
l.generate()
print(l)
l.save('tpi_8.svg')

l.tpi = 6
l.generate()
print(l)
l.save('tpi_6.svg')

l.tpi = 4
l.generate()
print(l)
l.save('tpi_4.svg')