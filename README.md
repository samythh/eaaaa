# Tugas Besar Enterprise Architecture — RS Universitas Andalas

Workspace kerja Kelompok 4 untuk pemodelan Enterprise Architecture pada Instalasi Farmasi RS Universitas Andalas menggunakan TOGAF 9.2.

## Status per 29 September 2026

- Perizinan/surat: **selesai** (berdasarkan pembaruan dari Mikail; berkas surat belum ada di workspace).
- Wawancara utama: **selesai pada 29 September 2026** bersama apt. Dirgan Yolanda, S.Farm.
- Objek: Instalasi Farmasi RS Universitas Andalas.
- Laporan kemajuan pascawawancara: tersedia pada `05_Laporan_Kemajuan/01_Draft/Laporan_Kemajuan_EA_Kelompok_4_REVISI.docx`.
- Artefak dikerjakan melalui paket paralel pada `06_Artefak_EA/PEMBAGIAN_TUGAS_INDEPENDEN.md`.
- Informasi yang belum terkonfirmasi tetap ditandai sebagai placeholder dan tidak diisi dengan asumsi.

## Struktur folder

| Folder | Isi |
|---|---|
| `00_Manajemen_Proyek` | Ringkasan konteks, status, daftar tindak lanjut, dan pembagian kerja |
| `01_Administrasi` | Surat, proposal, lembar persetujuan, dan bukti komunikasi resmi |
| `02_Acuan_Kuliah` | Acuan lokal; materi pihak ketiga tidak diunggah ke Git |
| `03_Referensi_TOGAF` | Referensi lokal; standar berlisensi tidak diunggah ke Git |
| `04_Wawancara` | Persiapan, bukti mentah, catatan, transkrip, dokumen RS, dan hasil terstruktur |
| `05_Laporan_Kemajuan` | Draft laporan, gambar/tabel, lampiran, dan hasil final |
| `06_Artefak_EA` | Artefak Preliminary dan Fase A–D serta model Sparx yang dikerjakan |
| `07_Presentasi` | Slide dan bahan latihan presentasi |
| `99_Arsip` | Versi usang yang tidak boleh dipakai sebagai sumber kerja aktif |

## Alur kerja artefak

1. Bekukan kamus elemen bersama berdasarkan laporan dan hasil wawancara.
2. Siapkan satu model dasar, lalu berikan salinannya kepada setiap anggota.
3. Setiap anggota mengerjakan package miliknya pada file `.qea` terpisah.
4. Ekspor package XMI/XML, gambar PNG, dan catatan penjelasan.
5. Integrasikan hasil satu pintu ke model master.
6. Periksa Relationship Matrix, konsistensi AS-IS/TO-BE, sumber, dan placeholder.
7. Masukkan gambar final ke laporan dan perbarui daftar isi/gambar/tabel.

## Kebijakan data repository

Repository tidak menyimpan rekaman wawancara mentah, foto mentah, dokumen internal RS, materi perkuliahan, atau salinan standar berlisensi. Bukti mentah disimpan pada media kelompok dengan akses terbatas. Git hanya memuat hasil yang telah disanitasi dan berkas kerja yang aman untuk kolaborasi.

## Aturan penamaan file

Gunakan pola `YYYY-MM-DD_Jenis_Isi_Versi.ext`, misalnya:

- `2026-09-29_Rekaman_Wawancara_Farmasi_Asli.m4a`
- `2026-09-29_Catatan_Mutiara_Alur-Proses.md`
- `2026-09-30_BPMN_AS-IS_v01.qea`
- `2026-10-02_Laporan_Kemajuan_v03.docx`

Jangan menimpa bukti mentah. Versi final menggunakan akhiran `_FINAL` hanya setelah disetujui kelompok.
