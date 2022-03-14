from tika import parser


def tika_pdf(url: str) -> dict:
    return parser.from_file(url, xmlContent=True)


def metadata(url: str) -> dict:
    return tika_pdf(url)["metadata"]
