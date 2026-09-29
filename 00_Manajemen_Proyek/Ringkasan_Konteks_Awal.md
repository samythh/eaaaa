# Ringkasan Konteks — Tugas Besar Enterprise Architecture (Kelompok Mikail)

Dokumen serah-terima untuk melanjutkan pekerjaan di chat atau AI lain. Disusun akhir September 2026.
Semua yang ditandai **[BELUM PASTI]** belum dikonfirmasi — jangan diperlakukan sebagai fakta.

---

## 0. Instruksi untuk AI yang Melanjutkan

- Bahasa Indonesia santai tapi sopan, langsung ke inti, output siap copas, setara mahasiswa semester 4. Hindari jargon berlebihan dan gaya khas AI.
- Berpihak pada kebenaran, bukan pada pengguna. Kalau salah, bilang salah. Kalau tidak tahu, bilang tidak tahu.
- Bedakan: fakta dari dokumen (sebut sumbernya), fakta dari web (sertakan tautan), pendapat, dan yang tidak diketahui.
- Jangan mengarang nomor peraturan, nama, gelar, angka, atau rujukan. Verifikasi hal yang bisa berubah (jabatan, dsb.).
- Kalau mengoreksi jawaban sendiri, sebutkan apa yang salah sebelumnya.
- Sebutkan risiko akademik, reputasi, atau privasi meski tidak ditanya.

---

## 1. Tentang Tugas

| Hal | Keterangan |
|---|---|
| Mata kuliah | Enterprise Architecture |
| Kampus | Departemen/Prodi Sistem Informasi, FTI, Universitas Andalas |
| Dosen | Adi Arga Arifnur, M.Kom |
| Ketua Departemen | Ricky Akbar, M.Kom |
| Admin surat | Bu Nindy (disebut di slide P2 untuk permintaan surat) |
| Framework | TOGAF 9.2 |
| Tools | Sparx Enterprise Architect (ada template di modul praktikum) |
| Status proposal | Tenggat sudah lewat, **tidak terkumpul** karena kendala perizinan. Lanjut ke Laporan Kemajuan. |
| Tenggat Laporan Kemajuan | **[BELUM PASTI]** belum diketahui |

---

## 2. Aturan dari Pak Adi

### 2.1 Laporan Kemajuan (slide Pertemuan 04)

- Format: Times New Roman 12, spasi 1,5, margin 2,54 cm semua sisi. Cover bebas.
- Nama file: `Laporan Kemajuan EA Kelompok X.docx`, dikumpulkan di Classroom (Tugas Besar – Laporan Kemajuan).
- **Wajib** melampirkan foto dokumentasi observasi/wawancara.
- Sistematika:
  - Cover, Lembar Persetujuan, Kata Pengantar, Daftar Isi, Daftar Gambar, Daftar Tabel, Daftar Lampiran
  - BAB I Pendahuluan: 1.1 Latar Belakang, 1.2 Rumusan Masalah, 1.3 Ruang Lingkup, 1.4 Tujuan dan Manfaat
  - BAB II Landasan Teori
  - BAB III Metode Pelaksanaan
  - BAB IV Hasil dan Pembahasan: 4.1 Preliminary Phase, 4.2 Architecture Vision, 4.3 Business Architecture
  - Daftar Referensi, Lampiran A, B, …, Z
- Presentasi: Pertemuan 06 dan 07, kelompok dipilih acak, maks. 30 menit dibagi rata ke semua anggota. **Semua anggota wajib hadir dan memahami keseluruhan pekerjaan.** Dosen bisa bertanya acak.

### 2.2 Sistematika Proposal (slide P2) — tetap berguna untuk isi laporan

- Proposal = penerapan Fase Preliminary TOGAF 9.2.
- Lembar Persetujuan: ttd **pimpinan organisasi/bagian** dan **ketua tim arsitek**.
- BAB III berisi: Subjek dan objek, Teknik pengumpulan data, Alur Pelaksanaan (Tailoring the Framework), Jadwal, Biaya, Tools (Sparx), Identifikasi Stakeholder, Tim Arsitek, Architecture Principles, Ringkasan Hasil Preliminary Phase (tabel).
- Proposal dan Laporan Kemajuan **tidak memakai Penutup**.
- Kriteria awal objek: organisasi besar (>50 orang), sebaiknya swasta, sudah punya SOP.

