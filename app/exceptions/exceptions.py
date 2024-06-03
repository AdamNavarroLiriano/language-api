class LanguagePairNotSupportedError(Exception):
    def __init__(
        self,
        src: str,
        tgt: str,
        message="Translation from {src} to {tgt} is not supported.",
    ):
        self.src = src
        self.tgt = tgt
        self.message = message.format(src=src, tgt=tgt)
        super().__init__(self.message)


__all__ = ["LanguagePairNotSupportedError"]
