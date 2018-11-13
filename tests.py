import run
from run import STR_NOT_VALID_JSON


class TestGeoBot:

    def __init__(self):
        self.successful_count = 0
        self.fail_count = 0

    def run_tests(self):
        self.test_document_not_json()
        self.test_invalid_geojson()
        self.test_not_geojson()
        self.test_single_geojson()
        self.test_normal_geojson()
        print("Successful tests: {}, Failed tests: {}".format(
            self.successful_count, self.fail_count))

    def assert_func(self, result, desired_result, test_name):
        if result == desired_result:
            self.successful_count += 1
            print(test_name, ": ok")
        else:
            self.fail_count += 1
            print(test_name, ": fail")

    def test_document_not_json(self):
        with open("TestFiles/archive.zip", "rb") as file:
            res = run.process_document(file.read())
        self.assert_func(res, STR_NOT_VALID_JSON, "Archive file")

        with open("TestFiles/desert.jpg", "rb") as file:
            res = run.process_document(file.read())
        self.assert_func(res, STR_NOT_VALID_JSON, "Image file")

        with open("TestFiles/presentation.pptx", "rb") as file:
            res = run.process_document(file.read())
        self.assert_func(res, STR_NOT_VALID_JSON, "Presentation file")

        with open("TestFiles/Test.docx", "rb") as file:
            res = run.process_document(file.read())
        self.assert_func(res, STR_NOT_VALID_JSON, "Docx file")

        with open("TestFiles/Test.pdf", "rb") as file:
            res = run.process_document(file.read())
        self.assert_func(res, STR_NOT_VALID_JSON, "PDF file")

        with open("TestFiles/text.txt", "rb") as file:
            res = run.process_document(file.read())
        self.assert_func(res, STR_NOT_VALID_JSON, "Text file")

    def test_invalid_geojson(self):
        with open("TestFiles/invalid.geojson", "rb") as file:
            res = run.process_document(file.read())
        self.assert_func(res, STR_NOT_VALID_JSON, "Invalid GeoJSON")

    def test_not_geojson(self):
        with open("TestFiles/not_geojson.geojson", "rb") as file:
            res = run.process_document(file.read())
        self.assert_func(res, STR_NOT_VALID_JSON, "Not GeoJSON")

    def test_single_geojson(self):
        with open("TestFiles/single_geom.geojson", "rb") as file:
            res = run.process_document(file.read())
        true_dict = {"Point": 1, "MultiPoint": 0, "LineString": 0,
                     "MultiLineString": 0, "Polygon": 0, "MultiPolygon": 0}
        self.assert_func(res, true_dict, "Single geometry object")

    def test_normal_geojson(self):
        with open("TestFiles/normal.geojson", "rb") as file:
            res = run.process_document(file.read())
        true_dict = {"Point": 10, "MultiPoint": 0, "LineString": 2,
                     "MultiLineString": 0, "Polygon": 3, "MultiPolygon": 0}
        self.assert_func(res, true_dict, "Normal GeoJSON")

if __name__ == '__main__':
    test_inst = TestGeoBot()
    test_inst.run_tests()
