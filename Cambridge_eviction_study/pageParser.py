# PageParser HTML parsing class
#   This class uses the BeautifulSoup parsing library to extract data from
#   the raw HTML of the case page
from stringMatch import StringMatch
from bs4 import BeautifulSoup


class PageParser():
    def __init__(self, fp, soup_parser):
        self.s = BeautifulSoup(fp, soup_parser)     # BeautifulSoup object
        self.matcher = StringMatch()

    # Clean text
    def _clean(self, str):
        return str.replace("\t", "").replace("\r", "").replace("\n", "")

    # Determines if the case is commercial (only add residential)
    def isCommercial(self):
        try:
            caseHeaderJMAX = self.s.find(id="caseHeader").find_all("td")[0]
            case_type_div = caseHeaderJMAX.find_all("td")[1].find("dd")
            return "Commercial" in self._clean(case_type_div.get_text())
        except IndexError:
            #selfsarray=self.s.find_all("div", class_="caseInfo-col3")
            for sec in self.s.find_all("div", class_="caseInfo-col3"):
                for d in sec.find_all("div"):
                    dt = d.find("ul")
                    if dt is None or dt == []:
                        continue
                    if ( "Initiating Action:" in dt.get_text()):
                        if "Commercial" in d.find("li").get_text():
                            return True
            return False

    # Return Case Number
    def get_case_num(self):
        return self._clean(self.s.find(id="titleBar").get_text().split(" ")[0])

    # Return Case status
    def get_status(self):
        try:
            chJMAX = self.s.find(id="caseHeader").find_all("td")[0]
            case_type_div = chJMAX.find_all("td")[2].find("dd")
            return self._clean(case_type_div.get_text())
        except IndexError:
            chJMAX = self.s.find(id="caseHeader").find_all("div")[0]
            case_type_div = chJMAX.find_all("div")[1].find_all("li")[1]
            return self._clean(case_type_div.get_text())

    # Return File date
    def get_file_date(self):
        try:
            chJMAX = self.s.find(id="caseHeader").find_all("td")[0]
            file_date_div = chJMAX.find_all("td")[4].find("dd")
            return self._clean(file_date_div.get_text())
        except IndexError:
            chJMAX = self.s.find(id="caseHeader").find_all("div")[0]
            file_date_div = chJMAX.find_all("div")[2].find_all("li")[1]
            return self._clean(file_date_div.get_text())

    # Return Plaintiff & Defendant
    def get_parties(self, plaintiffs, defendants):
        parties = self.s.find("div", id="ptyInfo").find_all("div")
        pflag=False
        dflag=False
        for p in parties:
            div_text = p.get_text()

            if "- Plaintiff" in div_text and pflag==False:
                plaintiff = self._clean(div_text).split(" -")[0]
                plaintiff = self.matcher.string_match(plaintiff, plaintiffs)
                pflag=True
            elif "- Defendant" in div_text and dflag==False:
                defendant = self._clean(div_text).split(" -")[0]
                defendant = self.matcher.string_match(defendant, defendants)
                dflag=True

        return (plaintiff, defendant)

    # Return full Docket text
    def get_docket(self):
        docket = self.s.find(id="docketInfo").find("tbody")
        remove = [("\n", " "), ("\t", " "), ("\r", ""), ("\'", ""), ("\"", "")]

        if docket is None:
            return "NA"
        else:
            docket_text = ""
            docket_list = docket.find_all("tr")

            for d in docket_list:
                row = d.find_all("td")
                date = row[0].get_text()
                action = row[1].get_text()

                for r in remove:
                    date = date.replace(r[0], r[1])
                    action = action.replace(r[0], r[1])

                docket_text += date + " - " + action + ", "

            return docket_text

    # Return Judgement Total amount (from docket)
    def get_judgement_total(self):
        docket = self.s.find(id="docketInfo").find("tbody")

        if docket is None:
            return None
        else:
            rows = docket.find_all("tr")
            j_total = None
            for r in rows:
                r_text = r.get_text()
                if "Judgment Total" in r_text:
                    j_total = r_text.split("Judgment Total:")[1]
                elif "Judgement Total" in r_text:
                    j_total = r_text.split("Judgement Total:")[1]

                if j_total is not None:
                    j_total = j_total.split("\n")[0].split("\t")[0]
                    j_total = j_total.replace(" ", "")

            return j_total

    # Get Execution Total amount (from docket)
    def get_execution_total(self, docketText):
        ex_total = None
        if "Execution Total:  " in docketText:
            split_on_ex = docketText.split("Execution Total:  ")
            last = split_on_ex[len(split_on_ex) - 1]
            ex_total = last.split(" ")[0].replace(" ", "")
        return ex_total


    # Return Judgement type, method, and date
    def get_judgement(self, status):
        # No judgement section - check events and docket sections for info
        if self.s.find("div", class_="judgementsInfo") is None:
            if (status == 'Open'):
                return ("", "NA", "NA")

            else:
                docketInfo = self.s.find(id="docketInfo")
                if docketInfo is None:
                    return ("", "NA", "NA")
                docket = docketInfo.find("tbody")

                eventInfo = self.s.find(id="eventInfo")
                if eventInfo is None:
                    return ("", "NA", "NA")
                events = eventInfo.find("tbody")



                # Repeated phrases
                phrases = ["Notice of dismissal without prejudice",
                           "Notice of dismissal with prejudice",
                           "All Parties Failed to Appear, Event Not Held",
                           "Not Held But Event Resolved",
                           "Stipulation of dismissal without prejudice filed",
                           "Stipulation of dismissal with prejudice filed",
                           "Case removed to Housing Court"]

                j_type, j_method, j_date = "", "", ""

                for p in phrases:
                    if p in docket.get_text():
                        docket = docket.find_all("tr")

                        for d in docket:
                            if p in d.get_text():
                                break

                        row = d.find_all("td")
                        j_date = self._clean(row[0].get_text())
                        j_type = self._clean(row[1].get_text())
                        j_method = "NA"

                        if p in j_type:
                            j_type = p
                        break

                    elif p in events.get_text():
                        event_items = events.find_all("tr")
                        for e in event_items:
                            if p in e.get_text():
                                break

                        row = e.find_all("td")
                        j_date = self._clean(row[0].get_text().split(" ")[0])
                        j_type = self._clean(row[4].get_text())
                        j_method = "NA"
                        break

                return (j_date, j_type, j_method)

        # HTML has judgement section
        else:
            case_info = self.s.find("div", class_="judgementsInfo")
            case_info = case_info.find("tbody").find_all("td")
            j_date = self._clean(case_info[0].get_text())
            j_type = self._clean(case_info[1].get_text())
            j_method = self._clean(case_info[2].get_text()).replace(", ", "")

            if "Notice of dismissal without prejudice" in j_type:
                j_type = "Notice of dismissal without prejudice"

            return (j_date, j_type, j_method)

    # Return full Property Address
    def get_address(self):
        address_div = self.s.find(id="addressInfo").find_all("div")
        a1 = address_div[0].find_all("span")
        a1_str = ""
        fst = 0

        for a in a1:
            if a.get_text() == "":
                continue
            if fst == 0:
                a1_str = a1_str + self._clean(a.get_text())
                fst += 1
            else:
                a1_str += " " + self._clean(a.get_text())

        a2 = self._clean(address_div[1].get_text()).replace("         ", " ")
        a2 = a2.replace("CambridgeMA", "Cambridge, MA")
        return a1_str + ", " + a2

    # Return parsed property address: unit, street_name, street_type
    def parse_address(self, address):
        street_address = address.split("Cambridge, MA")[0]
        street_address = street_address.replace(",", ""). replace("  ", " ")

        unit, street_name, street_type = None, None, None
        street_number = street_address.split(" ")[0]

        street_keywords = ["Street", "Drive", "Avenue", "Ave", "Way",
                           "Court", "Circle", "Road", "Place", "Lane",
                           "Drive", "Terrace", "Turnpike"]

        for s in street_keywords:
            if s in street_address:
                street_type = s
                break

        if street_type is not None:
            unit_raw = street_address.split(street_type)[1]
            to_replace = ["Apt", " ", ".", "#", "Unit"]
            for item in to_replace:
                unit_raw = unit_raw.replace(item, "")

            unit = unit_raw
            street_name = street_address.split(" ")[1].split(street_type)[0]

        else:
            street_components = street_address.split(" ")
            length = len(street_components)
            unit_raw = street_components[length - 2]
            to_replace = ["Apt", " ", ".", "#", "Unit"]
            for item in to_replace:
                unit_raw = unit_raw.replace(item, "")

            unit = unit_raw
            street_name = " ".join(street_components[1:length - 2])

        return unit, street_number, street_name, street_type
