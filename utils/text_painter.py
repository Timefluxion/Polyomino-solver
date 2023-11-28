from random import randint


class TextPainter:
    def set_colour(self, text, r, g, b):
        assert (0 <= r <= 255) and (0 <= b <= 255) and (0 <= b <= 255), "Wrong RGB colour"
        return self.get_ansi_colour(r, g, b) + f"m{text}\033[0m"

    def get_coloured_text(self, text, r, g, b):
        return self.set_colour(text, r, g, b)

    @staticmethod
    def get_random_colour():
        return randint(50, 200), randint(50, 200), randint(50, 200)

    @staticmethod
    def get_ansi_colour(r=0, g=0, b=0):
        assert (0 <= r <= 255) and (0 <= b <= 255) and (0 <= b <= 255), "Wrong RGB colour"
        return f"\033[38;2;{r};{g};{b}"