### 2.3 Arahan Lain

- **Stakeholder** menurut Pak Adi: *internal* = tim arsitek (kita), *eksternal* = organisasi yang diteliti.
- Cakupan: Laporan Kemajuan sampai Fase B. **Fase C dan D menyusul, "sepertinya setelah UTS" [BELUM PASTI]**. Fase E–H tidak dikerjakan.
- Pernah ditemukan beda di slide: tertulis 4 kelompok vs 5 kelompok (minor).

### 2.4 Modul Praktikum (Lab TKITI, 2026)

- Modul I — Fase A, 6 artefak: Architecture Principles, Architecture Goals, Vision-Mission-Strategic Planning, Value Chain Diagram, Business Model Canvas, Organization Decomposition Diagram.
- Modul II — Fase B, 10 artefak: Business Principles, Organization Role Diagram, Risk Diagram, KPI Diagram, Standard and Regulation, Business Process Diagram (BPMN), Functional Decomposition Diagram, BP–Risk Matrix, BP–KPI Matrix, BP–Standard and Regulation Matrix.
- **[BELUM PASTI]** Modul II juga menyebut versi lain deliverable Fase B: BPMN AS-IS & TO-BE, Functional Decomposition, Business Interaction Matrix, Gap Analysis. Perlu ditanyakan mana yang wajib. Pilihan aman: 10 artefak + BPMN AS-IS & TO-BE + gap analysis.
- Modul untuk Fase C dan D belum diterima.

---

## 3. Tim (6 orang)

| Nama | NIM | Peran arsitek (usulan) | Saat observasi |
|---|---|---|---|
| Mikail Samyth Habibillah (Ketua) | 2411523016 | Lead Architect | Memimpin wawancara; satu-satunya yang berkomunikasi dengan RS |
| Mutiara Ayudya Ramadhani | 2411523008 | Business Architect | Mencatat alur kerja (BPMN) |
| Firzatunnisa | 2411523011 | Data & Application Architect | Mencatat sistem, data, sesi IT |
| Taris Rafivdean | 2411523013 | Technology Architect | Mencatat risiko, indikator, regulasi |
| Sheva Ramadhan | 2411523020 | Documentation & Requirements | Mencatat unit dilayani, mitra, sumber daya, peran; urus dokumen |
| Ihsan Auliya Habiburrahim | 2411523022 | Documentation & Requirements | Dokumentasi foto & video |

**[PERIKSA]** Di surat fakultas tertulis "Ihsan Auliya **Habiburrohim**", sedangkan ejaan yang diberikan Mikail "**Habiburrahim**". Pastikan ejaan yang benar sebelum dokumen resmi berikutnya.

---

## 4. Objek Studi

| Hal | Keterangan |
|---|---|
| Organisasi | Rumah Sakit Universitas Andalas (RS Unand), Limau Manis, Kec. Pauh, Padang |
| Kontak resmi | (0751) 8465000 · rsp.unand.ac.id |
| Unit | Instalasi Farmasi — **nama resmi unit [BELUM PASTI]** |
| Fokus | Pengelolaan perbekalan farmasi: perencanaan, pengadaan, penerimaan, penyimpanan, distribusi, pengendalian stok, kedaluwarsa/rusak, pelaporan |
| Direktur Utama | Dr. dr. Muhammad Riendra, Sp.BTKV, Subsp.VE(K), FIATCVS (periode 2025–2029, terverifikasi dari situs resmi RS Unand) |
| Kepala Instalasi Farmasi | **[BELUM PASTI]** nama belum diketahui — kemungkinan penandatangan Lembar Persetujuan |

### 4.1 Struktur Organisasi RS Unand 2026

Sumber: Lampiran Keputusan Rektor Universitas Andalas Nomor 1143/UN16.R/KPT/XIII/2026, tanggal 6 April 2026 (salin nomor persis dari dokumen aslinya).

