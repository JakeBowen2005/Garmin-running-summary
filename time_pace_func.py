#Time converter function
def time_converter(time_str):
    h,m,s = time_str.split(":")
    h = int(h)
    m = int(m)
    s = round(float(s))
    min_time = (60)*h+m+(s)/60
    return round(min_time, 2)

# Pace converter function
def pace_converter(pace):
    # Handle missing or invalid data
    if not isinstance(pace, str) or ":" not in pace:
        return 0

    parts = pace.split(":")

    # Expecting MM:SS or MM:SS.sss
    if len(parts) == 2:
        m, s = parts
        try:
            m = int(m)
            s = float(s)   # allow fractional seconds
        except ValueError:
            return 0
    else:
        return 0

    # Convert pace into float minutes per mile
    min_per_mile = m + (s / 60)
    return round(min_per_mile, 2)

#Turning float pace to real min per mile pace
def float_to_pace(pace):
    m = int(pace)
    s= round((pace -m)*60)
    if s == 60:
        m += 1
        s = 0

    return f"{m}:{s:02d}"