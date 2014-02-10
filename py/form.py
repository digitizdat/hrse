"""Functions that relate to form manipulation for the HRSE

"""



def formvars(data):
    """Return a dictionary of variables for use with the yourinfo.html template

    This is all the work needed to pre-populate the form fields with any
    values already existing in the database for this participant (er, browser
    fingerprint).

    """
    # Initialize all the form variables to empty strings.
    results = {
      'age_lt12': '',
      'age_lt18': '',
      'age_lt25': '',
      'age_lt35': '',
      'age_lt45': '',
      'age_lt55': '',
      'age_lt65': '',
      'age_ge75': '',
      'sex_m': '',
      'sex_f': '',
      'handed_l': '',
      'handed_r': '',
      'color_red': '',
      'color_orange': '',
      'color_yellow': '',
      'color_green': '',
      'color_blue': '',
      'color_purple': '',
      'color_pink': '',
      'color_brown': '',
      'color_black': '',
      'color_white': '',
      'curzip': '',
      'enoughhours_y': '',
      'enoughhours_n': '',
      'suppow_flight': '',
      'suppow_telep': '',
      'suppow_invis': '',
      'suppow_healing': '',
      'suppow_strength': '',
      'suppow_mindre': '',
      'suppow_mindco': '',
      'suppow_mindco': '',
      'suppow_intel': '',
      'suppow_timetrav': '',
      'suppow_timefrez': '',
      'residence': '',
      'family_y': '',
      'family_n': '',
      'pets_y': '',
      'pets_n': '',
      'mari_single': '',
      'mari_married': '',
      'mari_divorced': '',
      'mari_widowed': '',
      'mari_civunion': '',
      'mari_dompart': '',
      'mari_separated': '',
      'mari_cohab': '',
      'military_y': '',
      'military_n': '',
      'edu_none': '',
      'edu_elem': '',
      'edu_hs': '',
      'edu_somecol': '',
      'edu_trade': '',
      'edu_assoc': '',
      'edu_under': '',
      'edu_master': '',
      'edu_prof': '',
      'edu_doctor': ''}


    if data['age'] == 'lt12': results['age_lt12'] = 'selected'
    elif data['age'] == 'lt18': results['age_lt18'] = 'selected'
    elif data['age'] == 'lt25': results['age_lt25'] = 'selected'
    elif data['age'] == 'lt35': results['age_lt35'] = 'selected'
    elif data['age'] == 'lt45': results['age_lt45'] = 'selected'
    elif data['age'] == 'lt55': results['age_lt55'] = 'selected'
    elif data['age'] == 'lt65': results['age_lt65'] = 'selected'
    elif data['age'] == 'ge75': results['age_ge75'] = 'selected'

    if data['sex'] == 'male': results['sex_m'] = 'checked'
    elif data['sex'] == 'female': results['sex_f'] = 'checked'

    if data['handed'] == 'left': results['handed_l'] = 'checked'
    elif data['handed'] == 'right': results['handed_r'] = 'checked'

    if data['favcolor'] == 'red': results['color_red'] = 'selected'
    elif data['favcolor'] == 'orange': results['color_orange'] = 'selected'
    elif data['favcolor'] == 'yellow': results['color_yellow'] = 'selected'
    elif data['favcolor'] == 'green': results['color_green'] = 'selected'
    elif data['favcolor'] == 'blue': results['color_blue'] = 'selected'
    elif data['favcolor'] == 'purple': results['color_purple'] = 'selected'
    elif data['favcolor'] == 'pink': results['color_pink'] = 'selected'
    elif data['favcolor'] == 'brown': results['color_brown'] = 'selected'
    elif data['favcolor'] == 'black': results['color_black'] = 'selected'
    elif data['favcolor'] == 'white': results['color_white'] = 'selected'

    if data['curzip'] != 'na': results['curzip'] = data['curzip']

    if data['enoughhours'] == 'yes': results['enoughhours_y'] = 'checked'
    elif data['enoughhours'] == 'no': results['enoughhours_n'] = 'checked'

    if data['superpower'] == 'flight': results['suppow_flight'] = 'selected'
    elif data['superpower'] == 'teleport': results['suppow_telep'] = 'selected'
    elif data['superpower'] == 'invisible': results['suppow_invis'] = 'selected'
    elif data['superpower'] == 'healing': results['suppow_healing'] = 'selected'
    elif data['superpower'] == 'strength': results['suppow_strength'] = 'selected'
    elif data['superpower'] == 'mindre': results['suppow_mindre'] = 'selected'
    elif data['superpower'] == 'mindco': results['suppow_mindco'] = 'selected'
    elif data['superpower'] == 'intelligence': results['suppow_intel'] = 'selected'
    elif data['superpower'] == 'timetravel': results['suppow_timetrav'] = 'selected'
    elif data['superpower'] == 'timefreeze': results['suppow_timefrez'] = 'selected'

    if data['residence'] != 'na': results['residence'] = data['residence']

    if data['family'] == 'yes': results['family_y'] = 'checked'
    elif data['family'] == 'no': results['family_n'] = 'checked'

    if data['pets'] == 'yes': results['pets_y'] = 'checked'
    elif data['pets'] == 'no': results['pets_n'] = 'checked'

    if data['maritalstatus'] == 'single': results['mari_single'] = 'selected'
    elif data['maritalstatus'] == 'married': results['mari_married'] = 'selected'
    elif data['maritalstatus'] == 'divorced': results['mari_divorced'] = 'selected'
    elif data['maritalstatus'] == 'widowed': results['mari_widowed'] = 'selected'
    elif data['maritalstatus'] == 'civunion': results['mari_civunion'] = 'selected'
    elif data['maritalstatus'] == 'dompart': results['mari_dompart'] = 'selected'
    elif data['maritalstatus'] == 'separated': results['mari_separated'] = 'selected'
    elif data['maritalstatus'] == 'cohab': results['mari_cohab'] = 'selected'

    if data['military'] == 'yes': results['military_y'] = 'checked'
    elif data['military'] == 'no': results['military_n'] = 'checked'

    if data['education'] == 'none': results['edu_none'] = 'selected'
    elif data['education'] == 'elementary': results['edu_elem'] = 'selected'
    elif data['education'] == 'hs': results['edu_hs'] = 'selected'
    elif data['education'] == 'somecol': results['edu_somecol'] = 'selected'
    elif data['education'] == 'trade': results['edu_trade'] = 'selected'
    elif data['education'] == 'assoc': results['edu_assoc'] = 'selected'
    elif data['education'] == 'under': results['edu_under'] = 'selected'
    elif data['education'] == 'master': results['edu_master'] = 'selected'
    elif data['education'] == 'prof': results['edu_prof'] = 'selected'
    elif data['education'] == 'doctor': results['edu_doctor'] = 'selected'

    return results


