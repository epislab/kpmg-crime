import pandas as pd
import os
from com.epislab.models.data_reader import DataReader
from com.epislab.models.dataset import Dataset

class CrimeService:

    dataset = Dataset()
    reader = DataReader()

    def new_model(self, fname) -> object:
        reader = self.reader
        print(f"😎🥇🐰파일명 : {fname}")
        reader.fname = fname
        if fname.endswith('csv'):
            return reader.csv_to_dframe()
        elif fname.endswith('xls'):
            return reader.xls_to_dframe(header=2, usecols='B,D,G,J,N')
    
    def preprocess(self, *args) -> object:
        print(f"------------모델 전처리 시작-----------")
        temp = []
        for i in list(args):
            # print(f"args 값 출력: {i}")
            temp.append(i)
 
        this = self.dataset
        this.cctv = self.new_model(temp[0])
        this = self.cctv_ratio(this)
        this.crime = self.new_model(temp[1])
        this = self.crime_ratio(this)
        this.pop = self.new_model(temp[2])
        this = self.pop_ratio(this)
        return this
    
    @staticmethod
    def cctv_ratio(this) -> object:
        this.cctv = this.cctv.drop(['2013년도 이전', '2014년', '2015년', '2016년'], axis = 1)
        print(f"CCTV 데이터 헤드: {this.cctv.head()}")
        cctv = this.cctv
        return this
    
    @staticmethod
    def crime_ratio(this) -> object:
        print(f"CRIME 데이터 헤드: {this.crime.head()}")
        crime = this.crime
        station_names = [] # 경찰서 관서명 리스트
        for name in crime['관서명']:
            station_names.append('서울' + str(name[:-1]) + '경찰서')
        print(f"🔥💧경찰서 관서명 리스트: {station_names}")
        station_addrs = []
        station_lats = []
        station_lngs = []
        gmaps = DataReader.create_gmaps()
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
        # 현재 스크립트의 절대 경로 가져오기
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # 저장할 디렉토리 설정 (스크립트 위치 기준)
        save_dir = os.path.join(script_dir, 'saved_data')

        # 디렉토리 존재 확인 후 생성
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # CSV 파일 저장
        crime.to_csv(os.path.join(save_dir, 'police_position.csv'), index=False)

        print(f"파일이 저장된 경로: {os.path.join(save_dir, 'police_position.csv')}")
        return this
    
    @staticmethod
    def pop_ratio(this) -> object:
        pop = this.pop
        pop.rename(columns = {
            # pop.columns[0] : '자치구',  # 변경하지 않음
            pop.columns[1]: '인구수',   
            pop.columns[2]: '한국인',
            pop.columns[3]: '외국인',
            pop.columns[4]: '고령자',}, inplace = True)
        print(f"POP 데이터 헤드: {this.pop.head()}")

     
        return this
    
