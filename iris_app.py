import tkinter as tk
from tkinter import messagebox
from data_manager import DataManager
from ui_components import UIComponents
from filter_sort import FilterSortManager
from visualizations import VisualizationManager

class IrisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng Quản lý Dữ liệu Iris")
        self.root.geometry("800x700")
        
        # Khởi tạo data manager
        self.data_manager = DataManager("iris_consolidated.csv")
        
        # Lấy dữ liệu từ data manager
        self.df = self.data_manager.df
        self.original_df = self.data_manager.original_df
        
        # Khởi tạo UI components
        self.ui = UIComponents(self)
        
        # Khởi tạo filter/sort manager
        self.filter_sort = FilterSortManager(self)
        
        # Khởi tạo visualization manager
        self.viz = VisualizationManager(self)
        
        # Tạo giao diện
        self.ui.create_widgets()
        
    def add_record(self):
        """Thêm bản ghi mới"""
        self.ui.show_add_dialog()
    
    def edit_record(self):
        """Chỉnh sửa bản ghi đã chọn"""
        selected_item = self.ui.tree.selection()
        
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một bản ghi để chỉnh sửa!")
            return
        
        # Lấy giá trị của item được chọn
        values = self.ui.tree.item(selected_item[0], 'values')
        record_id = int(values[0])  # ID của bản ghi
        
        # Tìm bản ghi trong DataFrame
        record = self.df[self.df['id'] == record_id].iloc[0]
        
        # Hiển thị dialog chỉnh sửa
        self.ui.show_edit_dialog(record, record_id)
    
    def delete_record(self):
        """Xóa bản ghi đã chọn"""
        selected_item = self.ui.tree.selection()
        
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một bản ghi để xóa!")
            return
        
        # Lấy giá trị của item được chọn
        values = self.ui.tree.item(selected_item[0], 'values')
        record_id = int(values[0])  # ID của bản ghi
        
        # Xác nhận xóa
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa bản ghi này?")
        
        if confirm:
            # Xóa bản ghi khỏi cả DataFrame hiện tại và gốc
            self.df = self.df[self.df['id'] != record_id]
            self.original_df = self.original_df[self.original_df['id'] != record_id]
            
            # Cập nhật hiển thị
            self.ui.populate_treeview()
            
            messagebox.showinfo("Thành công", "Đã xóa bản ghi!")
    
    def refresh_data(self):
        """Làm mới dữ liệu từ file CSV"""
        self.data_manager.load_data()
        self.df = self.data_manager.df
        self.original_df = self.data_manager.original_df
        self.ui.populate_treeview()
        
        # Xóa giá trị đang có trong filter
        self.ui.filter_value.delete(0, tk.END)
        messagebox.showinfo("Thông báo", "Đã làm mới dữ liệu!")
    
    def save_data(self):
        """Lưu dữ liệu vào file CSV"""
        self.data_manager.df = self.df
        self.data_manager.original_df = self.original_df
        self.data_manager.save_data()
    
    def show_visualization(self):
        """Hiển thị cửa sổ visualization"""
        self.viz.show_visualization_window()