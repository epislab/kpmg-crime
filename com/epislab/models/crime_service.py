import pandas as pd

from com.epislab.models.data_reader import DataReader
from com.epislab.models.dataset import Dataset

class CrimeService:
    dataset = Dataset()
    reader = DataReader()
    def csv_model(self, fname) -> object:
        reader = self.reader
        print(f"😎🥇🐰컨텍스트 경로 : {reader.context}")
        print(f"😎🥇🐰파일명 : {fname}")
        reader.fname = fname
        return reader.csv_to_dframe()
    
    def xls_model(self, fname) -> object:
        reader = self.reader
        print(f"😎🥇🐰컨텍스트 경로 : {reader.context}")
        print(f"😎🥇🐰파일명 : {fname}")
        reader.fname = fname
        return reader.xls_to_dframe()
    
    def preprocess(self, *args) -> object:
        print(f"------------모델 전처리 시작-----------")
        temp = []
        for i in list(args):
            print(f"args 값 출력: {i}")
            temp.append(i)
 
        this = self.dataset
        this.cctv = self.csv_model(temp[0])
        this.crime = self.csv_model(temp[1])
        # this.pop = self.xls_model(temp[2])
        return this