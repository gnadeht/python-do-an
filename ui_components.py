import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

class UIComponents:
    def __init__(self, app):
        self.app = app
        self.root = app.root
        self.tree = None
        self.status_label = None
        self.filter_column = None
        self.filter_operator = None
        self.filter_value = None
        self.sort_column = None
        self.sort_order = None
    
    def create_widgets(self):
        """Tạo các widget cho giao diện"""
        # Frame chứa các nút chức năng
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        # Các nút chức năng
        ttk.Button(btn_frame, text="Thêm mới", command=self.app.add_record).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Chỉnh sửa", command=self.app.edit_record).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Xóa", command=self.app.delete_record).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Làm mới", command=self.app.refresh_data).grid(row=0, column=3, padx=5)
        ttk.Button(btn_frame, text="Lưu", command=self.app.save_data).grid(row=0, column=4, padx=5)
        ttk.Button(btn_frame, text="Biểu đồ", command=self.app.show_visualization).grid(row=0, column=5, padx=5)
        
        # Frame cho bộ lọc
        filter_frame = ttk.LabelFrame(self.root, text="Bộ lọc dữ liệu")
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Cột để lọc
        ttk.Label(filter_frame, text="Cột:").grid(row=0, column=0, padx=5, pady=5)
        self.filter_column = ttk.Combobox(filter_frame, width=15)
        self.filter_column.grid(row=0, column=1, padx=5, pady=5)
        
        # Toán tử so sánh
        ttk.Label(filter_frame, text="Toán tử:").grid(row=0, column=2, padx=5, pady=5)
        operators = ["=", ">", "<", ">=", "<=", "!="]
        self.filter_operator = ttk.Combobox(filter_frame, values=operators, width=10)
        self.filter_operator.current(0)
        self.filter_operator.grid(row=0, column=3, padx=5, pady=5)
        
        # Giá trị để lọc
        ttk.Label(filter_frame, text="Giá trị:").grid(row=0, column=4, padx=5, pady=5)
        self.filter_value = ttk.Entry(filter_frame, width=15)
        self.filter_value.grid(row=0, column=5, padx=5, pady=5)
        
        # Nút áp dụng bộ lọc
        ttk.Button(filter_frame, text="Áp dụng", command=self.app.filter_sort.apply_filter).grid(row=0, column=6, padx=5, pady=5)
        
        # Nút xóa bộ lọc
        ttk.Button(filter_frame, text="Xóa bộ lọc", command=self.app.filter_sort.clear_filter).grid(row=0, column=7, padx=5, pady=5)
        
        # Frame cho sắp xếp
        sort_frame = ttk.LabelFrame(self.root, text="Sắp xếp dữ liệu")
        sort_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Cột để sắp xếp
        ttk.Label(sort_frame, text="Sắp xếp theo:").grid(row=0, column=0, padx=5, pady=5)
        self.sort_column = ttk.Combobox(sort_frame, width=15)
        self.sort_column.grid(row=0, column=1, padx=5, pady=5)
        
        # Thứ tự sắp xếp
        ttk.Label(sort_frame, text="Thứ tự:").grid(row=0, column=2, padx=5, pady=5)
        sort_orders = ["Tăng dần", "Giảm dần"]
        self.sort_order = ttk.Combobox(sort_frame, values=sort_orders, width=10)
        self.sort_order.current(0)
        self.sort_order.grid(row=0, column=3, padx=5, pady=5)
        
        # Nút áp dụng sắp xếp
        ttk.Button(sort_frame, text="Áp dụng", command=self.app.filter_sort.apply_sort).grid(row=0, column=4, padx=5, pady=5)
        
        # Nút xóa sắp xếp
        ttk.Button(sort_frame, text="Xóa sắp xếp", command=self.app.filter_sort.clear_sort).grid(row=0, column=5, padx=5, pady=5)
        
        # Frame chứa bảng dữ liệu
        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tạo Treeview để hiển thị dữ liệu dạng bảng
        self.tree = ttk.Treeview(table_frame)
        
        # Thêm thanh cuộn
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Cấu hình cột cho Treeview
        self.tree["columns"] = list(self.app.df.columns)
        self.tree["show"] = "headings"
        
        # Định dạng các cột
        column_widths = {
            "id": 50,
            "sepal_length_cm": 120,
            "sepal_width_cm": 120,
            "petal_length_cm": 120,
            "petal_width_cm": 120,
            "class": 100
        }
        
        for col in self.app.df.columns:
            width = column_widths.get(col, 100)
            self.tree.column(col, width=width, anchor=tk.CENTER)
            self.tree.heading(col, text=col.title().replace('_', ' '), 
                              command=lambda c=col: self.app.filter_sort.sort_treeview_column(c))
        
        # Thêm nhãn trạng thái
        self.status_label = ttk.Label(self.root, text=f"Tổng số bản ghi: {len(self.app.df)}")
        self.status_label.pack(pady=5)
        
        # Hiển thị dữ liệu
        self.populate_treeview()
        
        # Cập nhật combobox cho bộ lọc và sắp xếp
        self.update_comboboxes()
    
    def update_comboboxes(self):
        """Cập nhật các combobox với danh sách cột"""
        # Tất cả các cột cho sắp xếp
        sort_columns = list(self.app.df.columns)
        self.sort_column['values'] = sort_columns
        
        # Chỉ lấy các cột số cho lọc (loại bỏ 'id' và 'class')
        filter_columns = [col for col in self.app.df.columns if col not in ['id', 'class']]
        self.filter_column['values'] = filter_columns
        
        # Đặt giá trị mặc định
        if filter_columns:
            self.filter_column.current(0)
        if sort_columns:
            self.sort_column.current(0)
    
    def populate_treeview(self):
        """Hiển thị dữ liệu từ DataFrame lên Treeview"""
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Thêm dữ liệu mới
        for _, row in self.app.df.iterrows():
            values = [row[col] for col in self.app.df.columns]
            self.tree.insert("", tk.END, values=values)
        
        # Cập nhật nhãn trạng thái
        if hasattr(self, 'status_label'):
            self.status_label.config(text=f"Tổng số bản ghi: {len(self.app.df)} (Tổng dữ liệu: {len(self.app.original_df)})")
    
    def show_add_dialog(self):
        """Hiển thị dialog thêm bản ghi mới"""
        # Tạo cửa sổ dialog để nhập thông tin
        add_window = tk.Toplevel(self.root)
        add_window.title("Thêm bản ghi mới")
        add_window.geometry("400x300")
        add_window.grab_set()  # Ngăn tương tác với cửa sổ chính
        
        # Tạo các widget
        ttk.Label(add_window, text="Sepal Length (cm):").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        ttk.Label(add_window, text="Sepal Width (cm):").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        ttk.Label(add_window, text="Petal Length (cm):").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        ttk.Label(add_window, text="Petal Width (cm):").grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        ttk.Label(add_window, text="Class:").grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        
        sepal_length = ttk.Entry(add_window)
        sepal_length.grid(row=0, column=1, padx=10, pady=10)
        
        sepal_width = ttk.Entry(add_window)
        sepal_width.grid(row=1, column=1, padx=10, pady=10)
        
        petal_length = ttk.Entry(add_window)
        petal_length.grid(row=2, column=1, padx=10, pady=10)
        
        petal_width = ttk.Entry(add_window)
        petal_width.grid(row=3, column=1, padx=10, pady=10)
        
        # Combobox cho trường class
        class_values = self.app.original_df['class'].unique().tolist()
        class_var = ttk.Combobox(add_window, values=class_values)
        class_var.grid(row=4, column=1, padx=10, pady=10)
        
        def save_record():
            try:
                # Kiểm tra dữ liệu nhập vào
                sl = float(sepal_length.get())
                sw = float(sepal_width.get())
                pl = float(petal_length.get())
                pw = float(petal_width.get())
                cls = class_var.get()
                
                if not cls:
                    messagebox.showwarning("Cảnh báo", "Vui lòng chọn một lớp!")
                    return
                
                # Tạo ID mới
                new_id = 1 if len(self.app.original_df) == 0 else max(self.app.original_df['id']) + 1
                
                # Thêm bản ghi mới vào DataFrame gốc
                new_row = pd.DataFrame({
                    'id': [new_id],
                    'sepal_length_cm': [sl],
                    'sepal_width_cm': [sw],
                    'petal_length_cm': [pl],
                    'petal_width_cm': [pw],
                    'class': [cls]
                })
                
                self.app.original_df = pd.concat([self.app.original_df, new_row], ignore_index=True)
                
                # Áp dụng lại bộ lọc hiện tại (nếu có)
                self.app.filter_sort.apply_filter()
                
                # Đóng cửa sổ
                add_window.destroy()
                
                messagebox.showinfo("Thành công", "Đã thêm bản ghi mới!")
                
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ cho các trường số!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")
        
        # Nút lưu
        ttk.Button(add_window, text="Lưu", command=save_record).grid(row=5, column=0, padx=10, pady=20)
        
        # Nút hủy
        ttk.Button(add_window, text="Hủy", command=add_window.destroy).grid(row=5, column=1, padx=10, pady=20)
    
    def show_edit_dialog(self, record, record_id):
        """Hiển thị dialog chỉnh sửa bản ghi"""
        # Tạo cửa sổ dialog để chỉnh sửa
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Chỉnh sửa bản ghi")
        edit_window.geometry("400x300")
        edit_window.grab_set()
        
        # Tạo các widget
        ttk.Label(edit_window, text="Sepal Length (cm):").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        ttk.Label(edit_window, text="Sepal Width (cm):").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        ttk.Label(edit_window, text="Petal Length (cm):").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        ttk.Label(edit_window, text="Petal Width (cm):").grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        ttk.Label(edit_window, text="Class:").grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        
        sepal_length = ttk.Entry(edit_window)
        sepal_length.insert(0, record['sepal_length_cm'])
        sepal_length.grid(row=0, column=1, padx=10, pady=10)
        
        sepal_width = ttk.Entry(edit_window)
        sepal_width.insert(0, record['sepal_width_cm'])
        sepal_width.grid(row=1, column=1, padx=10, pady=10)
        
        petal_length = ttk.Entry(edit_window)
        petal_length.insert(0, record['petal_length_cm'])
        petal_length.grid(row=2, column=1, padx=10, pady=10)
        
        petal_width = ttk.Entry(edit_window)
        petal_width.insert(0, record['petal_width_cm'])
        petal_width.grid(row=3, column=1, padx=10, pady=10)
        
        # Combobox cho trường class
        class_values = self.app.original_df['class'].unique().tolist()
        class_var = ttk.Combobox(edit_window, values=class_values)
        class_var.set(record['class'])
        class_var.grid(row=4, column=1, padx=10, pady=10)
        
        def update_record():
            try:
                # Kiểm tra dữ liệu nhập vào
                sl = float(sepal_length.get())
                sw = float(sepal_width.get())
                pl = float(petal_length.get())
                pw = float(petal_width.get())
                cls = class_var.get()
                
                if not cls:
                    messagebox.showwarning("Cảnh báo", "Vui lòng chọn một lớp!")
                    return
                
                # Cập nhật bản ghi trong cả DataFrame hiện tại và gốc
                self.app.df.loc[self.app.df['id'] == record_id, 'sepal_length_cm'] = sl
                self.app.df.loc[self.app.df['id'] == record_id, 'sepal_width_cm'] = sw
                self.app.df.loc[self.app.df['id'] == record_id, 'petal_length_cm'] = pl
                self.app.df.loc[self.app.df['id'] == record_id, 'petal_width_cm'] = pw
                self.app.df.loc[self.app.df['id'] == record_id, 'class'] = cls
                
                # Cập nhật trong DataFrame gốc
                self.app.original_df.loc[self.app.original_df['id'] == record_id, 'sepal_length_cm'] = sl
                self.app.original_df.loc[self.app.original_df['id'] == record_id, 'sepal_width_cm'] = sw
                self.app.original_df.loc[self.app.original_df['id'] == record_id, 'petal_length_cm'] = pl
                self.app.original_df.loc[self.app.original_df['id'] == record_id, 'petal_width_cm'] = pw
                self.app.original_df.loc[self.app.original_df['id'] == record_id, 'class'] = cls
                
                # Cập nhật Treeview
                self.populate_treeview()
                
                # Đóng cửa sổ
                edit_window.destroy()
                
                messagebox.showinfo("Thành công", "Đã cập nhật bản ghi!")
                
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ cho các trường số!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")
        
        # Nút cập nhật
        ttk.Button(edit_window, text="Cập nhật", command=update_record).grid(row=5, column=0, padx=10, pady=20)
        
        # Nút hủy
        ttk.Button(edit_window, text="Hủy", command=edit_window.destroy).grid(row=5, column=1, padx=10, pady=20)