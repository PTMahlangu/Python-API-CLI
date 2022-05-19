import unittest
import sys
import os
import io
sys.path.insert(0, os.getcwd())
from app import getData,plotData,filterData
from .test_base import captured_io


class myTestCase(unittest.TestCase):
    def test_plotData_filtered_length(self):
        dateRange =['2022-01-11', '2022-01-14']
        users =[ [3500], [4000], [4500], [5000], [20000], [35000], [46000], [70000]]
        dates =[  '08-01-2022', '09-01-2022', '10-01-2022', '11-01-2022', 
        '12-01-2022', '13-01-2022', '14-01-2022', '15-01-2022']

        filteredLabels, filteredData= filterData(users,dates,dateRange)
        self.assertEqual(len(filteredLabels),4)

    def test_plotData_filtered_first_date(self):
        dateRange =['2022-01-11', '2022-01-14']
        users =[ [3500], [4000], [4500], [5000], [20000], [35000], [46000], [70000]]
        dates =[  '08-01-2022', '09-01-2022', '10-01-2022', '11-01-2022', 
        '12-01-2022', '13-01-2022', '14-01-2022', '15-01-2022']

        filteredLabels, filteredData= filterData(users,dates,dateRange)
        self.assertEqual(filteredLabels[0],'11-01-2022')
        self.assertEqual(filteredData[0],[5000])

    def test_plotData_filtered_last_date(self):
        dateRange =['2022-01-11', '2022-01-14']
        users =[ [3500], [4000], [4500], [5000], [20000], [35000], [46000], [70000]]
        dates =[  '08-01-2022', '09-01-2022', '10-01-2022', '11-01-2022', 
        '12-01-2022', '13-01-2022', '14-01-2022', '15-01-2022']

        filteredLabels, filteredData= filterData(users,dates,dateRange)
        self.assertEqual(filteredLabels[-1],'14-01-2022')
        self.assertEqual(filteredData[-1],[46000])

    def test_plotData_OutofBounds_lower(self):
        dateRange =['2021-01-11', '2022-01-14']
        users =[ [3500], [4000], [4500], [5000], [20000], [35000], [46000], [70000]]
        dates =[  '08-01-2022', '09-01-2022', '10-01-2022', '11-01-2022', 
        '12-01-2022', '13-01-2022', '14-01-2022', '15-01-2022']

        suppress_text = io.StringIO()
        sys.stdout = suppress_text

        with self.assertRaises(Exception) as context:
            filteredLabels, filteredData= filterData(users,dates,dateRange)
        self.assertTrue('cannot unpack non-iterable NoneType object' in str(context.exception))
        sys.stdout = sys.__stdout__


    def test_plotData_OutofBounds_upper(self):
        dateRange =['2022-01-11', '2022-01-18']
        users =[ [3500], [4000], [4500], [5000], [20000], [35000], [46000], [70000]]
        dates =[  '08-01-2022', '09-01-2022', '10-01-2022', '11-01-2022', 
        '12-01-2022', '13-01-2022', '14-01-2022', '15-01-2022']

        suppress_text = io.StringIO()
        sys.stdout = suppress_text
        
        with self.assertRaises(Exception) as context: 
            filteredLabels, filteredData= filterData(users,dates,dateRange)
        self.assertTrue('cannot unpack non-iterable NoneType object' in str(context.exception))
        sys.stdout = sys.__stdout__


if __name__ == "__main__":
    unittest.main()
