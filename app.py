"""
app.py — Backend Flask untuk website PT Bumilang Tanjung Nusantara
Step 5: Finishing + SEO routes + siap produksi
"""
import json
import os
from datetime import datetime
from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, send_from_directory
)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'bumilang-secret-2026-ganti-di-produksi')

# ===== KONFIGURASI =====
DATA_DIR = os.path.join(app.root_path, 'data')
MESSAGES_FILE = os.path.join(DATA_DIR, 'messages.json')
os.makedirs(DATA_DIR, exist_ok=True)


# ===== HELPER FUNCTIONS =====
def save_message(nama, email, telepon, subjek, pesan):
    """Menyimpan pesan kontak ke file JSON."""
    messages = []
    if os.path.exists(MESSAGES_FILE):
        with open(MESSAGES_FILE, 'r', encoding='utf-8') as f:
            try:
                messages = json.load(f)
            except json.JSONDecodeError:
                messages = []

    messages.append({
        'id': len(messages) + 1,
        'nama': nama,
        'email': email,
        'telepon': telepon,
        'subjek': subjek,
        'pesan': pesan,
        'waktu': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'dibaca': False
    })

    with open(MESSAGES_FILE, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)


def validate_email(email):
    """Validasi sederhana format email."""
    return '@' in email and '.' in email.split('@')[-1]


# ===== CONTEXT PROCESSOR =====
@app.context_processor
def inject_globals():
    return {
        'company_name': 'PT Bumilang Tanjung Nusantara',
        'company_tagline': 'Connecting Resources, Creating Impact',
        'company_location': 'Jakarta Selatan',
        'company_whatsapp': '6289627231262',
        'company_whatsapp_display': '0896 2723 1262',
        'company_instagram': 'bumilang.tanjungnusantara',
        'current_year': datetime.now().year,
    }


# ===== ROUTING =====

@app.route("/")
def index():
    """Halaman Beranda."""
    return render_template("index.html", active_page="index")


@app.route("/about")
def about():
    """Halaman Tentang Kami."""
    return render_template("about.html", active_page="about")


@app.route("/services")
def services():
    """Halaman Layanan dengan 6 bidang."""
    daftar_layanan = [
        {
            "icon": "bi-box-seam",
            "judul": "Pengadaan Barang dan Jasa",
            "deskripsi": "Penyediaan kebutuhan barang dan jasa untuk instansi, perusahaan, lembaga, dan organisasi.",
            "detail": "Cocok untuk kebutuhan operasional, program, kegiatan institusi, dan dukungan proyek."
        },
        {
            "icon": "bi-palette",
            "judul": "Media dan Kreatif",
            "deskripsi": "Produksi konten, desain, dokumentasi, publikasi, dan kebutuhan media komunikasi.",
            "detail": "Cocok untuk publikasi program, identitas komunikasi, dokumentasi kegiatan, dan kampanye."
        },
        {
            "icon": "bi-book",
            "judul": "Pendidikan dan Pelatihan",
            "deskripsi": "Seminar, workshop, pelatihan, pendampingan, dan pengembangan kompetensi.",
            "detail": "Cocok untuk peningkatan kapasitas, pembelajaran terapan, dan pengembangan SDM."
        },
        {
            "icon": "bi-people",
            "judul": "Program Sosial dan Pemberdayaan",
            "deskripsi": "Pelaksanaan kegiatan sosial, pemberdayaan masyarakat, dan pengembangan komunitas.",
            "detail": "Cocok untuk program berbasis manfaat sosial dan penguatan komunitas."
        },
        {
            "icon": "bi-calendar-event",
            "judul": "Event dan Kegiatan Profesional",
            "deskripsi": "Perencanaan dan pelaksanaan seminar, kegiatan edukasi, gathering, serta kegiatan institusi.",
            "detail": "Cocok untuk kegiatan yang membutuhkan koordinasi, produksi, dan dukungan pelaksanaan."
        },
        {
            "icon": "bi-briefcase",
            "judul": "Konsultasi dan Pendampingan",
            "deskripsi": "Pendampingan program dan pengembangan kegiatan sesuai kebutuhan mitra.",
            "detail": "Cocok untuk mitra yang memerlukan teman diskusi, perencanaan, atau dukungan implementasi."
        },
    ]
    return render_template("services.html", layanan=daftar_layanan, active_page="services")


@app.route("/portfolio")
def portfolio():
    """Halaman Portofolio."""
    return render_template("portfolio.html", active_page="portfolio")


