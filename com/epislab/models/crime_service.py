import pandas as pd
import os
from com.epislab.models.data_reader import DataReader
from com.epislab.models.dataset import Dataset
from com.epislab.models import save_dir
from com.epislab.models.google_map_singleton import GoogleMapSingleton

class CrimeService:


    dataset = Dataset()
    reader = DataReader()
        
        # CSV 파일 저장
        # 현재 스크립트의 절대 경로 가져오기
        # 저장할 디렉토리 설정 (스크립트 위치 기준)


    
    def preprocess(self, *args) -> object:
        print(f"------------모델 전처리 시작-----------")
        temp = []
        for i in list(args):
            # print(f"args 값 출력: {i}")
            temp.append(i)
 
        this = self.dataset
        print(f"*"*20,"🔥1.CCTV 편집 ")
        this.cctv = self.create_matrix(temp[0])
        this = self.update_cctv(this)
        this = self.save_object_to_csv(this, os.path.join(save_dir, 'cctv_in_seoul.csv'))
        print(f"*"*20,"🐬1. CRIME 편집 ")
        this.crime = self.create_matrix(temp[1])
        this = self.update_crime(this) 
        this = self.save_object_to_csv(this, os.path.join(save_dir, 'crime_in_seoul.csv'))
        print(f"*"*20,"🌥️3. POP 편집 ")
        this.pop = self.create_matrix(temp[2])
        this = self.update_pop(this)
        this = self.save_object_to_csv(this, os.path.join(save_dir, 'pop_in_seoul.xls'))
        return this
    
    def create_matrix(self, fname) -> object:
        reader = self.reader
        print(f"😎🥇🐰파일명 : {fname}")
        reader.fname = fname
        if fname.endswith('csv'):
            return reader.csv_to_dframe()
        elif fname.endswith('xls'):
            return reader.xls_to_dframe(header=2, usecols='B,D,G,J,N')
    

    def save_object_to_csv(self, this, param_path) -> object:
        print(f"⛔save_csv 처음 : {param_path}")
        param_path = os.path.join(save_dir, 'cctv_in_seoul.csv')
        if not os.path.exists(param_path) and  param_path == "cctv_in_seoul.csv":
            print(f"⛔1-cctv_in_seoul.csv: {param_path}")
            this = self.update_cctv(this)
            this.cctv.to_csv(os.path.join(save_dir, 'cctv_in_seoul.csv'), index=False)
            
        elif os.path.exists(param_path) and  param_path == "crime_in_seoul.csv":
            print(f"⛔2-crime_in_seoul.csv: {param_path}")
            this.crime.to_csv(os.path.join(save_dir, 'crime_in_seoul.csv'), index=False)
        elif os.path.exists(param_path) and  param_path == "pop_in_seoul.xls":
            print(f"⛔3-pop_in_seoul.xls: {param_path}")
            this.pop.to_csv(os.path.join(save_dir, 'pop_in_seoul.csv'), index=False)
        else:
            print(f"파일이 이미 존재합니다. {param_path}")
        return this
    
    
    @staticmethod
    def update_cctv(this) -> object:
        this.cctv = this.cctv.drop(['2013년도 이전', '2014년', '2015년', '2016년'], axis = 1)
        print(f"CCTV 데이터 헤드: {this.cctv.head()}")
        cctv = this.cctv
        cctv = cctv.rename(columns = {'기관명' : '자치구'})
        cctv.to_csv(os.path.join(save_dir, 'cctv_in_seoul.csv'), index=False)
        this.cctv = cctv
        return this
    
    @staticmethod
    def update_crime(this) -> object:
        print(f"CRIME 데이터 헤드: {this.crime.head()}")
        crime = this.crime
        station_names = [] # 경찰서 관서명 리스트
        for name in crime['관서명']:
            station_names.append('서울' + str(name[:-1]) + '경찰서')
        print(f"🔥💧경찰서 관서명 리스트: {station_names}")
        station_addrs = []
        station_lats = []
        station_lngs = []
        gmaps1 =  GoogleMapSingleton()
        gmaps2 =  GoogleMapSingleton()
        if gmaps1 is gmaps2:
            print("동일한 객체 입니다.")
        else:
            print("다른 객체 입니다.")
        gmaps = GoogleMapSingleton() # 구글맵 객체 생성
        for name in station_names:
            tmp = gmaps.geocode(name, language = 'ko')
            print(f"""{name}의 검색 결과: {tmp[0].get("formatted_address")}""")
            station_addrs.append(tmp[0].get("formatted_address"))
            tmp_loc = tmp[0].get("geometry")
            station_lats.append(tmp_loc['location']['lat'])
            station_lngs.append(tmp_loc['location']['lng'])
        print(f"🔥💧자치구 리스트: {station_addrs}")
        gu_names = []
        for addr in station_addrs:
            tmp = addr.split()
            tmp_gu = [gu for gu in tmp if gu[-1] == '구'][0]
            gu_names.append(tmp_gu)
        [print(f"🔥💧자치구 리스트 2: {gu_names}")]
        crime['자치구'] = gu_names
        # 저장할 디렉토리 경로 설정

        # CSV 파일 저장
        crime.to_csv(os.path.join(save_dir, 'crime_in_seoul.csv'), index=False)
        this.crime = crime
        return this
    
    @staticmethod
    def update_pop(this) -> object:
        pop = this.pop
        pop = pop.rename(columns = {
            # pop.columns[0] : '자치구',  # 변경하지 않음
            pop.columns[1]: '인구수',   
            pop.columns[2]: '한국인',
            pop.columns[3]: '외국인',
            pop.columns[4]: '고령자',})
        print(f"POP 데이터 헤드: {this.pop.head()}")
        pop.to_csv(os.path.join(save_dir, 'pop_in_seoul.csv'), index=False)
        this.pop = pop
        return this

     
        
    
