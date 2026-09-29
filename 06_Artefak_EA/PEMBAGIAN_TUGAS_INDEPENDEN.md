# Pembagian Tugas Artefak yang Dapat Dikerjakan Mandiri

## Keputusan kerja

Pembagian tidak lagi didasarkan pada jumlah diagram. Pembagian menggunakan **paket elemen sumber dan seluruh view turunannya**. Dengan pola ini, anggota yang mengerjakan Risk Diagram juga mengerjakan Business Process–Risk Matrix; anggota yang mengerjakan Standard and Regulation juga mengerjakan Business Process–Standard and Regulation Matrix.

Relationship Matrix di Sparx merupakan view atas elemen dan connector di model. Matriks akan menampilkan hubungan apabila:

1. elemen sumber dan target sudah tersedia;
2. connector antarelemen sudah dibuat; dan
3. source package, target package, tipe connector, serta arah matriks dipilih dengan benar.

Matriks tidak dianggap sebagai data baru dan tidak boleh diisi dengan hubungan yang tidak dapat dijelaskan.

## Persiapan satu kali sebelum semua anggota mulai

Mikail menyiapkan satu model dasar, lalu membagikan **salinan yang sama** kepada seluruh anggota. Persiapan ini dilakukan sekali sebelum pekerjaan paralel dimulai, bukan menunggu hasil pekerjaan anggota lain.

File kerja yang ada saat ini masih memuat banyak package dan elemen bawaan/template. Gunakan **Save As** untuk membuat model dasar baru, lalu buat root package `K4_RS_UNAND`. Jangan memakai elemen contoh sebagai fakta RS Unand dan jangan menghapus file acuan asli.

Model dasar harus sudah memuat elemen bersama berikut.

| Kelompok elemen | Kode yang dibekukan |
|---|---|
| Proses | BP-01 sampai BP-09 |
| Architecture Goals | AG-01 sampai AG-04 |
| Architecture Principles | AP-01 sampai AP-05 |
| Risiko | R-01 sampai R-04 |
| KPI | HR-01, HR-02, dan KPI-01 berstatus belum dikonfirmasi |
| Standar/regulasi | SR-01 sampai SR-04 |
| Masalah prioritas | M-01 sampai M-03 |
| Gap | G-01 sampai G-04 |
| Aktor | Kepala Instalasi, Kepala Ruangan/Pj Gudang, Petugas Gudang, Pengadaan, Depo/Apotek, Distributor, Pihak Ketiga, dan IT |

Nama dan definisi elemen mengikuti laporan `Laporan_Kemajuan_EA_Kelompok_4_REVISI.docx`. Semua anggota boleh memakai elemen bersama, tetapi tidak boleh mengganti kode, nama, stereotype, atau package asalnya. Perubahan terhadap kamus elemen disampaikan kepada Mikail untuk diterapkan pada master.

Setiap anggota bekerja pada salinan `.qea` masing-masing. Jangan mengedit satu file `.qea` yang sama secara bersamaan melalui Google Drive, OneDrive, atau aplikasi sinkronisasi lain.

## Pembagian paket kerja

### 1. Mikail — Model dasar, Architecture Vision, BMC, dan integrasi

**Artefak:**

- kamus elemen bersama dan struktur package master;
- ringkasan Architecture Vision;
- Business Model Canvas;
- pemeriksaan akhir kode, istilah, connector, caption, dan sumber;
- integrasi package seluruh anggota ke model master.

**Package Sparx:** `K4_01_Mikail_Integration_and_Vision`

**Diletakkan pada laporan:** Subbab 4.2.3 sampai 4.2.7 dan pemeriksaan konsistensi seluruh Subbab 4.3.

**Penjelasan di bawah artefak:** ruang lingkup, pemangku kepentingan, nilai yang didukung, batas pembahasan, dasar setiap elemen BMC, serta status bahwa rancangan merupakan analisis akademik.

### 2. Mutiara — Paket proses AS-IS

**Artefak:**

- Value Chain;
- Functional Decomposition Diagram;
- BPMN AS-IS.

**Package Sparx:** `K4_02_Mutiara_Process_ASIS`

**Diletakkan pada laporan:** Subbab 4.2.6, 4.3.5, dan 4.3.6.

**Penjelasan di bawah artefak:** pemicu, lane/aktor, urutan aktivitas, input-output, gateway atau keputusan, bagian yang memakai SIMRS/Excel/manual, kontrol yang sedang berjalan, dan sumber wawancara. Diagram hanya menggambarkan kondisi yang ditemukan, bukan kondisi ideal.

