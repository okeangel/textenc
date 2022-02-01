import re

def replace_chars(text, encoding='utf-8'):
    text = re.sub(r'\x1A', '-', text)
    text = re.sub(r'\x00', '', text)
    if encoding == 'IBM866':
        text = re.sub(r'ў', 'ё', text)
        text = re.sub(r'\r\n\f\r\n *- [0-9]* -\r\n\r\n', r'\r\n', text)
        text = re.sub(r'\r\n *[0-9]*\r\n\f\r\n', r'\r\n', text)
        text = re.sub(r'\r\n\f\r\n', r'\r\n', text)
    # TODO: replace \r[not\n] to \r\n
    # TODO: replace [not\r]\n to \r\n
    return text

print(replace_chars("""
Дядя Юпитера, Титус Джонс покупает для своего склада утильсырья 12 картин, написанных некоторое время назад человеком, который к этому времени умер. Почти сразу после того, как картины продали, за картинами является очень много народа, и ребята начинают подозревать, что в них содержится ключ к какойто тайне. И они оказываются правы, черт возьми!
"""))
