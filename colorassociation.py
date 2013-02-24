import colorsys

# Basic class for color database
class ColorDB:
    clrs = {}
    names = []
    
    def add_color (self, name, color):
        self.clrs[name] = color
        self.names.append(name)

    def between (self, color):
        for i in range(0, len(self.names)):
            k = i - 1
            if i == 0:
                k = len(self.names)-1
            if self.clrs[self.names[i]].hue > color.hue:
                k = i - 1
                if i == 0:
                    k = len(self.names)-1
                retlist = [self.clrs[self.names[k]]]
                retlist.append(self.clrs[self.names[i]])
                return retlist
                                
                 
# Basic class for individual colors
class Color:
    hue     = 0
    dance   = 0
    energy  = 0
    t_min   = 0
    t_max   = 0
    mode    = 0
    l_min   = 0
    l_max   = 0
    
    def __init__ (self, hue, dance, energy, t_min, t_max, mode, l_min, l_max):
        self.hue    = hue
        self.dance  = dance
        self.energy = energy
        self.t_min  = t_min
        self.t_max  = t_max
        self.mode   = mode
        self.l_min  = l_min
        self.l_max  = l_max

# http://stackoverflow.com/questions/214359/converting-hex-color-to-rgb-and-vice-versa
def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    if lv == 1:
        v = int(value, 16)*17
        return v, v, v
    if lv == 3:
        return tuple(int(value[i:i+1], 16)*17 for i in range(0, 3))
    return tuple(int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3))

# Single Point of Truth of Absolute Values
T_MIN = 0
T_MID = 110
T_MAX = 300
L_MIN = -60
L_MID = -14
L_MAX = 0

# Weights
dance_w     = 1
energy_w    = 1
t_min_w     = 1
t_max_w     = 1
mode_w      = 1
l_min_w     = 1
l_max_w     = 1

cls = []
nm  = []
nm.append ("red")
cls.append(Color (0.0,   0.5,   1.0,   T_MIN,  T_MAX,  0.5,  L_MID,  L_MAX))
nm.append ("yellow")
cls.append(Color (60.0,  1.0,   1.0,   T_MID,  T_MAX,  0,    L_MID,  L_MAX))
nm.append ("green")
cls.append(Color (120.0, 1.0,   0.75,  T_MID,  T_MAX,  0.5,  L_MIN,  L_MID))
nm.append ("cyan")
cls.append(Color (180.0, 1.0,   1.0,   T_MID,  T_MAX,  0.0,  L_MIN,  L_MID))
nm.append ("blue")
cls.append(Color (240.0, 0.0,   0.0,   T_MIN,  T_MID,  1.0,  L_MIN,  L_MAX))
nm.append ("magenta")
cls.append(Color (300.0, 1.0,   0.75,  T_MID,  T_MAX,  0.5,  L_MID,  L_MAX))
nm.append ("red-end")
cls.append(Color (360.0, 0.5,   1.0,   T_MIN,  T_MAX,  0.5,  L_MID,  L_MAX))

# Create the color database
colors = ColorDB ()
for i in range (0, len(cls)):
    colors.add_color(nm[i], cls[i])

hex_in = "#FF0000"
rgb = hex_to_rgb (hex_in)
hsv = colorsys.rgb_to_hsv (rgb[0], rgb[1], rgb[2])

hue = hsv[0] * 360
sat = float(hsv[1]*100)
bright = float(hsv[2]/255)*100

col_in = Color
col_in.hue = hue

col_left = colors.between(col_in)[0]
col_right = colors.between(col_in)[1]

mult = (hue%60)/60
# Assign attributes by algorithmically found values
col_in.dance    = dance_w  * (((1-mult)*col_left.dance) + (mult*col_right.dance))
col_in.energy   = energy_w * (((1-mult)*col_left.energy) + (mult*col_right.energy))
col_in.t_min    = t_min_w  * (((1-mult)*col_left.t_min) + (mult*col_right.t_min))
col_in.t_max    = t_max_w  * (((1-mult)*col_left.t_max) + (mult*col_right.t_max))
col_in.mode     = mode_w   * (((1-mult)*col_left.mode) + (mult*col_right.mode))
col_in.l_min    = l_min_w  * (((1-mult)*col_left.l_min) + (mult*col_right.l_min))
col_in.l_max    = l_max_w  * (((1-mult)*col_left.l_max) + (mult*col_right.l_max))
# Weight values with saturation and brightness weights
col_in.dance    *= (sat/100)
col_in.energy   *= (sat/100)
col_in.l_min    *= (sat/100)
col_in.l_max    *= (sat/100)



