HƯỚNG DẪN SỬ DỤNG SUPERLABEL  
  
superlabel là một tool dùng để gán nhãn dữ liệu theo kiểu gõ capcha.  
I.Sử dụng:  
- Vào link sau để sử dụng tool:  
http://xxx/superlabel/home?mode=index&index=0  
- Tool có 2 chế độ load ảnh:  
+ mode=random  
http://xxx/superlabel/home?mode=random  
Trong chế độ random ảnh sẽ được load ngẫu nhiên không theo thứ tự nào do đó sẽ có trường hợp bị load lại ảnh đã gán nhãn rồi. Phù hợp khi chỉ cần gán nhãn ngẫu nhiên một phần tập dữ liệu.  
+ mode=index  
http://xxx/superlabel/home?mode=index&index=0  
Trong chế độ ảnh sẽ được load theo thứ tự chỉ mục, trong link trên có index=0 nên khi load sẽ load ảnh tương ứng index=0. Do giá trị index không thay đổi nên khi nhiều người gán nhãn có thể chia tập dữ liệu thành nhiều phần, ví dụ:  
Tập dữ liệu có 15000 ảnh và mỗi người sẽ gán nhãn 5000 ảnh khi đó ta có thể chia tập dữ liệu thành 3 phần tương ứng với index=0, index=5000 và index=10000 như 3 link sau:  
http://xxx/superlabel/home?mode=index&index=0  
http://xxx/superlabel/home?mode=index&index=5000  
http://xxx/superlabel/home?mode=index&index=10000  
- Giao diện tool gồm: ảnh cần gán nhãn và ô nhập liệu.  
- Để sử dụng chỉ cần gõ nhãn của ảnh vào ô nhập liệu rồi nhấn enter để lưu (cập nhật) và chuyển sang ảnh tiếp theo.  
- Sử dụng dấu mũi tên trái, phải để thay đổi ảnh, lúc này kết quả không được lưu (cập nhật).  
  
II. Một số chú ý khi gán nhãn:  
- Đối với những ảnh quá mờ, không nhìn rõ chữ thì bỏ trống.  
- Nhãn phân biệt hoa, thường.  
- Nhập cả các dấu câu, ký tự đặc biệt.
