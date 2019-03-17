from laserloom import Loom

l = Loom()
l.loom_type = 'OPEN'
l.side_margin= 1/4.0
l.tooth_margin = 0.15
l.tpi = 10
l.working_size_length = 2.0
l.working_size_width = 2.0
l.generate()
print(l)
l.save('open_loom.svg')

l = Loom()
l.loom_type = 'PLATE'
l.side_margin= 1/8.0
l.tooth_margin = 1/4.0
l.strip_margin = 1/4.0
l.tpi = 8 
l.working_size_length = 2.0
l.working_size_width = 2.0
l.generate()
print(l)
l.save('plate_loom.svg')

l = Loom()
l.loom_type = 'PLATE'
l.side_margin= 1/8.0
l.tooth_margin = 1/4.0
l.strip_margin = 0
l.tpi = 6 
l.working_size_length = 7.0
l.working_size_width = 2.5
l.generate()
print(l)
l.save('long_plate_loom.svg')
