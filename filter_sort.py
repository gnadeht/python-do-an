from tkinter import messagebox

class FilterSortManager:
    def __init__(self, app):
        self.app = app
    
    def apply_filter(self):
        """Áp dụng bộ lọc cho dữ liệu"""
        column = self.app.ui.filter_column.get()
        operator = self.app.ui.filter_operator.get()
        value = self.app.ui.filter_value.get()
        
        if not column or not operator or not value:
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin bộ lọc!")
            return
        
        # Đặt lại DataFrame về dữ liệu gốc
        self.app.df = self.app.original_df.copy()
        
        try:
            # Đối với các cột số
            try:
                filter_value = float(value)
                if operator == "=":
                    self.app.df = self.app.df[self.app.df[column] == filter_value]
                elif operator == ">":
                    self.app.df = self.app.df[self.app.df[column] > filter_value]
                elif operator == "<":
                    self.app.df = self.app.df[self.app.df[column] < filter_value]
                elif operator == ">=":
                    self.app.df = self.app.df[self.app.df[column] >= filter_value]
                elif operator == "<=":
                    self.app.df = self.app.df[self.app.df[column] <= filter_value]
                elif operator == "!=":
                    self.app.df = self.app.df[self.app.df[column] != filter_value]
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập một số hợp lệ cho bộ lọc!")
                return
            
            # Cập nhật hiển thị
            self.app.ui.populate_treeview()
            
            # Hiển thị thông báo nếu không có dữ liệu nào thỏa mãn điều kiện
            if len(self.app.df) == 0:
                messagebox.showinfo("Thông báo", "Không có dữ liệu nào thỏa mãn điều kiện lọc!")
        
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi áp dụng bộ lọc: {str(e)}")
    
    def clear_filter(self):
        """Xóa bộ lọc và hiển thị tất cả dữ liệu"""
        self.app.df = self.app.original_df.copy()
        self.app.ui.filter_value.delete(0, "end")
        self.app.ui.populate_treeview()
        messagebox.showinfo("Thông báo", "Đã xóa bộ lọc!")
    
    def apply_sort(self):
        """Áp dụng sắp xếp cho dữ liệu"""
        column = self.app.ui.sort_column.get()
        order = self.app.ui.sort_order.get()
        
        if not column or not order:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn cột và thứ tự sắp xếp!")
            return
        
        try:
            # Xác định thứ tự sắp xếp
            ascending = True if order == "Tăng dần" else False
            
            # Sắp xếp DataFrame
            self.app.df = self.app.df.sort_values(by=column, ascending=ascending)
            
            # Cập nhật hiển thị
            self.app.ui.populate_treeview()
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi sắp xếp dữ liệu: {str(e)}")
    
    def clear_sort(self):
        """Xóa sắp xếp và trở về thứ tự ban đầu"""
        # Sắp xếp theo ID để trở về thứ tự ban đầu
        self.app.df = self.app.df.sort_values(by='id', ascending=True)
        self.app.ui.populate_treeview()
        messagebox.showinfo("Thông báo", "Đã xóa sắp xếp!")
    
    def sort_treeview_column(self, column):
        """Sắp xếp dữ liệu khi click vào tiêu đề cột"""
        # Lấy thứ tự sắp xếp hiện tại và đảo ngược
        try:
            # Sắp xếp theo cột đã chọn
            self.app.ui.sort_column.set(column)
            current_order = self.app.ui.sort_order.get()
            
            # Đảo ngược thứ tự sắp xếp khi click lại vào cùng một cột
            if current_order == "Tăng dần":
                self.app.ui.sort_order.set("Giảm dần")
            else:
                self.app.ui.sort_order.set("Tăng dần")
            
            # Áp dụng sắp xếp
            self.apply_sort()
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi sắp xếp dữ liệu: {str(e)}")