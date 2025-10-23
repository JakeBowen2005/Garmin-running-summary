#Time converter function
def time_converter(time_str):
    h,m,s = time_str.split(":")
    h = int(h)
    m = int(m)
    s = int(s)
    min_time = (60)*h+m+(s)/60
    return round(min_time, 2)

# Pace converter function
def pace_converter(pace):
    m,s = pace.split(":")
    m = int(m)
    s = int(s)
    s = s*((5/3))
    s = s/100
    final_pace = m+s
    return round(final_pace,2)

#Turning float pace to real min per mile pace
def float_to_pace(pace):
    m = int(pace)
    s= round((pace -m)*60)
    if s == 60:
        m += 1
        s = 0

    return f"{m}:{s:02d}" 