import codecs


def _make_uchr(chr: str):
    if len(chr) == 7:
        chr = chr.replace('+', '000')
    elif len(chr) == 6:
        chr = chr.replace('+', '0000')
    return codecs.decode(r'\U' + chr[1:], 'unicode_escape')
