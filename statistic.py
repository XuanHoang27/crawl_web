import matplotlib.pyplot as plt
import os

def del_empty(path):
    if not os.listdir(path):
        os.rmdir(path)

def count_images(folder_path):
    # Danh sách các định dạng ảnh được hỗ trợ
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

    # Khởi tạo biến đếm số lượng ảnh
    count = 0

    # Lặp qua các tệp tin trong thư mục
    for filename in os.listdir(folder_path):
        # Lấy đuôi tệp tin
        _, extension = os.path.splitext(filename)

        # Nếu đuôi tệp tin là định dạng ảnh hỗ trợ thì tăng biến đếm lên 1
        if extension.lower() in image_extensions:
            count += 1
    # Trả về số lượng ảnh
    return count


# khoi tạo giá trị biểu đồ cột
safe_folders = []
unsafe_folders = []
labels2 = []
# Khơi tạo giá trị biểu đồ tròn



def statistic_pure(path):
    labels = []
    sum_safe = 0
    sum_unsafe = 0
    # danh sách folder của path: i , i+1 , i+2
    list_sum_folder = os.listdir(path)
    for i in list_sum_folder:
        if(str(i).find(".") == -1):  # check phải folder ko - k có dấu chấm
            sub_list_sum_folder = os.listdir(path + "/" + str(i))
            for j in sub_list_sum_folder:  # Lặp từng folder j...
                del_empty(path + "/" + str(i) + "/" + str(j))
        del_empty(path + "/" + str(i))

    for i in list_sum_folder:  # lặp từng folder i ...
        try:
            if(str(i).find(".") == -1):  # check phải folder ko - k có dấu chấm
                # Danh sách folder của i là : j , j+1, ...
                labels.append(str(i))
                sum_safe_foldersub = 0
                sum_unsafe_foldersub = 0
                phantram = 0
                pt_unsafe = 0
                sub_list_sum_folder = os.listdir(path + "/" + str(i))
                for j in sub_list_sum_folder:  # Lặp từng folder j...
                    # thư mục safe trong j
                    dir_safe = path + "/" + str(i) + "/" + str(j) + "/Safe"
                    # thư mục unsafe trong j
                    dir_unsafe = path + "/" + str(i) + "/" + str(j) + "/UnSafe"

                    if os.path.exists(dir_safe):  # check có đường dẫn
                        count_images(dir_safe)  # đếm ảnh ở s trong j
                        sum_safe_foldersub += count_images(dir_safe)
                    if os.path.exists(dir_unsafe):
                        count_images(dir_unsafe)  # đếm ảnh uns trong j
                        sum_unsafe_foldersub += count_images(dir_unsafe)
                if (sum_unsafe_foldersub == 0 ) and (sum_safe_foldersub == 0): continue
                else:
                    # Tổng ảnh safe và unsafe cả page
                    sum_safe += sum_safe_foldersub
                    sum_unsafe += sum_unsafe_foldersub
                    # Tính phần trăm ảnh safe trong 1 thư mục
                    phantram = round(sum_safe_foldersub /
                                    (sum_unsafe_foldersub+sum_safe_foldersub), 4)
                    pt_unsafe = 1 - phantram
                    safe_folders.append(phantram*100)
                    unsafe_folders.append(pt_unsafe*100)
        except:
            pass

    # Vẽ biểu đồ cột đôi
    fig, ax = plt.subplots()
    ax.bar(labels, safe_folders, width=0.4, align='edge', label='Safe_Image')
    ax.bar(labels, unsafe_folders, width=-0.4,
           align='edge', label='Unsafe_Image')
    ax.set_title('TỈ LỆ ẢNH AN TOÀN VÀ KHÔNG AN TOÀN')
    ax.legend()
    plt.show()

    # Bieu do tron
    S3 = round(sum_safe/(sum_safe+sum_unsafe), 4)*100
    labels = ['an toàn', 'Không an toàn']
    global sizes1
    sizes1 = [S3, 100-S3]
    colors = ['lightskyblue', 'lightcoral']
    plt.pie(sizes1, labels=labels, colors=colors,
            autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.show()
    # return sizes



def statistic_Not_pure(path):
    list_sum_folder = os.listdir(path)
    for i in list_sum_folder:
        if(str(i).find(".") == -1):  # check phải folder ko - k có dấu chấm
            del_empty(path + "/" + str(i))

    for i in list_sum_folder:  # lặp từng folder i ...
        try:
            if(str(i).find(".") == -1):  # check phải folder ko - k có dấu chấm
                # Danh sách folder của i là : j , j+1, ...
                labels2.append(str(i))
                sum_safe_foldersub = 0
                sum_unsafe_foldersub = 0
                phantram = 0
                pt_unsafe = 0
                # sub_list_sum_folder = os.listdir(path + "/" + str(i))

                dir_safe = path + "/" + str(i) + "/Safe"
                # thư mục unsafe trong j
                dir_unsafe = path + "/" + str(i) + "/UnSafe"

                if os.path.exists(dir_safe):  # check có đường dẫn
                    count_images(dir_safe)  # đếm ảnh ở s trong j
                    sum_safe_foldersub += count_images(dir_safe)
                if os.path.exists(dir_unsafe):
                    count_images(dir_unsafe)  # đếm ảnh uns trong j
                    sum_unsafe_foldersub += count_images(dir_unsafe)
            if (sum_unsafe_foldersub == 0 ) and (sum_safe_foldersub == 0): continue
            else:
        # Tính phần trăm ảnh safe trong 1 thư mục
                phantram = round(sum_safe_foldersub /
                                (sum_unsafe_foldersub+sum_safe_foldersub), 4)
                pt_unsafe = 1 - phantram
                safe_folders.append(phantram*100)
                unsafe_folders.append(pt_unsafe*100)
        except:
            pass
    # Vẽ biểu đồ cột đôi
    fig, ax = plt.subplots()
    ax.bar(labels2, safe_folders, width=0.4, align='edge', label='Safe_Image')
    ax.bar(labels2, unsafe_folders, width=-0.4,
           align='edge', label='Unsafe_Image')
    ax.set_title('TỈ LỆ ẢNH AN TOÀN VÀ KHÔNG AN TOÀN')
    ax.legend()
    plt.show()

    # Bieu do tron
    S3 = round(sum_safe_foldersub /
               (sum_safe_foldersub+sum_unsafe_foldersub), 4)*100
    labels = ['an toàn', 'Không an toàn']
    global sizes2
    sizes2 = [S3, 100-S3]
    colors = ['lightskyblue', 'lightcoral']
    plt.pie(sizes2, labels=labels, colors=colors,
            autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.show()

def statistic_process(web):
    if "https://xemanhnong.asia" in web:
        path = "static/data/Detail/AnhNong"
        statistic_Not_pure(path)
    if "https://anhnude.info" in web:
        path = "static/data/Detail/AnhNude"
        statistic_Not_pure(path)
    if "https://vnexpress.net" in web:
        path = "static/data/Detail/VnExpress"
        statistic_pure(path)
    if "https://ngoisao.vnexpress" in web:
        path = "static/data/Detail/SaoStar"
        statistic_pure(path)
    if "https://thanhnien.vn" in web:
        path = "static/data/Detail/ThanhNien"
        statistic_pure(path)
