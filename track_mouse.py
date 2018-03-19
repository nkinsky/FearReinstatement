from ff_video_fixer import FFObj
from mouse_sessions import make_session_list
make_session_list('E:\Eraser\SessionDirectories')
sesh_num = input('Which session do you want to import from SessionDirectories.csv? (1-n)')
sesh_num -= 1  # adjust to 0 = 1st entry
t = FFObj(sesh_num)
t.process_video()
t.export_pos()
