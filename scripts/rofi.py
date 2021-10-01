import subprocess


def rofi(prompt, options, rofi_args=[], fuzzy=True):
    optionstr = '\n'.join(option.replace('\n', ' ') for option in options)
    args = ['rofi', '-sort', '-no-levenshtein-sort']
    if fuzzy:
        args += ['-matching', 'fuzzy']
    args += ['-dmenu', '-p', prompt, '-format', 's', '-i']
    args += rofi_args
    args = [str(arg) for arg in args]

    result = subprocess.run(args, input=optionstr, stdout=subprocess.PIPE, universal_newlines=True)
    returncode = result.returncode
    stdout = result.stdout.strip()

    selected = stdout.strip()
    try:
        index = [opt.strip() for opt in options].index(selected)
    except ValueError:
        index = -1

    # We handle the return code from rofi here:
    # 0 of course means successful, we pass this on
    # 1 means that the user exited the prompt without specifying an option
    # returns codes >=10 are custom return codes specified with '-kb-custom-<n> <keybind>' options
    # that are passed to rofi. We subtract 9 from them to pass '<n>' to the caller
    if returncode == 0:
        key = 0
    elif returncode == 1:
        key = -1
    elif returncode > 9:
        key = returncode - 9
    else:  # This case should never be reached
        key = -2

    return key, index, selected