@app.route("/career")
def career():
    """Halaman Karier & Magang."""
    return render_template("career.html", active_page="career")


@app.route("/faq")
def faq():
    """Halaman FAQ dengan 8 pertanyaan."""
    daftar_faq = [
        {
            "pertanyaan": "Bidang apa saja yang ditangani Bumilang?",
            "jawaban": "Bumilang bergerak dalam pengadaan barang dan jasa, media dan komunikasi, kegiatan sosial, pendidikan, pelatihan, event, serta konsultasi dan pendampingan."
        },
        {
            "pertanyaan": "Siapa yang dapat bekerja sama dengan Bumilang?",
            "jawaban": "Kami terbuka untuk instansi pemerintah, perusahaan swasta, lembaga pendidikan, organisasi, komunitas, UMKM, dan masyarakat umum."
        },
        {
            "pertanyaan": "Apakah layanan dapat disesuaikan?",
            "jawaban": "Ya. Bentuk layanan dan ruang lingkup dapat dibahas berdasarkan kebutuhan, tujuan program, keluaran yang diharapkan, serta pihak yang terlibat."
        },
        {
            "pertanyaan": "Bagaimana cara mengajukan kebutuhan kerja sama?",
            "jawaban": "Hubungi Bumilang melalui WhatsApp, Instagram, atau form kontak di halaman ini. Sampaikan nama, organisasi, kebutuhan utama, dan cara yang nyaman untuk dihubungi kembali."
        },
        {
            "pertanyaan": "Apakah sudah tersedia portofolio dan daftar mitra?",
            "jawaban": "Halaman portofolio disiapkan untuk menampilkan proyek, mitra, pencapaian, dan testimoni setelah materi serta izin publikasinya dikonfirmasi."
        },
        {
            "pertanyaan": "Di mana informasi terbaru perusahaan diumumkan?",
            "jawaban": "Informasi terbaru dapat ditampilkan di halaman pengumuman dan diakses melalui Instagram @bumilang.tanjungnusantara."
        },
        {
            "pertanyaan": "Apakah ada program magang?",
            "jawaban": "Informasi yang tersedia saat ini adalah MagangHub Batch 2 Tahun 2026. Detail pendaftaran disampaikan melalui Instagram perusahaan dan Contact Person HR 089627231262."
        },
        {
            "pertanyaan": "Apakah website ini menyimpan data pengguna?",
            "jawaban": "Website ini hanya menyimpan pesan yang Anda kirimkan melalui form kontak. Data tidak dibagikan ke pihak ketiga dan hanya digunakan untuk merespons pertanyaan Anda."
        },
    ]
    return render_template("faq.html", daftar_faq=daftar_faq, active_page="faq")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """Halaman Kontak dengan form fungsional."""
    if request.method == "POST":
        nama = request.form.get("nama", "").strip()
        email = request.form.get("email", "").strip()
        telepon = request.form.get("telepon", "").strip()
        subjek = request.form.get("subjek", "").strip()
        pesan = request.form.get("pesan", "").strip()

        # Validasi
        errors = []
        if not nama or len(nama) < 3:
            errors.append("Nama minimal 3 karakter.")
        if not email or not validate_email(email):
            errors.append("Format email tidak valid.")
        if not pesan or len(pesan) < 10:
            errors.append("Pesan minimal 10 karakter.")

        if errors:
            for err in errors:
                flash(err, "danger")
            return render_template(
                "contact.html",
                active_page="contact",
                form_data={
                    "nama": nama, "email": email,
                    "telepon": telepon, "subjek": subjek,
                    "pesan": pesan
                }
            )

        # Simpan pesan
        save_message(nama, email, telepon, subjek, pesan)

        flash(
            f"Terima kasih, {nama}! Pesan Anda telah kami terima. "
            "Tim kami akan merespons dalam 1x24 jam.",
            "success"
        )
        return redirect(url_for("contact"))

    return render_template("contact.html", active_page="contact")


# ===== SEO ROUTES =====

@app.route("/robots.txt")
def robots():
    """Robots.txt untuk mesin pencari."""
    return send_from_directory(app.static_folder, "robots.txt")


@app.route("/sitemap.xml")
def sitemap():
    """Sitemap untuk mesin pencari."""
    return send_from_directory(app.static_folder, "sitemap.xml", mimetype="application/xml")


# ===== ERROR HANDLER =====

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html", active_page=""), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html", active_page=""), 500


# ===== RUN =====

if __name__ == "__main__":
    # Development: jalankan di localhost:3000
    app.run(host="127.0.0.1", port=3000, debug=True)