- Rektor Universitas Andalas: Dr. Efa Yonnedi, SE, MPPM, Akt, CA, CRGP
- Direktur Utama → tiga direktur:
  - **Direktur Pelayanan Medik dan Keperawatan**: Dr. dr. Yose Ramda Ilhami, Sp.JP(K)
    - Kabid Pelayanan Medik, Kabid Keperawatan, **Kabid Penunjang Medik: dr. Elfira Yusri, Sp.PK(K), MMRS** (seksi: Perencanaan Alat Kesehatan — dr. Nining Kurniawati; Monev Alat Kesehatan)
  - **Direktur Umum dan Sumber Daya**: dr. Rozi Abdullah, MARS, Sp.FK
    - **Kabid Pendidikan dan Penelitian (= Diklit): dr. Putri Yuriandini Yulsam**, Kabid SDM, Kabid Umum, Kabid Hukum-Komunikasi-Kerjasama Strategis
  - **Direktur Keuangan dan Perencanaan**: Mohamad Fany Alfarisi, SE, MS.Fin, PhD
    - Kabid Perencanaan & Anggaran (Reinny Patrisina), Kabid Akuntansi & Perpajakan (termasuk **Seksi Logistik & Inventaris: Herrik Yuza, S.Kom., M.M**), Kabid Perbendaharaan
- Kotak **"INSTALASI"** (semua instalasi digabung, farmasi tidak disebut terpisah) terhubung **garis putus-putus** ke ketiga direktur.
- **[BELUM PASTI]** Instalasi Farmasi melapor langsung ke direktur mana. Unit yang mungkin terkait (dugaan dari nama jabatan): Bidang Penunjang Medik, Seksi Perencanaan Alat Kesehatan, Seksi Logistik & Inventaris, Bidang Perencanaan & Anggaran → tanyakan saat wawancara.

---

## 5. Riwayat Pencarian Objek (alasan memilih RS Unand & Farmasi)

1. Daftar calon perusahaan awal di file project banyak yang **tidak bisa dipercaya** (nomor telepon berpola urut/fabrikasi, duplikasi, lokasi salah).
2. Rumah sakit yang pertama dihubungi mensyaratkan **MoU antarinstitusi** → tidak mungkin dalam waktu tugas. Pak Adi: *"Ganti saja objek yang lain."*
3. **PT Suka Fajar** (dealer Mitsubishi, pusat di Padang) sempat mengarahkan ke HRD kantor pusat Jl. Veteran — tidak ditindaklanjuti.
4. **PT Hayati Pratama Mandiri** (Divisi Spare Part): proposal diantar, tapi HR tidak bisa memastikan persetujuan tepat waktu → dilepas.
5. **RS Unand**: bagian dari kampus sendiri, tidak mensyaratkan MoU, cukup surat.
6. Unit awalnya **Rekam Medis**, diganti **Instalasi Farmasi (sisi logistik)** karena Rekam Medis hampir seluruhnya data pasien dan sulit diamati/didokumentasikan.

Catatan: RS Unand bukan swasta (kriteria awal dosen). **[BELUM PASTI]** apakah Pak Adi sudah menyetujui RS Unand secara eksplisit.

---

## 6. Status Perizinan

Alur: **Surat → Tata Usaha → Direktur Utama → disposisi → Diklit (Bidang Pendidikan dan Penelitian) → Instalasi Farmasi**

| Status | Keterangan |
|---|---|
| Sudah | Surat pertama (tgl 21 Sept 2026, ttd Ketua Departemen Ricky Akbar & Pak Adi) masuk TU |
| Masalah | RS minta surat **diganti, harus diketahui Dekan atau Wakil Dekan**, karena Ketua Departemen dinilai tidak setara dengan Direktur Utama |
| Sedang | Surat pengganti diurus lewat Pak Ricky — **[BELUM PASTI] status terakhir** |
| Sudah | Proposal permohonan + lampiran pertanyaan sudah dibuat |
| Rencana | Datang ke Diklit untuk menanyakan prosedur |

Komunikasi ke RS **hanya lewat Mikail**.

---

## 7. Rencana Kunjungan

