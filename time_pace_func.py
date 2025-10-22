#Time converter function
def time_converter(str):
    h,m = str.split(":")
    h = int(h)
    m = int(m)
    return (60)*h+m

# Pace converter function
def pace_converter(pace):
    m,s = pace.split(":")
    m = int(m)
    s = int(s)
    s = s*((5/3))
    s = s/100
    final_pace = m+s
    return final_pace