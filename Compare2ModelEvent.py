import os
import csv
import json

this_file_path = os.path.dirname(os.path.abspath(__file__))
model1_result_path = os.path.join(this_file_path, '..', 'EPA-Dissipation', 'result_0514_rerun')
model2_result_path = os.path.join(this_file_path, '..', 'EPA-Dissipation', 'result_0514_rerun_new_model')

def print_factory_event_with_time(directory:str) -> dict:
    """印出各工廠、日期、ID、的各時段事件數

    Args:
        directory (str): 模型輸出結果路徑

    Returns:
        dict: 統計結果
    """
    factory_dict = dict()
    for factory in os.listdir(directory):
        factory_path = os.path.join(directory, factory)
        # print(factory_path)
        date_dict = dict()
        for date in os.listdir(factory_path):
            date_path = os.path.join(factory_path, date)

            date = date.split('-')
            date = ''.join(date)
            # print(date_path)
            camera_dict = dict()
            for time in os.listdir(date_path):
                time_path = os.path.join(date_path, time)
                # print(time_path)
                
                for camera_id in os.listdir(time_path):

                    if camera_id not in camera_dict.keys():
                        camera_dict[camera_id] = list()

                    camera_id_path = os.path.join(time_path, camera_id)
                    # print(camera_id_path)
                    csv_path = os.path.join(camera_id_path, 'csv')
                    date = date.split('-')
                    date = ''.join(date)
                    csv_file_name = f'{date}-{time}.csv'
                    csv_file_path = os.path.join(csv_path, csv_file_name)
                    # print(csv_file_path)
                    with open(csv_file_path, 'r', encoding='utf-8-sig', newline='') as csvReader:
                        csvReader = csv.reader(csvReader)
                        event_list = list(csvReader)
                    camera_dict[camera_id].append(len(event_list))
            date_dict[date] = camera_dict
        
        factory_dict[factory] = date_dict
    return factory_dict

result = print_factory_event_with_time(model1_result_path)
# print(result)

result2 = print_factory_event_with_time(model2_result_path)
# print(result2)


def calc_total_event(result:dict) -> dict:
    total_factory_events = dict()
    for fac, info in result.items():
        for date, event_dict in info.items():
            total_event = 0
            for id,event_list in event_dict.items():
                total_event += sum(event_list)

            if fac not in total_factory_events.keys():
                total_factory_events[fac] = dict()
            total_factory_events[fac][date] = total_event

    total_factory_events = {k: v for k, v in sorted(total_factory_events.items(), key=lambda item: item[0])}
    return total_factory_events

result = calc_total_event(result)
print('model1 : ', result)

result2 = calc_total_event(result2)
print('model2 : ', result2)

with open(f'model1_compare_result.json', mode='w', encoding='utf-8') as fp:
    json.dump(result, fp, indent=2, ensure_ascii=False)

with open(f'model2_compare_result.json', mode='w', encoding='utf-8') as fp:
    json.dump(result2, fp, indent=2, ensure_ascii=False)