import pandas as pd
from tkinter import messagebox

class DataManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.load_data()
        self.original_df = self.df.copy()
    
    def load_data(self):
        """Đọc dữ liệu từ file CSV"""
        try:
            self.df = pd.read_csv(self.file_path)
            # Thêm cột index để dễ theo dõi
            self.df['id'] = range(1, len(self.df) + 1)
            # Thay đổi thứ tự cột để cột id ở đầu
            cols = ['id'] + [col for col in self.df.columns if col != 'id']
            self.df = self.df[cols]
            self.original_df = self.df.copy()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc file: {str(e)}")
            self.df = pd.DataFrame(columns=['id', 'sepal_length_cm', 'sepal_width_cm', 
                                           'petal_length_cm', 'petal_width_cm', 'class'])
            self.original_df = self.df.copy()
    
    def save_data(self):
        """Lưu dữ liệu vào file CSV"""
        try:
            # Xóa cột id khi lưu xuống file
            save_df = self.original_df.drop('id', axis=1)
            save_df.to_csv(self.file_path, index=False)
            messagebox.showinfo("Thông báo", "Dữ liệu đã được lưu thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu file: {str(e)}")