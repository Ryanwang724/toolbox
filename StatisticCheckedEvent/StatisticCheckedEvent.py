import csv
import os 
from collections import defaultdict
from typing import List, Dict
import matplotlib
# matplotlib.use('tkagg')
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

# 查系統字型
# import matplotlib.font_manager as fm
# a=sorted([f.name for f in fm.fontManager.ttflist])
# for i in a:
#     print(i)



class StatisticCheckedEvent:
    FILE_NUMBERS = 13 # 080000~200000

    def __init__(self, csv_input_path:str, csv_output_path:str):
        self.this_file_path = os.path.dirname(os.path.abspath(__file__))
        self.csv_input_path = csv_input_path
        self.csv_output_path = csv_output_path
        self.output_file_name = 'statistic_result.csv'

    def _check_dir_exist(self):
        if not os.path.exists(self.csv_output_path):
            os.makedirs(self.csv_output_path)

    def _statistic_event(self, file_list:List[str]) -> dict:
        """統計各廠的各個鏡頭事件數

        Args:
            file_list (List[str]): 檔名組成的list

        Returns:
            dict: 該鏡頭的事件統計結果
        """
        ref_event = 0
        non_ref_event = 0
        total_event = 0
        for file in file_list:
            file_path = os.path.join(self.csv_input_path, file)
            with open(file_path, 'r', encoding='utf-8-sig', newline='') as csvReader:
                csvReader = csv.reader(csvReader)
                event_list = list(csvReader)
            ref_event += int(event_list[-1][1])
            non_ref_event += int(event_list[-1][3])

        total_event = ref_event + non_ref_event
        print(f'    Total Event: {total_event}')
        print(f'        ref_event: {ref_event}')
        print(f'        non_ref_event: {non_ref_event}')

        return_dict = dict()
        return_dict['total_event'] = total_event
        return_dict['ref_event'] = ref_event
        return_dict['non_ref_event'] = non_ref_event

        return return_dict
    
    def _calc_event_count(self, file_list:List[str]) -> list:
        event_count = list() # 放各時間點的事件數

        for file in file_list:
            file_path = os.path.join(self.csv_input_path, file)
            with open(file_path, 'r', encoding='utf-8-sig', newline='') as csvReader:
                csvReader = csv.reader(csvReader)
                event_list = list(csvReader)
            if (len(event_list) - 2) < 0:
                cnt = 0
            else:
                cnt = len(event_list) - 2
            event_count.append(cnt) # 刪除空行跟最後的統計結果，只保留每次事件

        return event_count

    def _plot_result(self, data:Dict[str, List[int]]):
        plt.figure(figsize=(10, 7))
        plt.rcParams['font.family'] = 'Noto Sans CJK JP' # 設定可顯示中文的字型
        time = [f"{i:06d}" for i in range(80000, 200001, 10000)] # 建立時間軸

        x = [_ for _ in range(1, 14)]

        for key, event_list in data.items():
            # print(event_list)
            plt.plot(x,event_list, label=key)

        plt.xticks(ticks=x, labels=time)
        plt.xlabel('Time')
        plt.ylabel('Events')
        plt.title('Relationship of Events Over Time')
        plt.legend()
        # plt.show()
        path = os.path.join(self.this_file_path, 'output', 'result.png')
        plt.savefig(path)
    
    def _remove_output_csv(self):
        file = os.path.join(self.csv_output_path, self.output_file_name)
        if os.path.isfile(file):
            os.remove(file)
    
    def _write_csv(self, data):
        file = os.path.join(self.csv_output_path, self.output_file_name)
        with open(file, 'a', encoding='utf-8-sig', newline='') as csvWriter:
            writer = csv.writer(csvWriter)
            writer.writerow(data)

    def _statistic_results(self):
        """將各廠各鏡頭結果作統計，整合成同工廠

        Raises:
            KeyError: 確認標題欄位
        """
        data_dict = defaultdict(lambda: {'total_event': 0, 'ref_event': 0})

        file_path = os.path.join(self.csv_output_path, self.output_file_name)
        with open(file_path, 'r', encoding='utf-8-sig', newline='') as csvReader:
            csvReader = csv.DictReader(csvReader)
            csv_title = csvReader.fieldnames

            if 'factory_name' not in csv_title:
                raise KeyError("CSV files not include 'factory_name' title.")
            if 'total_event' not in csv_title:
                raise KeyError("CSV files not include 'total_event' title.")
            if 'ref_event' not in csv_title:
                raise KeyError("CSV files not include 'ref_event' title.")
            
            for row in csvReader:
                factory_name = row['factory_name']
                data_dict[factory_name]['total_event'] += int(row['total_event'])
                data_dict[factory_name]['ref_event'] += int(row['ref_event'])

        self._write_csv([]) # 空一行
        self._write_csv(['factory', 'total_event', 'ref_event'])
        for factory, event_count in data_dict.items():
            self._write_csv([factory, event_count['total_event'], event_count['ref_event']])

    def execute(self):
        self._check_dir_exist()
        self._remove_output_csv()

        file_list = [_ for _ in os.listdir(self.csv_input_path) if _.endswith(r'.csv') and _[-12:-4] == "_checked"] # 取出符合條件的檔案
        file_dict = defaultdict(list)

        for file in file_list:
            key = '-'.join(file.split('-')[:-1])
            file_dict[key].append(file)

        title = ['factory_name','camera_ID','date','total_event','ref_event','non_ref_event']
        self._write_csv(title)

        plot_dict = dict()
        for key,value in file_dict.items():
            if len(value) == self.FILE_NUMBERS:
                print(key)
                event_dict = self._statistic_event(value)
                plot_dict[key] = self._calc_event_count(value)
                split_key = key.split('-')
                data = [split_key[0],split_key[1],split_key[2],event_dict['total_event'],event_dict['ref_event'],event_dict['non_ref_event']]
                self._write_csv(data)
            else:
                print(f'{key} have not provided enough files. Only have {len(value)} files.')

        self._plot_result(plot_dict)
        self._statistic_results()

        print('[StatisticCheckedEvent] done.')


if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_input_path = os.path.join(current_dir, 'input')
    csv_output_path = os.path.join(current_dir, 'output')
    
    statistic_checked_event = StatisticCheckedEvent(csv_input_path = csv_input_path,
                                                    csv_output_path = csv_output_path)
    statistic_checked_event.execute()