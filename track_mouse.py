from ff_video_fixer import FFObj
from mouse_sessions import make_session_list
make_session_list('E:\Eraser\SessionDirectories')
sesh_str = input('Which session do you want to import from SessionDirectories.csv? (0,1,2,...)')
sesh_num = int(sesh_str)
t = FFObj(sesh_num)
print('Tracking mouse')

t.process_video()
t.save_data()
t.export_pos()
print('Tracking successfully finished')




# exporting files to csv files - look in export_pos in ff_video_fixer (shown here below). Will have to change some stuff
# to write the appropriate variables (e.g. one row could be the day you are calculating and the other row could be the
# DI value).
def export_pos(self):
    import csv
    directory, _ = path.split(self.avi_location)
    pos_filename = path.join(directory, 'pos.csv')
    print(pos_filename)
    with open(pos_filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(self.position[:, 0])
        writer.writerow(self.position[:, 1])
