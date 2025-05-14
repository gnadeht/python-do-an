import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
from matplotlib.figure import Figure

class VisualizationManager:
    def __init__(self, app):
        self.app = app
    
    def show_visualization_window(self):
        """Hiển thị cửa sổ visualization với các tùy chọn biểu đồ"""
        viz_window = tk.Toplevel(self.app.root)
        viz_window.title("Biểu đồ dữ liệu Iris")
        viz_window.geometry("900x700")
        viz_window.grab_set()
        
        # Frame cho các tùy chọn
        options_frame = ttk.LabelFrame(viz_window, text="Tùy chọn biểu đồ")
        options_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Loại biểu đồ
        ttk.Label(options_frame, text="Loại biểu đồ:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        plot_types = ["Scatter Plot", "Histogram", "Box Plot", "Correlation Matrix", "Pair Plot"]
        plot_type_var = ttk.Combobox(options_frame, values=plot_types)
        plot_type_var.current(0)  # Mặc định chọn Scatter Plot
        plot_type_var.grid(row=0, column=1, padx=5, pady=5)
        
        # Tùy chọn thuộc tính
        ttk.Label(options_frame, text="Thuộc tính X:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(options_frame, text="Thuộc tính Y:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        
        # Lấy danh sách các thuộc tính (loại bỏ 'id' và 'class')
        feature_columns = [col for col in self.app.df.columns if col not in ['id', 'class']]
        
        x_var = ttk.Combobox(options_frame, values=feature_columns)
        x_var.current(0)  # Mặc định chọn thuộc tính đầu tiên
        x_var.grid(row=1, column=1, padx=5, pady=5)
        
        y_var = ttk.Combobox(options_frame, values=feature_columns)
        y_var.current(1)  # Mặc định chọn thuộc tính thứ hai
        y_var.grid(row=2, column=1, padx=5, pady=5)
        
        # Frame để chứa biểu đồ
        plot_frame = ttk.LabelFrame(viz_window, text="Biểu đồ")
        plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Hàm cập nhật biểu đồ
        def update_plot():
            # Xóa biểu đồ cũ nếu có
            for widget in plot_frame.winfo_children():
                widget.destroy()
            
            plot_type = plot_type_var.get()
            x_feature = x_var.get()
            y_feature = y_var.get()
            
            # Sử dụng dữ liệu đang hiển thị (đã lọc) cho biểu đồ
            plot_data = self.app.df
            
            # Tạo figure và axes mới
            fig = Figure(figsize=(10, 6), dpi=100)
            ax = fig.add_subplot(111)
            
            if plot_type == "Scatter Plot":
                # Vẽ scatter plot với màu phân biệt theo class
                for class_name in plot_data['class'].unique():
                    subset = plot_data[plot_data['class'] == class_name]
                    ax.scatter(subset[x_feature], subset[y_feature], label=class_name, alpha=0.7)
                ax.set_xlabel(x_feature)
                ax.set_ylabel(y_feature)
                ax.set_title(f'Scatter Plot: {x_feature} vs {y_feature}')
                ax.legend()
                ax.grid(True, linestyle='--', alpha=0.7)
                
            elif plot_type == "Histogram":
                # Vẽ histogram cho thuộc tính X
                for class_name in plot_data['class'].unique():
                    subset = plot_data[plot_data['class'] == class_name]
                    ax.hist(subset[x_feature], bins=10, alpha=0.5, label=class_name)
                ax.set_xlabel(x_feature)
                ax.set_ylabel('Frequency')
                ax.set_title(f'Histogram of {x_feature}')
                ax.legend()
                ax.grid(True, linestyle='--', alpha=0.7)
                
            elif plot_type == "Box Plot":
                # Vẽ box plot cho các class
                data = []
                labels = []
                for class_name in plot_data['class'].unique():
                    subset = plot_data[plot_data['class'] == class_name]
                    data.append(subset[x_feature])
                    labels.append(class_name)
                ax.boxplot(data, labels=labels)
                ax.set_xlabel('Class')
                ax.set_ylabel(x_feature)
                ax.set_title(f'Box Plot of {x_feature} by Class')
                ax.grid(True, linestyle='--', alpha=0.7)
                
            elif plot_type == "Correlation Matrix":
                # Vẽ ma trận tương quan giữa các thuộc tính số
                corr_data = plot_data[feature_columns].corr()
                im = ax.imshow(corr_data, cmap='coolwarm')
                
                # Thêm giá trị vào các ô
                for i in range(len(corr_data.columns)):
                    for j in range(len(corr_data.columns)):
                        text = ax.text(j, i, f'{corr_data.iloc[i, j]:.2f}',
                                      ha="center", va="center", color="black")
                
                ax.set_title('Correlation Matrix')
                ax.set_xticks(np.arange(len(feature_columns)))
                ax.set_yticks(np.arange(len(feature_columns)))
                ax.set_xticklabels(feature_columns)
                ax.set_yticklabels(feature_columns)
                fig.colorbar(im)
                plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
                
            elif plot_type == "Pair Plot":
                # Xóa axes hiện tại và tạo subplot matrix mới
                fig.clear()
                n = len(feature_columns)
                axes = fig.subplots(n, n)
                fig.subplots_adjust(hspace=0.5, wspace=0.5)
                
                # Vẽ pair plot
                for i in range(n):
                    for j in range(n):
                        ax = axes[i, j]
                        
                        if i == j:  # Vẽ histogram trên đường chéo
                            for class_name in plot_data['class'].unique():
                                subset = plot_data[plot_data['class'] == class_name]
                                ax.hist(subset[feature_columns[i]], bins=10, alpha=0.5, label=class_name)
                            if i == 0:  # Chỉ hiển thị legend ở biểu đồ đầu tiên
                                ax.legend(fontsize='xx-small')
                        else:  # Vẽ scatter plot ở các ô khác
                            for class_name in plot_data['class'].unique():
                                subset = plot_data[plot_data['class'] == class_name]
                                ax.scatter(subset[feature_columns[j]], subset[feature_columns[i]], alpha=0.5, s=10)
                        
                        # Thêm nhãn cho các trục
                        if i == n-1:  # Dòng cuối
                            ax.set_xlabel(feature_columns[j], fontsize=8)
                        if j == 0:  # Cột đầu
                            ax.set_ylabel(feature_columns[i], fontsize=8)
                        
                        # Đặt kích thước font cho các tick nhỏ lại
                        ax.tick_params(axis='both', labelsize=6)
                
                fig.suptitle(f'Pair Plot của {len(plot_data)} bản ghi đã lọc', fontsize=16)
            
            # Tạo canvas để hiển thị biểu đồ trong Tkinter
            canvas = FigureCanvasTkAgg(fig, master=plot_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Thêm thanh công cụ (toolbar)
            toolbar = NavigationToolbar2Tk(canvas, plot_frame)
            toolbar.update()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Nút để cập nhật biểu đồ
        ttk.Button(options_frame, text="Tạo biểu đồ", command=update_plot).grid(row=3, column=0, columnspan=2, padx=5, pady=10)
        
        # Nút lưu biểu đồ
        def save_plot():
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("PDF files", "*.pdf")]
            )
            if file_path:
                # Lấy biểu đồ hiện tại từ plot_frame
                for widget in plot_frame.winfo_children():
                    if isinstance(widget, FigureCanvasTkAgg):
                        widget.figure.savefig(file_path, dpi=300, bbox_inches='tight')
                        messagebox.showinfo("Thông báo", f"Đã lưu biểu đồ tại: {file_path}")
                        return
                messagebox.showwarning("Cảnh báo", "Không có biểu đồ để lưu!")
        
        ttk.Button(options_frame, text="Lưu biểu đồ", command=save_plot).grid(row=3, column=2, padx=5, pady=10)
        
        # Hiển thị biểu đồ mặc định khi mở cửa sổ
        update_plot()