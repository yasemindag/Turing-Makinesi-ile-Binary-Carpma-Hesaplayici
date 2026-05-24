# Turing Makinesi ile İkili (Binary) Çarpma Hesaplayıcı
Bu proje, Python kullanılarak tek bantlı bir Turing Makinesi üzerinde ikili (binary) sayıların çarpım işlemini gerçekleştiren bir simülasyondur. Özdevinirler Kuramı ve biçimsel diller bağlamında Turing makinelerinin çalışma prensibini anlamak ve göstermek amacıyla geliştirilmiştir.
## Özellikler
- **Tek Bantlı Turing Makinesi**: Standart tek bantlı Turing makinesi mantığıyla çalışır.
- **İkili (Binary) Çarpma**: Sadece `0` ve `1` karakterlerinden oluşan iki sayıyı çarparak sonucu hesaplar.
- **Adım Adım Simülasyon**: Çalışma sırasında her adımda durum (state), okunan karakter, yazılan karakter, kafa yönü ve bantın güncel hali konsola yazdırılır.
- **Kafa Pozisyonu Gösterimi**: Bant üzerinde Turing makinesinin kafasının (head) o an bulunduğu konum `[...]` (köşeli parantez) ile net bir şekilde belirtilir.
- **Onaltılık (Decimal) Dönüşüm**: İşlem sonunda çıkan binary sonuç otomatik olarak onluk sayı sistemine (decimal) dönüştürülür.
## Gereksinimler
- Python 3.x ortamı yeterlidir. Ekstra bir kütüphane kurulumu gerektirmez. (Sadece `graphviz.svg` dosyasını görüntülemek için bir görsel görüntüleyici veya tarayıcı kullanılabilir).
## Kurulum ve Çalıştırma
1. Projeyi klonlayın veya indirin:
   ```bash
   git clone <repo_url>
   ```
2. Terminal (veya Komut İstemi) üzerinden proje dizinine gidin:
   ```bash
   cd Turing-Makinesi-ile-Binary-Carpma-Hesaplayici
   ```
3. Python dosyasını çalıştırın:
   ```bash
   python turing_machine.py
   ```
4. Program sizden iki adet binary sayı isteyecektir. Sırasıyla giriş yapın:
   ```text
   1. Binary Sayıyı Girin (Örn: 11): 11
   2. Binary Sayıyı Girin (Örn: 10): 10
   ```
## Proje Yapısı
- `turing_machine.py`: Turing makinesinin temel durum (state) geçişlerini, bant (tape) yapısını ve simülasyon mantığını barındıran ana kaynak kodudur.
- `girdi_cikti_ornekleri/`: Makinenin doğru çalıştığını kanıtlamak adına hazırlanmış çeşitli test senaryolarını barındıran dizin.
- `graphviz.svg`: Turing makinesinin karmaşık durum geçişlerini görselleştiren diyagram dosyası.
## Makine Mantığı (Algoritma)
Bant üzerindeki format şu şekildedir: `SAYI1*SAYI2=`
Makine çarpma işlemini temel olarak **tekrarlı toplama** mantığı ile yapar:
1. `SAYI1` üzerinden bir bit işaretlenir.
2. `SAYI2`'nin tamamı, sonucun yazılacağı `=` işaretinin sağ tarafına kopyalanır (toplanır).
3. `SAYI1`'deki tüm bitler işlenene kadar bu işlem kaydırma (shift) ve işaretleme adımlarıyla devam eder.
4. Çarpma tamamlandığında bant üzerindeki yardımcı işaretler temizlenir ve makine `q_halt` durumuna ulaşarak işlemi sonlandırır.
## Örnek Çıktı
```text
**************************************************
Tek Bantlı Turing Makinesi - İkili Çarpma
**************************************************
1. Binary Sayıyı Girin (Örn: 11): 11
2. Binary Sayıyı Girin (Örn: 10): 10
Başlangıç Bant İçeriği: 11*10=
--- Simülasyon Başlıyor ---
Adım: 001 | Durum: q_start               | Okunan: 1 | Yazılan: 1 | Yön: R | Bant: 1[1]*10=
Adım: 002 | Durum: q_start               | Okunan: 1 | Yazılan: 1 | Yön: R | Bant: 11[*]*10=
...
...
...
--- Simülasyon Başarıyla Tamamlandı ---
Sonuç (Binary): 110
Sonuç (Decimal): 6
```