### 3. Firzatunnisa — Paket target dan gap

**Artefak:**

- Architecture Goals;
- BPMN TO-BE;
- Gap Analysis.

**Package Sparx:** `K4_03_Firzatunnisa_Target_and_Gap`

**Diletakkan pada laporan:** Subbab 4.2.4, 4.3.13, dan 4.3.14.

**Penjelasan di bawah artefak:** perubahan dari baseline, masalah yang ditanggapi, hubungan dengan AG/AP/M/G, kontrol lama yang dipertahankan, aktivitas yang ditambah atau diubah, serta bagian yang masih memerlukan validasi Farmasi/IT. TO-BE tidak boleh ditulis sebagai rencana yang telah disetujui RS.

Firzatunnisa tidak menunggu BPMN Mutiara. Keduanya memakai spesifikasi proses BP-01 sampai BP-09 dan rincian AS-IS yang sudah dibekukan di laporan. Saat integrasi, Mikail hanya memeriksa konsistensi antara dua model tersebut.

### 4. Taris — Paket risiko dan KPI

**Artefak:**

- Risk Diagram;
- KPI Diagram;
- Business Process–Risk Matrix;
- Business Process–KPI Matrix.

**Package Sparx:** `K4_04_Taris_Risk_and_KPI`

**Diletakkan pada laporan:** Subbab 4.3.7, 4.3.8, dan 4.3.10 untuk dua matriks terkait.

**Penjelasan di bawah artefak:** definisi risiko, penyebab, dampak, kontrol saat ini, proses terkait, alasan setiap tanda hubungan dalam matriks, serta sumbernya. HR-01 dan HR-02 harus dijelaskan sebagai indikator personel, bukan KPI proses. KPI-01 tetap diberi status belum dikonfirmasi; jangan membuat nama, rumus, atau target resmi sendiri.

### 5. Sheva — Paket prinsip, standar, dan regulasi

**Artefak:**

- Architecture Principles;
- Business Principles;
- Standard and Regulation Diagram;
- Business Process–Standard and Regulation Matrix.

**Package Sparx:** `K4_05_Sheva_Principles_and_Standards`

**Diletakkan pada laporan:** Subbab 4.1.4, 4.3.2, 4.3.9, dan 4.3.10 untuk matriks standar/regulasi.

**Penjelasan di bawah artefak:** statement, rationale, implication, sumber aturan, status berlaku, proses yang dipengaruhi, dan alasan setiap hubungan dalam matriks. SR-01 dapat memakai Permenkes Nomor 72 Tahun 2016. SR-02 sampai SR-04 tetap ditandai belum lengkap sampai judul, nomor, versi, atau dokumen internal diperoleh.

### 6. Ihsan — Paket organisasi dan interaksi

**Artefak:**

- Organization Decomposition Diagram;
- Organization Role Diagram;
- Business Interaction Matrix;
- ringkasan stakeholder dan concern.

**Package Sparx:** `K4_06_Ihsan_Organization_and_Interaction`

**Diletakkan pada laporan:** Subbab 4.2.3, 4.2.8, 4.3.3, dan 4.3.11.

**Penjelasan di bawah artefak:** struktur organisasi yang terkonfirmasi, aktor dan perannya, hubungan aktor dengan proses, arti R/A/C/I, kewenangan yang masih bersifat draf, dan sumber setiap peran. Jabatan apt. Dirgan Yolanda, S.Farm. pada wawancara dibedakan dari catatan historis tahun 2022.

## Lokasi hasil setiap anggota

Gunakan pola berikut agar integrasi tidak tercampur:

- file kerja: `06_Artefak_EA/Model_Sparx/Working_Anggota/[NIM]_[Nama]_Working.qea`;
- package hasil ekspor: `06_Artefak_EA/Model_Sparx/Package_XMI/[Nama]/`;
- gambar PNG: `05_Laporan_Kemajuan/02_Gambar_dan_Tabel/[Nama]/`;
- catatan penjelasan: `06_Artefak_EA/Catatan_Artefak/[Nama]/`.

Nama file gambar memakai nomor laporan, misalnya `Gambar_4.6_BPMN_ASIS.png`. Setiap anggota menyerahkan file `.qea`, package XMI/XML, gambar PNG, dan catatan penjelasan. Untuk matriks, sertakan juga screenshot/ekspor matriks serta catatan source package, target package, connector type, dan direction karena pengaturan tampilan matriks dapat perlu dibuat ulang pada master.

## Aturan agar pekerjaan benar-benar paralel

