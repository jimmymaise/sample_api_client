class Common:
    @staticmethod
    def to_camel(string: str) -> str:
        return ''.join(word.capitalize() if i > 0 else word for i, word in enumerate(string.split('_')))

    @staticmethod
    def to_snake(string: str) -> str:
        return ''.join(['_' + i.lower() if i.isupper() else i for i in string]).lstrip('_')
