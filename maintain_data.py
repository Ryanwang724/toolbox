from RoiDownloadFromAPI.RoiDownloader import RoiDownloader

input_path = './factory_list.json'
output_path = './roi_from_url'
downloader = RoiDownloader(input_path=input_path, output_path=output_path)
downloader.execute()
print('[maintain_data] done')