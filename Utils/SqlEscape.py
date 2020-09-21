def escape_sqlalchemy_like(string, escape_char='*'):
    return ' '.join((string.replace(escape_char, escape_char * 2)
            .replace('%', escape_char + '%')
            .replace('_', escape_char + '_')).split())