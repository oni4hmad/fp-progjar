# FP-Progjar Pendorong Handal 💪
Final Project: Pemrograman Jaringan kelas D - Kelompok 2
![awal_github](https://user-images.githubusercontent.com/62281277/174250732-690bedd4-10af-4c40-9a6c-9b4bd0806b4f.jpg)

## ☑ Requirement
Pastikan sudah menginstall pygame
```python
pip install pygame
```

## 🕹 Untuk bermain
![preview_pendorong_handal](https://user-images.githubusercontent.com/62281277/174254486-56e1e699-5e43-4a5a-8e11-b76b451970c8.gif)

Pada folder [net-oop-single-client](https://github.com/oni4hmad/fp-progjar-game-sumo/tree/main/net-oop-single-client) terdapat file client.py, logic.py, protocol.py, server.py. Untuk dapat bermain, server perlu berjalan kemudian jalankan client.py

#### Jika dijalankan pada mesin yang berbeda
Mesin-mesin atau laptop yang digunakan berada dalam suatu koneksi WiFi, misal terdapat laptop A, laptop B, dan laptop C yang terhubung dalam suatu WiFi
1. Misal laptop A menjadi server, maka jalankan server.py, 
   setelah server berjalan di laptop A, selanjutnya jalankan client.py di laptop B dan laptop C dengan cara berikut
2. di Laptop B
   Ubah server address yang ada pada file client.py sesuai IP dari Laptop A(laptop yang menjadi server)                                
   ![image](https://user-images.githubusercontent.com/62281277/174252974-62bb16dd-ac36-4d17-a074-d7841bfb880b.png)                                        
   untuk melihat address dari laptop A atau yang menjadi server bisa dengan cara berikut
   pada laptop A buka command prompt dan ketikkan ipconfig                            
   ![image](https://user-images.githubusercontent.com/62281277/174253362-4ebd5d0c-c680-4975-9ed5-fcb702542058.png)                     
   jika pada gambar diatas yang menjadi address dalam koneksi WiFi adalah 192.168.1.3
   setelah melakukan penyesuian terhadap server address, jalankan client.py, maka laptop B akan menjadi player 1, namun screen akan merujuk pada waiting screen untuk menginformasikan menunggu adanya pasangan bermain
3. Pada laptop C
   Ulangi langkah-langkah pada laptop B, yaitu pengaturan server address(menggunakan address laptop A atau yang menjadi server) dan port kemudian jalankan client.py
   
   
### Jika dijalankan pada mesin yang sama
1. Jalankan server
2. buka terminal dan jalankan client.py dengan server address 127.0.0.1




