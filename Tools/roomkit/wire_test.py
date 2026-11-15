"""Hook the unattended room test (IndevAutoTest.bb, Game.exe -roomtest) into Main.bb and Menu.bb.
Safe to run twice. Originals are kept once as *.bak_test."""
import os
import shutil

ROOT = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9"


def load(rel):
    raw = open(os.path.join(ROOT, rel), 'rb').read()
    nl = b'\r\n' if b'\r\n' in raw else b'\n'
    return raw.decode('latin-1'), nl.decode()


def save(rel, text):
    p = os.path.join(ROOT, rel)
    bak = p + '.bak_test'
    if not os.path.exists(bak):
        shutil.copy2(p, bak)
    open(p, 'wb').write(text.encode('latin-1'))


def swap(text, old, new, marker, nl, what):
    """replace the one occurrence of old (written with \\n) by new; skipped when marker is already there"""
    if marker in text:
        return text, False
    old, new = old.replace('\n', nl), new.replace('\n', nl)
    assert text.count(old) == 1, (what, text.count(old))
    return text.replace(old, new), True


if __name__ == '__main__':
    done = []
    t, nl = load('Main.bb')
    t, c = swap(t, 'Include "IndevT12Data.bb"\n', 'Include "IndevT12Data.bb"\nInclude "IndevAutoTest.bb"\n',
                'Include "IndevAutoTest.bb"', nl, 'include')
    done.append(('Main include', c))
    t, c = swap(t, '\n\t\tUpdateMainMenu()\n\tElse\n',
                # (a block, not one line: Blitz cannot parse "Then Foo() Else Bar()")
                '\n\t\tIf IndevTestOn And IndevTestState = 0 Then ;Indev: -roomtest starts a game by itself (IndevAutoTest.bb)\n'
                '\t\t\tIndevTestStart()\n\t\tElse\n\t\t\tUpdateMainMenu()\n\t\tEndIf\n\tElse\n',
                'IndevTestStart()', nl, 'menu')
    done.append(('Main menu branch', c))
    t, c = swap(t, '\t\t\tUpdateEmitters()\n\t\t\tMouseLook()\n',
                '\t\t\tUpdateEmitters()\n\t\t\tIf IndevTestOn Then IndevTestPose() ;Indev: -roomtest holds the view still (IndevAutoTest.bb)\n\t\t\tMouseLook()\n',
                'IndevTestPose()', nl, 'pose')
    done.append(('Main pose', c))
    t, c = swap(t, '\t\tLocal rawY# = MouseYSpeed() * (MouseSens + 0.6)\n',
                '\t\tLocal rawY# = MouseYSpeed() * (MouseSens + 0.6)\n\t\tIf IndevTestOn Then rawX = 0 : rawY = 0 ;Indev: -roomtest ignores the mouse (IndevAutoTest.bb)\n',
                'rawX = 0 : rawY = 0', nl, 'mouse speed')
    done.append(('Main mouse speed', c))
    t, c = swap(t, '\tIf SelectedEnding = "" Then MoveMouse viewport_center_x, viewport_center_y\n',
                '\tIf SelectedEnding = "" And (Not IndevTestOn) Then MoveMouse viewport_center_x, viewport_center_y ;Indev: -roomtest leaves the cursor alone\n',
                'And (Not IndevTestOn) Then MoveMouse', nl, 'mouse capture')
    done.append(('Main mouse capture', c))
    t, c = swap(t, '\n\tFlip Vsync Lor MainMenuOpen\n',
                '\n\tIf IndevTestOn Then IndevTestFrame() ;Indev: -roomtest saves the frame and moves on (IndevAutoTest.bb)\n\tFlip Vsync Lor MainMenuOpen\n',
                'IndevTestFrame()', nl, 'flip')
    done.append(('Main frame end', c))
    save('Main.bb', t)

    t, nl = load('Menu.bb')
    t, c = swap(t, '\t\tIf percent <> 100 Then Exit\n',
                '\t\tIf percent <> 100 Then Exit\n\t\tIf IndevTestOn Then Exit ;Indev: -roomtest does not wait for a key (IndevAutoTest.bb)\n',
                'If IndevTestOn Then Exit', nl, 'loading')
    done.append(('Menu loading screen', c))
    save('Menu.bb', t)

    for d in done:
        print(d)