| Kunjungan | Durasi | Isi |
|---|---|---|
| Kunjungan 1 | ±90 menit | Wawancara Instalasi Farmasi, pengumpulan dokumen, foto & video |
| Sesi IT | ±30 menit | Gambaran umum sistem untuk Fase C & D — **idealnya hari yang sama dengan K1** |
| Kunjungan 2 | ±30 menit | Klarifikasi BPMN AS-IS + tanda tangan Lembar Persetujuan |

- Kalau sesi IT tidak bisa digabung → jadi 3 kali datang.
- Kunjungan 1 = satu-satunya kesempatan mengambil data. Wajib dapat nomor WA narasumber Farmasi **dan** IT untuk pertanyaan susulan.
- Lembar Persetujuan = pengesahan bahwa kegiatan dilakukan di unit tersebut, **bukan** validasi isi analisis. Kirim draf 2–3 hari sebelum K2.
- **[BELUM PASTI]** apakah laporan akhir Fase C–D butuh Lembar Persetujuan tersendiri (bisa berarti kunjungan tambahan).

---

## 8. Data yang Dimohonkan (8)

1. Profil rumah sakit
2. Visi, misi, dan nilai organisasi yang berlaku saat ini
3. Struktur organisasi rumah sakit *(sudah didapat — lihat 4.1)*
4. Struktur organisasi Instalasi Farmasi
5. Tugas pokok dan fungsi Instalasi Farmasi
6. Prosedur kerja pengelolaan perbekalan farmasi
7. Indikator mutu atau sasaran kerja Instalasi Farmasi
8. Gambaran umum sistem informasi yang digunakan Instalasi Farmasi

**Tidak diminta:** data pasien, rekam medis, resep, data keuangan, rincian konfigurasi jaringan/alamat server/keamanan sistem.

---

## 9. Pokok Pertanyaan Wawancara (36)

### Instalasi Farmasi (1–28)
*Gambaran Umum*
1. Tugas pokok dan fungsi Instalasi Farmasi?
2. Unit pelayanan mana saja yang dilayani?
3. Pihak luar mana yang bekerja sama dalam pengelolaan perbekalan?
4. Sasaran/rencana strategis RS yang berkaitan dengan Instalasi Farmasi? *(dok: renstra, jika diizinkan)*
5. Sumber daya apa yang paling dibutuhkan? *(manusia, fisik, teknologi, informasi — jangan kejar angka anggaran)*
6. Kegiatan pendukung apa yang menunjang pekerjaan utama?

*Struktur dan Peran*
7. Kedudukan Instalasi Farmasi dalam struktur RS (melapor ke siapa)?
8. Peran/jabatan di instalasi dan tanggung jawabnya?
9. Siapa yang berwenang menyetujui prosedur kerja?

*Alur Pengelolaan Perbekalan Farmasi*
10. Perencanaan kebutuhan
11. Pengadaan/pemesanan ke pemasok
12. Penerimaan dan pemeriksaan barang
13. Penyimpanan
14. Distribusi ke unit pelayanan
15. Pengendalian stok, stok opname
16. Penanganan kedaluwarsa/rusak
17. Laporan rutin dan tujuannya
18. Tahap yang paling sering ada kendala

*Sistem Informasi yang Digunakan*
19. Aplikasi/sistem yang dipakai sehari-hari
20. Modul/fitur yang dipakai di tiap tahap
21. Data yang dicatat dan medianya (sistem/Excel/kertas)
22. Untuk tiap data: siapa menginput, siapa memakai
23. Laporan yang dihasilkan sistem
24. Bagian yang masih manual

*Risiko dan Indikator*
25. Risiko/kejadian yang paling perlu diantisipasi
26. Indikator mutu dan targetnya

*Acuan Kerja*
27. Peraturan/standar/pedoman acuan *(catat persis, jangan tebak nomor peraturan)*

*Harapan Pengembangan*
28. Harapan/kebutuhan pengembangan alur kerja maupun sistem

### Bagian Sistem Informasi / IT (29–36)
29. Sistem RS dan modul yang dipakai farmasi
30. Berbasis web/desktop; dikembangkan internal/pihak luar
31. Keterhubungan dengan unit lain dan pihak luar (mis. BPJS)
32. Secara umum: server di RS atau layanan luar
33. Secara umum: akses lewat jaringan internal atau internet
34. Perangkat yang dipakai staf farmasi
35. Kendala teknis yang sering terjadi
36. Rencana pengembangan sistem dalam waktu dekat

