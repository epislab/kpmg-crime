import pandas as pd

from com.epislab.models.data_reader import Dataset
class CrimeService:
    dataset = Dataset()
    def new_model(self, fname) -> object:
        this = self.dataset
        print(f"Dataset 객체 확인: {this}")
     
        return pd.read_csv(this.context + this.fname)
    
    def preprocess(self, *args) -> object:
        print(f"------------모델 전처리 시작-----------")
        temp = []
        for i in list(args):
            print(f"args 값 출력: {i}")
            temp.append(i)
 
        this = self.dataset
        this.cctv = self.new_model(temp[0])
        this.crime = self.new_model(temp[1])
        this.pop = self.new_model(temp[2])
        return this