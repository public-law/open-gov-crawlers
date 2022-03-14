from tika import parser


def pdf_to_xml(url: str) -> dict:
    return parser.from_file(url, xmlContent=True)
