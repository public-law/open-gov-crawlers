from scrapy.http import HtmlResponse

from public_law.parsers.us.georgia import (
    opinion_date_to_iso8601,
    parse_ag_opinion,
    OpinionParseResult,
)


def parsed_opinion(filename: str) -> OpinionParseResult:
    with open(f"test/fixtures/{filename}") as f:
        html = HtmlResponse(
            url="https://law.georgia.gov/opinions/2017-3",
            body=f.read(),
            encoding="UTF-8",
        )
        return parse_ag_opinion(html)


class TestOpinionDateToISO8601:
    def test_sample_1(self):
        opinion_date = "OCTOBER 02, 2017"
        assert opinion_date_to_iso8601(opinion_date) == "2017-10-02"


class TestParseAgOpinion:
    def setup(self):
        self.result = parsed_opinion("opinion-2017-3.html")

    def test_gets_the_summary(self):
        expected_summary = (
            "Updating of crimes and offenses for which "
            "the Georgia Crime Information Center is "
            "authorized to collect and file fingerprints."
        )
        assert self.result.summary == expected_summary

    def test_gets_the_title(self):
        assert self.result.title == "Official Opinion 2017-3"

    def test_gets_is_official(self):
        assert self.result.is_official

    def test_gets_the_date(self):
        assert self.result.date == "2017-10-02"

    def test_gets_the_full_text(self):
        expected_text = (
            "You have requested, in your letter of August 16, 2017, my opinion concerning whether any of the following misdemeanor offenses enacted during the 2017 Session of the General Assembly should be designated as offenses for which persons charged with violations are to be fingerprinted.\n"
            "Those offenses include: O.C.G.A. § 26-5-58 (violation of the Narcotic Treatment Programs Enforcement Act); and O.C.G.A. § 42-4-13(d.1) (obtaining, procuring, or giving an inmate tobacco or any product containing tobacco).\n"
            "The first misdemeanor offense is O.C.G.A. § 26-5-58. This Code section provides that it shall be a misdemeanor to violate any provision of Article 2 of Chapter 5, Title 26. Article 2 (O.C.G.A. § 26-5-40 et. seq.) establishes the requirements for governing bodies that seek to apply for and operate a narcotic treatment program. An offense arising from a violation of this Code section does not, at this time, appear to be an offense for which fingerprinting is required and I am not, at this time, designating this offense as one for which those charged are to be fingerprinted.\n"
            "The second misdemeanor offense is O.C.G.A. § 42-4-13(d.1). This Code section provides that it shall be a misdemeanor for any person to obtain for, to procure for, or to give to an inmate tobacco or any product containing tobacco without the knowledge and consent of the jailer. This office previously designated offenses related to providing an inmate with alcoholic beverages and other items without the consent of the jailer as offenses for which those charged are to be fingerprinted. See O.C.G.A. §§ 42-4-13(d)(1)(B), 42-4-13(e). In order to promote consistency in the treatment of offenders, I hereby designate misdemeanor offenses arising under O.C.G.A. § 42-4-13(d.1), specifically committed by offenders not already incarcerated within the facility, as offenses for which those charged are to be fingerprinted. To the extent the person charged is already incarcerated, it is unnecessary to designate this offense as one that requires fingerprinting, as O.C.G.A. § 35-3-33(a)(1)(C) already requires that persons confined in prisons, penitentiaries, or other prison institutions are to be fingerprinted.\n"
            "I trust that my revisions of the specific designations of those offenses for which persons charged with violations are to be fingerprinted will aid you in discharging your duties pursuant to the Georgia Crime Information Act.\n"
            "Prepared by:\n"
            "Rebecca Dobras\n"
            "Assistant Attorney General"
        )
        assert self.result.full_text == expected_text

    def test_gets_the_source_url(self):
        assert self.result.source_url == "https://law.georgia.gov/opinions/2017-3"
