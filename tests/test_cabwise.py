
import json
import unittest

import tfl


class CabwiseTest(unittest.TestCase):

    SAMPLE_JSON = '''{"OperatorId": 0, "OrganisationName": "Addison Lee Limited", "TradingName": "Addison Lee", "CentreId": 29776, "AddressLine1": "FIRST FLOOR, 35-37", "AddressLine2": "WILLIAM ROAD", "AddressLine3": ",", "Town": ",", "County": ",", "Postcode": "NW1 3ER", "BookingsPhoneNumber": "0207 387 8888", "BookingsEmail": "BOOKINGS@ADDISONLEE.COM /HTTP://WWW.ADDISONLEE.COM"}'''

    def _SampleCabwise(self):
        return tfl.Cabwise(
            OperatorId=0,
            OrganisationName="Addison Lee Limited",
            TradingName="Addison Lee",
            CentreId=29776,
            AddressLine1="FIRST FLOOR, 35-37",
            AddressLine2="WILLIAM ROAD",
            AddressLine3=",",
            Town=",",
            County=",",
            Postcode="NW1 3ER",
            BookingsPhoneNumber="0207 387 8888",
            BookingsEmail="BOOKINGS@ADDISONLEE.COM /HTTP://WWW.ADDISONLEE.COM",
        )

    def test_parameters(self):
        cabwise = tfl.Cabwise()
        cabwise.OperatorId = 0
        self.assertEqual(0, cabwise.OperatorId)

        cabwise.OrganisationName = "Addison Lee Limited"
        self.assertEqual("Addison Lee Limited", cabwise.OrganisationName)

        cabwise.TradingName = "Addison Lee"
        self.assertEqual("Addison Lee", cabwise.TradingName)

        cabwise.CentreId = 29776
        self.assertEqual(29776, cabwise.CentreId)

        cabwise.AddressLine1 = "FIRST FLOOR, 35-37"
        self.assertEqual("FIRST FLOOR, 35-37", cabwise.AddressLine1)

        cabwise.AddressLine2 = "WILLIAM ROAD"
        self.assertEqual("WILLIAM ROAD", cabwise.AddressLine2)

        cabwise.AddressLine3 = ","
        self.assertEqual(",", cabwise.AddressLine3)

        cabwise.Town = ","
        self.assertEqual(",", cabwise.Town)

        cabwise.County = ","
        self.assertEqual(",", cabwise.County)

        cabwise.Postcode = "NW1 3ER"
        self.assertEqual("NW1 3ER", cabwise.Postcode)

        cabwise.BookingsPhoneNumber = "0207 387 8888"
        self.assertEqual("0207 387 8888", cabwise.BookingsPhoneNumber)

        cabwise.BookingsEmail = ("BOOKINGS@ADDISONLEE.COM /"
                                 "HTTP://WWW.ADDISONLEE.COM")
        self.assertEqual(
            "BOOKINGS@ADDISONLEE.COM /HTTP://WWW.ADDISONLEE.COM",
            cabwise.BookingsEmail
        )

    def test_to_dict(self):
        cabwise = self._SampleCabwise()
        data = cabwise.toDict()
        self.assertEqual(0, data["OperatorId"])
        self.assertEqual("Addison Lee Limited", data["OrganisationName"])
        self.assertEqual("Addison Lee", data["TradingName"])
        self.assertEqual(29776, data["CentreId"])
        self.assertEqual("FIRST FLOOR, 35-37", data["AddressLine1"])
        self.assertEqual("WILLIAM ROAD", data["AddressLine2"])
        self.assertEqual(",", data["AddressLine3"])
        self.assertEqual(",", data["Town"])
        self.assertEqual(",", data["County"])
        self.assertEqual("NW1 3ER", data["Postcode"])
        self.assertEqual("0207 387 8888", data["BookingsPhoneNumber"])
        self.assertEqual(
            "BOOKINGS@ADDISONLEE.COM /HTTP://WWW.ADDISONLEE.COM",
            data["BookingsEmail"]
        )

    def test_from_json(self):
        data = json.loads(self.SAMPLE_JSON)
        cabwise = tfl.Cabwise.fromJSON(data)
        self.assertEqual(self._SampleCabwise(), cabwise)