1. Gunakan salinan model dasar yang sama agar GUID elemen bersama tetap sama.
2. Kerjakan hanya di bawah root package `K4_RS_UNAND`; elemen bawaan/template tidak boleh dimasukkan ke laporan.
3. Jangan membuat ulang BP, AG, AP, R, KPI, SR, M, G, atau aktor yang sudah tersedia.
4. Jangan mengubah elemen bersama; hanya buat diagram, connector, note, atau elemen lokal pada package milik sendiri.
5. Jangan menunggu gambar anggota lain. Gunakan fakta dan kamus elemen yang sudah dibekukan dalam laporan.
6. Jika menemukan konflik data, tandai `[PERLU KONFIRMASI]`; jangan menebak dan jangan menghentikan pekerjaan anggota lain.
7. Integrasi dilakukan satu pintu oleh Mikail setelah seluruh package selesai.
8. Sesudah integrasi, pemilik paket memeriksa kembali hasilnya, tetapi tidak mengedit master secara bersamaan.

## Format penjelasan singkat di bawah setiap gambar atau matriks

Gunakan satu atau dua paragraf dengan urutan berikut:

1. **Apa yang digambarkan:** tujuan dan batas artefak.
2. **Apa isinya:** elemen, aktor, aktivitas, atau hubungan utama.
3. **Dasarnya:** wawancara, dokumen resmi, atau analisis tim.
4. **Maknanya:** temuan yang dapat ditarik dari artefak.
5. **Statusnya:** fakta AS-IS, usulan TO-BE, atau bagian yang masih perlu konfirmasi.

Hindari kalimat “gambar di atas menjelaskan” tanpa isi. Sebutkan temuan konkretnya dan jangan menyatakan analisis tim sebagai kebijakan resmi RS.

## Teks siap kirim ke WhatsApp

Teman-teman, pembagian artefak kita revisi supaya masing-masing bisa bekerja paralel dan tidak perlu menunggu diagram orang lain.

Di Sparx, matrix sebenarnya hanya menampilkan hubungan antara elemen sumber dan target. Contohnya BP–Risk Matrix memakai elemen Business Process dan Risk. Jadi matrix tidak dibagikan sebagai tugas yang berdiri sendiri, tetapi disatukan dengan orang yang mengerjakan elemen targetnya.

Sebelum mulai, Mikail menyiapkan satu model dasar yang sudah berisi kode dan elemen bersama: BP-01–BP-09, AG-01–AG-04, AP-01–AP-05, R-01–R-04, KPI, SR-01–SR-04, M-01–M-03, G-01–G-04, dan daftar aktor. Setelah itu, semua orang mendapat salinan model dasar yang sama dan bekerja di file `.qea` masing-masing. Jadi tidak perlu menunggu orang lain selesai.

Pembagiannya:

1. **Mikail:** model dasar, Architecture Vision, Business Model Canvas, dan integrasi akhir.
2. **Mutiara:** Value Chain, Functional Decomposition, dan BPMN AS-IS.
3. **Firzatunnisa:** Architecture Goals, BPMN TO-BE, dan Gap Analysis.
4. **Taris:** Risk Diagram, KPI Diagram, BP–Risk Matrix, dan BP–KPI Matrix.
5. **Sheva:** Architecture Principles, Business Principles, Standard and Regulation, serta BP–Standard/Regulation Matrix.
6. **Ihsan:** Organization Decomposition, Organization Role, Business Interaction Matrix, serta stakeholder dan concern.

Mutiara dan Firzatunnisa tetap bisa bekerja bersamaan karena keduanya memakai BP-01–BP-09 serta rincian proses yang sudah ada dalam laporan. Firzatunnisa tidak perlu menunggu gambar AS-IS selesai. Nanti saat integrasi, Mikail memeriksa konsistensinya.

Setiap orang mengumpulkan empat hal: file kerja `.qea`, package hasil ekspor XMI/XML, gambar PNG, dan penjelasan singkat. Untuk matrix, tambahkan screenshot/ekspor matrix dan catat source package, target package, connector type, serta direction.

Di bawah setiap artefak jelaskan: tujuan artefak, isi/relasi utamanya, sumber datanya, temuan yang terlihat, dan statusnya apakah AS-IS, usulan TO-BE, atau masih perlu konfirmasi. Jangan membuat data, KPI, regulasi, atau kebijakan yang tidak ada sumbernya.

Penting: jangan edit file `.qea` yang sama secara bersamaan dan jangan membuat ulang elemen yang sudah ada di model dasar. Kalau ada data yang belum jelas, beri tanda `[PERLU KONFIRMASI]`, lanjutkan bagian lain, lalu sampaikan saat integrasi.
