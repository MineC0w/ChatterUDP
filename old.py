__author__ = 'User'

def fragment_data(msg):

    break_ignore = [" ", "\n", "\r", "\t"]  # Characters that break between words
    special_chars = [":", "*"]  # Characters that mean special fragment
    special_chars_end = {":": ":", "*": "*", "~": "~"}  # Ending characters of each starting charachter
    special_chars_type = {"NONE": "TEXT", ":": "EMOJI", "*": "BOLD"}  # Fragment names

    special_c = ""
    ignore = False
    buffer_ = ""
    len_ = len(msg)

    fragment_stack = []
    fragments_types = []

    for i in range(0, len_):
        if i < len_-1 and msg[i] == "\\" and special_c == "":
            ignore = True
            print "Saw \\, ignoring rest of word."
            continue
        if msg[i] in break_ignore:  # Should stop ignoring stuff now
            ignore = False
            print "Word ended, no longer ignoring."
        if not special_c == "":  # Check if currently expecting special fragment chars
            if msg[i] == special_c:  # End of fragment
                fragment_stack.append(buffer_)
                fragments_types.append(special_chars_type[special_c])
                buffer_ = ""
                special_c = ""
            else:
                buffer_ += msg[i]
        elif msg[i] in special_chars and not ignore:  # Beginning of special fragment.
            fragment_stack.append(buffer_)
            fragments_types.append(special_chars_type["NONE"])
            buffer_ = ""
            special_c = msg[i]
        else: buffer_ += msg[i]
    if buffer_ != "":
        fragment_stack.append(buffer_)
        fragments_types.append(special_chars_type["NONE"])
    return (fragment_stack, fragments_types)

# OLD PRINT SPECIAL =================================================================


def print_message(msg, text_box):
    fragments, types = fragment_data(msg)

    for i in range(0, len(fragments)):
        font = get_font()
        type_ = types[i]
        fragment = fragments[i]
        if type_ == "TEXT":
            text_box.tag_config("regular", font=font)
            text_box.insert(Tkinter.END, fragment, "regular")
        if type_ == "EMOJI":
            print "Emoji"
            if fragment in loaded_emoticons:
                text_box.image_create(Tkinter.END, image=loaded_emoticons[fragment])
            else: print "Emoji \"%s\" not loaded" % fragment
        if type_ == "BOLD":
            font["weight"] = "bold"
            text_box.tag_config("bold", font=font)
            text_box.insert(Tkinter.END, fragment, "bold")