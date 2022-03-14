from tika import parser

from public_law.parsers.int.rome_statute import pdf_to_xml


class TestRomeStatute:
    def test_can_use_the_tika_api(self):
        french_xml = pdf_to_xml(
            "https://www.icc-cpi.int/Publications/Statut-de-Rome.pdf"
        )

        assert set(french_xml.keys()) == {"metadata", "content", "status"}

    # def test_raises_error_when_pdf_not_found(self):
    #     pass