### Pertanyaan tambahan dari bagan struktur
- Instalasi Farmasi melapor langsung ke direktur mana?
- Apakah Seksi Logistik & Inventaris terlibat dalam pengadaan?
- Apakah Bidang Penunjang Medik berperan dalam alur kerja instalasi?

### Pemetaan ke fase
| Fase | Nomor |
|---|---|
| Preliminary | 7–9 + data 1–4 |
| A — Architecture Vision | 1–6 |
| B — Business Architecture | 7–18, 25–27 |
| C — Data & Aplikasi | 19–24, 29–31 |
| D — Teknologi | 32–35 |
| Kondisi target (semua fase) | 28, 36 |

---

## 10. Artefak dan Sumber Datanya

### 4.1 Preliminary
| Artefak | Bahan |
|---|---|
| Ruang lingkup organisasi (Farmasi = core unit) | Data 3, no. 2, 3, 7 |
| Architecture Principles | Data 2, no. 27 |
| Identifikasi Stakeholder | no. 2, 3, 8, 9 + tim |
| Tim Arsitek, Tailoring (berhenti di Fase D; E–H tidak), Tools | Keputusan tim |
| Ringkasan Hasil Preliminary | Tabel 6 langkah |

### 4.2 Fase A
| Artefak | Bahan |
|---|---|
| Architecture Principles | Data 2, no. 27 |
| Architecture Goals | no. 4, 18, 26 |
| Vision, Mission, Strategic Planning | Data 2, no. 4 |
| Value Chain | Primer: no. 10–17; pendukung: no. 6 |
| Business Model Canvas | no. 1, 2, 3, 5, 11 (biaya & pendapatan diisi deskriptif, tanpa angka) |
| Organization Decomposition | Data 3, Data 4, no. 7 |

### 4.3 Fase B
| Artefak | Bahan |
|---|---|
| Business Principles | Data 2, no. 9, 27 |
| Organization Role Diagram | Data 4, no. 8, 9 |
| Risk Diagram | no. 18, 25 |
| KPI Diagram | Data 7, no. 26 |
| Standard and Regulation | no. 27 |
| BPMN AS-IS | no. 10–17, Data 6, tabel alur di lembar wawancara |
| BPMN TO-BE | **Dirancang tim**, berpedoman pada Fase A + no. 18, 28 |
| Functional Decomposition | no. 1, 10–17 |
| 3 Matriks (Risk/KPI/Standard) | Disusun tim: BPMN × Risk/KPI/Standard |
| Gap Analysis | AS-IS vs TO-BE |

### Fase C & D (setelah UTS — nama artefak masih umum TOGAF, cocokkan dengan modul nanti)
- Data: daftar data (no. 21), matriks data × pengguna (22)
- Aplikasi: daftar aplikasi & modul (19, 29), matriks aplikasi × tahap proses (20), keterhubungan (31), kekurangan/target (23, 24, 28, 36)
- Teknologi: platform & perangkat (30, 34), lokasi server & akses (32, 33), kendala/target (35, 36)

### BAB I
Rumusan Masalah dari no. 18, 24, 35.

---

## 11. Logika Kerja

- Preliminary = aturan main. Fase A = arah (visi, tujuan, prinsip).
- Fase B, C, D masing-masing: **AS-IS → TO-BE → Gap → Rekomendasi**.
- **TO-BE tidak dirancang bebas** — harus berpedoman pada visi, tujuan, prinsip Fase A. Saat ditanya "kenapa TO-BE-nya begini", jawab dengan merujuk prinsip/tujuan Fase A.
- Berantai: TO-BE C mendukung TO-BE B; TO-BE D mendukung TO-BE C.
- AS-IS harus **apa adanya**, termasuk yang tidak efisien. AS-IS yang terlalu rapi = gap kosong.
- **Nama tahap proses harus sama persis** di BPMN, Value Chain, Functional Decomposition, ketiga matriks, dan matriks aplikasi Fase C. Tetapkan daftar nama resmi sehari setelah wawancara.
- Titik akhir: rekomendasi. Roadmap/anggaran/implementasi = Fase E–H, tidak dikerjakan.

