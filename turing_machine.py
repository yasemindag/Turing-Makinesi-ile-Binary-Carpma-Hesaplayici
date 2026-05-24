import sys

class TuringMachine:
    def __init__(self, tape_str):
        self.tape = list(tape_str)
        self.head = 0
        self.state = 'q_start'
        self.step_count = 0
        self.transitions = {
            # Başlangıç ve Sonucun 0'a eşitlenmesi
            ('q_start', '0'): ('q_start', '0', 'R'),
            ('q_start', '1'): ('q_start', '1', 'R'),
            ('q_start', '*'): ('q_start', '*', 'R'),
            ('q_start', '='): ('q_init_res', '=', 'R'),
            ('q_init_res', '_'): ('q_main_loop_find_eq', '0', 'L'),
            ('q_main_loop_find_eq', '='): ('q_main_loop', '=', 'L'),
            ('q_main_loop_find_eq', '0'): ('q_main_loop_find_eq', '0', 'L'),
            ('q_main_loop_find_eq', '1'): ('q_main_loop_find_eq', '1', 'L'),

            # Ana Döngü
            ('q_main_loop', 'a'): ('q_main_loop', 'a', 'L'),
            ('q_main_loop', 'b'): ('q_main_loop', 'b', 'L'),
            ('q_main_loop', '0'): ('q_shift_num1_find_star', 'a', 'L'),
            ('q_main_loop', '1'): ('q_add_return_to_num1', 'b', 'L'),
            ('q_main_loop', '*'): ('q_cleanup', '*', 'R'),

            # 1. Sayıyı Sola Kaydırma (0 ekleme) - Arama
            ('q_shift_num1_find_star', '0'): ('q_shift_num1_find_star', '0', 'L'),
            ('q_shift_num1_find_star', '1'): ('q_shift_num1_find_star', '1', 'L'),
            ('q_shift_num1_find_star', '='): ('q_shift_num1_find_star', '=', 'L'),
            ('q_shift_num1_find_star', 'a'): ('q_shift_num1_find_star', 'a', 'L'),
            ('q_shift_num1_find_star', 'b'): ('q_shift_num1_find_star', 'b', 'L'),
            ('q_shift_num1_find_star', '*'): ('q_shift_hold_star', '0', 'R'),

            # Sağa Kaydırma (Tutma) Durumları
            ('q_shift_hold_star', '0'): ('q_shift_hold_0', '*', 'R'),
            ('q_shift_hold_star', '1'): ('q_shift_hold_1', '*', 'R'),
            ('q_shift_hold_star', 'a'): ('q_shift_hold_a', '*', 'R'),
            ('q_shift_hold_star', 'b'): ('q_shift_hold_b', '*', 'R'),
            ('q_shift_hold_star', '='): ('q_shift_hold_eq', '*', 'R'),

            ('q_shift_hold_0', '0'): ('q_shift_hold_0', '0', 'R'),
            ('q_shift_hold_0', '1'): ('q_shift_hold_1', '0', 'R'),
            ('q_shift_hold_0', 'a'): ('q_shift_hold_a', '0', 'R'),
            ('q_shift_hold_0', 'b'): ('q_shift_hold_b', '0', 'R'),
            ('q_shift_hold_0', '='): ('q_shift_hold_eq', '0', 'R'),
            ('q_shift_hold_0', '_'): ('q_main_loop_find_eq', '0', 'L'),

            ('q_shift_hold_1', '0'): ('q_shift_hold_0', '1', 'R'),
            ('q_shift_hold_1', '1'): ('q_shift_hold_1', '1', 'R'),
            ('q_shift_hold_1', 'a'): ('q_shift_hold_a', '1', 'R'),
            ('q_shift_hold_1', 'b'): ('q_shift_hold_b', '1', 'R'),
            ('q_shift_hold_1', '='): ('q_shift_hold_eq', '1', 'R'),
            ('q_shift_hold_1', '_'): ('q_main_loop_find_eq', '1', 'L'),

            ('q_shift_hold_a', '0'): ('q_shift_hold_0', 'a', 'R'),
            ('q_shift_hold_a', '1'): ('q_shift_hold_1', 'a', 'R'),
            ('q_shift_hold_a', 'a'): ('q_shift_hold_a', 'a', 'R'),
            ('q_shift_hold_a', 'b'): ('q_shift_hold_b', 'a', 'R'),
            ('q_shift_hold_a', '='): ('q_shift_hold_eq', 'a', 'R'),

            ('q_shift_hold_b', '0'): ('q_shift_hold_0', 'b', 'R'),
            ('q_shift_hold_b', '1'): ('q_shift_hold_1', 'b', 'R'),
            ('q_shift_hold_b', 'a'): ('q_shift_hold_a', 'b', 'R'),
            ('q_shift_hold_b', 'b'): ('q_shift_hold_b', 'b', 'R'),
            ('q_shift_hold_b', '='): ('q_shift_hold_eq', 'b', 'R'),

            ('q_shift_hold_eq', '0'): ('q_shift_hold_0', '=', 'R'),
            ('q_shift_hold_eq', '1'): ('q_shift_hold_1', '=', 'R'),
            ('q_shift_hold_eq', '_'): ('q_main_loop_find_eq', '=', 'L'),

            # Toplama İşlemi (1. Sayıya Dönüş)
            ('q_add_return_to_num1', '0'): ('q_add_return_to_num1', '0', 'L'),
            ('q_add_return_to_num1', '1'): ('q_add_return_to_num1', '1', 'L'),
            ('q_add_return_to_num1', 'a'): ('q_add_return_to_num1', 'a', 'L'),
            ('q_add_return_to_num1', 'b'): ('q_add_return_to_num1', 'b', 'L'),
            ('q_add_return_to_num1', '='): ('q_add_return_to_num1', '=', 'L'),
            ('q_add_return_to_num1', 'x'): ('q_add_return_to_num1', 'x', 'L'),
            ('q_add_return_to_num1', 'y'): ('q_add_return_to_num1', 'y', 'L'),
            ('q_add_return_to_num1', '*'): ('q_add_find_unmarked', '*', 'L'),

            # İşlenmemiş Bit Bulma
            ('q_add_find_unmarked', 'A'): ('q_add_find_unmarked', 'A', 'L'),
            ('q_add_find_unmarked', 'B'): ('q_add_find_unmarked', 'B', 'L'),
            ('q_add_find_unmarked', '0'): ('q_add_0_to_res_find_end', 'A', 'R'),
            ('q_add_find_unmarked', '1'): ('q_add_1_to_res_find_end', 'B', 'R'),
            ('q_add_find_unmarked', '_'): ('q_add_unmark', '_', 'R'),

            # Sonuca 0 veya 1 Eklemek İçin Bant Sonuna Gitme
            ('q_add_0_to_res_find_end', 'A'): ('q_add_0_to_res_find_end', 'A', 'R'),
            ('q_add_0_to_res_find_end', 'B'): ('q_add_0_to_res_find_end', 'B', 'R'),
            ('q_add_0_to_res_find_end', '*'): ('q_add_0_to_res_find_end', '*', 'R'),
            ('q_add_0_to_res_find_end', 'a'): ('q_add_0_to_res_find_end', 'a', 'R'),
            ('q_add_0_to_res_find_end', 'b'): ('q_add_0_to_res_find_end', 'b', 'R'),
            ('q_add_0_to_res_find_end', '='): ('q_add_0_to_res_find_end', '=', 'R'),
            ('q_add_0_to_res_find_end', '0'): ('q_add_0_to_res_find_end', '0', 'R'),
            ('q_add_0_to_res_find_end', '1'): ('q_add_0_to_res_find_end', '1', 'R'),
            ('q_add_0_to_res_find_end', 'x'): ('q_add_0_to_res_find_end', 'x', 'R'),
            ('q_add_0_to_res_find_end', 'y'): ('q_add_0_to_res_find_end', 'y', 'R'),
            ('q_add_0_to_res_find_end', '_'): ('q_add_0_to_res', '_', 'L'),

            ('q_add_1_to_res_find_end', 'A'): ('q_add_1_to_res_find_end', 'A', 'R'),
            ('q_add_1_to_res_find_end', 'B'): ('q_add_1_to_res_find_end', 'B', 'R'),
            ('q_add_1_to_res_find_end', '*'): ('q_add_1_to_res_find_end', '*', 'R'),
            ('q_add_1_to_res_find_end', 'a'): ('q_add_1_to_res_find_end', 'a', 'R'),
            ('q_add_1_to_res_find_end', 'b'): ('q_add_1_to_res_find_end', 'b', 'R'),
            ('q_add_1_to_res_find_end', '='): ('q_add_1_to_res_find_end', '=', 'R'),
            ('q_add_1_to_res_find_end', '0'): ('q_add_1_to_res_find_end', '0', 'R'),
            ('q_add_1_to_res_find_end', '1'): ('q_add_1_to_res_find_end', '1', 'R'),
            ('q_add_1_to_res_find_end', 'x'): ('q_add_1_to_res_find_end', 'x', 'R'),
            ('q_add_1_to_res_find_end', 'y'): ('q_add_1_to_res_find_end', 'y', 'R'),
            ('q_add_1_to_res_find_end', '_'): ('q_add_1_to_res', '_', 'L'),

            # Toplama Mantığı (0 Ekle)
            ('q_add_0_to_res', 'x'): ('q_add_0_to_res', 'x', 'L'),
            ('q_add_0_to_res', 'y'): ('q_add_0_to_res', 'y', 'L'),
            ('q_add_0_to_res', '0'): ('q_add_return_to_num1', 'x', 'L'),
            ('q_add_0_to_res', '1'): ('q_add_return_to_num1', 'y', 'L'),
            ('q_add_0_to_res', '='): ('q_insert_res_x', '=', 'R'),

            # Toplama Mantığı (1 Ekle)
            ('q_add_1_to_res', 'x'): ('q_add_1_to_res', 'x', 'L'),
            ('q_add_1_to_res', 'y'): ('q_add_1_to_res', 'y', 'L'),
            ('q_add_1_to_res', '0'): ('q_add_return_to_num1', 'y', 'L'),
            ('q_add_1_to_res', '1'): ('q_add_carry', 'x', 'L'),
            ('q_add_1_to_res', '='): ('q_insert_res_y', '=', 'R'),

            # Elde (Carry) Mantığı
            ('q_add_carry', '0'): ('q_add_return_to_num1', '1', 'L'),
            ('q_add_carry', '1'): ('q_add_carry', '0', 'L'),
            ('q_add_carry', '='): ('q_insert_res_1', '=', 'R'),

            # Yeni Basamak Ekleme (Araya Girme)
            ('q_insert_res_x', '0'): ('q_insert_hold_0', 'x', 'R'),
            ('q_insert_res_x', '1'): ('q_insert_hold_1', 'x', 'R'),
            ('q_insert_res_x', 'x'): ('q_insert_hold_x', 'x', 'R'),
            ('q_insert_res_x', 'y'): ('q_insert_hold_y', 'x', 'R'),
            ('q_insert_res_x', '_'): ('q_add_return_to_num1', 'x', 'L'),

            ('q_insert_res_y', '0'): ('q_insert_hold_0', 'y', 'R'),
            ('q_insert_res_y', '1'): ('q_insert_hold_1', 'y', 'R'),
            ('q_insert_res_y', 'x'): ('q_insert_hold_x', 'y', 'R'),
            ('q_insert_res_y', 'y'): ('q_insert_hold_y', 'y', 'R'),
            ('q_insert_res_y', '_'): ('q_add_return_to_num1', 'y', 'L'),

            ('q_insert_res_1', '0'): ('q_insert_hold_0', '1', 'R'),
            ('q_insert_res_1', '1'): ('q_insert_hold_1', '1', 'R'),
            ('q_insert_res_1', 'x'): ('q_insert_hold_x', '1', 'R'),
            ('q_insert_res_1', 'y'): ('q_insert_hold_y', '1', 'R'),
            ('q_insert_res_1', '_'): ('q_add_return_to_num1', '1', 'L'),

            ('q_insert_hold_0', '0'): ('q_insert_hold_0', '0', 'R'),
            ('q_insert_hold_0', '1'): ('q_insert_hold_1', '0', 'R'),
            ('q_insert_hold_0', 'x'): ('q_insert_hold_x', '0', 'R'),
            ('q_insert_hold_0', 'y'): ('q_insert_hold_y', '0', 'R'),
            ('q_insert_hold_0', '_'): ('q_add_return_to_num1', '0', 'L'),

            ('q_insert_hold_1', '0'): ('q_insert_hold_0', '1', 'R'),
            ('q_insert_hold_1', '1'): ('q_insert_hold_1', '1', 'R'),
            ('q_insert_hold_1', 'x'): ('q_insert_hold_x', '1', 'R'),
            ('q_insert_hold_1', 'y'): ('q_insert_hold_y', '1', 'R'),
            ('q_insert_hold_1', '_'): ('q_add_return_to_num1', '1', 'L'),

            ('q_insert_hold_x', '0'): ('q_insert_hold_0', 'x', 'R'),
            ('q_insert_hold_x', '1'): ('q_insert_hold_1', 'x', 'R'),
            ('q_insert_hold_x', 'x'): ('q_insert_hold_x', 'x', 'R'),
            ('q_insert_hold_x', 'y'): ('q_insert_hold_y', 'x', 'R'),
            ('q_insert_hold_x', '_'): ('q_add_return_to_num1', 'x', 'L'),

            ('q_insert_hold_y', '0'): ('q_insert_hold_0', 'y', 'R'),
            ('q_insert_hold_y', '1'): ('q_insert_hold_1', 'y', 'R'),
            ('q_insert_hold_y', 'x'): ('q_insert_hold_x', 'y', 'R'),
            ('q_insert_hold_y', 'y'): ('q_insert_hold_y', 'y', 'R'),
            ('q_insert_hold_y', '_'): ('q_add_return_to_num1', 'y', 'L'),

            # İşaretleri Kaldırma (Bir Sonraki Sayı İçin)
            ('q_add_unmark', 'A'): ('q_add_unmark', '0', 'R'),
            ('q_add_unmark', 'B'): ('q_add_unmark', '1', 'R'),
            ('q_add_unmark', 'x'): ('q_add_unmark', '0', 'R'),
            ('q_add_unmark', 'y'): ('q_add_unmark', '1', 'R'),
            ('q_add_unmark', '0'): ('q_add_unmark', '0', 'R'),
            ('q_add_unmark', '1'): ('q_add_unmark', '1', 'R'),
            ('q_add_unmark', '*'): ('q_add_unmark', '*', 'R'),
            ('q_add_unmark', 'a'): ('q_add_unmark', 'a', 'R'),
            ('q_add_unmark', 'b'): ('q_add_unmark', 'b', 'R'),
            ('q_add_unmark', '='): ('q_add_unmark', '=', 'R'),
            ('q_add_unmark', '_'): ('q_shift_num1_find_star', '_', 'L'),

            # Temizlik ve Kabul
            ('q_cleanup', '*'): ('q_cleanup', '*', 'R'),
            ('q_cleanup', 'a'): ('q_cleanup', '0', 'R'),
            ('q_cleanup', 'b'): ('q_cleanup', '1', 'R'),
            ('q_cleanup', '='): ('q_halt', '=', 'R'),
        }

    def read_tape(self):
        if self.head < 0:
            self.tape.insert(0, '_')
            self.head = 0
        elif self.head >= len(self.tape):
            self.tape.append('_')
        return self.tape[self.head]

    def write_tape(self, char):
        self.tape[self.head] = char

    def step(self):
        self.step_count += 1
        read_sym = self.read_tape()
        key = (self.state, read_sym)
        if key in self.transitions:
            next_state, write_sym, move = self.transitions[key]
            self.write_tape(write_sym)
            
            # Kafa pozisyonunu bant üzerinde netçe göstermek için köşeli parantez kullanıyoruz
            tape_with_head = "".join(self.tape[:self.head]) + f"[{self.tape[self.head]}]" + "".join(self.tape[self.head+1:])
            
            print(f"Adım: {self.step_count:03d} | Durum: {self.state:<22} | Okunan: {read_sym} | Yazılan: {write_sym} | Yön: {move} | Bant: {tape_with_head}")
            
            self.state = next_state
            if move == 'R':
                self.head += 1
            elif move == 'L':
                self.head -= 1
        else:
            print(f"\nHATA: Geçiş bulunamadı. Adım: {self.step_count}, Durum: {self.state}, Okunan: {read_sym}")
            self.state = 'q_reject'

    def run(self):
        print("--- Simülasyon Başlıyor ---")
        while self.state not in ['q_halt', 'q_reject']:
            self.step()
        
        if self.state == 'q_halt':
            tape_str = "".join(self.tape)
            result_bin = tape_str.split('=')[1].replace('_', '')
            if not result_bin:
                result_bin = "0"
            result_dec = int(result_bin, 2)
            print("\n--- Simülasyon Başarıyla Tamamlandı ---")
            print(f"Sonuç (Binary): {result_bin}")
            print(f"Sonuç (Decimal): {result_dec}")
        else:
            print("\n--- Simülasyon Reddedildi (q_reject) ---")

if __name__ == "__main__":
    print("*" * 50)
    print("Tek Bantlı Turing Makinesi - İkili Çarpma")
    print("*" * 50)
    num1 = input("1. Binary Sayıyı Girin (Örn: 11): ").strip()
    num2 = input("2. Binary Sayıyı Girin (Örn: 10): ").strip()
    
    if not all(c in '01' for c in num1) or not all(c in '01' for c in num2):
        print("HATA: Girdiler sadece '0' ve '1' içermelidir!")
        sys.exit(1)
        
    initial_tape = f"{num1}*{num2}="
    print(f"\nBaşlangıç Bant İçeriği: {initial_tape}")
    
    tm = TuringMachine(initial_tape)
    tm.run()
