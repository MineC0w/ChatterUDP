import Tkinter
import tkFont
from PIL import Image, ImageTk
import time

__author__ = 'Yair'

# Returns a stack where each element is of same format
'''
TODO:(1) Fix problems with double fragmnet starters that never end
    (2) implement fragment tree (fragments composed of fragments)
    (3) fragment object
'''
emoticon_size = (16,16)
emoticon_list = ["upside_down_smile"]
loaded_emoticons = {}
garbage = 0
class AtomicFragment:
    def __init__(self, type_, content):
        self.Type = type_
        self.Content = content
class MolecularFragment():
    def __init__(self,modifier):
        self.Fragments = []
        self.Modifier = modifier


def get_font(modifiers = []):
    font = tkFont.Font(family="Ariel", size="11", weight="normal", underline=1)
    if "BOLD" in modifiers:
        font["weight"] = "bold"
    print font.actual()
    return font

def load_emoticon(emoji):
    # TODO: Make sure file exists
    emoticon = ImageTk.PhotoImage(Image.open("emojis/%s.png" % emoji).resize(emoticon_size, Image.ANTIALIAS))
    loaded_emoticons[emoji] = emoticon
    print "Loaded emoji/%s.png" % emoticon

def load_emoticons():
    for emoticon in emoticon_list:  # Load all emoticons
        if emoticon not in loaded_emoticons:  # Check if already loaded
            load_emoticon(emoticon)  # If not, load



def breakable(c):
    return c in [":"]

def fragment_data(msg, modifier):
    break_ignore = [" ", "\n", "\r", "\t"]  # Characters that break between words
    special_chars = [":", "*", "~", "_"]  # Characters that mean special fragment
    special_chars_end = {":": ":", "*": "*", "~": "~", "_":"_"}  # Ending characters of each starting charachter
    special_chars_type = {"NONE": "TEXT", ":": "EMOJI", "*": "BOLD", "~": "OVERSTRIKE", "_": "UNDERLINE"}  # Fragment names

    fragmented_msg = MolecularFragment(modifier)
    len_ = len(msg)
    buffer_ = ""
    i = 0

    s_char = ""
    ignore = False

    while i < len_:
        if msg[i] in special_chars:  # Start of fragment

            s_char = msg[i]
            tmp_buffer = ""
            i += 1
            while (i < len_) and (msg[i] != special_chars_end[s_char]):
                if msg[i] in break_ignore and breakable(s_char):  # If emoji should stop
                    buffer_ +=  s_char + tmp_buffer
                    s_char = ""
                    break
                else:
                    tmp_buffer += msg[i]
                i += 1

            # Exited loop. Check why

            if i == len_: # False alarm
                buffer_ += s_char + tmp_buffer
            elif msg[i] in break_ignore:
                buffer_ += msg[i]

            elif msg[i] == special_chars_end[s_char]:  # End of fragment
                if buffer_ != "":
                    fragmented_msg.Fragments.append(AtomicFragment("TEXT", buffer_))
                    buffer_ = ""
                if special_chars_type[s_char] == "EMOJI":
                    fragmented_msg.Fragments.append(AtomicFragment("EMOJI", tmp_buffer))
                    tmp_buffer = ""
                if special_chars_type[s_char] == "BOLD":
                    fragmented_msg.Fragments.append(fragment_data(tmp_buffer, "BOLD"))
                    tmp_buffer = ""
                if special_chars_type[s_char] == "OVERSTRIKE":
                    fragmented_msg.Fragments.append(fragment_data(tmp_buffer, "OVERSTRIKE"))
                    tmp_buffer = ""
                if special_chars_type[s_char] == "UNDERLINE":
                    fragmented_msg.Fragments.append(fragment_data(tmp_buffer, "UNDERLINE"))
                    tmp_buffer = ""


        else:  # Not start of fragment
            buffer_ += msg[i]
        i += 1
    if buffer_ != "":
        fragmented_msg.Fragments.append(AtomicFragment("TEXT", buffer_))
    return fragmented_msg


# Print a special message to text box

def print_fragment(frg, text_box, modifiers):
    global garbage
    if isinstance(frg, AtomicFragment):
        print str(modifiers) + str(frg.Content)
        type_ = frg.Type
        fragment = frg.Content
        if type_ == "TEXT":
            text_box.insert(Tkinter.END, fragment, tuple(modifiers))
        elif type_ == "EMOJI":
            if fragment in loaded_emoticons:
                text_box.image_create(Tkinter.END, image=loaded_emoticons[fragment])
            else: print "Emoji \"%s\" not loaded" % fragment
    elif isinstance(frg, MolecularFragment):
        new_modifiers = modifiers[:]
        new_modifiers.append(frg.Modifier)
        for fragment in frg.Fragments:
            print_fragment(fragment, text_box, new_modifiers)

def print_message(msg, box):
    fragments = fragment_data(msg, "MAIN")
    print_fragment(fragments, box, [])

def setup(box):
    load_emoticons()
    box.tag_config("MAIN", font=tkFont.Font(None, name="normal",family="Ariel", size=11, weight="normal"))
    box.tag_config("BOLD", font=tkFont.Font(None, name="bold",family="Ariel", size=11, weight="bold"))
    box.tag_config("OVERSTRIKE", overstrike=True)
    box.tag_config("UNDERLINE", underline=1)
    print "Finished setting up MessageHandler."


def print_fragments(fragment):
    if isinstance(fragment, MolecularFragment):
        print "============= %s" % fragment.Modifier
        for frag in fragment.Fragments:
            print_fragments(frag)
        print "============="
    elif isinstance(fragment, AtomicFragment):
        print "%s (%s)" % (fragment.Content, fragment.Type)


def main():
    msg = "_Me_: *Watermelons _are ~not~ delicious_ :upside_down_smile:*"
    fragments = fragment_data(msg, "MAIN")

    root = Tkinter.Tk()

    box = Tkinter.Text(root)
    box.grid(row=0, column=0)
    setup(box)
    print_message(msg, box)
    root.mainloop()





if __name__ == "__main__":
    main()