---

## 12. Urutan Kerja

1. Surat pengganti (Dekan/Wadek) → TU
2. Ke Diklit: tanya prosedur, minta sesi IT di hari yang sama
3. **Paralel sekarang:** tulis BAB I–III, ambil data dari website RS, latih minimal 2 orang memakai Sparx
4. Kirim lampiran pertanyaan ke narasumber via WA 2–3 hari sebelum K1
5. Kunjungan 1 (Farmasi + IT)
6. Hari itu juga: satukan catatan & foto, cadangkan rekaman, rapikan sketsa alur, rumuskan 2–3 masalah utama, tetapkan nama resmi tahap proses
7. BAB IV: 4.1 Preliminary → 4.2 Fase A → 4.3 Fase B (Business Principles → Org Role → **BPMN AS-IS** → Functional Decomposition → Risk/KPI/Standard → 3 matriks → **BPMN TO-BE** → Gap & rekomendasi)
8. Kunjungan 2: klarifikasi AS-IS + tanda tangan
9. Finalisasi, kumpulkan, latihan internal, presentasi
10. Setelah UTS: Fase C, Fase D, WA susulan, laporan akhir

---

## 13. Aturan Lapangan & Privasi

- Kalimat wajib di awal: *"Yang kami amati alur prosesnya, bukan isi datanya. Kami tidak memerlukan data pasien, resep, maupun data keuangan."*
- Minta izin rekam audio di awal; minta izin foto **setiap kali**.
- **Boleh difoto:** papan nama RS + kelompok, papan nama instalasi, suasana wawancara, gudang & rak obat, area penerimaan barang, papan alur/visi-misi di dinding, video 30–60 detik, foto bersama narasumber.
- **Jangan difoto:** resep, kartu/etiket bernama pasien, layar sistem berisi data pasien, wajah pasien/pengunjung, dokumen keuangan/faktur/harga, kunci/brankas/obat khusus, ruang server/perangkat jaringan.
- Yang bertanya hanya Mikail. Jangan sebut TOGAF/istilah teknis kecuali ditanya. Jangan bertanya menghakimi.
- Jangan tanya konfigurasi jaringan, IP, keamanan sistem, atau angka anggaran.
- Datang ke Diklit cukup 2–3 orang.

---

## 14. Jawaban Siap Pakai

**Ke pihak RS**
- *Penelitian apa?* Bukan penelitian klinis; pemetaan alur kerja untuk tugas mata kuliah, bukan skripsi.
- *Perlu ethical clearance?* Jangan jawab sendiri — tanyakan balik ("kami tidak mengambil data pasien sama sekali, apakah tetap perlu?"). Kalau perlu, segera kabari Pak Adi.
- *Hasilnya apa?* Laporan tugas kuliah: gambaran alur kerja sekarang + usulan perbaikan dari sudut pandang mahasiswa. Bukan aplikasi, tidak wajib diterapkan, tidak dipublikasikan. Salinan bisa diserahkan bila RS memerlukan.
- *Bisa dipakai untuk apa?* Bahan masukan: dokumentasi tertulis alur kerja, gambaran awal kebutuhan bila sistem dikembangkan. Perlu dikaji RS sebelum dipakai untuk keputusan. **Jangan klaim** siap diterapkan, membantu akreditasi, atau menyelesaikan masalah mereka.
- *Kenapa Farmasi?* Alurnya jelas dan hampir tidak bersinggungan dengan data pasien.
- *Kenapa perlu IT?* Untuk gambaran umum sistem; tidak meminta konfigurasi/keamanan.

**Ke Pak Adi saat presentasi**
- EA = cetak biru organisasi (kondisi sekarang & yang dituju) pada domain bisnis, data, aplikasi, teknologi.
- Preliminary vs Fase A: menyiapkan kemampuan berarsitektur vs menyusun visi proyek.
- Requirements Management bukan fase berurutan; di tengah siklus, berjalan di semua fase.
- Kenapa RS Unand bukan swasta: sudah mencoba beberapa (termasuk swasta), terkendala MoU dan kepastian waktu.
- Masalah utama yang ditemukan: diisi setelah observasi — semua anggota wajib hafal.

