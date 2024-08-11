from pathlib import Path

import cv2 as cv

EXTENSION = input("Your video extension: ")
SKIP_VALUE = int(input("Seconds to skip forward: "))
OUTPUT = "fast_forward.rpy"

def get_video_info(video_extension):
    for path in Path.cwd().glob(f"**/*.{video_extension}"):
        if path.is_file():
            cap = cv.VideoCapture(path)
            seconds = cap.get(7) / cap.get(5)
            cap.release()
            yield path, seconds
    cv.destroyAllWindows()


def generate_code():
    code = """init python:
    from pathlib import Path
    import time
    
    def ff_cutscene(path):
        renpy.call(f"{Path(path).stem}_ff")

style fast_forward_text:
    color "#DDD"
    size 16
    xalign 0.5

screen fast_forward:
    style_prefix "fast_forward"
    frame:
        background "#00000050"
        ysize config.screen_height
        xalign 1.0
        xpadding 15
        has vbox
        align (0.5, 0.5)
        text "[jump_time_iso]" style "fast_forward"
        hbox:
            spacing 9
            xalign 0.5
            text "▸" at delayed_blink(0.0, 1.0)
            text "▸" at delayed_blink(0.2, 1.0)
            text "▸" at delayed_blink(0.4, 1.0)


label fast_forward():
    $jump_time_iso = time.strftime("%H:%M:%S", time.gmtime(jump_time))
    show screen fast_forward with dissolve
    hide screen fast_forward with dissolve
    return

"""
    for info in get_video_info(EXTENSION):
        name, tag, seconds = info[0].name, info[0].stem, info[1]
        nr_of_segments = int(seconds / SKIP_VALUE) + 1
        code += f"label {tag}_ff():\n"
        for i in range(nr_of_segments):
            code += f"    image {tag}_part_{i + 1} = Movie(play='<from {i * SKIP_VALUE}>videos/{name}', size = (config.screen_width, config.screen_height), loop=False, channel='movsound')\n"
        code += f"""    ${tag}_duration = {seconds}
    $shown_time = time.perf_counter()
    $passed_time = 0
    window hide
    show {tag}_part_1
    pause {tag}_duration
    $passed_time += time.perf_counter() - shown_time + {SKIP_VALUE}
    $shown_time = time.perf_counter()
    $jump_time = min(int({tag}_duration - {tag}_duration % {SKIP_VALUE} + {SKIP_VALUE}), int(passed_time - passed_time % {SKIP_VALUE}))
    $came_from = 1
    $renpy.jump(f'{tag}_position_{{jump_time}}')
"""

        for i in range(nr_of_segments - 1):
            code += f"""    label {tag}_position_{(i + 1) * SKIP_VALUE}:
        call fast_forward
        show {tag}_part_{i + 2}
        $renpy.hide(f'{tag}_part_{{came_from}}')
"""

            if i < nr_of_segments - 2:
                code += f"""        pause {round((seconds - (i + 1) * SKIP_VALUE), 2)}
    $passed_time += time.perf_counter() - shown_time + {SKIP_VALUE}
    $shown_time = time.perf_counter()
    $jump_time = min(int({tag}_duration - {tag}_duration %{SKIP_VALUE} + {SKIP_VALUE}), int(passed_time - passed_time % {SKIP_VALUE}))
    $came_from = {i} + 2
    $renpy.jump(f'{tag}_position_{{jump_time}}')
"""

        code += f"""        pause {round((seconds - (nr_of_segments - 1) * SKIP_VALUE), 2)}
    hide {tag}_part_{i + 2}
    label {tag}_position_{int(seconds - seconds % SKIP_VALUE + SKIP_VALUE)}:
    $renpy.hide(f'{tag}_part_{{came_from}}')
    window show
    return

"""

    Path(OUTPUT).write_text(code, encoding="utf8")
    print("Finished.")


if __name__ == "__main__":
    generate_code()
