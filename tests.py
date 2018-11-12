import run
from run import STR_NOT_VALID_JSON

class MockChat:

    def __init__(self, id):
        self.id = id
		

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
        print("Successful tests: {}, Failed tests: {}".format(self.successful_count, self.fail_count))

    def assert_func(self, result, desired_result, test_name):
        if result == desired_result:
            self.successful_count += 1
            print(test_name, ": ok")
        else:
            self.fail_count += 1
            print(test_name, ": fail")

    def test_document_not_json(self):
        file = open("TestFiles/archive.zip", "rb")
        res = run.process_document(file.read())
        file.close()
        self.assert_func(res, STR_NOT_VALID_JSON, "Archive file")

        file = open("TestFiles/desert.jpg", "rb")
        res = run.process_document(file.read())
        file.close()
        self.assert_func(res, STR_NOT_VALID_JSON, "Image file")

        file = open("TestFiles/presentation.pptx", "rb")
        res = run.process_document(file.read())
        file.close()
        self.assert_func(res, STR_NOT_VALID_JSON, "Presentation file")

        file = open("TestFiles/Test.docx", "rb")
        res = run.process_document(file.read())
        file.close()
        self.assert_func(res, STR_NOT_VALID_JSON, "Docx file")

        file = open("TestFiles/Test.pdf", "rb")
        res = run.process_document(file.read())
        file.close()
        self.assert_func(res, STR_NOT_VALID_JSON, "PDF file")

        file = open("TestFiles/text.txt", "rb")
        res = run.process_document(file.read())
        file.close()
        self.assert_func(res, STR_NOT_VALID_JSON, "Text file")

    def test_invalid_geojson(self):
        file = open("TestFiles/invalid.geojson", "rb")
        res = run.process_document(file.read())
        file.close()
        self.assert_func(res, STR_NOT_VALID_JSON, "Invalid GeoJSON")

    def test_not_geojson(self):
        file = open("TestFiles/not_geojson.geojson", "rb")
        res = run.process_document(file.read())
        file.close()
        self.assert_func(res, STR_NOT_VALID_JSON, "Not GeoJSON")

    def test_single_geojson(self):
        file = open("TestFiles/single_geom.geojson", "rb")
        res = run.process_document(file.read())
        file.close()
        true_dict = {"Point": 1, "MultiPoint": 0, "LineString": 0,
                     "MultiLineString": 0, "Polygon": 0, "MultiPolygon": 0}
        self.assert_func(res, true_dict, "Single geometry object")

    def test_normal_geojson(self):
        file = open("TestFiles/normal.geojson", "rb")
        res = run.process_document(file.read())
        file.close()
        true_dict = {"Point": 10, "MultiPoint": 0, "LineString": 2,
                     "MultiLineString": 0, "Polygon": 3, "MultiPolygon": 0}
        self.assert_func(res, true_dict, "Normal GeoJSON")

if __name__ == '__main__':
    test_inst = TestGeoBot()
    test_inst.run_tests()
