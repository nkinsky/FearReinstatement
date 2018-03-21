from ff_video_fixer import FFObj
from mouse_sessions import make_session_list
make_session_list('E:\Eraser\SessionDirectories')
sesh_str = input('Which session do you want to import from SessionDirectories.csv? (1,2,3,...)')
sesh_num = int(sesh_str)
sesh_num -= 1  # adjust to 0 = 1st entry
t = FFObj(sesh_num)
print('Tracking mouse')
t.process_video()
t.dsave_data()
t.export_pos()
print('Tracking successfully finished')