---

## 15. File yang Sudah Dibuat

| File | Status |
|---|---|
| `Proposal_Permohonan_Observasi_RS_Unand.docx` | Terbaru (8 hlm, isi + lampiran versi daftar). **Ganti tanggal** (masih 24 Sept 2026), **sisipkan tanda tangan**. Kalau memakai lampiran tabel di bawah, **hapus 2 halaman lampiran lama** agar tidak dobel. |
| `Daftar_Data_dan_Pertanyaan_Wawancara_RS_Unand_Vertikal.docx` | **Terbaru** — lampiran tabel, 36 pertanyaan, kolom Tujuan & Dokumen Pendukung, berlabel LAMPIRAN |
| `Daftar_Data_dan_Pertanyaan_Wawancara_RS_Unand.docx` (horizontal) | Usang (26 pertanyaan) |
| `Lembar_Wawancara_dan_Checklist_RS_Unand.pdf` | Dipakai di lapangan, 8 hlm — **belum sinkron** dengan 36 pertanyaan (belum ada: modul per tahap, jaringan, harapan, rencana pengembangan) |
| `Briefing_Tim_Tugas_Besar_EA.pdf` | Versi di folder unduhan **belum memuat** pembaruan Fase C–D & sesi IT |
| `Panduan_Wawancara_RS_Unand_Rekam_Medis.pdf`, file-file Hayati | Usang, jangan dipakai |

---

## 16. Hal yang Belum Pasti — Perlu Ditanyakan

| Hal | Tanya ke |
|---|---|
| Tenggat pengumpulan Laporan Kemajuan | Pak Adi |
| Lembar Persetujuan wajib sudah ditandatangani saat dikumpulkan, atau boleh menyusul | Pak Adi |
| Deliverable Fase B yang wajib (10 artefak vs AS-IS/TO-BE/Interaction Matrix/Gap) | Pak Adi / asisten |
| Architecture Principles, Tim Arsitek, Stakeholder ditaruh di BAB III atau 4.1 | Pak Adi |
| RS Unand (bukan swasta) sudah disetujui sebagai objek | Pak Adi |
| Kapan Fase C & D, sampai C saja atau sampai D; format laporan akhir | Pak Adi |
| Status surat pengganti (Dekan/Wadek) | Pak Ricky / fakultas |
| Nama resmi unit & nama lengkap Kepala Instalasi Farmasi | RS |
| Instalasi Farmasi melapor ke direktur mana | RS |
| Perlu ethical clearance atau tidak | Diklit |
| Narasumber IT & bisa di hari yang sama dengan K1 | Diklit |
| Siapa penandatangan Lembar Persetujuan (nama & jabatan) | Diklit / RS |
| Ejaan nama Ihsan (Habiburrahim vs Habiburrohim) | Ihsan |

---

## 17. Perkiraan Biaya (untuk subbab Biaya — pakai angka riil di laporan)

| Pos | Perkiraan |
|---|---|
| Transportasi ke RS Unand (dekat kampus) | Rp 50.000 – 100.000 |
| Cetak surat & proposal | Rp 30.000 – 50.000 |
| Cetak laporan (tanda tangan & arsip) | Rp 80.000 – 150.000 |
| ATK & map | Rp 20.000 – 30.000 |
| Buah tangan narasumber | Rp 50.000 – 100.000 |
| **Total** | **Rp 230.000 – 430.000** (perkiraan, bukan harga pasti) |

---

## 18. Prioritas Langkah Berikutnya

1. Pastikan surat pengganti (diketahui Dekan/Wadek) selesai dan masuk TU.
2. Datang ke Diklit (Bidang Pendidikan dan Penelitian) dengan proposal + lampiran; tanyakan prosedur, ethical clearance, narasumber IT, penandatangan.
3. WA ke Pak Adi: tenggat Laporan Kemajuan, Lembar Persetujuan, deliverable Fase B.
4. Tim mulai menulis BAB I–III sekarang dan belajar Sparx — jangan menunggu izin.
5. Sinkronkan lembar wawancara lapangan dengan 36 pertanyaan.
6. Kirim lampiran pertanyaan ke narasumber 2–3 hari sebelum Kunjungan 1.