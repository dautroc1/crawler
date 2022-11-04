

## 1. Cài đặt  

Cài đặt crawler như sau (trên Ubuntu)  

~~~
cd ~
git clone https://github.com/hailoc12/docbao_crawler  
cd crawler  
bash install.sh  

~~~  

Crawler sẽ tự cài đặt các lib cần thiết cùng với Firefox browser, Geckodriver  

## 2. Sử dụng  

Khi cần quét một trang, bạn chỉ cần gọi hàm read_url_source() từ module lib/utils.py  

Hàm này có cú pháp như sau:  

~~~  
def read_url_source(url, webconfig,_firefox_browser=BrowserWrapper())

function 
--------
trả về string chưá HTML source code cuả trang mà tham số url dẫn tới. Trang có thể sử dụng Ajax để load dữ liệu hoặc yêu cầu login  

input
-----
- url: link tới trang cần quét  
- webconfig: object cuả lớp WebConfig (trong lib/config.py) chứa thông tin cấu hình để quét trang url. Một số cấu hình quan trọng nhất là:  
   + 'use_browser': sử dụng Firefox browser để quét thay cho phương thức request thông thường  
   + 'browser_fast_load': kích hoạt extension adblock, chặn flash, chặn css để load trang nhanh khi dùng browser  
   + 'browser_profile': sử dụng Firefox profile (đã cài đặt trước thông qua việc chạy file setup_browser.sh) để truy cập các trang cần login  
   + 'display_browser': tắt chế độ headless cuả Browser để dễ debug hơn    
- _firefox_browser: sử dụng một browser đã được instantiate từ cuộc gọi tới read_url_source() lần trước để sử dụng tiếp trong lần quét này.  

output
------
Thành công: trả về string chứa toàn bộ HTML source cuả trang  
Thất bại: trả về None (do lỗi timeout, mất mạng...)  
Trong mọi trường hợp, _firefox_browser sẽ trả về reference tới browser được sử dụng trong cuộc gọi hàm để tái sử dụng, hoặc kill  
~~~  

## 3. Ví dụ   



a. Quét một trang duy nhất, sử dụng trình duyệt hoặc không  

~~~  
python3 crawl_single_page.py  
~~~  


~~~  
b. Quét song song nhiều trang  

python3 crawl_multiprocessing.py   



