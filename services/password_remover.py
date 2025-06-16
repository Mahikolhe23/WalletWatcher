import os
import pikepdf

def get_all_files(folder_path):
    
    if not os.path.isdir(folder_path):
        print('Folder Path Not Found')
    else:
        file_list = []
        for root, _, filenames in os.walk(folder_path):
            for file in filenames:
                file_list.append(os.path.join(root,file))
        return file_list
        
def remove_password(folder_path):
    all_files = get_all_files(folder_path)

    passwords = ['HPCPK0146D','23051996','2305@8043','MAHE2305','MAHE8043','7350458043','niki2603']

    for file in all_files:
        for password in passwords:
            try:
                with pikepdf.open(file, password=password) as pdf:
                    old_file_name = file
                    file = file.lower()
                    new_pdf = file.split('.pdf')[0] + '_new.pdf'
                    pdf.save(new_pdf)
                    os.remove(file)
                    os.rename(new_pdf, old_file_name)
                    break
            except:
                print('Wrong Password')

